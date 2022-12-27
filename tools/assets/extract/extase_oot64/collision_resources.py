import io

from ..extase import (
    SegmentedAddressResolution,
    GetResourceAtResult,
    File,
)
from ..extase.cdata_resources import (
    CDataResource,
    CDataExt_Struct,
    CDataExt_Array,
    CDataExt_Value,
    INDENT,
)

Vec3s = CDataExt_Struct(
    (
        ("x", CDataExt_Value.s16),
        ("y", CDataExt_Value.s16),
        ("z", CDataExt_Value.s16),
    )
)

# TODO would be better for array resources to be of unknown size at instanciation
# and have their size set later, like LimbsArrayResource,
# which allows declaring them with offsets in xmls and have the data parsing
# fill in the length for both cases of it instantiating the array,
# and it being instantiated much earlier from the xml


class CollisionVtxListResource(CDataResource):
    cdata_ext_elem = Vec3s

    def __init__(self, file: File, range_start: int, name: str, length: int):
        self.cdata_ext = CDataExt_Array(self.cdata_ext_elem, length)
        super().__init__(file, range_start, name)

    def get_c_declaration_base(self):
        return f"Vec3s {self.symbol_name}[]"

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


class CollisionPolyListResource(CDataResource):
    def write_vtxData(
        resource: "CollisionPolyListResource", v, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, list)
        assert len(v) == 3
        vtxData = v
        f.write(line_prefix)
        f.write("{\n")
        for i in range(3):
            vI = vtxData[i]
            vtxId = vI & 0x1FFF
            flags = (vI & 0xE000) >> 13
            flags_str_list = []
            if i == 0:
                if flags & 1:
                    flags &= ~1
                    flags_str_list.append("1")
                if flags & 2:
                    flags &= ~2
                    flags_str_list.append("2")
                if flags & 4:
                    flags &= ~4
                    flags_str_list.append("4")
            elif i == 1:
                if flags & 1:
                    flags &= ~1
                    flags_str_list.append("1")
            if flags != 0:
                flags_str_list.append(f"0x{flags:X}")
            if flags_str_list:
                flags_str = " | ".join(flags_str_list)
            else:
                flags_str = "0"
            f.write(line_prefix)
            f.write(INDENT)
            f.write(f"{vtxId} | (({flags_str}) << 13), // {i}\n")
        f.write(line_prefix)
        f.write("}")
        return True

    def write_normal_component(
        resource: "CollisionPolyListResource", v, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, int)
        nf = v / 0x7FFF
        f.write(line_prefix)
        f.write(f"COLPOLY_SNORMAL({nf})")

        return True

    normal_component = CDataExt_Value("h").set_write(write_normal_component)
    cdata_ext_elem = CDataExt_Struct(
        (
            ("type", CDataExt_Value.u16),
            ("vtxData", CDataExt_Array(CDataExt_Value.u16, 3).set_write(write_vtxData)),
            (
                "normal",
                CDataExt_Struct(
                    (
                        ("x", normal_component),
                        ("y", normal_component),
                        ("z", normal_component),
                    )
                ),
            ),
            ("dist", CDataExt_Value.s16),
        )
    )

    def __init__(self, file: File, range_start: int, name: str, length: int):
        self.cdata_ext = CDataExt_Array(self.cdata_ext_elem, length)
        super().__init__(file, range_start, name)

    def try_parse_data(self):
        super().try_parse_data()
        self.max_surface_type_index = max(elem["type"] for elem in self.cdata_unpacked)
        assert isinstance(self.max_surface_type_index, int)

    def get_c_declaration_base(self):
        return f"CollisionPoly {self.symbol_name}[]"

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


