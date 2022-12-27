from pathlib import Path

import io

from typing import Union, Optional, Callable

from ..extase import (
    SegmentedAddressResolution,
    GetResourceAtResult,
    NoSegmentBaseError,
    Resource,
    File,
)
from ..extase.cdata_resources import (
    CDataResource,
    CDataExt_Array,
    CDataExt_Struct,
    CDataExt_Value,
)


# FIXME ...
import sys

sys.path.insert(0, "/home/dragorn421/Documents/pygfxd/")
import pygfxd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....pygfxd import pygfxd


class VtxArrayResource(CDataResource):
    def write_elem(resource, v, f: io.TextIOBase, line_prefix):
        assert isinstance(v, dict)
        f.write(line_prefix)
        f.write(
            f"VTX({v['x']:6}, {v['y']:6}, {v['z']:6}, "
            f"{v['s']:#7X}, {v['t']:#7X}, "
            f"{v['crnx']:#04X}, {v['cgny']:#04X}, {v['cbnz']:#04X}, {v['a']:#04X})"
        )
        return True

    element_cdata_ext = CDataExt_Struct(
        (
            ("x", CDataExt_Value.s16),
            ("y", CDataExt_Value.s16),
            ("z", CDataExt_Value.s16),
            (
                "pad6",
                CDataExt_Value.pad16,
            ),  # Not technically padding but unused and expected to always be 0
            ("s", CDataExt_Value.s16),
            ("t", CDataExt_Value.s16),
            ("crnx", CDataExt_Value.u8),
            ("cgny", CDataExt_Value.u8),
            ("cbnz", CDataExt_Value.u8),
            ("a", CDataExt_Value.u8),
        )
    ).set_write(write_elem)

    def __init__(self, file: File, range_start: int, range_end: int, name: str):
        # TODO this is stupid (range_end -> num -> size -> range_end)
        num = (range_end - range_start) // self.element_cdata_ext.size
        self.cdata_ext = CDataExt_Array(self.element_cdata_ext, num)
        super().__init__(file, range_start, name)

    def get_c_declaration_base(self):
        return f"Vtx {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset % self.element_cdata_ext.size != 0:
            raise ValueError(
                "unaligned offset into vtx array",
                hex(resource_offset),
                self.element_cdata_ext.size,
            )
        index = resource_offset // self.element_cdata_ext.size
        return f"&{self.symbol_name}[{index}]"

from ...n64 import G_IM_FMT, G_IM_SIZ

sys.path.insert(0, "/home/dragorn421/Documents/n64texconv/")
import n64texconv

sys.path.insert(0, "/home/dragorn421/Documents/oot/tools/assets/png2raw/")
import raw2png

if TYPE_CHECKING:
    from png2raw import raw2png


def png_from_data(
    outpath, width, height, greyscale, alpha, bitdepth, image_data, palette
):
    # assert raw2png current limitations
    assert not greyscale
    assert alpha
    assert bitdepth == 8

    # unimplemented
    assert palette is None

    raw2png.write(outpath, width, height, bytearray(image_data))


n64texconv.png_from_data = png_from_data


def write_n64_image_to_png(
    path: Path, width: int, height: int, fmt: G_IM_FMT, siz: G_IM_SIZ, data: memoryview
):
    tex = n64texconv.Image.from_bin(data, width, height, fmt.i, siz.i, None)
    tex.to_png(path)


