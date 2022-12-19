
class DataKind:
    def __init__(self, format_c: Callable[[Resource, Any], str]):
        self.format_c = format_c


class DataKind_Pointer(DataKind):
    def __init__(
        self,
        new_resource_pointed_to_get_size: Callable[["CStructResource"], int],
        new_resource_pointed_to_get_name: Callable[["CStructResource"], str],
        resource_pointed_to_type: type[
            Resource
        ],  # or a subclass, but with the same constructor
    ):
        super().__init__(self._format_c)

        self.new_resource_pointed_to_get_size = new_resource_pointed_to_get_size
        self.new_resource_pointed_to_get_name = new_resource_pointed_to_get_name
        self.resource_pointed_to_type = resource_pointed_to_type

    def new_resource_pointed_to(
        self,
        resource: "CStructResource",
        pointed_file: File,
        pointed_offset: int,
    ):
        size = self.new_resource_pointed_to_get_size(resource)
        range_start = pointed_offset
        range_end = pointed_offset + size
        name = self.new_resource_pointed_to_get_name(resource)

        assert range_end <= len(pointed_file.data)

        resource_pointed_to = self.resource_pointed_to_type(
            pointed_file,
            range_start,
            range_end,
            pointed_file.data[range_start:range_end],
            name,
        )

        return resource_pointed_to

    def _format_c(self, resource: Resource, v):
        assert isinstance(v, int)

        return resource.file.memory_context.get_c_reference_at_segmented(v)


class DataKind_Length(DataKind):
    def __init__(self, target_member_name):
        super().__init__(self._format_c)

        self.target_member_name = target_member_name
        """The name of the member in the struct that the data with this kind indicates the length of"""

    def _format_c(self, resource: Resource, v):

        assert isinstance(v, int)  # idk

        # :thonk: isn't DataKind supposed to only be with CStructResource anyway?
        assert isinstance(resource, CStructResource)

        target_member_name = self.target_member_name

        if __debug__:
            assert target_member_name in resource.members_vals_by_name

            members_kinds_by_name = {
                name: kind for name, kind in resource.struct_members
            }
            assert isinstance(
                members_kinds_by_name[target_member_name], DataKind_Pointer
            )

        address = resource.members_vals_by_name[target_member_name]
        return resource.file.memory_context.get_c_expression_length_at_segmented(
            address
        )


class DataKind_Padding(DataKind):
    def __init__(self):
        super().__init__(self._format_c)

    def _format_c(self, resource: Resource, v):
        raise Exception("Can't format struct padding")


class DataKinds:
    PADDING = DataKind_Padding()

    DECIMAL = DataKind(lambda resource, v: f"{v}")
    HEXADECIMAL = DataKind(lambda resource, v: f"0x{v:X}")


class CStructResource(Resource):
    # Set by subclasses
    struct_name: str
    struct_layout: struct.Struct
    struct_members: Sequence[tuple[str, DataKind]]

    # Set by try_parse_data
    members_vals: tuple[Any] = None
    members_vals_by_name: dict[str, Any] = None

    def try_parse_data(self):
        if __debug__:
            if self.members_vals is None:
                assert self.members_vals_by_name is None
            else:
                assert self.members_vals_by_name is not None

        if self.members_vals is None:
            self.members_vals = self.struct_layout.unpack(self.data)
            self.members_vals_by_name = {
                name: val
                for (name, kind), val in zip(self.struct_members, self.members_vals)
            }

            for (name, kind), val in zip(self.struct_members, self.members_vals):
                assert name is not None, (self.__class__, self.struct_members)
                assert kind is not None

                if isinstance(kind, DataKind_Padding):
                    assert isinstance(val, int)
                    if val != 0:
                        raise ValueError("non-0 struct padding", val)
                elif isinstance(kind, DataKind_Pointer):
                    assert isinstance(val, int)
                    address = val
                    self.file.memory_context.report_resource_at_segmented(
                        address,
                        lambda pointed_file, pointed_offset: kind.new_resource_pointed_to(
                            self, pointed_file, pointed_offset
                        ),
                    )
                else:
                    pass

        ...  # ?

        self.is_data_parsed = True

    def get_c_reference(self, resource_offset):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise NotImplementedError(
                "CStructResource doesn't handle referencing specific members yet, "
                "and maybe it shouldn't anyway",
                resource_offset,
            )

    def write_extracted(self):
        members_vals = self.struct_layout.unpack(self.data)
        assert len(self.struct_members) == len(members_vals)
        with self.extract_to_path.open("w") as f:
            for (name, kind), val in zip(self.struct_members, members_vals):
                if isinstance(kind, DataKind_Padding):
                    if val != 0:
                        raise ValueError("non-0 struct padding", val)
                else:
                    f.write(kind.format_c(self, val))
                    if name is not None:
                        f.write(f", // {name}\n")
                    else:
                        f.write(",\n")

    def get_c_declaration_base(self):
        return f"{self.struct_name} {self.symbol_name}"


