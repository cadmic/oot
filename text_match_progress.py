#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import difflib
from enum import Enum
import itertools
from pathlib import Path
import subprocess
import sys

class RelocType(Enum):
    R_MIPS_LO16 = 1
    R_MIPS_HI16 = 2
    R_MIPS_26 = 3

@dataclass
class Inst:
    mnemonic: str
    args: list[str]
    reloc_type: str|None
    reloc_symbol: str|None

def run_objdump(filename):
    # mips-linux-gnu-objdump -m mips:4300 -drz -j .text
    command = [
        "mips-linux-gnu-objdump",
        "-drz",
        "-m", "mips:4300",
        "-j", ".text",
        str(filename),
    ]
    try:
        lines = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            encoding="utf-8"
        ).stdout.splitlines()
    except subprocess.CalledProcessError as e:
        return []

    result = []
    i = 6  # skip preamble
    while i < len(lines):
        row = lines[i]
        i += 1

        if not row or not row.startswith(" "):
            continue

        parts = row.split()
        mnemonic = parts[2]
        args = []
        if len(parts) > 3:
            for part in parts[3].split(","):
                if "(" in part:
                    # move immediate to the end
                    offset, rest = part.split("(")
                    args.append(rest[:-1])
                    args.append(offset)
                else:
                    args.append(part)

        reloc_type = None
        reloc_symbol = None
        while i < len(lines) and lines[i].startswith("\t"):
            reloc = lines[i]
            i += 1

            reloc_symbol = reloc.split()[-1]
            if "R_MIPS_LO16" in reloc:
                reloc_type = RelocType.R_MIPS_LO16
            elif "R_MIPS_HI16" in reloc:
                reloc_type = RelocType.R_MIPS_HI16
            elif "R_MIPS_26" in reloc:
                reloc_type = RelocType.R_MIPS_26
            else:
                raise Exception(f"unknown relocation '{reloc}' for line '{row}'")

        result.append(Inst(mnemonic, args, reloc_type, reloc_symbol))

    return result

def trim_trailing_nops(lines):
    while lines and lines[-1].mnemonic == "nop":
        lines.pop()

def diff_lines(lines1, lines2):
    differ = difflib.SequenceMatcher(
        a=[line.mnemonic for line in lines1],
        b=[line.mnemonic for line in lines2],
        autojunk=False)
    for (tag, i1, i2, j1, j2) in differ.get_opcodes():
        for line1, line2 in itertools.zip_longest(lines1[i1:i2], lines2[j1:j2]):
            yield (line1, line2)

def print_progress(version):
    expected_dir = Path("expected/build") / version
    build_dir = Path("build") / version

    print("path,expected,actual,added,removed,data diff,other diff")
    for object_file in sorted(expected_dir.glob("src/**/*.o")):
        path = object_file.relative_to(expected_dir)

        lines1 = run_objdump(expected_dir / path)
        lines2 = run_objdump(build_dir / path)

        trim_trailing_nops(lines1)
        trim_trailing_nops(lines2)

        if not lines1 or not lines2:
            continue

        added = 0
        removed = 0
        data_diff = 0
        other_diff = 0
        for line1, line2 in diff_lines(lines1, lines2):
            if line1 is None:
                added += 1
            elif line2 is None:
                removed += 1
            elif line1 != line2:
                if (
                    line1 is not None
                    and line2 is not None
                    and line1.mnemonic == line2.mnemonic
                    and line1.args[:2] == line2.args[:2]
                    and line1.reloc_type == line2.reloc_type
                ):
                    data_diff += 1
                else:
                    other_diff += 1

        print(f"{path},{len(lines1)},{len(lines2)},{added},{removed},{data_diff},{other_diff}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate progress matching .text sections")
    parser.add_argument("-v", "--version", help="version to compare", required=True)
    args = parser.parse_args()
    print_progress(args.version)
