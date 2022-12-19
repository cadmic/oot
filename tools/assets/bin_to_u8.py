#!/bin/env python3
"""
Convert a binary file to a comma separated sequence of bytes

bin_to_u8.py <in_path> <out_path>
"""

import sys
from pathlib import Path

in_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])

in_bytes = memoryview(in_path.read_bytes())

from conf import WRITE_HINTS

with out_path.open("w") as f:
    if WRITE_HINTS:
        import os.path

        # Somehow this works in VSCode
        f.write(f"// file://./{os.path.relpath(in_path, out_path.parent)}\n")

        # "ValueError: relative path can't be expressed as a file URI"
        # indeed...
        # f.write(f"// {Path(os.path.relpath(in_path, out_path.parent)).as_uri()}\n")

        f.write(f"// {in_path.absolute().as_uri()}\n")

    f.write(
        "{\n"
        + ",\n".join(
            ", ".join(f"0x{b:02X}" for b in in_bytes[i : i + 16])
            for i in range(0, len(in_bytes), 16)
        )
        + "\n"
        + "}\n"
    )
