from pathlib import Path
from xml.etree import ElementTree
import functools
from pprint import pprint

from .extase import MemoryContext, File

from . import xml_errors
from . import z64_resource_handlers

#
# main
#

VERBOSE1 = False
VERBOSE_DUMMY_SEGMENT = False

# "options"
RM_SOURCE = True
WRITE_SOURCE = True
RM_EXTRACT = True
WRITE_EXTRACT = True
from ..conf import WRITE_HINTS, I_D_OMEGALUL


BASEROM_PATH = Path("baserom")
BUILD_PATH = Path("build")


@functools.lru_cache(maxsize=200)
def get_baserom_file_data(baserom_file_name: str):
    return memoryview((BASEROM_PATH / baserom_file_name).read_bytes())


def xml_process_file(
    memory_context: MemoryContext,
    file_elem: ElementTree.Element,
    files_by_segment: dict[
        int, list[File]
    ],  # mutable, contents modified by this function
):
    """Create a File object from a <File> xml element.

    Handles all the <File> attributes.

    Returns a (file, file_range_start) tuple that contains the new File object,
    and the RangeStart offset value (file_range_start, typically 0).

    About why file_range_start is returned:
     Resource objects of File objects handle offsets relative to the start of
     the File, but xml resource elements in <File> elements are relative to
     the start of the full data of the base file (baserom file).
     So file_range_start is needed when processing xml resource elements, to
     go from offsets relative to the start of the base file, to offsets relative
     to file_range_start.
     Note that typically file_range_start is 0 when a whole baserom file
     corresponds to a single <File> / File object.

    This does not process the resources inside the <File>
    (for that, see xml_process_resources_of_file)
    """

    assert file_elem.tag == "File"  # Already checked
    xml_errors.xml_check_attributes(
        file_elem,
        {"Name"},
        {"OutName", "RangeStart", "RangeEnd", "Segment", "BaseAddress"},
    )

    baserom_file_name = file_elem.attrib["Name"]

    file_name = file_elem.attrib.get("OutName")
    if file_name is None:
        file_name = baserom_file_name

    file_bytes_all = get_baserom_file_data(baserom_file_name)

    # Handle range start/end, if any,
    # or default to start/end of the full data.

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

    # Create the File object
    file = File(memory_context, file_name, file_bytes_ranged)

    # Handle where in memory is this file (nowhere, segment or vram)

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

    if segment_str is not None and file_base_ram_start_str is not None:
        # It doesn't entirely not make sense,
        # but it's probably a mistake, so just error.
        raise Exception(
            "It doesn't make sense for both Segment and BaseAddress to be set",
            file_name,
        )

    return file, file_range_start


# TODO hack
def HACK_handle_symbol_fakeresource(
    file_elem: ElementTree.Element, file: File, resource_elem: ElementTree.Element
):
    assert file_elem.tag == "File", file_elem.tag  # Already checked
    assert (
        "BaseAddress" in file_elem.attrib
    )  # TODO if not in vram idk what <Symbol> means

    assert resource_elem.tag == "Symbol", resource_elem.tag  # Already checked
    xml_errors.xml_check_attributes(
        resource_elem, {"Name", "Type", "TypeSize", "Offset"}, {"Count"}
    )

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


def xml_process_resources_of_file(
    file_elem: ElementTree.Element, file: File, file_range_start: int
):
    """Collect resources from the xml into the file object.

    Turn resource elements from the xml (children of <File>) into resource objects,
    and adds them to the file object.

    Does not do any processing of the data itself: no parsing, no discovering more resources.
    """

    assert file_elem.tag == "File"  # Already checked

    prev_resource = None

    for resource_elem in file_elem:

        # TODO this is hacky but for now I don't see a non-hacky way to handle this hacky not-a-resource
        if resource_elem.tag == "Symbol":
            HACK_handle_symbol_fakeresource(file_elem, file, resource_elem)

            # Clear the prev resource I guess?
            prev_resource = None
            continue

        # A resource element is allowed to not set Offset,
        # then its start offset defaults to the end offset of the element before it.
        if prev_resource is not None:
            # Note this may be None
            default_offset = prev_resource.range_end
        else:
            default_offset = None

        base_file_offset_str = resource_elem.attrib.get("Offset")
        if base_file_offset_str is None:
            if default_offset is None:
                # TODO better message
                raise Exception("no Offset nor default_offset")
            file_offset = default_offset
        else:
            base_file_offset = int(base_file_offset_str, 16)
            # Offset in the xml is relative to the base file (baserom file),
            # while resource ranges are relative to the start of the File.
            # Subtracting file_range_start accounts for that.
            # Typically a File is the full base file and file_range_start is 0.
            file_offset = base_file_offset - file_range_start

        resource = z64_resource_handlers.get_resource_from_xml(
            file, resource_elem, file_offset
        )

        file.add_resource(resource)

        prev_resource = resource

    # At this point, all xml-declared resources were turned into the
    # appropriate resource objects, with no parsing nor discovering
    # other resources done at all (yet).
    # So the file resources are exactly the ones declared in the xml.

    if VERBOSE1:
        print(file)
        print(file.name, file._resources)

    # Check if xml-declared resources overlap
    file.sort_resources()
    file.check_overlapping_resources()


