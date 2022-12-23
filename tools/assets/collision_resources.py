import io

from extract_xml import (
    SegmentedAddressResolution,
    File,
    CDataResource,
    CDataExt_Struct,
    CDataExt_Array,
    CDataExt_Value,
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
    cdata_ext_elem = CDataExt_Struct(
        (
            ("type", CDataExt_Value.u16),
            ("vtxData", CDataExt_Array(CDataExt_Value.u16, 3)),
            ("normal", Vec3s),
            ("dist", CDataExt_Value.s16),
        )
    )

    def __init__(self, file: File, range_start: int, name: str, length: int):
        self.cdata_ext = CDataExt_Array(self.cdata_ext_elem, length)
        super().__init__(file, range_start, name)

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
    cdata_ext_elem = CDataExt_Struct((("data", CDataExt_Array(CDataExt_Value.u32, 2)),))


class CollisionBgCamListResource(CDataResource):
    cdata_ext_elem = CDataExt_Struct(
        (
            ("setting", CDataExt_Value.u16),
            ("count", CDataExt_Value.s16),
            ("bgCamFuncData", CDataExt_Value.pointer),  # Vec3s*
        )
    )


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
            ("surfaceTypeList", CDataExt_Value.pointer),  # SurfaceType*
            ("bgCamList", CDataExt_Value.pointer),  # BgCamInfo*
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

    def try_parse_data(self):
        super().try_parse_data()

        return  # TODO report surfaceTypeList, bgCamList based on their lengths guessed from polyList and waterBoxes data

        resolution, resolution_info = self.file.memory_context.resolve_segmented(
            self.cdata_unpacked["bgCamList"]
        )
        if resolution == SegmentedAddressResolution.SYMBOL:
            raise NotImplementedError()
        elif resolution == SegmentedAddressResolution.FILE:
            assert isinstance(resolution_info, tuple)
            file, offset = resolution_info
            assert isinstance(file, File)
            assert isinstance(offset, int)

            ...
        else:
            raise NotImplementedError()

        self.is_data_parsed = False

    def get_c_declaration_base(self):
        return f"CollisionHeader {self.symbol_name}"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return f"&{self.symbol_name}"
        else:
            raise ValueError()
