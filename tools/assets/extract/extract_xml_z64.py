from pathlib import Path
from xml.etree import ElementTree
from pprint import pprint

from .extase import MemoryContext, File

from . import z64_resource_handlers

#
# main
#

# "options"
VERBOSE1 = False
RM_SOURCE = True
WRITE_SOURCE = True
RM_EXTRACT = True
WRITE_EXTRACT = True
from ..conf import WRITE_HINTS, I_D_OMEGALUL


BASEROM_PATH = Path("baserom")
BUILD_PATH = Path("build")


# 0) load the file data bytes
def xml_to_file_step0(
    memory_context: MemoryContext,
    file_elem: ElementTree.Element,
    files_by_segment: dict[
        int, list[File]
    ],  # mutable, contents modified by this function
):

    baserom_file_name = file_elem.attrib.get("Name")

    if baserom_file_name is None:
        raise Exception("baserom_file_name is None")

    file_name = file_elem.attrib.get("OutName")
    if file_name is None:
        file_name = baserom_file_name

    # TODO if the same file (on disk / in the rom) is used by several <File>s,
    # reading the file every time is very wasteful
    file_bytes_all = memoryview((BASEROM_PATH / baserom_file_name).read_bytes())

    file_range_start_str = file_elem.attrib.get("RangeStart")
    if file_range_start_str is not None:
        file_range_start = int(file_range_start_str, 16)
    else:
        file_range_start = 0
    file_range_end_str = file_elem.attrib.get("RangeEnd")
    if file_range_end_str is not None:
        file_range_end = int(file_range_end_str, 16)
    else:
        file_range_end = len(file_bytes_all)

    assert 0 <= file_range_start < file_range_end <= len(file_bytes_all), (
        hex(file_range_start),
        hex(file_range_end),
        hex(len(file_bytes_all)),
    )
    file_bytes_ranged = file_bytes_all[file_range_start:file_range_end]

    file = File(memory_context, file_name, file_bytes_ranged)

    # TODO not sure if this is the right place to set the segment,
    # maybe it should be more external
    segment_str = file_elem.attrib.get("Segment")
    if segment_str is not None:
        if file_range_start_str is not None:
            # this is just a sanity check
            # TODO not sure this case would be handled properly (or if it even makes sense)
            # (the current segmented addresses implementation (in MemoryContext)
            #  cannot map data at a segmented address with a non-0 offset)
            raise NotImplementedError(
                "RangeStart and Segment both used", file_name, file_elem
            )
        segment = int(segment_str)
        files_by_segment.setdefault(segment, []).append(file)

    file_base_ram_start_str = file_elem.attrib.get("BaseAddress")
    if file_base_ram_start_str is not None:
        file_base_ram_start = int(file_base_ram_start_str, 16)
        file_ram_start = file_base_ram_start + file_range_start
        memory_context.set_vram(file_ram_start, file)

    return file, file_range_start


# TODO hack
def HACK_handle_symbol_fakeresource(
    file_elem: ElementTree.Element, file: File, resource_elem: ElementTree.Element
):
    assert {"Name", "Type", "TypeSize", "Count", "Offset"}.issuperset(
        resource_elem.attrib.keys()
    )
    assert {"Name", "Type", "TypeSize", "Offset"}.issubset(resource_elem.attrib.keys())
    name = resource_elem.attrib["Name"]
    type_name = resource_elem.attrib["Type"]
    type_size_str = resource_elem.attrib["TypeSize"]
    type_size = int(type_size_str)
    count_str = resource_elem.attrib.get("Count")
    if count_str is not None:
        count = int(count_str, 16)
    else:
        count = None
    offset_str = resource_elem.attrib["Offset"]
    offset = int(offset_str, 16)
    from .extase import Symbol

    range_start = int(file_elem.attrib["BaseAddress"], 16) + offset
    if count is None:
        range_end = range_start + type_size
    else:
        range_end = range_start + type_size * count
    sym = Symbol(name, range_start, range_end)
    if count is not None:

        def get_c_reference(offset: int):
            if offset == 0:
                return name
            if (offset % type_size) != 0:
                raise ValueError()
            index = offset // type_size
            return f"&{name}[{index}]"

        sym.get_c_reference = get_c_reference
    file.memory_context.vram_symbols.append(sym)


