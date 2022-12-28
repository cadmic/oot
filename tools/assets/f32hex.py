#!/usr/bin/env python3

import sys
import struct
import re

# Freely adapted from https://github.com/simonlindholm/asm-processor which is under the UNLICENSE

float_regexpr = re.compile(r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?f")


def repl_float_hex(m: re.Match[str]):
    val_float_str = m.group(0).strip()
    val_float = float(val_float_str.rstrip("f"))
    (val_u32,) = struct.unpack(
        ">I",
        struct.pack(
            ">f",
            val_float,
        ),
    )
    return f"0x{val_u32:08X} /* {val_float_str} */"


def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = re.sub(float_regexpr, repl_float_hex, line)
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
