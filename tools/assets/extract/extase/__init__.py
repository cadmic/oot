from pathlib import Path
import abc
from dataclasses import dataclass
import enum
import reprlib

import io
from typing import Sequence, Optional, Callable, Union


#
# memory context
#


# TODO rename to just AddressResolution
class SegmentedAddressResolution(enum.Enum):
    SYMBOL = enum.auto()
    FILE = enum.auto()


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


class NoSegmentBaseError(Exception):
    """Indicates a segmented address could not be resolved because a base / data wasn't set for the corresponding segment."""

    pass


class NoPhysicalMappingError(Exception):
    """Indicates a physical address could not be resolved because nothing was found for the address."""

    pass


class NoVRAMMappingError(Exception):
    """Indicates a vram address could not be resolved because nothing was found for the address."""

    pass


class MemoryContext:
    """
    handles segmented addresses, pointers, external symbols (eg gMtxClear)

    maps offsets to data
    """

    def __init__(self, *, I_D_OMEGALUL=False):
        self.segments: dict[int, Optional["File"]] = {i: None for i in range(1, 16)}
        self.symbols: Sequence[Symbol] = (
            # TODO config for this
            Symbol("gMtxClear", 0x12DB80, 0x12DB80 + 0x40),
        )
        self.vram_symbols: list[Symbol] = []  # TODO
        self.files_by_physical: dict[
            int, File
        ] = dict()  # range_start (physical) : file
        self.files_by_vram: dict[int, File] = dict()  # range_start (vram) : file
        self.resource_buffer_markers_by_resource_type: dict[
            type[Resource], list[ResourceBufferMarker]
        ] = dict()

        self.I_D_OMEGALUL = I_D_OMEGALUL  # accomodate for IDO stuff (TODO rework)

    def save_segment_map(self):
        saved_segment_map = self.segments.copy()
        return saved_segment_map

    def restore_segment_map(self, saved_segment_map):
        self.segments = saved_segment_map

    def set_segment(self, segment_num: int, target: "File"):
        if not (1 <= segment_num < 16):
            raise ValueError(
                "Segment number must be between 1 and 15 (inclusive)", segment_num
            )

        if self.segments[segment_num] is not None:
            raise Exception("Segment is already set", segment_num)

        self.segments[segment_num] = target

    def set_vram(self, address: int, target: "File"):
        # TODO this function is copypasted from set_physical, find a way to refactor
        # note I want to keep vram/physical mapping separate as finding an umbrella term is uneasy
        # vram refers to the linker's knowledge of the rom,
        # and physical to the addresses at run time
        try:
            resolved_result = self.resolve_vram(address)
        except NoVRAMMappingError:
            # The address isn't taken, we can use it.
            self.files_by_vram[address] = target
        else:
            # Successfuly resolved the address.
            # The address is taken, we cannot use it.
            raise ValueError(
                "Address is already mapped to something", hex(address), resolved_result
            )

    def resolve_vram(self, address: int):
        # TODO this function is copypasted from resolve_physical, find a way to refactor (but, see set_vram)
        for symbol in self.vram_symbols:
            if symbol.range_start <= address < symbol.range_end:
                offset = address - symbol.range_start
                return SegmentedAddressResolution.SYMBOL, (symbol, offset)

        if __debug__:
            for range_start_vram_a, file_a in self.files_by_vram.items():
                range_end_vram_a = range_start_vram_a + len(file_a.data)
                assert range_start_vram_a < range_end_vram_a
                for range_start_vram_b, file_b in self.files_by_vram.items():
                    range_end_vram_b = range_start_vram_b + len(file_b.data)
                    assert range_start_vram_b < range_end_vram_b
                    if file_a != file_b:
                        if range_end_vram_a <= range_start_vram_b:
                            assert (
                                range_start_vram_a
                                < range_end_vram_a
                                <= range_start_vram_b
                                < range_end_vram_b
                            )
                        else:
                            assert (
                                range_start_vram_b
                                < range_end_vram_b
                                <= range_start_vram_a
                                < range_end_vram_a
                            )

        for range_start_vram, file in self.files_by_vram.items():
            range_end_vram = range_start_vram + len(file.data)
            if range_start_vram <= address < range_end_vram:
                offset = address - range_start_vram
                assert 0 <= offset < len(file.data)
                return SegmentedAddressResolution.FILE, (file, offset)

        raise NoVRAMMappingError("vram address doesn't map to anything", hex(address))

    def set_virtual(self, address: int, target: "File"):
        if (address & 0xF000_0000) != 0x8000_0000:
            raise ValueError(
                "address high bits are not 0x8000_0000 (KSEG0, typically for ram addresses),"
                " something is probably wrong.",
                hex(address),
            )

        return self.set_physical(address & 0x0FFF_FFFF, target)

    def set_physical(self, address: int, target: "File"):
        assert address < 8 * 1024 * 1024, (
            "addressing physical memory beyond 8MB of ram: this is probably wrong",
            hex(address),
        )
        try:
            resolved_result = self.resolve_physical(address)
        except NoPhysicalMappingError:
            # The address isn't taken, we can use it.
            self.files_by_physical[address] = target
        else:
            # Successfuly resolved the address.
            # The address is taken, we cannot use it.
            raise ValueError(
                "Address is already mapped to something", hex(address), resolved_result
            )

    def resolve_physical(self, address: int):
        assert address < 8 * 1024 * 1024, (
            "addressing physical memory beyond 8MB of ram: this is probably wrong",
            hex(address),
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
                assert 0 <= offset < len(file.data)
                return SegmentedAddressResolution.FILE, (file, offset)

        raise NoPhysicalMappingError(
            "physical address doesn't map to anything", hex(address)
        )

    def resolve_segmented(self, address: int):
        address_high_bits = address & 0xF000_0000
        # global TODO that is relevant in a lot of places: clean up asserts (ie replace with errors)
        assert address_high_bits in {0, 0x8000_0000}, (
            "Address high bits are not 0 (typically for segmented addresses)"
            " nor 0x8000_0000 (KSEG0, typically for ram addresses),"
            " something is probably wrong.",
            hex(address),
        )
        segment_num = (address & 0x0F00_0000) >> 24
        offset = address & 0x00FF_FFFF

        if segment_num == 0:
            """
            # TODO idk. also there's nothing checking for overlap between physical and vram
            # so this implementation allows the vram mapping to overshadow the physical ones
            # Start with trying vram, because physical checks 8 MB bounds so it fails on pure vram addresses
            try:
                return self.resolve_vram(offset)
            except NoVRAMMappingError:
                return self.resolve_physical(offset)
            """
            # the above doesn't work for figuring out stuff since it hides if a vram check non-legitimately / unintendedly fails
            # TODO idk how to pick physical/vram
            # for now assume <8MB=physical
            if offset < 8 * 1024 * 1024:
                return self.resolve_physical(offset)
            else:
                # note: using the address here, ie offset with the "high bits" (eg 0x8000_0000)
                # indeed vram is mapped from the linker's pov which includes the virtual memory segment (eg kseg0)
                return self.resolve_vram(address)
        else:
            file = self.segments.get(segment_num)
            if file is None:
                raise NoSegmentBaseError(
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
                # TODO figure out what to do with perhaps resources
                # for now just add resources, but this may dupe stuff if the resource is supposed to be the same
                # (eg vertex arrays, currently handled with the buffer reporting mark_resource_buffer_at_segmented )
                print(
                    "!!! GetResourceAtResult.PERHAPS report_resource_at_segmented , may duplicate stuff idk !!!",
                    hex(address),
                    hex(offset),
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

                if result == GetResourceAtResult.PERHAPS:
                    # TODO (see above)
                    print(
                        "     >>> ",
                        result,
                        "followup",
                        "added:",
                        new_resource.name,
                        new_resource.__class__,
                        new_resource,
                    )

                return new_resource, offset

        elif resolution == SegmentedAddressResolution.SYMBOL:
            assert isinstance(resolution_info, tuple)
            symbol, offset = resolution_info
            assert isinstance(symbol, Symbol)
            assert isinstance(offset, int)

            # TODO
            print(
                "!!!",
                resolution,
                symbol,
                hex(offset),
                "resource found at symbol, ignoring",
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
            try:
                return resource.get_c_reference(resource_offset)
            except:
                print(
                    f"Couldn't call resource.get_c_reference(0x{resource_offset:X}) on",
                    resource,
                )
                raise

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
        self.referenced_files: set[File] = set()

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

        # Resources may use a defined range with both start and end defined,
        # or a range that only has its start defined.

        # While looking for a resource with a defined range the request offset
        # belongs to, also keep track of the last resource that starts at or before
        # offset (note: that resource may or may not have an end range defined).
        last_resource_before_offset: Union[Resource, None] = None

        for resource in self.resources:

            if resource.range_start <= offset:
                if (
                    last_resource_before_offset is None
                    or last_resource_before_offset.range_start < resource.range_start
                ):
                    last_resource_before_offset = resource

            if resource.range_end is not None:
                # If the requested offset falls within a defined range, return that
                # resource with GetResourceAtResult.DEFINITIVE .
                if resource.range_start <= offset < resource.range_end:
                    return GetResourceAtResult.DEFINITIVE, resource

        # If the loop exits normally, without returning a defined range resource,
        # check if the last resource starting at or before the requested offset
        # (if any) has an undefined range.
        if (
            last_resource_before_offset is not None
            and last_resource_before_offset.range_end is None
        ):
            if last_resource_before_offset.range_start == offset:
                # Resources are always more than 0 bytes in size, so if the resource
                # starts exactly at the requested offset, then it is guaranteed to
                # cover (at least) that offset.
                return GetResourceAtResult.DEFINITIVE, last_resource_before_offset
            else:
                # Return it with GetResourceAtResult.PERHAPS , as it may extend up to
                # and beyond the requested offset (or not).
                return GetResourceAtResult.PERHAPS, last_resource_before_offset
        else:
            # No (potential) resource at that offset (currently).
            return GetResourceAtResult.NONE_YET, None

    def get_overlapping_resources(self):
        if not self.is_resources_sorted:
            raise Exception("sort resources first")

        overlaps: list[tuple[Resource, Resource]] = []

        for i in range(1, len(self.resources)):
            resource_a = self.resources[i - 1]

            if resource_a.range_end is not None:
                for j in range(i, len(self.resources)):
                    resource_b = self.resources[j]

                    # This should hold true, as resources are sorted
                    assert resource_a.range_start <= resource_b.range_start

                    if resource_a.range_end > resource_b.range_start:
                        overlaps.append((resource_a, resource_b))
                    else:
                        break
            else:
                for j in range(i, len(self.resources)):
                    resource_b = self.resources[j]

                    assert resource_a.range_start <= resource_b.range_start

                    if resource_a.range_start == resource_b.range_start:
                        overlaps.append((resource_a, resource_b))
                    else:
                        break

        return overlaps

    def check_overlapping_resources(self):
        try:
            overlaps = self.get_overlapping_resources()
            if overlaps:
                raise Exception("resources overlap", overlaps)
        except:
            print(self.str_report())
            raise

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

        # TODO replace having Resource.try_parse_data set is_data_parsed to True/False,
        # by them raising a DataNotParsed exception instead.
        # Would also allow to provide a reason why data was not parsed
        if __debug__:
            resources_data_not_parsed = [
                resource for resource in self.resources if not resource.is_data_parsed
            ]
            assert not resources_data_not_parsed, (
                len(resources_data_not_parsed),
                [(r.name, r.__class__) for r in resources_data_not_parsed],
                resources_data_not_parsed,
            )

    def add_unaccounted_resources(self):
        assert self.is_resources_sorted

        unaccounted_resources: list[Resource] = []

        def add_unaccounted(range_start, range_end):
            if self.memory_context.I_D_OMEGALUL:
                pad_bytes = (4 - range_start % 4) % 4
                if pad_bytes != 0:
                    pad_range_end = range_start + pad_bytes
                    assert pad_range_end <= range_end
                    pad_data = self.data[range_start:pad_range_end]
                    if set(pad_data) != {0}:
                        raise Exception(
                            "Expected pad bytes to be 0",
                            hex(range_start),
                            hex(pad_range_end),
                            set(pad_data),
                            bytes(pad_data),
                        )
                    pad_resource = ZeroPaddingResource(
                        self,
                        range_start,
                        pad_range_end,
                        f"{self.name}_zero_padding_{range_start:06X}",
                        include_in_source=False,
                    )
                    unaccounted_resources.append(pad_resource)
                    range_start += pad_bytes
                    if range_start == pad_range_end:
                        return
            assert range_start < range_end
            unaccounted_data = self.data[range_start:range_end]
            if set(unaccounted_data) == {0}:
                unaccounted_resource = ZeroPaddingResource(
                    self,
                    range_start,
                    range_end,
                    f"{self.name}_zeros_{range_start:06X}",
                )
            else:
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

    # These two are set by calling set_source_path
    source_c_path: Path
    source_h_path: Path

    def set_source_path(self, source_path: Path):
        file_name = self.name

        # May catch random problems but not a hard requirement otherwise
        assert file_name and all(
            (c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789")
            for c in file_name
        ), file_name

        self.source_file_name = file_name
        self.source_c_path = source_path / f"{file_name}.c"
        self.source_h_path = source_path / f"{file_name}.h"

    def write_source(self):
        assert hasattr(
            self, "source_c_path"
        ), "set_source_path must be called before write_source"
        assert hasattr(self, "source_h_path")
        with self.source_c_path.open("w") as c:
            with self.source_h_path.open("w") as h:

                headers_includes = (
                    '#include "ultra64.h"\n',
                    '#include "z64.h"\n',
                    '#include "macros.h"\n',
                )

                # Paths to files to be included
                file_include_paths_complete: list[Path] = []
                file_include_paths_complete.append(self.source_h_path)
                for referenced_file in self.referenced_files:
                    assert isinstance(referenced_file, File), referenced_file
                    repr(referenced_file)
                    assert hasattr(referenced_file, "source_c_path"), (
                        "set_source_path must be called on all files before any write_source call",
                        referenced_file,
                    )
                    assert hasattr(referenced_file, "source_h_path")
                    file_include_paths_complete.append(referenced_file.source_h_path)

                # Same as file_include_paths_complete,
                # but paths that can be are made relative to the source C.
                file_include_paths: list[Path] = []
                for path_complete in file_include_paths_complete:
                    try:
                        path = path_complete.relative_to(self.source_c_path.parent)
                    except ValueError:
                        # Included path is not relative to this file's source C folder.
                        # Just use the complete path.
                        path = path_complete
                    file_include_paths.append(path)

                c.writelines(headers_includes)
                c.write("\n")
                for file_include_path in file_include_paths:
                    c.write(f'#include "{file_include_path}"\n')
                c.write("\n")

                INCLUDE_GUARD = self.source_file_name.upper() + "_H"

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

                    if resource.write_c_definition(c):
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
            f"0x{resource.range_start:06X}-"
            + (
                f"0x{resource.range_end:06X}"
                if resource.range_end is not None
                else "..."
            )
            + f" {resource.name}"
            for resource in self.resources
        )

    @reprlib.recursive_repr()
    def __repr__(self):
        return (
            self.__class__.__qualname__
            + f"({self.name!r}, {self.data!r}, {self.resources!r})"
        )


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
    def get_c_reference(self, resource_offset: int) -> str:
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
            "This resource has no data with a length that can be referenced",
            self.__class__,
            self,
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
    def get_c_declaration_base(self) -> str:
        """Get the base source for declaring this resource's symbol in C.

        For example:
        - "u8 blob[]", `return f"u8 {self.symbol_name}[]"`
        - "DataStruct data", `return f"DataStruct {self.symbol_name}"`
        """
        ...

    def write_c_definition(self, c: io.TextIOBase) -> bool:
        """
        Returns True if something was written
        """

        if hasattr(self, "HACK_IS_STATIC_ON"):
            c.write("static ")
        c.write(self.get_c_declaration_base())
        c.write(" =\n")

        c.write(f'#include "{self.inc_c_path}"\n')
        c.write(";\n")

        return True

    def write_c_declaration(self, h: io.TextIOBase) -> None:

        if hasattr(self, "HACK_IS_STATIC_ON"):
            h.write("static ")
        else:
            h.write("extern ")
        h.write(self.get_c_declaration_base())
        h.write(";\n")

    @reprlib.recursive_repr()
    def __repr__(self):
        return (
            self.__class__.__qualname__
            + "("
            + ", ".join(
                (
                    repr(self.name),
                    (
                        f"0x{self.range_start:08X}-"
                        + (
                            f"0x{self.range_end:08X}"
                            if self.range_end is not None
                            else "..."
                        )
                    ),
                    f"file.name={self.file.name!r}",
                )
            )
            + ")"
        )


class ZeroPaddingResource(Resource):
    def __init__(
        self,
        file: File,
        range_start: int,
        range_end: int,
        name: str,
        *,
        include_in_source=True,
    ):
        assert set(file.data[range_start:range_end]) == {0}
        super().__init__(file, range_start, range_end, name)
        self.include_in_source = include_in_source

    def try_parse_data(self):
        # Nothing specific to do
        self.is_data_parsed = True

    def get_c_reference(self, resource_offset):
        raise ValueError("Referencing zero padding should not happen")

    def write_extracted(self):
        # No need to extract zeros
        pass

    def get_c_declaration_base(self):
        length_bytes = self.range_end - self.range_start
        assert length_bytes > 0
        return f"u8 {self.symbol_name}[{length_bytes}]"

    def write_c_definition(self, c: io.TextIOBase):
        if self.include_in_source:
            c.write(self.get_c_declaration_base())
            c.write(" = { 0 };\n")
            return True
        else:
            return False

    def write_c_declaration(self, h: io.TextIOBase):
        # No need to declare zeros
        pass


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
