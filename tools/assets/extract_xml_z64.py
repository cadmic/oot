from pathlib import Path
from xml.etree import ElementTree
from pprint import pprint

from extase import MemoryContext, File

import z64_resource_handlers

#
# main
#

# "options"
VERBOSE1 = False
RM_SOURCE = True
WRITE_SOURCE = True
RM_EXTRACT = True
WRITE_EXTRACT = True
from conf import WRITE_HINTS, I_D_OMEGALUL


BASEROM_PATH = Path("baserom")
BUILD_PATH = Path("build")


# 0) load the file data bytes
def xml_to_file_step0(memory_context: MemoryContext, file_elem: ElementTree.Element):

    file_name = file_elem.attrib.get("Name")

    if file_name is None:
        raise Exception("file_name is None")

    file_bytes = memoryview((BASEROM_PATH / file_name).read_bytes())

    file = File(memory_context, file_name, file_bytes)

    # TODO not sure if this is the right place to set the segment,
    # maybe it should be more external
    segment_str = file_elem.attrib.get("Segment")
    if segment_str is not None:
        segment = int(segment_str)
        memory_context.set_segment(segment, file)

    return file


# 1) read resources as described from the xml
def xml_to_file_step1(file_elem: ElementTree.Element, file: File):

    prev_resource = None

    for resource_elem in file_elem:

        if prev_resource is not None:
            default_offset = prev_resource.range_end
        else:
            default_offset = None

        resource = z64_resource_handlers.get_resource_from_xml(
            file, resource_elem, default_offset
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


def extract_object(object_name):
    top_xml_path = Path(f"assets/xml/objects/{object_name}.xml")
    source_path = Path(f"assets/objects/{object_name}/")
    extract_path = Path(f"assets/_extracted/objects/{object_name}/")

    memory_context = MemoryContext(I_D_OMEGALUL=I_D_OMEGALUL)  # TODO

    if RM_SOURCE:
        import shutil

        if source_path.exists():
            shutil.rmtree(source_path)
    if RM_EXTRACT:
        import shutil

        if extract_path.exists():
            shutil.rmtree(extract_path)

        if (BUILD_PATH / extract_path).exists():
            # FIXME needed to prevent issues with similar paths build/assets/_extracted/xxx and assets/_extracted/xxx
            # (due to include path having build/ and ./ )
            shutil.rmtree(BUILD_PATH / extract_path)

    def mainxml_wrap_steps01(xml_path: Path):

        with xml_path.open() as f:
            xml = ElementTree.parse(f)

        root_elem = xml.getroot()

        assert root_elem.tag == "Root", root_elem.tag

        files_to_do_stuff_with: list[File] = []
        external_files_to_include = (
            []
        )  # TODO figure out how to properly handle building paths to .h files

        for file_elem in root_elem:
            if file_elem.tag == "ExternalFile":
                external_xml = file_elem.attrib["XmlPath"]
                external_out_path = file_elem.attrib["OutPath"]
                # TODO what with OutPath?
                mainxml_wrap_steps01(Path("assets/xml") / external_xml)

                external_files_to_include.append(
                    str(Path(external_out_path) / Path(external_xml).stem) + ".h"
                )
                continue

            assert file_elem.tag == "File", file_elem.tag

            # start previously File.from_xml
            # (some stuff changed too and split into xml_to_file_)

            file = xml_to_file_step0(memory_context, file_elem)

            xml_to_file_step1(file_elem, file)

            # TODO step 1) should be done on several files if
            # there are several in the context, to have the
            # memory_context ready before going to step 2
            # -> this means this function should be split by step
            #     (or the steps moved at the memorycontext level but hmm)
            # this todo also applies to parsing data, that should be done
            # iteratively across all files at once instead of one file at a time
            files_to_do_stuff_with.append(file)

        return files_to_do_stuff_with, external_files_to_include

    top_files_to_do_stuff_with, top_external_files_to_include = mainxml_wrap_steps01(
        top_xml_path
    )

    # solves the above TODO about step 1 and splitting by step, maybe
    for file in top_files_to_do_stuff_with:

        xml_to_file_step2(file)

        xml_to_file_step3(file)

        # end previously File.from_xml

        extract_path.mkdir(parents=True, exist_ok=True)
        file.set_resources_paths(extract_path, BUILD_PATH)

        if VERBOSE1:
            print(file.str_report())

        if WRITE_EXTRACT:
            file.write_resources_extracted()

        if WRITE_SOURCE:
            source_path.mkdir(parents=True, exist_ok=True)

            file.write_source(
                source_path, additional_includes=top_external_files_to_include
            )


def main():

    z64_resource_handlers.register_resource_handlers()

    if False:
        for object_name in ["gameplay_keep"]:
            extract_object(object_name)

    if True:
        xmls = list(Path("assets/xml/objects/").glob("*.xml"))
        # xmls = xmls[250:]
        for i, object_xml in enumerate(xmls):
            object_name = object_xml.stem
            print(f"{i+1:4} / {len(xmls)}", int(i / len(xmls) * 100), object_name)
            extract_object(object_name)
