from pathlib import Path
from xml.etree import ElementTree
import struct
import abc
from dataclasses import dataclass
from pprint import pprint
import enum

import io
from typing import Sequence, Optional, Callable, Any, Union


#
# memory context
#


class SegmentedAddressResolution(enum.Enum):
    SYMBOL = enum.auto()
    FILE = enum.auto()
    UNK_RAM = enum.auto()
    UNK_SEGMENTED = enum.auto()


@dataclass
class Symbol:
    name: str
    range_start: int  # physical
    range_end: int

    def get_c_reference(self, offset):
        if offset != 0:
            raise NotImplementedError("todo")
        # TODO if array, just name
        return f"&{self.name}"

    def get_c_expression_length(self, offset):
        raise NotImplementedError("todo x2")


@dataclass
class ResourceBufferMarker:
    name: str
    start: int  # segmented
    end: int  # segmented


class MemoryContext:
    """
    handles segmented addresses, pointers, external symbols (eg gMtxClear)

    maps offsets to data
    """

    def __init__(self):
        self.segments: dict[int, Optional["File"]] = {i: None for i in range(1, 16)}
        self.symbols: Sequence[Symbol] = (
            # TODO config for this
            Symbol("gMtxClear", 0x12DB80, 0x12DB80 + 0x40),
        )
        self.files_by_physical: dict[
            int, File
        ] = dict()  # range_start (physical) : file
        self.resource_buffer_markers_by_resource_type: dict[
            type[Resource], list[ResourceBufferMarker]
        ] = dict()

    def set_segment(self, segment_num: int, target: "File"):
        assert segment_num != 0
        assert segment_num < 16

        self.segments[segment_num] = target

    def resolve_physical(self, address: int):
        assert address < 8 * 1024 * 1024, (
            "addressing physical memory beyond 8MB of ram: " "this is probably wrong"
        )

        for symbol in self.symbols:
            if symbol.range_start <= address < symbol.range_end:
                offset = address - symbol.range_start
                return SegmentedAddressResolution.SYMBOL, (symbol, offset)

        if __debug__:
            for range_start_physical_a, file_a in self.files_by_physical.items():
                range_end_physical_a = range_start_physical_a + len(file_a.data)
                assert range_start_physical_a < range_end_physical_a
                for range_start_physical_b, file_b in self.files_by_physical.items():
                    range_end_physical_b = range_start_physical_b + len(file_b.data)
                    assert range_start_physical_b < range_end_physical_b
                    if file_a != file_b:
                        if range_end_physical_a <= range_start_physical_b:
                            assert (
                                range_start_physical_a
                                < range_end_physical_a
                                <= range_start_physical_b
                                < range_end_physical_b
                            )
                        else:
                            assert (
                                range_start_physical_b
                                < range_end_physical_b
                                <= range_start_physical_a
                                < range_end_physical_a
                            )

        for range_start_physical, file in self.files_by_physical.items():
            range_end_physical = range_start_physical + len(file.data)
            if range_start_physical <= address < range_end_physical:
                offset = address - range_start_physical
                if offset >= len(file.data):
                    raise Exception("offset is past the bounds of file", hex(address))
                return SegmentedAddressResolution.FILE, (file, offset)

        raise Exception("physical address maps to nothing", hex(address))

    def resolve_segmented(self, address: int):
        segment_num = (address & 0x0F00_0000) >> 24
        offset = address & 0x00FF_FFFF

        if segment_num == 0:
            return self.resolve_physical(offset)
        else:
            file = self.segments.get(segment_num)
            if file is None:
                raise Exception(
                    "no file set on this segment", hex(address), segment_num
                )
            if offset >= len(file.data):
                raise Exception("offset is past the bounds of file", hex(address))
            return SegmentedAddressResolution.FILE, (file, offset)

    def report_resource_at_segmented(
        self,
        address,
        new_resource_pointed_to: Callable[["File", int], "Resource"],
    ):
        resolution, resolution_info = self.resolve_segmented(address)

        if resolution == SegmentedAddressResolution.FILE:
            assert isinstance(resolution_info, tuple)
            file, offset = resolution_info
            assert isinstance(file, File)
            assert isinstance(offset, int)

            try:
                result, existing_resource = file.get_resource_at(offset)
            except:
                print(
                    "Couldn't get resource in file at offset",
                    hex(address),
                    file,
                    hex(offset),
                )
                raise

            if result == GetResourceAtResult.PERHAPS:
                # TODO
                print(
                    "!!! GetResourceAtResult.PERHAPS report_resource_at_segmented , may duplicate stuff idk !!!",
                    existing_resource,
                    existing_resource.name,
                )
            """
            assert (
                result != GetResourceAtResult.PERHAPS
            ), "Not sure how to handle this yet"
            """

            if result == GetResourceAtResult.DEFINITIVE:
                assert existing_resource is not None
                return existing_resource, offset
            else:
                new_resource = new_resource_pointed_to(file, offset)
                file.add_resource(new_resource)

                return new_resource, offset

        elif resolution == SegmentedAddressResolution.SYMBOL:
            assert isinstance(resolution_info, tuple)
            symbol, offset = resolution_info
            assert isinstance(symbol, Symbol)
            assert isinstance(offset, int)

            raise NotImplementedError(
                "not sure what to do here if it ever happens", resolution
            )

        else:
            raise NotImplementedError(
                "unhandled SegmentedAddressResolution", resolution
            )

    def mark_resource_buffer_at_segmented(
        self, resource_type: type["Resource"], name: str, start: int, end: int
    ):
        resource_buffer_markers = (
            self.resource_buffer_markers_by_resource_type.setdefault(resource_type, [])
        )
        resource_buffer_markers.append(ResourceBufferMarker(name, start, end))

        resource_buffer_markers.sort(key=lambda rbm: rbm.start)

        def do_fuse(i_start, i_end):
            assert i_start < i_end
            if i_start + 1 == i_end:
                return False
            fused = resource_buffer_markers[i_start:i_end]
            resource_buffer_markers[i_start:i_end] = [
                ResourceBufferMarker(
                    fused[0].name.removesuffix("_fused_") + "_fused_",  # TODO
                    fused[0].start,
                    fused[-1].end,
                )
            ]
            return True

        def fuse_more():
            stride_first_i = None
            for i, rbm in enumerate(resource_buffer_markers):
                if stride_first_i is None:
                    stride_first_i = i
                else:
                    assert i > 0
                    prev = resource_buffer_markers[i - 1]
                    if prev.end < rbm.start:
                        # disjointed
                        if do_fuse(stride_first_i, i):
                            return True
                        stride_first_i = i
            if stride_first_i is not None:
                return do_fuse(stride_first_i, len(resource_buffer_markers))
            else:
                return False

        while fuse_more():
            pass

    def get_c_reference_at_segmented(self, address):
        resolution, resolution_info = self.resolve_segmented(address)

        if resolution == SegmentedAddressResolution.FILE:
            assert isinstance(resolution_info, tuple)
            file, offset = resolution_info
            assert isinstance(file, File)
            assert isinstance(offset, int)

            result, resource = file.get_resource_at(offset)

            if result != GetResourceAtResult.DEFINITIVE:
                raise Exception("No definitive resource", result, hex(address))
            assert resource is not None

            resource_offset = offset - resource.range_start
            return resource.get_c_reference(resource_offset)

        elif resolution == SegmentedAddressResolution.SYMBOL:
            assert isinstance(resolution_info, tuple)
            symbol, offset = resolution_info
            assert isinstance(symbol, Symbol)
            assert isinstance(offset, int)

            return symbol.get_c_reference(offset)

        else:
            raise NotImplementedError(
                "unhandled SegmentedAddressResolution", resolution
            )

    def get_c_expression_length_at_segmented(self, address):
        resolution, resolution_info = self.resolve_segmented(address)

        if resolution == SegmentedAddressResolution.FILE:
            assert isinstance(resolution_info, tuple)
            file, offset = resolution_info
            assert isinstance(file, File)
            assert isinstance(offset, int)

            result, resource = file.get_resource_at(offset)

            if result != GetResourceAtResult.DEFINITIVE:
                raise Exception("No definitive resource", result, hex(address))
            assert resource is not None

            resource_offset = offset - resource.range_start
            try:
                return resource.get_c_expression_length(resource_offset)
            except:
                print(
                    "Couldn't get C expression for length of resource at some offset",
                    resource,
                    resource_offset,
                )
                raise

        elif resolution == SegmentedAddressResolution.SYMBOL:
            assert isinstance(resolution_info, tuple)
            symbol, offset = resolution_info
            assert isinstance(symbol, Symbol)
            assert isinstance(offset, int)

            return symbol.get_c_expression_length(offset)

        else:
            raise NotImplementedError(
                "unhandled SegmentedAddressResolution", resolution
            )


