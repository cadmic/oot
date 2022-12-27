#!/bin/env python3
"""
Convert a binary file to a comma separated sequence of words (4 bytes)

bin_to_u32.py <in_path> <out_path>
"""

import sys
import struct
from pathlib import Path

in_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])

in_bytes = memoryview(in_path.read_bytes())

assert len(in_bytes) % 4 == 0

from conf import WRITE_HINTS

with out_path.open("w") as f:
    if WRITE_HINTS:
        f.write(f"// {in_path.absolute().as_uri()}\n")

    f.write(
        "{\n"
        + ",\n".join(
            ", ".join(
                f"0x{w:08X}"
                for (w,) in struct.iter_unpack(">I", in_bytes[i : i + 16])
            )
            for i in range(0, len(in_bytes), 16)
        )
        + "\n"
        + "}\n"
    )