# 1) read resources as described from the xml
def xml_to_file_step1(
    file_elem: ElementTree.Element, file: File, file_range_start: int
):

    prev_resource = None

    for resource_elem in file_elem:

        # TODO this is hacky but for now I don't see a non-hacky way to handle this hacky not-a-resource
        if resource_elem.tag == "Symbol":
            HACK_handle_symbol_fakeresource(file_elem, file, resource_elem)

            # Clear the prev resource I guess?
            prev_resource = None
            continue

        if prev_resource is not None:
            default_offset = prev_resource.range_end
        else:
            default_offset = None

        # TODO centralize Offset logic in this function here, outside of get_resource_from_xml
        # and only pass the final offset to get_resource_from_xml
        # would avoid passing file_range_start further
        resource = z64_resource_handlers.get_resource_from_xml(
            file, resource_elem, file_range_start, default_offset
        )

        file.add_resource(resource)

        prev_resource = resource

    if VERBOSE1:
        print(file)
        print(file.name, file.resources)

    file.sort_resources()
    file.check_overlapping_resources()


# 2) parse: iteratively discover and parse data
# (discover = add resources, parse = make friendlier than binary)
def xml_to_file_step2(file: File):

    file.parse_resources_data()

    # FIXME : bad code, shouldn't be here

    # also actually this won't play well with manually defined vtx arrays
    # probably can't merge the vbuf refs so quick

    for (
        resource_type,
        resource_buffer_markers,
    ) in file.memory_context.resource_buffer_markers_by_resource_type.items():
        if VERBOSE1:
            print(resource_type, resource_buffer_markers)
        for rbm in resource_buffer_markers:
            file.memory_context.report_resource_at_segmented(
                rbm.start,
                lambda file, offset: resource_type(
                    file, offset, offset + rbm.end - rbm.start, rbm.name
                ),
            )

    file.parse_resources_data()

    # end bad code

    file.sort_resources()
    file.check_overlapping_resources()


# 3) add dummy (binary) resources for the unaccounted gaps
def xml_to_file_step3(file: File):

    file.add_unaccounted_resources()

    file.parse_resources_data()  # FIXME this is to set is_data_parsed=True on binary blob unaccounteds, handle better

    file.sort_resources()
    assert not file.get_overlapping_resources()

    # done loading this file

    if VERBOSE1:
        pprint(file.resources)


def extract_object(object_name: str):
    extract_xml(Path("objects/") / object_name)


def extract_scene(subfolder: str, scene_name: str):
    extract_xml(Path("scenes/") / subfolder / scene_name)


def extract_overlaydata(ovl_name: str):
    extract_xml(Path("overlays/") / ovl_name)


def extract_codedata(coded_name: str):
    extract_xml(Path("code/") / coded_name)


def extract_filetexture(ftex_name: str):
    extract_xml(Path("textures/") / ftex_name)