def extract_xml(sub_path: Path):
    """
    sub_path: Path under assets/ such as objects/gameplay_keep
    Uses the xml file assets/xml/ sub_path .xml
    """
    top_xml_path = (Path("assets/xml/") / sub_path).with_suffix(".xml")
    top_source_path = Path("assets/") / sub_path
    top_extract_path = Path("assets/_extracted/") / sub_path

    memory_context = MemoryContext(I_D_OMEGALUL=I_D_OMEGALUL)  # TODO

    # TODO dummy segments config
    class DummyData:
        def __init__(self, size: int):
            self.size = size

        def __len__(self):
            return self.size

    class DummyResource:
        def __init__(self, segment_num: int, range_start: int):
            self.segment_num = segment_num
            self.range_start = range_start

        def get_c_reference(self, resource_offset: int):
            addr = (self.segment_num << 24) | (self.range_start + resource_offset)
            return f"0x{addr:08X}"

    # "parse" as long as data is being parsed, so the dummy file receives "real" reported resources,
    # then set to "write" which 'locks' the DummyFile instances and makes them return DummyResource for non-definitive offsets
    DUMMY_MODE = "parse"

    class DummyFile(File):
        def __init__(
            self, memory_context: MemoryContext, name: str, size: int, segment_num: int
        ):
            super().__init__(memory_context, name, DummyData(size))
            self.segment_num = segment_num

        def get_resource_at(self, offset: int):
            result, resource = super().get_resource_at(offset)
            from .extase import GetResourceAtResult

            if result == GetResourceAtResult.DEFINITIVE or DUMMY_MODE == "parse":
                if DUMMY_MODE == "write":
                    resource.segment_num = self.segment_num

                    def get_c_reference(resource_offset):
                        return DummyResource.get_c_reference(resource, resource_offset)

                    resource.get_c_reference = get_c_reference
                    from .extase_oot64 import dlist_resources

                    if isinstance(resource, dlist_resources.TextureResource):
                        resource.width_name = f"{resource.width}"
                        resource.height_name = f"{resource.height}"
                return result, resource
            else:
                return GetResourceAtResult.DEFINITIVE, DummyResource(
                    self.segment_num, offset
                )

    def set_dummy_segment(memory_context: MemoryContext, segment_num: int):
        if VERBOSE_DUMMY_SEGMENT:
            print("Setting dummy segment", segment_num)
        memory_context.set_segment(
            segment_num,
            DummyFile(
                memory_context,
                f"dummy_segment_{segment_num}",
                1024 * 1024,
                segment_num,
            ),
        )

    if sub_path.is_relative_to("objects") or sub_path.is_relative_to("overlays"):
        # billboardMtx, typically (but not always) TODO
        set_dummy_segment(memory_context, 1)

    if sub_path.is_relative_to("scenes"):
        # TODO this may be more refined, cf scene configs
        for segment_num in (0x6, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD):
            set_dummy_segment(memory_context, segment_num)

    if sub_path.is_relative_to("objects") or sub_path.is_relative_to("overlays"):
        if str(sub_path) in {
            "objects/object_mori_objects",
            "objects/object_mori_hineri2",
            "objects/object_mori_tex",
            "objects/object_mori_hineri1a",
            "objects/object_mori_hineri1",
            "objects/object_mori_hineri2a",
        }:
            set_dummy_segment(memory_context, 9)
        else:
            # TODO this can be more refined, but it's a lot of work
            for segment_num in (0x8, 0x9):
                set_dummy_segment(memory_context, segment_num)

    for segment_num, set_dummy_for_sub_paths in (
        (
            0x7,
            (
                "objects/object_ny",
                "objects/object_zf",
            ),
        ),
        (
            0xA,
            (
                "objects/object_warp1",
                "objects/object_ik",
                "objects/object_tw",
                "objects/object_efc_erupc",
                "objects/object_cne",
                "objects/object_po_composer",
                "objects/object_spot07_object",
                "objects/object_demo_kekkai",
                "objects/object_bv",
                "objects/object_po_field",
                "objects/object_gt",
                "objects/object_mizu_objects",
                "objects/object_mu",
                "overlays/ovl_Boss_Ganon",
            ),
        ),
        (
            0xB,
            (
                "objects/object_link_child",
                "objects/object_tw",
                "objects/object_po_composer",
                "objects/object_zl2",
                "objects/object_mu",
            ),
        ),
        (
            0xC,
            (
                "overlays/ovl_En_Ganon_Mant",
                "overlays/ovl_En_Jsjutan",
                "objects/object_bxa",
                "objects/object_rr",
                "objects/object_mo",
                "objects/object_zl2",
                "objects/object_ru2",
                "objects/object_skj",
                "objects/object_tw",
                "objects/object_rl",
                "objects/object_sa",
                "objects/object_nb",
                "objects/object_link_child",
                "objects/object_po_composer",
                "objects/object_kw1",
                "objects/object_im",
                "objects/object_bigokuta",
                "objects/object_link_boy",
                "objects/object_po_field",
                "objects/object_zo",
                "objects/object_du",
                "objects/object_torch2",
                "objects/object_km1",
                "objects/object_md",
                "objects/object_oE1s",
                "objects/object_fa",
                "objects/object_oE4s",
                "objects/object_mizu_objects",
                "objects/object_ru1",
            ),
        ),
        (
            0xD,
            (
                "objects/object_link_child",
                "objects/object_link_boy",
                "overlays/ovl_Boss_Ganon",
                "objects/object_oE12",
                "objects/object_oE4",
                "objects/object_oE5",
                "objects/object_oE7",
                "objects/object_oE9",
                "objects/object_oE3",
                "objects/object_oE10",
                "objects/object_oE11",
                "objects/object_oE1",
                "objects/object_blkobj",
                "objects/object_oE6",
                "objects/object_mo",
                "objects/object_oE8",
                "objects/object_oE2",
            ),
        ),
    ):
        if str(sub_path) in set_dummy_for_sub_paths:
            set_dummy_segment(memory_context, segment_num)

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

    def xml_process(xml_path: Path, source_path: Path):
        try:
            return xml_process_impl(xml_path, source_path)
        except xml_errors.XmlProcessError as e:
            e.set_xml_file_path_if_missing(xml_path)
            raise

    def xml_process_impl(xml_path: Path, source_path: Path):

        with xml_path.open() as f:
            xml = ElementTree.parse(f)

        root_elem = xml.getroot()

        xml_errors.xml_check_tag(root_elem, "Root")
        xml_errors.xml_check_attributes(root_elem, set(), set())

        # Files defined in the xml being processed (xml_path / xml)
        own_files: list[File] = []
        # Files defined by external xmls referenced by <ExternalFile>, **not recursive**
        # i.e. only contains the files from external xmls directly referenced by the current xml being processed
        #      and not any file from any "external external xml" referenced by external xml to the current xml
        # For example, if xml_path is a xml referencing gameplay_keep, gameplay_keep will be in direct_external_files,
        # but link_animetion (which is referenced by gameplay_keep) will **not** be in direct_external_files.
        direct_external_files: list[File] = []
        # Maps segment numbers to Files found for that segment
        # (files among "own files" and "direct external files", as described above)
        own_files_by_segment: dict[int, list[File]] = dict()
        direct_external_files_by_segment: dict[int, list[File]] = dict()

        for file_elem in root_elem:
            xml_errors.xml_check_tag(file_elem, {"File", "ExternalFile"})

            if file_elem.tag == "File":
                assert file_elem.tag == "File"

                file, file_range_start = xml_process_file(
                    memory_context, file_elem, own_files_by_segment
                )

                xml_process_resources_of_file(file_elem, file, file_range_start)

                # Call these for every file before writing anything,
                # since the paths may be used by some files to reference others.
                # For example for `#include`s.
                # It is fine to call this before the resources in the file are parsed,
                # since that has no bearing on the source path.
                # (also note the resources in the file may not even be parsed if this file
                #  isn't from the top xml, but from an external one instead)
                file.set_source_path(source_path)

                own_files.append(file)

            elif file_elem.tag == "ExternalFile":
                xml_errors.xml_check_attributes(
                    file_elem, {"XmlPath", "OutPath"}, set()
                )

                external_xml_partial_path_str = file_elem.attrib["XmlPath"]
                external_xml_path = Path("assets/xml") / external_xml_partial_path_str

                # From the ZAPD extraction XML reference:
                # > The path were the header for the corresponding external file is
                # For us, this is known as the "source path" where both the main .c and .h are.
                external_out_path_str = file_elem.attrib["OutPath"]
                external_out_path = Path(external_out_path_str)

                # TODO no protection from infinite recursion
                # also TODO no need to recurse more than once since recursive info is dropped
                #     actually this hints that the memorycontext should be per file and not global:
                #     the own and external direct defines the memoryctx for the current xml
                (
                    external_own_files,
                    external_direct_external_files,  # Ignore, since direct_external_ is not recursive.
                    external_own_files_by_segment,
                    external_direct_external_files_by_segment,  # same as external_direct_external_files
                ) = xml_process(external_xml_path, external_out_path)

                # Merge the external xml's own files information into the current xml's direct external information
                direct_external_files.extend(external_own_files)
                for segment_num, files in external_own_files_by_segment.items():
                    direct_external_files_by_segment.setdefault(segment_num, []).extend(
                        files
                    )

            else:
                assert False, file_elem.tag

        if __debug__:
            names = [file.name for file in direct_external_files]
            assert len(names) == len(set(names)), direct_external_files

        return (
            own_files,
            direct_external_files,
            own_files_by_segment,
            direct_external_files_by_segment,
        )

    (
        top_own_files,
        top_direct_external_files,
        top_own_files_by_segment,
        top_direct_external_files_by_segment,
    ) = xml_process(top_xml_path, top_source_path)

    # The "top" segment mapping comes from the top xml and its direct external files
    top_files_by_segment: dict[int, list[File]] = dict()
    for _files_by_segment in (
        top_own_files_by_segment,
        top_direct_external_files_by_segment,
    ):
        for segment_num, files in _files_by_segment.items():
            top_files_by_segment.setdefault(segment_num, []).extend(files)

    # Disputed segments are segments that several files were set to use (with the Segment attribute).
    # For example, segment 3 is typically used by the several room files associated to a scene.
    # But only one file can be set on a segment at once, because a segment simply cannot point to
    # several things at once.
    # This is resolved by figuring out the disputed segments, and (for now) only setting the segment
    # bases (with MemoryContext.set_segment) for non-disputed segments that are used by a single file.
    # Later, when parsing/extracting, disputed segments are set according to the current file being
    # parsed/extracted.
    # For example with scenes and rooms, while the scene is parsed segment 3 is unset,
    # and while a room is parsed segment 3 is set to that file.
    disputed_segments: list[int] = []
    for segment_num, files in top_files_by_segment.items():
        if len(files) == 1:
            file = files[0]
            memory_context.set_segment(segment_num, file)
        else:
            for file in files:
                if file not in top_own_files:
                    # This is not really a problem for processing but it's weird enough
                    # to raise an error.
                    # For example it could happen if a scene xml had a ExternalFile
                    # for another scene xml (which afaict doesn't make sense) (TODO test)
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
                        top_own_files,
                    )
            disputed_segments.append(segment_num)

    if len(disputed_segments) > 1:
        # TODO this may actually be fine but idk
        raise NotImplementedError(disputed_segments)

    def for_each_file_with_adequate_memory_context(callback):
        results = []

        for file in top_own_files:

            # Save the current segment map, before setting disputed segments,
            # and to be restored before moving on from this file
            saved_segment_map = memory_context.save_segment_map()

            for segment_num in disputed_segments:
                if file in top_files_by_segment[segment_num]:
                    memory_context.set_segment(segment_num, file)

            # TODO along with dummy segments cleanup: clean this hack
            # set 0xD dummy segment for flex skeletons
            from .extase_oot64.skeleton_resources import SkeletonFlexResource

            if any(isinstance(r, SkeletonFlexResource) for r in file._resources):
                set_dummy_segment(memory_context, 0xD)
            # end flex seg hack

            res = callback(file)
            results.append(res)

            # At this point the file is completely mapped with resources
            # (though per the above TODO this will be reworked)

            file.set_resources_paths(top_extract_path, BUILD_PATH)

            if VERBOSE1:
                print(file.str_report())

            memory_context.restore_segment_map(saved_segment_map)

        return results

    # 2) parse: iteratively discover and parse data
    # (discover = add resources, parse = make friendlier than binary)

    def file_try_parse_resources_data(file: File):
        any_progress = file.try_parse_resources_data()

        # TODO rework resource buffers
        # FIXME this may be a bad place to put this but idk. Ideally would call this after a single file is fully parsed,
        # but since the memctx may switch segment base for the resource buffers we also can't keep the markers alive across
        # iterations in for_each_file_with_adequate_memory_context
        file.memory_context.report_resource_buffers()

        return any_progress

    def parse_all_files():
        while True:
            results_any_progress = for_each_file_with_adequate_memory_context(
                file_try_parse_resources_data
            )
            any_progress = any(results_any_progress)
            if not any_progress:
                break

        for file in top_own_files:
            file.check_non_parsed_resources()

    parse_all_files()

    for file in top_own_files:
        file.sort_resources()
        file.check_overlapping_resources()

    # 3) add dummy (binary) resources for the unaccounted gaps

    def file_add_unaccounted_resources(file: File):
        file.add_unaccounted_resources()

    for_each_file_with_adequate_memory_context(file_add_unaccounted_resources)

    parse_all_files()  # FIXME this is to set is_data_parsed=True on binary blob unaccounteds, handle better

    for file in top_own_files:
        file.sort_resources()
        assert not file.get_overlapping_resources()

    # 4)

    DUMMY_MODE = "write"

    def file_do_write(file: File):
        # write to assets/_extracted/
        if WRITE_EXTRACT:
            top_extract_path.mkdir(parents=True, exist_ok=True)

            file.write_resources_extracted()

        # "source" refers to the main .c and .h `#include`ing all the extracted resources
        if WRITE_SOURCE:
            top_source_path.mkdir(parents=True, exist_ok=True)

            # TODO fill referenced_files properly,
            # probably in MemoryContext when references to files are requested,
            # instead of assuming like here that all files in the xml / referenced by the xml
            # are included by all files the xml defines
            # (or if keeping the logic this way, write it better)
            file.referenced_files = set(top_own_files) | set(top_direct_external_files)
            file.write_source()

    for_each_file_with_adequate_memory_context(file_do_write)


