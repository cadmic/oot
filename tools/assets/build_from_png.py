#!/usr/bin/env python3

import sys
from pathlib import Path

png_path = Path(sys.argv[1])
out_bin_path = Path(sys.argv[2])


sys.path.insert(0, "/home/dragorn421/Documents/n64texconv/")
import n64texconv

sys.path.insert(0, "/home/dragorn421/Documents/oot/tools/assets/png2raw/")
import png2raw

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from png2raw import png2raw


def png_to_data(file):
    with png2raw.Instance(file) as inst:
        width, height = inst.get_dimensions()
        if inst.is_paletted():
            palette_data = inst.get_palette_rgba32()
            image_data = inst.read_palette_indices()

            row_len = width
        else:
            palette_data = None
            image_data = inst.read_to_rgba32()

            row_len = width * 4

    image_data = image_data
    rows = [image_data[row * row_len :][:row_len] for row in range(height)]

    png_data = width, height, rows
    return png_data, palette_data


n64texconv.png_to_data = png_to_data

# TODO put G_IM_FMT, G_IM_SIZ somewhere else
from extase_oot64.dlist_resources import G_IM_FMT, G_IM_SIZ

suffixes = png_path.suffixes
assert len(suffixes) >= 2
assert suffixes[-1] == ".png"
suffixes.pop()
if suffixes[-1] in {".u64", ".u32"}:
    suffixes.pop()
assert len(suffixes) > 0
fmtsiz_str = suffixes[-1].removeprefix(".")

fmt, siz = None, None
for candidate_fmt in G_IM_FMT:
    for candidate_siz in G_IM_SIZ:
        candidate_fmtsiz_str = f"{candidate_fmt.name.lower()}{candidate_siz.bpp}"
        if candidate_fmtsiz_str == fmtsiz_str:
            fmt = candidate_fmt
            siz = candidate_siz

assert fmt is not None and siz is not None, fmtsiz_str

tex = n64texconv.Image.from_png(png_path, fmt=fmt.i, siz=siz.i)
tex_bin = tex.to_bin()
# print(len(tex_bin), tex_bin[:0x10], tex_bin[-0x10:], file=sys.stderr)
# sys.stdout.buffer.write(tex_bin) # for some reason the *string* "None." is also written to stdout???
out_bin_path.write_bytes(tex_bin)
