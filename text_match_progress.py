#!/usr/bin/env python3

import argparse
import collections
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
    func_name: str
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

    func_name = None
    result = []
    i = 6  # skip preamble
    while i < len(lines):
        row = lines[i]
        i += 1

        if not row:
            continue

        if not row.startswith(" "):
            label = row.split()[-1]
            # strip '<' and '>:'
            func_name = label[1:-2]
            continue

        if not func_name:
            raise Exception(f"no function name for line '{row}'")

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

        result.append(Inst(func_name, mnemonic, args, reloc_type, reloc_symbol))

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

def should_ignore_diff(line1, line2):
    if (
        line1.mnemonic == line2.mnemonic
        and line1.args[:2] == line2.args[:2]
        and line1.reloc_type == line2.reloc_type
    ):
        # ignore symbol differences
        return True

    if line1.mnemonic == line2.mnemonic and line1.mnemonic.startswith("b"):
        return True

    return False

def report_file(version, file):
    expected_dir = Path("expected/build") / version
    build_dir = Path("build") / version

    lines1 = run_objdump(expected_dir / file)
    lines2 = run_objdump(build_dir / file)

    trim_trailing_nops(lines1)
    trim_trailing_nops(lines2)

    functions_with_diffs = collections.OrderedDict()
    for line1, line2 in diff_lines(lines1, lines2):
        if line1 is None:
            functions_with_diffs[line2.func_name] = True
        elif line2 is None:
            functions_with_diffs[line1.func_name] = True
        elif line1 != line2:
            if not should_ignore_diff(line1, line2):
                functions_with_diffs[line1.func_name] = True
                functions_with_diffs[line2.func_name] = True

    if not functions_with_diffs:
        print(f"{file}: no diffs")
        return

    print(f"{file} functions with diffs:")
    for func_name in functions_with_diffs:
        print(f"  {func_name}")

def report_all_files(version):
    expected_dir = Path("expected/build") / version
    build_dir = Path("build") / version

    print("path,expected,actual,added,removed,changed")
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
        changed = 0
        for line1, line2 in diff_lines(lines1, lines2):
            if line1 is None:
                added += 1
            elif line2 is None:
                removed += 1
            elif line1 != line2:
                if not should_ignore_diff(line1, line2):
                    changed += 1

        print(f"{path},{len(lines1)},{len(lines2)},{added},{removed},{changed}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate progress matching .text sections")
    parser.add_argument("-v", "--version", help="version to compare", required=True)
    parser.add_argument("-f", "--file", help="object file to compare")
    args = parser.parse_args()

    if args.file is not None:
        report_file(args.version, args.file)
    else:
        report_all_files(args.version)