class CollisionSurfaceTypeListResource(CDataResource):
    def write_data(
        resource: "CollisionSurfaceTypeListResource", v, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, list)
        assert len(v) == 2

        f.write(line_prefix)
        f.write("{\n")

        for i_data, bitfield_info in (
            (
                0,
                (
                    (0x000000FF, 0, "bgCamIndex"),
                    (0x00001F00, 8, "exitIndex"),
                    (0x0003E000, 13, "floorType"),
                    (0x001C0000, 18, "unk18"),
                    (0x03E00000, 21, "wallType"),
                    (0x3C000000, 26, "floorProperty"),
                    (0x40000000, 30, "isSoft"),
                    (0x80000000, 31, "isHorseBlocked"),
                ),
            ),
            (
                1,
                (
                    (0x0000000F, 0, "material"),
                    (0x00000030, 4, "floorEffect"),
                    (0x000007C0, 6, "lightSetting"),
                    (0x0001F800, 11, "echo"),
                    (0x00020000, 17, "canHookshot"),
                    (0x001C0000, 18, "conveyorSpeed"),
                    (0x07E00000, 21, "conveyorDirection"),
                    (0x08000000, 27, "unk27"),
                ),
            ),
        ):

            data_val = v[i_data]

            f.write(line_prefix)
            f.write(INDENT)
            f.write("(\n")

            has_prev = False
            for mask, shift, name in bitfield_info:
                val = (data_val & mask) >> shift

                f.write(line_prefix)
                f.write(INDENT * 2)
                if has_prev:
                    f.write("| ")
                else:
                    f.write("  ")

                f.write(f"({val} << {shift:2}) & 0x{mask:08X} // {name}\n")

                has_prev = True

            f.write(line_prefix)
            f.write(INDENT)
            f.write(f"), // {i_data}\n")

        f.write(line_prefix)
        f.write("}")

        return True

    cdata_ext_elem = CDataExt_Struct(
        (("data", CDataExt_Array(CDataExt_Value.u32, 2).set_write(write_data)),)
    )

    def __init__(self, file: File, range_start: int, name: str, length: int):
        self.cdata_ext = CDataExt_Array(self.cdata_ext_elem, length)
        super().__init__(file, range_start, name)

    def try_parse_data(self):
        super().try_parse_data()
        self.max_bgCamIndex = max(
            elem["data"][0] & 0xFF for elem in self.cdata_unpacked
        )

    def get_c_declaration_base(self):
        return f"SurfaceType {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class CollisionBgCamListResource(CDataResource):
    def report_bgCamFuncData(resource, v):
        if v != 0:
            raise NotImplementedError(
                "didn't implement extracting BgCamFuncData yet", hex(v)
            )

    def write_bgCamFuncData(
        resource: "CollisionSurfaceTypeListResource", v, f: io.TextIOBase, line_prefix
    ):
        assert v == 0, "should have NotImplementedError'ed in report_bgCamFuncData"
        f.write(line_prefix)
        f.write("NULL")
        return True

    cdata_ext_elem = CDataExt_Struct(
        (
            ("setting", CDataExt_Value.u16),
            ("count", CDataExt_Value.s16),
            (
                "bgCamFuncData",
                CDataExt_Value("I")
                .set_report(report_bgCamFuncData)
                .set_write(write_bgCamFuncData),
            ),  # Vec3s*
        )
    )

    def __init__(self, file: File, range_start: int, name: str, length: int):
        self.cdata_ext = CDataExt_Array(self.cdata_ext_elem, length)
        super().__init__(file, range_start, name)

    def get_c_declaration_base(self):
        return f"BgCamInfo {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()


class CollisionWaterBoxesResource(CDataResource):
    cdata_ext_elem = CDataExt_Struct(
        (
            ("xMin", CDataExt_Value.s16),
            ("ySurface", CDataExt_Value.s16),
            ("zMin", CDataExt_Value.s16),
            ("xLength", CDataExt_Value.s16),
            ("zLength", CDataExt_Value.s16),
            ("pad12", CDataExt_Value.pad16),
            ("properties", CDataExt_Value.u32),
        )
    )

    # TODO object_am collision doesn't have waterboxes,
    # implement that once working from a xml that does have some