def extract_xml(sub_path: Path):
    """
    sub_path: Path under assets/ such as objects/gameplay_keep
    Uses the xml file assets/xml/ sub_path .xml
    """
    top_xml_path = (Path(f"assets/xml/") / sub_path).with_suffix(".xml")
    top_source_path = Path(f"assets/") / sub_path
    top_extract_path = Path(f"assets/_extracted/") / sub_path

    memory_context = MemoryContext(I_D_OMEGALUL=I_D_OMEGALUL)  # TODO

    # TODO dummy segments config
    class DummyData:
        def __init__(self, size: int):
            self.size = size

        def __len__(self):
            return self.size

    class DummyResource:
        def __init__(self, range_start):
            self.range_start = range_start

        def get_c_reference(self, resource_offset: int):
            addr = 0x0C00_0000 | (self.range_start + resource_offset)
            return f"0x{addr:08X}"

    class DummyFile(File):
        def __init__(self, memory_context: MemoryContext, name: str, size: int):
            super().__init__(memory_context, name, DummyData(size))

        def get_resource_at(self, offset: int):
            from .extase import GetResourceAtResult

            return GetResourceAtResult.DEFINITIVE, DummyResource(offset)

    if str(sub_path) in {
        "overlays/ovl_En_Ganon_Mant",
        "overlays/ovl_En_Jsjutan",
    }:
        memory_context.set_segment(
            0xC, DummyFile(memory_context, "dummy_segment_12", 1024 * 1024)
        )

    if RM_SOURCE:
        import shutil

        if top_source_path.exists():
            shutil.rmtree(top_source_path)
    if RM_EXTRACT:
        import shutil

        if top_extract_path.exists():
            shutil.rmtree(top_extract_path)

        if (BUILD_PATH / top_extract_path).exists():
            # FIXME needed to prevent issues with similar paths build/assets/_extracted/xxx and assets/_extracted/xxx
            # (due to include path having build/ and ./ )
            shutil.rmtree(BUILD_PATH / top_extract_path)

    def mainxml_wrap_steps01(xml_path: Path, source_path: Path):

        with xml_path.open() as f:
            xml = ElementTree.parse(f)

        root_elem = xml.getroot()

        assert root_elem.tag == "Root", root_elem.tag
        assert set().issuperset(root_elem.attrib.keys()), root_elem.attrib

        files_to_do_stuff_with: list[File] = []
        external_files_all: list[File] = []
        files_by_segment: dict[int, list[File]] = dict()

        for file_elem in root_elem:
            assert file_elem.tag in {"File", "ExternalFile"}, file_elem.tag

            if file_elem.tag == "ExternalFile":
                assert {
                    "XmlPath",
                    "OutPath",
                }.issuperset(file_elem.attrib.keys()), file_elem.attrib
                external_xml = file_elem.attrib["XmlPath"]

                # From the ZAPD extraction XML reference:
                # > The path were the header for the corresponding external file is
                # For us, this is known as the "source path" where both the main .c and .h are.
                external_out_path_str = file_elem.attrib["OutPath"]
                external_out_path = Path(external_out_path_str)

                # TODO no protection from infinite recursion
                (
                    external_files_to_do_stuff_with,
                    _,  # external_files_all for the file external to the current xml_path, ignore (TODO?)
                    external_files_by_segment,  # files_by_segment for the external files
                ) = mainxml_wrap_steps01(
                    Path("assets/xml") / external_xml, external_out_path
                )

                external_files_all.extend(external_files_to_do_stuff_with)

                # Recursively collect all files set on each segment
                # (TODO idk if this makes more sense than only taking
                #  the immediate neighbours like for external_files_all)
                for segment_num, files in external_files_by_segment.items():
                    files_by_segment.setdefault(segment_num, []).extend(files)

                continue

            assert file_elem.tag == "File"
            assert {
                "Name",
                "OutName",
                "Segment",
                "BaseAddress",
                "RangeStart",
                "RangeEnd",
            }.issuperset(file_elem.attrib.keys()), file_elem.attrib

            file, file_range_start = xml_to_file_step0(
                memory_context, file_elem, files_by_segment
            )

            xml_to_file_step1(file_elem, file, file_range_start)

            # Call these for every file before writing anything,
            # since the paths may be used by some files to reference others.
            # For example for `#include`s.
            # It is fine to call this before the resources in the file are parsed,
            # since that has no bearing on the source path.
            # (also note the resources in the file may not even be parsed if this file
            # isn't from the top xml, but from an external one instead)
            file.set_source_path(source_path)

            # TODO step 1) should be done on several files if
            # there are several in the context, to have the
            # memory_context ready before going to step 2
            # -> this means this function should be split by step
            #     (or the steps moved at the memorycontext level but hmm)
            # this todo also applies to parsing data, that should be done
            # iteratively across all files at once instead of one file at a time
            files_to_do_stuff_with.append(file)

        if __debug__:
            names = [file.name for file in external_files_all]
            assert len(names) == len(set(names)), external_files_all

        return files_to_do_stuff_with, external_files_all, files_by_segment

    (
        top_files_to_do_stuff_with,
        top_external_files_to_include,
        top_files_by_segment,
    ) = mainxml_wrap_steps01(top_xml_path, top_source_path)

    disputed_segments: list[int] = []
    for segment_num, files in top_files_by_segment.items():
        if len(files) == 1:
            file = files[0]
            memory_context.set_segment(segment_num, file)
        else:
            for file in files:
                if file not in top_files_to_do_stuff_with:
                    raise Exception(
                        "Segment is used for several files,"
                        " so it would normally be set to each file as they are processed one by one."
                        " But (at least) one of the files using the segment is not a file that is going to be processed,"
                        " so the segment would never be set to point to it."
                        " A 'fix' could be to rework the contents of xmls indicated as external,"
                        " so they don't use segment also used by the main processed xml.",
                        segment_num,
                        files,
                        file,
                        top_files_to_do_stuff_with,
                    )
            disputed_segments.append(segment_num)

    if len(disputed_segments) > 1:
        # TODO this may actually be fine but idk
        raise NotImplementedError(disputed_segments)

    # solves the above TODO about step 1 and splitting by step, maybe
    for file in top_files_to_do_stuff_with:

        saved_segment_map = memory_context.save_segment_map()

        for segment_num in disputed_segments:
            if file in top_files_by_segment[segment_num]:
                memory_context.set_segment(segment_num, file)

        xml_to_file_step2(file)
        # TODO run all step2 before any step3 ? (I think that's part of the "TODO step 1)" above)
        xml_to_file_step3(file)

        file.set_resources_paths(top_extract_path, BUILD_PATH)

        if VERBOSE1:
            print(file.str_report())

        memory_context.restore_segment_map(saved_segment_map)

    for file in top_files_to_do_stuff_with:

        saved_segment_map = memory_context.save_segment_map()

        for segment_num in disputed_segments:
            if file in top_files_by_segment[segment_num]:
                memory_context.set_segment(segment_num, file)

        if WRITE_EXTRACT:
            top_extract_path.mkdir(parents=True, exist_ok=True)

            file.write_resources_extracted()

        if WRITE_SOURCE:
            top_source_path.mkdir(parents=True, exist_ok=True)

            # TODO fill referenced_files properly,
            # probably in MemoryContext when references to files are requested,
            # instead of assuming like here that all files in the xml / referenced by the xml
            # are included by all files the xml defines
            # (or if keeping the logic this way, write it better)
            file.referenced_files = set(top_files_to_do_stuff_with) | set(
                top_external_files_to_include
            )
            file.write_source()

        memory_context.restore_segment_map(saved_segment_map)


