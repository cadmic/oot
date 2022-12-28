import io

from ..extase import File, SegmentedAddressResolution, GetResourceAtResult
from ..extase.cdata_resources import (
    CDataResource,
    CDataExt_Struct,
    CDataExt_Value,
    CDataExt_Array,
)

from . import dlist_resources


class KnotCountsArrayResource(CDataResource, can_size_be_unknown=True):
    elem_cdata_ext = CDataExt_Value.u8

    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, name)
        self.length = None

    def try_parse_data(self):
        if self.length is not None:
            self.cdata_ext = CDataExt_Array(self.elem_cdata_ext, self.length)
            self.range_end = self.range_start + self.cdata_ext.size
            super().try_parse_data()

    def get_c_declaration_base(self):
        return f"u8 {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class CurveInterpKnotArrayResource(CDataResource, can_size_be_unknown=True):
    elem_cdata_ext = CDataExt_Struct(
        (
            ("flags", CDataExt_Value.u16),
            ("abscissa", CDataExt_Value.s16),
            ("leftGradient", CDataExt_Value.s16),
            ("rightGradient", CDataExt_Value.s16),
            ("ordinate", CDataExt_Value.f32),
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
        return f"CurveInterpKnot {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class ConstantDataArrayResource(CDataResource, can_size_be_unknown=True):
    elem_cdata_ext = CDataExt_Value.s16

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


class CurveAnimationHeaderResource(CDataResource):
    def report_knotCounts(resource, v):
        assert isinstance(v, int)
        address = v
        resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: KnotCountsArrayResource(
                file, offset, f"{resource.name}_{address:08X}_KnotCounts"
            ),
        )

    def write_knotCounts(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    def report_interpolationData(resource, v):
        assert isinstance(v, int)
        address = v
        resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: CurveInterpKnotArrayResource(
                file, offset, f"{resource.name}_{address:08X}_InterpolationData"
            ),
        )

    def write_interpolationData(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    def report_constantData(resource, v):
        assert isinstance(v, int)
        address = v
        resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: ConstantDataArrayResource(
                file, offset, f"{resource.name}_{address:08X}_ConstantData"
            ),
        )

    def write_constantData(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    cdata_ext = CDataExt_Struct(
        (
            (
                "knotCounts",
                CDataExt_Value("I")
                .set_report(report_knotCounts)
                .set_write(write_knotCounts),
            ),  # u8*
            (
                "interpolationData",
                CDataExt_Value("I")
                .set_report(report_interpolationData)
                .set_write(write_interpolationData),
            ),  # CurveInterpKnot*
            (
                "constantData",
                CDataExt_Value("I")
                .set_report(report_constantData)
                .set_write(write_constantData),
            ),  # s16*
            ("unk_0C", CDataExt_Value.s16),
            ("frameCount", CDataExt_Value.s16),
        )
    )

    def try_parse_data(self):
        super().try_parse_data()
        knotCounts = self.cdata_unpacked["knotCounts"]
        interpolationData = self.cdata_unpacked["interpolationData"]
        constantData = self.cdata_unpacked["constantData"]
        (
            knotCounts_resolution,
            knotCounts_resolution_info,
        ) = self.file.memory_context.resolve_segmented(knotCounts)
        (
            interpolationData_resolution,
            interpolationData_resolution_info,
        ) = self.file.memory_context.resolve_segmented(interpolationData)
        (
            constantData_resolution,
            constantData_resolution_info,
        ) = self.file.memory_context.resolve_segmented(constantData)
        if (
            knotCounts_resolution
            == interpolationData_resolution
            == constantData_resolution
            == SegmentedAddressResolution.FILE
        ):
            (
                knotCounts_file,
                knotCounts_offset,
            ) = knotCounts_resolution_info
            (
                interpolationData_file,
                interpolationData_offset,
            ) = interpolationData_resolution_info
            (
                constantData_file,
                constantData_offset,
            ) = constantData_resolution_info
            if (
                knotCounts_file
                == interpolationData_file
                == constantData_file
                == self.file
            ):
                (
                    knotCounts_resource_get_result,
                    knotCounts_resource,
                ) = self.file.get_resource_at(knotCounts_offset)
                assert (
                    knotCounts_resource_get_result == GetResourceAtResult.DEFINITIVE
                ), knotCounts_resource_get_result
                assert isinstance(
                    knotCounts_resource, KnotCountsArrayResource
                ), knotCounts_resource

                (
                    interpolationData_resource_get_result,
                    interpolationData_resource,
                ) = self.file.get_resource_at(interpolationData_offset)
                assert (
                    interpolationData_resource_get_result
                    == GetResourceAtResult.DEFINITIVE
                ), interpolationData_resource_get_result
                assert isinstance(
                    interpolationData_resource, CurveInterpKnotArrayResource
                ), interpolationData_resource

                (
                    constantData_resource_get_result,
                    constantData_resource,
                ) = self.file.get_resource_at(constantData_offset)
                assert (
                    constantData_resource_get_result == GetResourceAtResult.DEFINITIVE
                ), constantData_resource_get_result
                assert isinstance(
                    constantData_resource, ConstantDataArrayResource
                ), constantData_resource

                animHeader_offset = self.range_start
                assert (
                    knotCounts_offset
                    < constantData_offset
                    < interpolationData_offset
                    < animHeader_offset
                )
                knotCounts_resource.length = (
                    constantData_offset - knotCounts_offset
                ) // knotCounts_resource.elem_cdata_ext.size
                constantData_resource.length = (
                    interpolationData_offset - constantData_offset
                ) // constantData_resource.elem_cdata_ext.size
                interpolationData_resource.length = (
                    animHeader_offset - interpolationData_offset
                ) // interpolationData_resource.elem_cdata_ext.size

            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def get_c_declaration_base(self):
        return f"CurveAnimationHeader {self.symbol_name}"

    def get_c_reference(self, resource_offset: int):
        raise ValueError()


class SkelCurveLimbResource(CDataResource):
    def report_dList_element(resource, v):
        assert isinstance(v, int)
        address = v
        if address != 0:
            resource.file.memory_context.report_resource_at_segmented(
                address,
                lambda file, offset: dlist_resources.DListResource(
                    file, offset, f"{resource.name}_{address:08X}_Dl"
                ),
            )

    def write_dList_element(resource, v, f: io.TextIOBase, line_prefix):
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
            ("child", CDataExt_Value.u8),
            ("sibling", CDataExt_Value.u8),
            ("pad2", CDataExt_Value.pad16),
            (
                "dList",
                CDataExt_Array(
                    CDataExt_Value("I")
                    .set_report(report_dList_element)
                    .set_write(write_dList_element),  # Gfx*
                    2,
                ),
            ),
        )
    )

    def get_c_declaration_base(self):
        return f"SkelCurveLimb {self.symbol_name}"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()


