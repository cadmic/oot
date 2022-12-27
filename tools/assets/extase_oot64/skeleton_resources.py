import io

from extase import (
    File,
)
from extase.cdata_resources import (
    CDataResource,
    CDataExt_Value,
    CDataExt_Struct,
    CDataExt_Array,
)

from extase_oot64.dlist_resources import DListResource


Vec3s = CDataExt_Struct(
    (
        ("x", CDataExt_Value.s16),
        ("y", CDataExt_Value.s16),
        ("z", CDataExt_Value.s16),
    )
)


class StandardLimbResource(CDataResource):
    def report_dList(resource, v):
        assert isinstance(v, int)
        address = v
        if address != 0:
            resource.file.memory_context.report_resource_at_segmented(
                address,
                lambda file, offset: DListResource(
                    file,
                    offset,
                    f"{resource.name}_DL",
                ),
            )

    def write_dList(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        if address == 0:
            f.write("NULL")
        else:
            f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    cdata_ext = CDataExt_Struct(
        (
            ("jointPos", Vec3s),
            ("child", CDataExt_Value.u8),
            ("sibling", CDataExt_Value.u8),
            (
                "dList",
                CDataExt_Value("I").set_report(report_dList).set_write(write_dList),
            ),
        )
    )

    def get_c_declaration_base(self):
        return f"StandardLimb {self.symbol_name}"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()


class LimbsArrayResource(CDataResource, can_size_be_unknown=True):
    def report_limb_element(resource, v):
        assert isinstance(v, int)
        address = v
        resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: StandardLimbResource(
                file, offset, f"{resource.name}_{address:08X}"
            ),
        )

    elem_cdata_ext = CDataExt_Value("I").set_report(report_limb_element)

    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, name)
        self.length = None

    def try_parse_data(self):
        if self.length is not None:
            self.cdata_ext = CDataExt_Array(self.elem_cdata_ext, self.length)
            self.range_end = self.range_start + self.cdata_ext.size
            super().try_parse_data()

    def get_c_declaration_base(self):
        return f"void* {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"{self.symbol_name}"
        else:
            raise ValueError()

    def get_c_expression_length(self, resource_offset: int):
        if resource_offset == 0:
            return f"ARRAY_COUNT({self.symbol_name})"
        else:
            raise ValueError()


class SkeletonNormalResource(CDataResource):
    def report_segment(resource, v):
        assert isinstance(v, int)
        address = v
        (
            limbs_resource,
            limbs_offset,
        ) = resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: LimbsArrayResource(
                file,
                offset,
                f"{resource.name}_Limbs_421_",
            ),
        )
        assert isinstance(limbs_resource, LimbsArrayResource)
        assert limbs_resource.range_start == limbs_offset
        limbs_resource.length = resource.get_skeleton_header_cdata_unpacked()[
            "limbCount"
        ]

    def write_segment(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    def write_limbCount(resource, v, f: io.TextIOBase, line_prefix):
        f.write(line_prefix)
        f.write(
            resource.file.memory_context.get_c_expression_length_at_segmented(
                resource.get_skeleton_header_cdata_unpacked()["segment"]
            )
        )
        return True

    cdata_ext = CDataExt_Struct(
        (
            (
                "segment",
                CDataExt_Value("I").set_report(report_segment).set_write(write_segment),
            ),
            (
                "limbCount",
                CDataExt_Value("B").set_write(write_limbCount),
            ),
            ("pad5", CDataExt_Value.pad8),
            ("pad6", CDataExt_Value.pad16),
        )
    )

    def get_skeleton_header_cdata_unpacked(self):
        return self.cdata_unpacked

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()

    def get_c_declaration_base(self):
        return f"SkeletonHeader {self.symbol_name}"


class SkeletonFlexResource(CDataResource):
    cdata_ext = CDataExt_Struct(
        (
            ("sh", SkeletonNormalResource.cdata_ext),
            ("dListCount", CDataExt_Value.u8),
            ("pad9", CDataExt_Value.pad8),
            ("pad10", CDataExt_Value.pad16),
        )
    )

    def get_skeleton_header_cdata_unpacked(self):
        return self.cdata_unpacked["sh"]

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()

    def get_c_declaration_base(self):
        return f"FlexSkeletonHeader {self.symbol_name}"
