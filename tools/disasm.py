#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import os
from pathlib import Path

import spimdisasm
from spimdisasm import frontendCommon as fec

@dataclass
class Split:
    section: spimdisasm.mips.sections.SectionBase
    outputPath: Path

def loadFile(
    context: spimdisasm.common.Context,
    csvDir: Path,
    outputDir: Path,
    rom: bytearray,
    filename: str,
    vromStart: int,
    vromEnd: int,
    vramStart: int,
) -> Split:
    fileSplitsPath = csvDir / f"files_{filename}.csv"
    if fileSplitsPath.exists():
        splitsData = spimdisasm.common.FileSplitFormat()
        splitsData.readCsvFile(fileSplitsPath)
        relocSection = None
    elif filename.startswith("ovl_"):
        splitsData = None
        relocSection = spimdisasm.mips.sections.SectionRelocZ64(
            context,
            vromStart=vromStart,
            vromEnd=vromEnd,
            vram=vramStart,
            filename=filename,
            array_of_bytes=rom,
            segmentVromStart=vromStart,
            overlayCategory=None)
    else:
        splitsData = None
        relocSection = None

    segment = spimdisasm.mips.FileSplits(
        context,
        vromStart=vromStart,
        vromEnd=vromEnd,
        vram=vramStart,
        filename=filename,
        array_of_bytes=rom,
        segmentVromStart=vromStart,
        overlayCategory=None,
        splitsData=splitsData,
        relocSection=relocSection)

    splits = []
    for sectionType, filesInSection in segment.sectionsDict.items():
       for splitName, section in filesInSection.items():
            splits.append(Split(section, outputDir / filename / splitName))
    return splits

def main():
    parser = argparse.ArgumentParser(description="Disassemble an uncompressed ROM")
    parser.add_argument("--csv-dir", help="Version-specific configuration directory", required=True)
    parser.add_argument("--output-dir", help="Output directory", required=True)
    parser.add_argument("rom", help="ROM to disassemble")

    spimdisasm.common.Context.addParametersToArgParse(parser)
    spimdisasm.common.GlobalConfig.addParametersToArgParse(parser)
    spimdisasm.mips.InstructionConfig.addParametersToArgParse(parser)

    args = parser.parse_args()
    csvDir = Path(args.csv_dir)
    outputDir = Path(args.output_dir)
    romPath = Path(args.rom)

    context = spimdisasm.common.Context()
    context.parseArgs(args)
    context.changeGlobalSegmentRanges(0x00000000, 0x01000000, 0x8000000, 0x81000000)
    context.globalSegment.readFunctionsCsv(csvDir / "functions.csv")

    spimdisasm.mips.InstructionConfig.parseArgs(args)
    spimdisasm.common.GlobalConfig.parseArgs(args)

    spimdisasm.common.GlobalConfig.PRODUCE_SYMBOLS_PLUS_OFFSET = True
    spimdisasm.common.GlobalConfig.TRUST_USER_FUNCTIONS = True

    rom = spimdisasm.common.Utils.readFileAsBytearray(romPath)

    splits = []
    with open(csvDir / "file_addresses.csv") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            name = row["name"]
            vromStart = int(row["vrom_start"], 16)
            vromEnd = int(row["vrom_end"], 16)
            vramStart = int(row["vram_start"], 16)
            splits += loadFile(context, csvDir, outputDir, rom, name, vromStart, vromEnd, vramStart)

    # analyze .text first to generate data symbols
    splits.sort(key=lambda split: split.section.sectionType)

    for split in splits:
        spimdisasm.common.Utils.printQuietless(f"Analyzing {split.outputPath}{split.section.sectionType.toStr()} ...")
        split.section.analyze()

    for split in splits:
        spimdisasm.common.Utils.printQuietless(f"Writing {split.outputPath}{split.section.sectionType.toStr()} ...")
        split.outputPath.parent.mkdir(parents=True, exist_ok=True)
        split.section.saveToFile(str(split.outputPath))

if __name__ == '__main__':
    main()
