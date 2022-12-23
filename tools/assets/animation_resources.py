import io

from extract_xml import (
    Resource,
    File,
    CDataResource,
    CDataExt_Value,
    CDataExt_Struct,
    CDataExt_Array,
)


class AnimationFrameDataResource(CDataResource, can_size_be_unknown=True):
    def write_binang(resource, v, f: io.TextIOBase, line_prefix):
        f.write(line_prefix)
        f.write(f" 0x{v:04X}" if v >= 0 else "-0x" + f"{v:04X}".removeprefix("-"))
        return True

    elem_cdata_ext = CDataExt_Value("h").set_write(write_binang)

    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, name)
        self.length = None

    def try_parse_data(self):
        if self.length is not None:
            self.cdata_ext = CDataExt_Array(self.elem_cdata_ext, self.length)
            self.range_end = self.range_start + self.cdata_ext.size
            super().try_parse_data()

    def get_c_declaration_base(self):
        return f"s16 {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class AnimationJointIndicesResource(CDataResource, can_size_be_unknown=True):
    elem_cdata_ext = CDataExt_Struct(
        (
            ("x", CDataExt_Value.u16),
            ("y", CDataExt_Value.u16),
            ("z", CDataExt_Value.u16),
        )
    )

    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, name)
        self.length = None

    def try_parse_data(self):
        if self.length is not None:
            self.cdata_ext = CDataExt_Array(self.elem_cdata_ext, self.length)
            self.range_end = self.range_start + self.cdata_ext.size
            super().try_parse_data()

    def get_c_declaration_base(self):
        return f"JointIndex {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class AnimationResource(CDataResource):
    def write_frameData(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    def write_jointIndices(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    cdata_ext = CDataExt_Struct(
        (
            (
                "common",
                CDataExt_Struct((("frameCount", CDataExt_Value.s16),)),
            ),
            ("pad2", CDataExt_Value.pad16),
            (
                "frameData",
                CDataExt_Value("I").set_write(write_frameData),
            ),
            (
                "jointIndices",
                CDataExt_Value("I").set_write(write_jointIndices),
            ),
            ("staticIndexMax", CDataExt_Value.u16),
            ("padE", CDataExt_Value.pad16),
        )
    )

    def try_parse_data(self):
        super().try_parse_data()

        (
            frameData_resource,
            frameData_offset,
        ) = self.file.memory_context.report_resource_at_segmented(
            self.cdata_unpacked["frameData"],
            lambda file, offset: AnimationFrameDataResource(
                file,
                offset,
                f"{self.name}_FrameData_421_",
            ),
        )
        assert isinstance(frameData_resource, AnimationFrameDataResource)
        assert frameData_resource.range_start == frameData_offset

        (
            jointIndices_resource,
            jointIndices_offset,
        ) = self.file.memory_context.report_resource_at_segmented(
            self.cdata_unpacked["jointIndices"],
            lambda file, offset: AnimationJointIndicesResource(
                file,
                offset,
                f"{self.name}_JointIndices_421_",
            ),
        )
        assert isinstance(jointIndices_resource, AnimationJointIndicesResource)
        assert jointIndices_resource.range_start == jointIndices_offset

        # The length of the frameData and jointIndices arrays is
        # for now assumed to fill the space to the animation,
        # at the very least before subtracting the offsets check that
        # the offsets belong to the same file
        # TODO better idea for computing this data's size

        if not (frameData_resource.file == jointIndices_resource.file == self.file):
            raise NotImplementedError(
                "Expected frameData and jointIndices to be in the same file as the animation",
                self.cdata_unpacked,
                frameData_resource.file,
                jointIndices_resource.file,
                self.file,
            )

        if frameData_offset < jointIndices_offset < self.range_start:
            frameData_resource.length = (
                jointIndices_offset - frameData_offset
            ) // AnimationFrameDataResource.elem_cdata_ext.size
            jointIndices_resource.length = (
                self.range_start - jointIndices_offset
            ) // AnimationJointIndicesResource.elem_cdata_ext.size
        else:
            raise NotImplementedError(
                "Expected offsets of frameData, jointIndices, animation to be in order",
                self.cdata_unpacked,
                hex(frameData_offset),
                hex(jointIndices_offset),
                hex(self.range_start),
            )

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()

    def get_c_declaration_base(self):
        return f"AnimationHeader {self.symbol_name}"