class TextureResource(Resource):
    needs_build = True
    extracted_path_suffix = ".png"

    def __init__(
        self,
        file: File,
        range_start: int,
        name: str,
        fmt: G_IM_FMT,
        siz: G_IM_SIZ,
        width: int,
        height: int,
    ):
        size_bits = siz.bpp * width * height
        assert size_bits % 8 == 0, size_bits
        size_bytes = size_bits // 8
        range_end = range_start + size_bytes

        super().__init__(file, range_start, range_end, name)

        self.fmt = fmt
        self.siz = siz
        self.width = width
        self.height = height

        if size_bytes % 8 == 0 and range_start % 8 == 0:
            self.alignment = 8
        elif size_bytes % 4 == 0 and range_start % 4 == 0:
            self.alignment = 4
        else:
            raise NotImplementedError(
                "unimplemented: unaligned texture size/offset",
                hex(size_bytes),
                hex(range_start),
            )

        alignment_bits = self.alignment * 8
        self.elem_type = f"u{alignment_bits}"
        assert self.elem_type in {"u64", "u32"}

        self.width_name = f"{self.symbol_name}_WIDTH"
        self.height_name = f"{self.symbol_name}_HEIGHT"

    def get_filename_stem(self):
        return (
            super().get_filename_stem()
            + f".{self.fmt.name.lower()}{self.siz.bpp}.{self.elem_type}"
        )

    def get_c_declaration_base(self):
        return f"{self.elem_type} {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError(self, hex(resource_offset))

    def try_parse_data(self):
        # Nothing to do
        self.is_data_parsed = True

    def write_extracted(self) -> None:
        data = self.file.data[self.range_start : self.range_end]
        assert len(data) == self.range_end - self.range_start
        if self.fmt == G_IM_FMT.CI:
            # TODO
            self.extract_to_path.with_suffix(".bin").write_bytes(data)
            return
        write_n64_image_to_png(
            self.extract_to_path, self.width, self.height, self.fmt, self.siz, data
        )

    def write_c_declaration(self, h: io.TextIOBase):
        h.writelines((f"#define {self.width_name} {self.width}\n"))
        h.writelines((f"#define {self.height_name} {self.height}\n"))
        super().write_c_declaration(h)


def gfxdis(
    *,
    input_buffer: Union[bytes, memoryview],
    output_callback: Optional[
        Callable[[bytes], None]  # deviates a bit from gfxd, no count arg/return
    ] = None,
    enable_caps: set[pygfxd.GfxdCap] = {
        pygfxd.GfxdCap.stop_on_end,
        pygfxd.GfxdCap.emit_dec_color,
    },
    target=pygfxd.gfxd_f3dex2,
    vtx_callback: Optional[Callable[[int, int], int]] = None,
    timg_callback: Optional[Callable[[int, int, int, int, int, int], int]] = None,
    macro_fn: Optional[Callable[[], int]] = None,
    arg_fn: Optional[Callable[[int], None]] = None,
):
    for cap in (
        pygfxd.GfxdCap.stop_on_invalid,
        pygfxd.GfxdCap.stop_on_end,
        pygfxd.GfxdCap.emit_dec_color,
        pygfxd.GfxdCap.emit_q_macro,
        pygfxd.GfxdCap.emit_ext_macro,
    ):
        if cap in enable_caps:
            pygfxd.gfxd_enable(cap)
        else:
            pygfxd.gfxd_disable(cap)

    pygfxd.gfxd_target(target)

    pygfxd.gfxd_input_buffer(bytes(input_buffer))

    exceptions = []

    # output_callback

    if output_callback:

        def output_callback_wrapper(buf, count):
            try:
                output_callback(buf)
            except:
                import sys

                e = sys.exc_info()[1]
                exceptions.append(e)
            return count

    else:

        def output_callback_wrapper(buf, count):
            return count

    pygfxd.gfxd_output_callback(output_callback_wrapper)

    # vtx_callback

    if vtx_callback:

        def vtx_callback_wrapper(vtx, num):
            try:
                ret = vtx_callback(vtx, num)
            except:
                import sys

                e = sys.exc_info()[1]
                exceptions.append(e)

                ret = 0
            return ret

    else:

        def vtx_callback_wrapper(vtx, num):
            return 0

    pygfxd.gfxd_vtx_callback(vtx_callback_wrapper)

    # timg_callback

    if timg_callback:

        def timg_callback_wrapper(timg, fmt, siz, width, height, pal):
            try:
                ret = timg_callback(timg, fmt, siz, width, height, pal)
            except:
                import sys

                e = sys.exc_info()[1]
                exceptions.append(e)

                ret = 0
            return ret

    else:

        def timg_callback_wrapper(timg, fmt, siz, width, height, pal):
            return 0

    pygfxd.gfxd_timg_callback(timg_callback_wrapper)

    # TODO
    # pygfxd.gfxd_dl_callback
    # pygfxd.gfxd_mtx_callback
    # pygfxd.gfxd_tlut_callback

    # macro_fn

    if macro_fn:

        def macro_fn_wrapper():
            try:
                ret = macro_fn()
            except:
                import sys

                e = sys.exc_info()[1]
                exceptions.append(e)

                ret = 0

            # TODO consider:
            if exceptions:
                ret = 1

            return ret

    else:

        def macro_fn_wrapper():
            ret = pygfxd.gfxd_macro_dflt()

            # TODO consider:
            if exceptions:
                ret = 1

            return ret

    pygfxd.gfxd_macro_fn(macro_fn_wrapper)

    # arg_fn

    if arg_fn:

        def arg_fn_wrapper(arg_num):
            try:
                arg_fn(arg_num)
            except:
                import sys

                e = sys.exc_info()[1]
                exceptions.append(e)

        pygfxd.gfxd_arg_fn(arg_fn_wrapper)
    else:
        pygfxd.gfxd_arg_fn(None)

    # Execute

    pygfxd.gfxd_execute()

    # The offset is in bytes and indicates the last command,
    # so add 8 (sizeof(Gfx))
    size = pygfxd.gfxd_macro_offset() + 8

    if exceptions:
        import traceback

        msg = "There were uncaught python errors in callbacks during gfxd execution."

        print()
        print(msg)
        print("vvv See below for a list of the traces of the uncaught errors:")

        for e in exceptions:
            print()
            traceback.print_exception(e)

        print()
        print(msg)
        print("^^^ See above for a list of the traces of the uncaught errors.")

        raise Exception(
            msg,
            "See the standard output for a list of the traces of the uncaught errors.",
            exceptions,
        )

    return size