#
# file
#


class GetResourceAtResult(enum.Enum):
    DEFINITIVE = enum.auto()
    PERHAPS = enum.auto()
    NONE_YET = enum.auto()


class File:
    """A file is a collection of resources

    It typically corresponds to a rom file (segment) but doesn't have to
    It doesn't even need to correspond to the entirety of one or more .c files,
    it can be only a fraction
    """

    def __init__(self, memory_context: MemoryContext, name: str, data: memoryview):
        self.memory_context = memory_context
        self.name = name
        self.data = data
        self.resources: list[Resource] = []
        self.is_resources_sorted = True

    def add_resource(self, resource: "Resource"):
        self.resources.append(resource)
        self.is_resources_sorted = False

    def extend_resources(self, resources: Sequence["Resource"]):
        self.resources.extend(resources)
        self.is_resources_sorted = False

    def sort_resources(self):
        self.resources.sort(key=lambda resource: resource.range_start)
        self.is_resources_sorted = True

    def get_resource_at(self, offset: int):
        assert offset < len(self.data)

        # TODO explain the logic here...

        last_resource_before_offset: Union[Resource, None] = None

        for resource in self.resources:

            if resource.range_end is None:
                if resource.range_start <= offset:
                    if (
                        last_resource_before_offset is None
                        or last_resource_before_offset.range_start
                        < resource.range_start
                    ):
                        last_resource_before_offset = resource

            else:
                if resource.range_end <= offset:
                    if (
                        last_resource_before_offset is None
                        or last_resource_before_offset.range_start
                        < resource.range_start
                    ):
                        last_resource_before_offset = resource

                if resource.range_start <= offset < resource.range_end:
                    return GetResourceAtResult.DEFINITIVE, resource

        if (
            last_resource_before_offset is not None
            and last_resource_before_offset.range_end is None
        ):
            return GetResourceAtResult.PERHAPS, last_resource_before_offset
        else:
            return GetResourceAtResult.NONE_YET, None

    def get_overlapping_resources(self):
        assert self.is_resources_sorted

        overlaps: list[tuple[Resource, Resource]] = []

        for i in range(1, len(self.resources)):
            resource_a = self.resources[i - 1]

            # TODO: idk yet how to handle this
            assert resource_a.range_end is not None

            for j in range(i, len(self.resources)):
                resource_b = self.resources[j]

                # TODO: idk yet how to handle this
                assert resource_b.range_end is not None

                if resource_a.range_end <= resource_b.range_start:
                    break
                else:
                    overlaps.append((resource_a, resource_b))

        return overlaps

    def check_overlapping_resources(self):
        overlaps = self.get_overlapping_resources()
        if overlaps:
            print(self.str_report())
            raise Exception("resources overlap", overlaps)

    def parse_resources_data(self):

        # Set this to True just to enter the loop
        keep_looping = True

        while keep_looping:
            any_data_parsed = False

            # Parsing resources may add more, copy the list
            # to avoid concurrent modification while iterating
            resources_copy = self.resources.copy()

            for resource in resources_copy:
                if resource.is_data_parsed:
                    pass
                else:
                    try:
                        resource.try_parse_data()
                    except:
                        print("Error while attempting to parse data", resource)
                        raise
                    any_data_parsed = any_data_parsed or resource.is_data_parsed

                    if resource.is_data_parsed:
                        assert resource.range_end is not None

            any_resource_added = len(self.resources) != len(resources_copy)
            keep_looping = any_data_parsed or any_resource_added

        if __debug__:
            resources_data_not_parsed = [
                resource for resource in self.resources if not resource.is_data_parsed
            ]
            assert not resources_data_not_parsed, resources_data_not_parsed

    def add_unaccounted_resources(self):
        assert self.is_resources_sorted

        unaccounted_resources: list[Resource] = []

        def add_unaccounted(range_start, range_end):
            unaccounted_resource = BinaryBlobResource(
                self,
                range_start,
                range_end,
                f"{self.name}_unaccounted_{range_start:06X}",
            )
            unaccounted_resources.append(unaccounted_resource)

        if self.resources:
            # Add unaccounted if needed at the start of the file
            resource_first = self.resources[0]
            if resource_first.range_start > 0:
                add_unaccounted(
                    0,
                    resource_first.range_start,
                )

            # Add unaccounted if needed at the end of the file
            resource_last = self.resources[-1]
            if resource_last.range_end < len(self.data):
                add_unaccounted(
                    resource_last.range_end,
                    len(self.data),
                )
        else:
            # Add unaccounted for the whole file
            add_unaccounted(0, len(self.data))

        for i in range(1, len(self.resources)):
            resource_a = self.resources[i - 1]
            resource_b = self.resources[i]
            assert resource_a.range_end <= resource_b.range_start

            # Add unaccounted if needed between two successive resources
            if resource_a.range_end < resource_b.range_start:
                add_unaccounted(
                    resource_a.range_end,
                    resource_b.range_start,
                )

        self.extend_resources(unaccounted_resources)

    def set_resources_paths(self, extracted_path, build_path):
        for resource in self.resources:
            resource.set_paths(extracted_path, build_path)

    def write_resources_extracted(self):
        for resource in self.resources:
            assert resource.is_data_parsed, resource
            try:
                resource.write_extracted()
            except:
                print("Couldn't write extracted resource", resource)
                raise

    def write_source(self, source_path: Path):
        file_name = self.name

        with (source_path / f"{file_name}.c").open("w") as c:
            with (source_path / f"{file_name}.h").open("w") as h:

                headers_includes = (
                    '#include "ultra64.h"\n',
                    '#include "z64.h"\n',
                    '#include "macros.h"\n',
                )

                c.writelines(headers_includes)
                c.write(f'#include "{file_name}.h"\n')
                c.write("\n")

                INCLUDE_GUARD = file_name.upper() + "_H"

                h.writelines(
                    (
                        f"#ifndef {INCLUDE_GUARD}\n",
                        f"#define {INCLUDE_GUARD}\n",
                        "\n",
                    )
                )
                h.writelines(headers_includes)
                h.write("\n")

                for resource in self.resources:

                    resource.write_c_definition(c)
                    c.write("\n")

                    resource.write_c_declaration(h)

                h.writelines(
                    (
                        "\n",
                        "#endif\n",
                    )
                )

    def str_report(self):
        return "\n".join(
            f"0x{resource.range_start:06X}-0x{resource.range_end:06X} {resource.name}"
            for resource in self.resources
        )

    @staticmethod
    def from_xml(memory_context: MemoryContext, file_elem: ElementTree.Element):

        # 0) load the file data bytes

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

        # 1) read resources as described from the xml

        prev_resource = None

        for resource_elem in file_elem:

            if prev_resource is not None:
                default_offset = prev_resource.range_end
            else:
                default_offset = None

            resource = get_resource_from_xml(file, resource_elem, default_offset)

            file.add_resource(resource)

            prev_resource = resource

        print(file_name, file.resources)

        file.sort_resources()
        file.check_overlapping_resources()

        # TODO step 1) should be done on several files if
        # there are several in the context, to have the
        # memory_context ready before going to step 2
        # -> this means this function should be split by step
        #     (or the steps moved at the memorycontext level but hmm)

        # 2) parse: iteratively discover and parse data
        # (discover = add resources, parse = make friendlier than binary)

        file.parse_resources_data()

        # FIXME : bad code, shouldn't be here

        # also actually this won't play well with manually defined vtx arrays
        # probably can't merge the vbuf refs so quick

        for (
            resource_type,
            resource_buffer_markers,
        ) in memory_context.resource_buffer_markers_by_resource_type.items():
            print(resource_type, resource_buffer_markers)
            for rbm in resource_buffer_markers:
                memory_context.report_resource_at_segmented(
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

        file.add_unaccounted_resources()

        file.parse_resources_data()  # FIXME this is to set is_data_parsed=True on binary blob unaccounteds, handle better

        file.sort_resources()
        assert not file.get_overlapping_resources()

        # done loading this file

        pprint(file.resources)

        return file


#
# resources
#


class Resource(abc.ABC):
    """A resource is a blob of data inside a file.

    (at least for now,) one resource = one symbol

    Examples:
    - a struct-defined piece of data, such as a SkeletonHeader
    - an array of data, such as a display list Gfx[], or a texture u64[]
    """

    def __init_subclass__(cls, /, can_size_be_unknown=False, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.can_size_be_unknown = can_size_be_unknown

    def __init__(
        self,
        file: File,
        range_start: int,
        range_end: Optional[int],
        name: str,
    ):
        assert 0 <= range_start < len(file.data)
        if range_end is None:
            assert self.can_size_be_unknown
        else:
            assert range_start < range_end <= len(file.data)

        self.file = file

        self.range_start = range_start
        """Offset in the file data this resource starts at (inclusive)

        Example:
        range_start = 1 and range_end = 3
        means the resource is two bytes, the second and third bytes in the file
        """

        self.range_end = range_end
        """Offset in the file data this resource end at (exclusive)

        May be None if the resource size isn't known yet
        (only if can_size_be_unknown is True, see __init_subclass__)
        Must be set at the latest before is_data_parsed is set to True

        See range_start
        """

        self.name = name
        """Name of this resource, for logging/reporting.

        This member is NOT to be used as a C identifier, symbol name or file name.

        See also:
        - symbol_name
        - get_filename_stem
        """

        self.symbol_name = name
        """Name of the symbol to use to reference this resource"""

        self.is_data_parsed = False
        """See try_parse_data"""

    @abc.abstractmethod
    def try_parse_data(self):
        """Parse this resource's data bytes

        This can typically result in finding more resources,
        for example from pointer types.

        If data was successfully parsed, set `self.is_data_parsed` to `True`

        Otherwise it is assumed other resources need to parse their data
        before this one can be, and this will be called again later.

        Note this can both add found resources to the file,
        and wait before further parsing its own data (by not setting `is_data_parsed` to True).
        """
        ...

    @abc.abstractmethod
    def get_c_reference(self, resource_offset: int):
        """Get a C expression for referencing data in this resource (as a pointer)

        The offset `resource_offset` is relative to the resource:
        0 means the start of the resource data,
        and NOT the start of the file the resource is in.

        Should raise `ValueError` if the `resource_offset` isn't meaningful.

        Examples:
        - `StructData data`, `get_c_reference(0)` -> `&data`
        - `u8 array[]`, `get_c_reference(0)` -> `&array[0]`
        - `u8 array[]`, `get_c_reference(6)` -> `&array[6]`
        - `u16 array[]`, `get_c_reference(6)` -> `&array[3]`
        - `u16 array[]`, `get_c_reference(1)` -> raises `ValueError`
        - `u64 texture[]`, `get_c_reference(0)` -> `texture`
        """
        ...

    def get_c_expression_length(self, resource_offset: int):
        """Get a C expression for referencing the length of data in this resource

        The offset `resource_offset` is relative to the resource, as in get_c_reference.

        Should raise `ValueError` if the `resource_offset` isn't meaningful.

        Examples:
        - `StructData data`, `get_c_expression_length(0)` -> raises `ValueError`
        - `u8 array[]`, `get_c_reference(0)` -> `ARRAY_COUNT(array)`
        - `u8 array[]`, `get_c_reference(1)` -> raises `ValueError`
        """
        # Override in children classes if needed
        raise ValueError(
            "This resource has no data with a length that can be referenced"
        )

    needs_build = False
    """Whether this resource needs processing by the build system.

    If False, it is extracted directly as .inc.c and included as is.

    See set_paths
    """

    extracted_path_suffix = ".inc.c"
    """The file extension for constructing the path to extract this resource to.

    See set_paths
    """

    def get_filename_stem(self):
        """Stem (name without suffix) for the file to write this resource to

        See set_paths
        """
        return self.name

    # These two are set by calling set_paths
    extract_to_path: Path
    inc_c_path: Path

    def set_paths(self, extracted_path: Path, build_path: Path):
        """Compute and set `self.extract_to_path` and `self.inc_c_path`

        Examples:
        with extracted_path: `assets/_extracted/.../`
        and build_path: `build/`

        Binary: extracted_path_suffix = ".bin"
        with get_filename_stem() = "blob"
            extract_to_path: `assets/_extracted/.../blob.bin`
            inc_c_path: `build/assets/_extracted/.../blob.inc.c`

        C: extracted_path_suffix = ".inc.c"
        with get_filename_stem() = "data"
            extract_to_path: `assets/_extracted/.../data.inc.c`
            inc_c_path: `assets/_extracted/.../data.inc.c`

        rgba16 image: extracted_path_suffix = ".png"
        with get_filename_stem() = "img.rgba16"
            extract_to_path: `assets/_extracted/.../img.rgba16.png`
            inc_c_path: `build/assets/_extracted/.../img.rgba16.inc.c`
        """

        filename_stem = self.get_filename_stem()

        extract_to_path = extracted_path / (filename_stem + self.extracted_path_suffix)

        if self.needs_build:
            inc_c_path = build_path / extracted_path / (filename_stem + ".inc.c")
        else:
            assert self.extracted_path_suffix == ".inc.c"
            inc_c_path = extract_to_path

        self.extract_to_path = extract_to_path
        self.inc_c_path = inc_c_path

    @abc.abstractmethod
    def write_extracted(self) -> None:
        """Write the extracted resource data to self.extract_to_path"""
        ...

    @abc.abstractmethod
    def get_c_declaration_base(self):
        """Get the base source for declaring this resource's symbol in C.

        For example:
        - "u8 blob[]", `return f"u8 {self.symbol_name}[]"`
        - "DataStruct data", `return f"DataStruct {self.symbol_name}"`
        """
        ...

    def write_c_definition(self, c: io.TextIOBase) -> None:

        c.write(self.get_c_declaration_base())
        c.write(" =\n")

        if WRITE_HINTS:
            if self.needs_build:
                if False:
                    import os.path

                    rel_path = os.path.relpath(
                        self.extract_to_path, "assets/objects/object_am/"
                    )
                    c.write(f"// file://./{rel_path}\n")
            else:
                if False:
                    c.write("// needs_build=False\n")

        c.write(f'#include "{self.inc_c_path}"\n')
        c.write(";\n")

    def write_c_declaration(self, h: io.TextIOBase) -> None:

        h.write("extern ")
        h.write(self.get_c_declaration_base())
        h.write(";\n")


class BinaryBlobResource(Resource):
    needs_build = True
    extracted_path_suffix = ".bin"

    def try_parse_data(self):
        # Nothing specific to do
        self.is_data_parsed = True

    def get_c_reference(self, resource_offset):
        return f"&{self.symbol_name}[{resource_offset}]"

    def get_filename_stem(self):
        return super().get_filename_stem() + ".u8"

    def write_extracted(self):
        data = self.file.data[self.range_start : self.range_end]
        assert len(data) == self.range_end - self.range_start
        self.extract_to_path.write_bytes(data)

    def get_c_declaration_base(self):
        return f"u8 {self.symbol_name}[]"

    def get_c_expression_length(self, resource_offset: int):
        raise Exception(
            "A binary blob resource could support returning a C expression for its length, "
            "but it would be error-prone due to the 'anything goes' nature of binary blobs. "
            "Make a dedicated resource instead"
        )

    @staticmethod
    def get_fixed_size_resource_handler(size) -> "ResourceHandler":
        def resource_handler(
            file: File,
            resource_elem: ElementTree.Element,
            offset: int,
        ):
            return BinaryBlobResource(
                file,
                offset,
                offset + size,
                resource_elem.attrib["Name"],
            )

        return resource_handler


from repr_c_struct import CData, CData_Value, CData_Struct, CData_Array


class CDataExt(CData, abc.ABC):

    report_f = None
    write_f = None

    # TODO not sure what to name this, it doesn't have to be used for pointer reporting,
    # more generic "callback" may be better idk yet
    def set_report(self, report_f: Callable[["CDataResource", Any], None]):
        self.report_f = report_f
        return self

    def set_write(self, write_f: Callable[["CDataResource", Any, io.TextIOBase], bool]):
        self.write_f = write_f
        return self

    def freeze(self):
        self.set_report = None
        self.set_write = None
        return self

    @abc.abstractmethod
    def write_default(
        self, resource: "CDataResource", v: Any, f: io.TextIOBase
    ) -> bool:
        ...

    def report(self, resource: "CDataResource", v: Any):
        if self.report_f:
            self.report_f(resource, v)

    def write(self, resource: "CDataResource", v: Any, f: io.TextIOBase):
        """
        Returns True if something has been written
        (typically, False will be returned if this data is struct padding)
        """
        if self.write_f:
            return self.write_f(resource, v, f)
        else:
            return self.write_default(resource, v, f)


class CDataExt_Value(CData_Value, CDataExt):
    is_padding = False

    def padding(self):
        self.is_padding = True
        return self

    def freeze(self):
        self.padding = None
        return super().freeze()

    def report(self, resource: "CDataResource", v: Any):
        super().report(resource, v)
        if self.is_padding:
            if v != 0:
                raise Exception("non-0 padding")

    def write_default(self, resource: "CDataResource", v: Any, f: io.TextIOBase):
        if not self.is_padding:
            f.write(str(v))
            return True
        else:
            return False


CDataExt_Value.s8 = CDataExt_Value("b").freeze()
CDataExt_Value.u8 = CDataExt_Value("B").freeze()
CDataExt_Value.s16 = CDataExt_Value("h").freeze()
CDataExt_Value.u16 = CDataExt_Value("H").freeze()
CDataExt_Value.s32 = CDataExt_Value("i").freeze()
CDataExt_Value.u32 = CDataExt_Value("I").freeze()
CDataExt_Value.f32 = CDataExt_Value("f").freeze()
CDataExt_Value.f64 = CDataExt_Value("d").freeze()
CDataExt_Value.pointer = CDataExt_Value("I").freeze()

CDataExt_Value.pad8 = CDataExt_Value("b").padding().freeze()
CDataExt_Value.pad16 = CDataExt_Value("h").padding().freeze()
CDataExt_Value.pad32 = CDataExt_Value("i").padding().freeze()


class CDataExt_Array(CData_Array, CDataExt):
    def __init__(self, element_cdata_ext: CDataExt, length: int):
        super().__init__(element_cdata_ext, length)
        self.element_cdata_ext = element_cdata_ext

    def report(self, resource: "CDataResource", v: Any):
        assert isinstance(v, list)
        super().report(resource, v)
        for elem in v:
            self.element_cdata_ext.report(resource, elem)

    def write_default(self, resource: "CDataResource", v: Any, f: io.TextIOBase):
        assert isinstance(v, list)
        f.write("{\n")
        for i, elem in enumerate(v):
            ret = self.element_cdata_ext.write(resource, elem, f)
            assert ret
            f.write(f", // {i}\n")
        f.write("}")
        return True


class CDataExt_Struct(CData_Struct, CDataExt):
    def __init__(self, members: Sequence[tuple[str, CDataExt]]):
        super().__init__(members)
        self.members_ext = members

    def report(self, resource: "CDataResource", v: Any):
        assert isinstance(v, dict)
        super().report(resource, v)
        for member_name, member_cdata_ext in self.members_ext:
            member_cdata_ext.report(resource, v[member_name])

    def write_default(self, resource: "CDataResource", v: Any, f: io.TextIOBase):
        assert isinstance(v, dict)
        f.write("{\n")
        for member_name, member_cdata_ext in self.members_ext:
            if member_cdata_ext.write(resource, v[member_name], f):
                f.write(f", // {member_name}\n")
        f.write("}")
        return True


class CDataResource(Resource):

    # Set by child classes
    cdata_ext: CDataExt

    # Resource implementation

    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, range_start + self.cdata_ext.size, name)

    def try_parse_data(self):
        self.cdata_unpacked = self.cdata_ext.unpack_from(
            self.file.data, self.range_start
        )

        self.cdata_ext.report(self, self.cdata_unpacked)

        self.is_data_parsed = True

    def write_extracted(self):
        with self.extract_to_path.open("w") as f:
            self.cdata_ext.write(self, self.cdata_unpacked, f)
            f.write("\n")


import skeleton_resources
import animation_resources

#
# resource handlers
#


def resource_handler(
    file: File,
    resource_elem: ElementTree.Element,
    offset: int,
) -> Resource:
    ...


del resource_handler
ResourceHandler = Callable[[File, ElementTree.Element, int], Resource]


def skeleton_resource_handler(
    file: File,
    resource_elem: ElementTree.Element,
    offset: int,
):
    if resource_elem.attrib["Type"] != "Normal":
        raise NotImplementedError(
            "unimplemented Skeleton Type",
            resource_elem.attrib["Type"],
        )
    return skeleton_resources.SkeletonNormalResource(
        file,
        offset,
        resource_elem.attrib["Name"],
    )


def animation_resource_handler(
    file: File,
    resource_elem: ElementTree.Element,
    offset: int,
):
    return animation_resources.AnimationResource(
        file,
        offset,
        resource_elem.attrib["Name"],
    )


RESOURCE_HANDLERS: dict[str, ResourceHandler] = {
    "Skeleton": skeleton_resource_handler,
    "Animation": animation_resource_handler,
    "Collision": BinaryBlobResource.get_fixed_size_resource_handler(0x2C),
}


def get_resource_from_xml(
    file: File,
    resource_elem: ElementTree.Element,
    default_offset=None,
) -> Resource:
    resource_handler = RESOURCE_HANDLERS.get(resource_elem.tag)

    if resource_handler is None:
        raise Exception("Unknown resource tag", resource_elem.tag)

    offset = resource_elem.attrib.get("Offset")
    if offset is None:
        if default_offset is None:
            raise Exception("no Offset nor default_offset")
        offset = default_offset
    else:
        offset = int(offset, 16)

    resource = resource_handler(file, resource_elem, offset)

    return resource


#
# main
#

# "options"
RM_SOURCE = True
WRITE_SOURCE = True
RM_EXTRACT = True
WRITE_EXTRACT = True
from conf import WRITE_HINTS


BASEROM_PATH = Path("baserom")
BUILD_PATH = Path("build")


def main():

    xml_path = Path("assets/xml/objects/object_am.xml")
    source_path = Path("assets/objects/object_am/")
    extract_path = Path("assets/_extracted/objects/object_am/")

    memory_context = MemoryContext()  # TODO

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

    with xml_path.open() as f:
        xml = ElementTree.parse(f)

    root_elem = xml.getroot()

    assert root_elem.tag == "Root", root_elem.tag

    for file_elem in root_elem:
        assert file_elem.tag == "File", file_elem.tag

        file = File.from_xml(memory_context, file_elem)

        extract_path.mkdir(parents=True, exist_ok=True)
        file.set_resources_paths(extract_path, BUILD_PATH)

        print(file.str_report())

        if WRITE_EXTRACT:
            file.write_resources_extracted()

        if WRITE_SOURCE:
            source_path.mkdir(parents=True, exist_ok=True)

            file.write_source(source_path)


if __name__ == "__main__":
    profile = True
    if profile:
        import cProfile

        cProfile.run("main()", "cprof_assets421.txt")
    else:
        main()