"""
# TODO arrays
# it's probably time to refactor the struct code,
# since array elements should borrow it
class ArrayResource(Resource):
    array_elem_c_type: str
    array_elem_layout: struct.Struct
    array_elem_data_kind: DataKind

    def try_parse_data(self):
        self.array_elem_data_kind
        raise NotImplementedError()

    def get_c_reference(self, resource_offset: int):
        raise NotImplementedError()

    def get_c_expression_length(self, resource_offset: int):
        if resource_offset == 0:
            return f"ARRAY_COUNT({self.symbol_name})"
        else:
            raise ValueError()

    def write_extracted(self):
        raise NotImplementedError()

    def get_c_declaration_base(self):
        return f"{self.array_elem_c_type} {self.symbol_name}[]"


class SkeletonLimbsArrayResource(ArrayResource):
    array_c_type = "void*"
    array_elem_layout = 
    array_elem_data_kind = DataKind_Pointer(
        (lambda resource: 1),
        (lambda resource: f"{resource.name}_Limb{resource.cur_index}_421_"),
        BinaryBlobResource,
    )
"""


class SkeletonLimbsArrayResource(Resource):
    def try_parse_data(self):
        self.limbs = [limb for (limb,) in struct.Struct(">I").iter_unpack(self.data)]
        for limb in self.limbs:
            SIZEOF_StandardLimb = 0xC
            self.file.memory_context.report_resource_at_segmented(
                limb,
                lambda file, offset: BinaryBlobResource(
                    file,
                    offset,
                    offset + SIZEOF_StandardLimb,
                    file.data[offset : offset + SIZEOF_StandardLimb],
                    f"{self.name}_{limb:06X}_",
                ),
            )
        self.is_data_parsed = True

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()

    def get_c_expression_length(self, resource_offset: int):
        if resource_offset == 0:
            return f"ARRAY_COUNT({self.symbol_name})"
        else:
            raise ValueError()

    def write_extracted(self):
        with self.extract_to_path.open("w") as f:
            for i, limb in enumerate(self.limbs):
                f.write(self.file.memory_context.get_c_reference_at_segmented(limb))
                f.write(f", // {i} 0x{limb:08X}\n")

    def get_c_declaration_base(self):
        return f"void* {self.symbol_name}[]"


class SkeletonNormalResource(CStructResource):
    struct_name = "SkeletonHeader"
    struct_layout = struct.Struct(">IBBBB")
    struct_members = (
        (
            "segment",
            DataKind_Pointer(
                (lambda resource: 4 * resource.members_vals_by_name["limbCount"]),
                (lambda resource: f"{resource.name}_Limbs_421_"),
                # BinaryBlobResource,
                SkeletonLimbsArrayResource,
            ),
        ),
        ("limbCount", DataKind_Length("segment")),
        ("pad5", DataKinds.PADDING),  # padding but this is for testing
        ("pad6", DataKinds.PADDING),
        ("pad7", DataKinds.PADDING),
    )


@CStruct("SkeletonHeader", ">IBBBB")
class SkeletonHeaderCStruct:
    segment = DataKind_Pointer(
        (lambda resource: 4 * resource.members_vals_by_name["limbCount"]),
        (lambda resource: f"{resource.name}_Limbs_421_"),
        # BinaryBlobResource,
        SkeletonLimbsArray,
    )
    limbCount = DataKind_Length(length_for=segment)
    pad5 = DataKinds.PADDING
    pad6 = DataKinds.PADDING
    pad7 = DataKinds.PADDING


"""
class SkeletonNormalResource(Resource):
    def write_extracted(self):
        segment, limbCount, pad5, pad6, pad7 = struct.unpack(">IBBBB", self.data)
        assert pad5 == pad6 == pad7 == 0
        self.extract_to_path.write_text(f"0x{segment:08X}, {limbCount}")

    def get_declaration_base(self):
        return f"SkeletonHeader {self.symbol_name}"
"""