def main():

    z64_resource_handlers.register_resource_handlers()

    def extract_all_objects():
        xmls = list(Path("assets/xml/objects/").glob("*.xml"))
        # xmls = xmls[250:]
        for i, object_xml in enumerate(xmls):
            object_name = object_xml.stem
            print(f"{i+1:4} / {len(xmls)}", int(i / len(xmls) * 100), object_name)
            extract_object(object_name)

    def extract_all_scenes():
        xmls = list(Path("assets/xml/scenes/").glob("**/*.xml"))
        for i, scene_xml in enumerate(xmls):
            subfolder = scene_xml.parent.name
            scene_name = scene_xml.stem
            print(
                f"{i+1:4} / {len(xmls)}",
                int(i / len(xmls) * 100),
                subfolder,
                scene_name,
            )
            extract_scene(subfolder, scene_name)

    def extract_all_overlaysdata():
        xmls = list(Path("assets/xml/overlays/").glob("*.xml"))
        # xmls = xmls[250:]
        for i, ovld_xml in enumerate(xmls):
            ovl_name = ovld_xml.stem
            print(f"{i+1:4} / {len(xmls)}", int(i / len(xmls) * 100), ovl_name)
            extract_overlaydata(ovl_name)

    def extract_all_codedata():
        xmls = list(Path("assets/xml/code/").glob("*.xml"))
        # xmls = xmls[250:]
        for i, coded_xml in enumerate(xmls):
            coded_name = coded_xml.stem
            print(f"{i+1:4} / {len(xmls)}", int(i / len(xmls) * 100), coded_name)
            extract_codedata(coded_name)

    def extract_all_filetextures():
        xmls = list(Path("assets/xml/textures/").glob("*.xml"))
        # xmls = xmls[250:]
        for i, ftex_xml in enumerate(xmls):
            ftex_name = ftex_xml.stem
            print(f"{i+1:4} / {len(xmls)}", int(i / len(xmls) * 100), ftex_name)
            extract_filetexture(ftex_name)

    # extract_scene("indoors", "hylia_labo")
    # extract_object("gameplay_keep")
    # extract_overlaydata("ovl_En_Jsjutan")  # The only xml with <Symbol>
    # extract_overlaydata("ovl_Magic_Wind")  # SkelCurve
    extract_all_objects()
    extract_all_scenes()
    extract_all_overlaysdata()
    extract_all_codedata()
    extract_all_filetextures()
