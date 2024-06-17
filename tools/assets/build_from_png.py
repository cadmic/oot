#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pigment64

from utils import str_removeprefix, str_removesuffix

IMAGE_TYPES = {
    "i1": pigment64.ImageType.I1,
    "i4": pigment64.ImageType.I4,
    "i8": pigment64.ImageType.I8,
    "ia4": pigment64.ImageType.IA4,
    "ia8": pigment64.ImageType.IA8,
    "ia16": pigment64.ImageType.IA16,
    "ci4": pigment64.ImageType.CI4,
    "ci8": pigment64.ImageType.CI8,
    "rgba16": pigment64.ImageType.RGBA16,
    "rgba32": pigment64.ImageType.RGBA32,
}


def main():
    png_path = Path(sys.argv[1])
    out_bin_path = Path(sys.argv[2])

    suffixes = png_path.suffixes
    assert len(suffixes) >= 2
    assert suffixes[-1] == ".png"
    suffixes.pop()
    if suffixes[-1] in {".u64", ".u32"}:
        suffixes.pop()
    assert len(suffixes) > 0
    if suffixes[-1].startswith(".tlut_"):
        tlut_info = str_removeprefix(suffixes.pop(), ".")
    else:
        tlut_info = None
    assert len(suffixes) > 0
    fmtsiz_str = str_removeprefix(suffixes[-1], ".")
    image_type = IMAGE_TYPES[fmtsiz_str]

    with open(png_path, "rb") as png:
        input_data = png.read()
    png_image = pigment64.PNGImage.read(input_data)

    if image_type not in (pigment64.ImageType.CI4, pigment64.ImageType.CI8):
        out_bin_path.write_bytes(png_image.as_native(image_type))
    else:
        # TODO probably move tlut_info and overall tex file suffix construction/parsing to its own library

        if tlut_info is None:
            tlut_elem_type = "u64"
            tlut_out_bin_path_base_str = str(out_bin_path)
            tlut_out_bin_path_base_str = str_removesuffix(
                tlut_out_bin_path_base_str, ".bin"
            )
            if tlut_out_bin_path_base_str.endswith(".u64"):
                tlut_out_bin_path_base_str = str_removesuffix(
                    tlut_out_bin_path_base_str, ".u64"
                )
        else:
            tlut_elem_type = "u64"
            if tlut_info.endswith("_u64"):
                tlut_elem_type = "u64"
                tlut_name = str_removesuffix(
                    str_removeprefix(tlut_info, "tlut_"), "_u64"
                )
            elif tlut_info.endswith("_u32"):
                tlut_elem_type = "u32"
                tlut_name = str_removesuffix(
                    str_removeprefix(tlut_info, "tlut_"), "_u32"
                )
            else:
                tlut_name = str_removeprefix(tlut_info, "tlut_")
            tlut_out_bin_path_base_str = str(out_bin_path.parent / tlut_name)

        tlut_out_bin_path = Path(
            f"{tlut_out_bin_path_base_str}.tlut.rgba16.{tlut_elem_type}.bin"
        )

        out_bin_path.write_bytes(png_image.as_native(image_type))
        tlut_out_bin_path.write_bytes(pigment64.create_palette_from_png(input_data))

        import subprocess

        # HACK since the makefile doesn't know the tlut file should be built (bin2c'd), build it here
        cmd = [
            "tools/assets/bin2c/bin2c",
            tlut_elem_type,
        ]
        with tlut_out_bin_path.open("rb") as fin:
            with tlut_out_bin_path.with_suffix(".inc.c").open("w") as fout:
                subprocess.check_call(cmd, stdin=fin, stdout=fout)


if __name__ == "__main__":
    main()