def main():

    z64_resource_handlers.register_resource_handlers()

    XMLS_PATH = Path("assets/xml")

    def extract_all_xmls(subpath: Path, slice_start=None):
        path = XMLS_PATH / subpath
        xmls = list(path.glob("**/*.xml"))
        if slice_start:
            xmls = xmls[slice_start:]
        for i, xml in enumerate(xmls):
            sub_path = xml.relative_to(XMLS_PATH).with_suffix("")
            print(f"{i+1:4} / {len(xmls)}", int(i / len(xmls) * 100), sub_path)
            extract_xml(sub_path)

    # extract_xml(Path("objects/object_am"))
    # extract_xml(Path("scenes/indoors/hylia_labo"))
    # extract_xml(Path("objects/gameplay_keep"))
    # extract_xml(Path("overlays/ovl_En_Jsjutan"))  # The only xml with <Symbol>
    # extract_xml(Path("overlays/ovl_Magic_Wind"))  # SkelCurve
    # extract_xml(Path("objects/object_link_child"))  # The only xml with <Mtx>
    # extract_xml(Path("scenes/dungeons/ddan")) # cutscene test
    # extract_xml(Path("scenes/dungeons/ganontikasonogo")) # has a spawn not in the entrance table
    extract_all_xmls(Path("objects"))
    extract_all_xmls(Path("scenes"))
    extract_all_xmls(Path("overlays"))
    extract_all_xmls(Path("code"))
    extract_all_xmls(Path("textures"))
    extract_all_xmls(Path("misc"))

    pprint(get_baserom_file_data.cache_info())