class StringWrapper:
    def __init__(
        self,
        data: Union[str, bytes],
        max_line_length,
        writer: Callable[[Union[str, bytes]], None],
    ):
        self.max_line_length = max_line_length
        self.pending_data = data
        self.writer = writer
        self.newline_char = "\n" if isinstance(data, str) else b"\n"
        self.space_char = " " if isinstance(data, str) else b" "

    def append(self, data: Union[str, bytes]):
        self.pending_data += data
        self.proc()

    def proc(self, flush=False):
        while len(self.pending_data) > self.max_line_length or (
            flush and self.pending_data
        ):
            i = self.pending_data.find(self.newline_char, 0, self.max_line_length)
            if i >= 0:
                i += 1
                self.writer(self.pending_data[:i])
                self.pending_data = self.pending_data[i:]
                continue

            i = self.pending_data.rfind(self.space_char, 1, self.max_line_length)
            if i < 0:
                i = self.pending_data.find(self.space_char, 1)
                if i < 0:
                    if flush:
                        i = len(self.pending_data)
                    else:
                        # Avoid adding a line return in the middle of a word
                        return
            self.writer(self.pending_data[:i])
            self.pending_data = self.pending_data[i:]
            if not flush or self.pending_data:
                self.writer(self.newline_char)

    def flush(self):
        self.proc(flush=True)