class CollisionResource(CDataResource):
    def write_numVertices(
        resource: "CollisionResource", v, f: io.TextIOBase, line_prefix
    ):
        f.write(line_prefix)
        f.write(
            resource.file.memory_context.get_c_expression_length_at_segmented(
                resource.cdata_unpacked["vtxList"]
            )
        )
        return True

    def report_vtxList(resource: "CollisionResource", v):
        assert isinstance(v, int)
        resource.file.memory_context.report_resource_at_segmented(
            v,
            lambda file, offset: CollisionVtxListResource(
                file,
                offset,
                f"{resource.name}_VtxList_",
                resource.cdata_unpacked["numVertices"],
            ),
        )

    def write_vtxList(resource: "CollisionResource", v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(v))
        return True

    def write_numPolygons(
        resource: "CollisionResource", v, f: io.TextIOBase, line_prefix
    ):
        f.write(line_prefix)
        f.write(
            resource.file.memory_context.get_c_expression_length_at_segmented(
                resource.cdata_unpacked["polyList"]
            )
        )
        return True

    def report_polyList(resource: "CollisionResource", v):
        assert isinstance(v, int)
        resource.file.memory_context.report_resource_at_segmented(
            v,
            lambda file, offset: CollisionPolyListResource(
                file,
                offset,
                f"{resource.name}_PolyList_",
                resource.cdata_unpacked["numPolygons"],
            ),
        )

    def write_polyList(resource: "CollisionResource", v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, int)
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(v))
        return True

    def write_numWaterBoxes(
        resource: "CollisionResource", v, f: io.TextIOBase, line_prefix
    ):
        f.write(line_prefix)
        length = resource.cdata_unpacked["numWaterBoxes"]
        if length != 0:
            f.write(
                resource.file.memory_context.get_c_expression_length_at_segmented(
                    resource.cdata_unpacked["waterBoxes"]
                )
            )
        else:
            f.write("0")
        return True

    def report_waterBoxes(resource: "CollisionResource", v):
        assert isinstance(v, int)
        length = resource.cdata_unpacked["numWaterBoxes"]
        if length != 0:
            assert v != 0, v  # should not be NULL
            resource.file.memory_context.report_resource_at_segmented(
                v,
                lambda file, offset: CollisionWaterBoxesResource(
                    file,
                    offset,
                    f"{resource.name}_WaterBoxes_",
                    length,
                ),
            )

    def write_surfaceTypeList(
        resource: "CollisionResource", v, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, int)
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(v))
        return True

    def write_bgCamList(
        resource: "CollisionResource", v, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, int)
        f.write(line_prefix)
        f.write(resource.file.memory_context.get_c_reference_at_segmented(v))
        return True

    def write_waterBoxes(
        resource: "CollisionResource", v, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, int)
        length = resource.cdata_unpacked["numWaterBoxes"]
        f.write(line_prefix)
        if length != 0:
            f.write(resource.file.memory_context.get_c_reference_at_segmented(v))
        else:
            if v == 0:
                f.write("NULL")
            else:
                f.write(f"0x{v:08X}")
        return True

    cdata_ext = CDataExt_Struct(
        (
            ("minBounds", Vec3s),
            ("maxBounds", Vec3s),
            ("numVertices", CDataExt_Value("H").set_write(write_numVertices)),
            ("pad14", CDataExt_Value.pad16),
            (
                "vtxList",
                CDataExt_Value("I").set_report(report_vtxList).set_write(write_vtxList),
            ),  # Vec3s*
            ("numPolygons", CDataExt_Value("H").set_write(write_numPolygons)),
            ("pad22", CDataExt_Value.pad16),
            (
                "polyList",
                CDataExt_Value("I")
                .set_report(report_polyList)
                .set_write(write_polyList),
            ),  # CollisionPoly*
            (
                "surfaceTypeList",
                CDataExt_Value("I").set_write(write_surfaceTypeList),
            ),  # SurfaceType*
            ("bgCamList", CDataExt_Value("I").set_write(write_bgCamList)),  # BgCamInfo*
            ("numWaterBoxes", CDataExt_Value("H").set_write(write_numWaterBoxes)),
            ("pad38", CDataExt_Value.pad16),
            (
                "waterBoxes",
                CDataExt_Value("I")
                .set_report(report_waterBoxes)
                .set_write(write_waterBoxes),
            ),  # WaterBox*
        )
    )

    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, name)
        self.is_reported_surfaceTypeList = False
        self.is_reported_bgCamList = False

    def try_parse_data(self):
        super().try_parse_data()

        #  report surfaceTypeList based on its length guessed from polyList data

        resolution, resolution_info = self.file.memory_context.resolve_segmented(
            self.cdata_unpacked["polyList"]
        )
        if resolution == SegmentedAddressResolution.SYMBOL:
            raise NotImplementedError()
        elif resolution == SegmentedAddressResolution.FILE:
            assert isinstance(resolution_info, tuple)
            file, offset = resolution_info
            assert isinstance(file, File)
            assert isinstance(offset, int)

            result, resource = file.get_resource_at(offset)
            assert result == GetResourceAtResult.DEFINITIVE
            assert resource is not None
            assert isinstance(resource, CollisionPolyListResource)

            if resource.is_data_parsed:
                length_surfaceTypeList = resource.max_surface_type_index + 1
                self.file.memory_context.report_resource_at_segmented(
                    self.cdata_unpacked["surfaceTypeList"],
                    lambda file, offset: CollisionSurfaceTypeListResource(
                        file,
                        offset,
                        f"{self.name}_SurfaceTypes_",
                        length_surfaceTypeList,
                    ),
                )
                self.is_reported_surfaceTypeList = True
        else:
            raise NotImplementedError(resolution)

        if self.is_reported_surfaceTypeList:

            #  report bgCamList based on its length guessed from surfaceTypeList data

            resolution, resolution_info = self.file.memory_context.resolve_segmented(
                self.cdata_unpacked["surfaceTypeList"]
            )
            if resolution == SegmentedAddressResolution.SYMBOL:
                raise NotImplementedError()
            elif resolution == SegmentedAddressResolution.FILE:
                assert isinstance(resolution_info, tuple)
                file, offset = resolution_info
                assert isinstance(file, File)
                assert isinstance(offset, int)

                result, resource = file.get_resource_at(offset)
                assert result == GetResourceAtResult.DEFINITIVE
                assert resource is not None
                assert isinstance(resource, CollisionSurfaceTypeListResource)

                if resource.is_data_parsed:
                    length_bgCamList = resource.max_bgCamIndex + 1
                    self.file.memory_context.report_resource_at_segmented(
                        self.cdata_unpacked["bgCamList"],
                        lambda file, offset: CollisionBgCamListResource(
                            file,
                            offset,
                            f"{self.name}_BgCamList_",
                            length_bgCamList,
                        ),
                    )
                    self.is_reported_bgCamList = True
            else:
                raise NotImplementedError(resolution)

        self.is_data_parsed = (
            self.is_reported_surfaceTypeList and self.is_reported_bgCamList
        )

    def get_c_declaration_base(self):
        return f"CollisionHeader {self.symbol_name}"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()