class SkelCurveLimbArrayResource(CDataResource):
    def report_limb_element(resource, v):
        assert isinstance(v, int)
        address = v
        resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: SkelCurveLimbResource(
                file, offset, f"{resource.name}_{address:08X}"
            ),
        )

    def write_limb_element(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    elem_cdata_ext = (
        CDataExt_Value("I")
        .set_report(report_limb_element)
        .set_write(write_limb_element)
    )

    def __init__(self, file: File, range_start: int, name: str, length: int):
        self.cdata_ext = CDataExt_Array(self.elem_cdata_ext, length)
        super().__init__(file, range_start, name)

    def get_c_declaration_base(self):
        return f"SkelCurveLimb* {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class CurveSkeletonHeaderResource(CDataResource):
    def report_limbs(resource, v):
        assert isinstance(v, int)
        address = v
        resource.file.memory_context.report_resource_at_segmented(
            address,
            lambda file, offset: SkelCurveLimbArrayResource(
                file,
                offset,
                f"{resource.name}_Limbs_",
                resource.cdata_unpacked["limbCount"],
            ),
        )

    def write_limbs(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    cdata_ext = CDataExt_Struct(
        (
            (
                "limbs",
                CDataExt_Value("I").set_report(report_limbs).set_write(write_limbs),
            ),  # SkelCurveLimb**
            ("limbCount", CDataExt_Value.u8),
            ("pad5", CDataExt_Value.pad8),
            ("pad6", CDataExt_Value.pad16),
        )
    )

    def get_c_declaration_base(self):
        return f"CurveSkeletonHeader {self.symbol_name}"

    def get_c_reference(self, resource_offset: int):
        raise ValueError()