class DListResource(Resource, can_size_be_unknown=True):
    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, None, name)

    def try_parse_data(self):
        offset = self.range_start

        if VERBOSE2:
            print(self.name, hex(offset))

        def vtx_cb(vtx, num):
            # TODO be smarter about buffer merging
            # (don't merge buffers from two different DLs, if they can be split cleanly)
            self.file.memory_context.mark_resource_buffer_at_segmented(
                VtxArrayResource,
                f"{self.name}_Vtx_{vtx:08X}",
                vtx,
                vtx + num * VtxArrayResource.element_cdata_ext.size,
            )
            return 0

        def timg_cb(timg, fmt, siz, width, height, pal):
            try:
                self.file.memory_context.report_resource_at_segmented(
                    timg,
                    lambda file, offset: TextureResource(
                        file,
                        offset,
                        f"{self.name}_Tex_{offset:08X}_",
                        G_IM_FMT.by_i[fmt],
                        G_IM_SIZ.by_i[siz],
                        width,
                        height,
                    ),
                )
            except NoSegmentBaseError:
                pass
            return 0

        size = gfxdis(
            input_buffer=self.file.data[self.range_start :],
            vtx_callback=vtx_cb,
            timg_callback=timg_cb,
        )

        self.range_end = self.range_start + size

        if VERBOSE2:
            print(self.name, hex(offset), hex(self.range_end))

        self.is_data_parsed = True

    def get_c_declaration_base(self):
        return f"Gfx {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError()

    def write_extracted(self):
        def macro_fn():
            ret = pygfxd.gfxd_macro_dflt()
            pygfxd.gfxd_puts(",\n")
            return ret

        def arg_fn(arg_num: int):
            timg = pygfxd.gfxd_value_by_type(pygfxd.GfxdArgType.Timg, 0)
            if (
                timg is not None
                and pygfxd.gfxd_arg_type(arg_num) == pygfxd.GfxdArgType.Dim
            ):
                _, timg_segmented, _ = timg
                dim_args_i = []
                for arg_i in range(pygfxd.gfxd_arg_count()):
                    if pygfxd.gfxd_arg_type(arg_i) == pygfxd.GfxdArgType.Dim:
                        dim_args_i.append(arg_i)
                assert arg_num in dim_args_i
                assert len(dim_args_i) <= 2
                if len(dim_args_i) == 2:
                    width_arg_i, height_arg_i = dim_args_i
                    # TODO this width/height stuff is jank code
                    # probably introduce an attribute system instead for resources, generalizing the length system
                    try:
                        (
                            resolution,
                            resolution_info,
                        ) = self.file.memory_context.resolve_segmented(timg_segmented)
                    except NoSegmentBaseError:
                        resolution = None
                    if resolution == SegmentedAddressResolution.FILE:
                        resolved_file, resolved_offset = resolution_info
                        result, resolved_resource = resolved_file.get_resource_at(
                            resolved_offset
                        )
                        assert result == GetResourceAtResult.DEFINITIVE
                        assert resolved_resource is not None
                        assert isinstance(resolved_resource, TextureResource)
                        width_arg_value = pygfxd.gfxd_arg_value(width_arg_i)[1]
                        height_arg_value = pygfxd.gfxd_arg_value(height_arg_i)[1]
                        if (resolved_resource.width, resolved_resource.height) == (
                            width_arg_value,
                            height_arg_value,
                        ):
                            if arg_num == width_arg_i:
                                if resolved_resource.width_name:
                                    pygfxd.gfxd_puts(resolved_resource.width_name)
                            else:
                                assert arg_num == height_arg_i
                                if resolved_resource.height_name:
                                    pygfxd.gfxd_puts(resolved_resource.height_name)
                            return
                        else:
                            if arg_num == width_arg_i:
                                print(
                                    "Unexpected texture dimensions used: in dlist =",
                                    self,
                                    "texture =",
                                    resolved_resource,
                                    "texture resource has WxH =",
                                    (resolved_resource.width, resolved_resource.height),
                                    "but dlist uses WxH =",
                                    (width_arg_value, height_arg_value),
                                )
                                pygfxd.gfxd_puts(
                                    " /* ! Unexpected texture dimensions !"
                                    + " DL={0[0]}x{0[1]} vs Tex={1[0]}x{1[1]} */ ".format(
                                        (width_arg_value, height_arg_value),
                                        (
                                            resolved_resource.width,
                                            resolved_resource.height,
                                        ),
                                    )
                                )

            pygfxd.gfxd_arg_dflt(arg_num)

        def vtx_cb(vtx, num):
            pygfxd.gfxd_puts(self.file.memory_context.get_c_reference_at_segmented(vtx))
            return 1

        def timg_cb(timg, fmt, siz, width, height, pal):
            try:
                timg_c_ref = self.file.memory_context.get_c_reference_at_segmented(timg)
            except NoSegmentBaseError:
                timg_c_ref = None
            except ValueError:
                # TODO handle better once I know why this even happens
                import traceback

                traceback.print_exc()
                pygfxd.gfxd_puts("/* BAD TIMG REF */")
                return 0
            if timg_c_ref:
                pygfxd.gfxd_puts(timg_c_ref)
                return 1
            return 0

        with self.extract_to_path.open("wb") as f:
            f.write(b"{\n")

            out_string_wrapper = StringWrapper(b"", 120, f.write)

            def output_cb(buf: bytes):
                out_string_wrapper.append(buf)

            gfxdis(
                input_buffer=self.file.data[self.range_start : self.range_end],
                output_callback=output_cb,
                enable_caps={pygfxd.GfxdCap.emit_dec_color},
                vtx_callback=vtx_cb,
                timg_callback=timg_cb,
                macro_fn=macro_fn,
                arg_fn=arg_fn,
            )

            out_string_wrapper.flush()

            f.write(b"}\n")


VERBOSE2 = False
