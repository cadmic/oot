#!/usr/bin/env python3

import argparse
import collections
import os

from mapfile_parser import mapfile

def main():
    parser = argparse.ArgumentParser(description="Generate CSV files for disasm.py from z64.map")
    parser.add_argument("--csv-dir", help="Directory to write CSVs to", required=True)
    parser.add_argument("mapfile", help="Mapfile to parse")

    args = parser.parse_args()

    mapFile = mapfile.MapFile()
    mapFile.readMapFile(args.mapfile)

    segments = []
    fileLists = collections.defaultdict(list)
    functions = []

    for segment in mapFile:
        name = segment.name
        if name in ('..boot', '..code') or (name.startswith('..ovl_') and not name.endswith('.bss')):
            segments.append(segment)

        for file in segment:
            if file.sectionType == '.text':
                functions.extend(file)

            if file.sectionType in ('.text', '.data', '.rodata', '.bss', '.ovl'):
                if name.startswith('..boot'):
                    fileLists['boot'].append(file)
                elif name.startswith('..code'):
                    fileLists['code'].append(file)
                elif name.startswith('..ovl_file_choose'):
                    fileLists['ovl_file_choose'].append(file)
                elif name.startswith('..ovl_kaleido_scope'):
                    fileLists['ovl_kaleido_scope'].append(file)

    outputDir = args.csv_dir
    os.makedirs(outputDir, exist_ok=True)

    with open(f'{outputDir}/file_addresses.csv', 'w') as f:
        f.write('name,vrom_start,vrom_end,vram_start\n')
        for segment in segments:
            f.write(f'{segment.name[2:]},{segment.vrom:X},{segment.vrom + segment.size:X},{segment.vram:X}\n')

    for romFile, section in fileLists.items():
        with open(f'{outputDir}/files_{romFile}.csv', 'w') as f:
            offset = 0
            prevFile = None
            for file in section:
                name, ext = os.path.splitext(os.path.basename(file.filepath))
                if ext != '.o':
                    continue

                # disambiguate audio files
                if '/audio/lib/' in str(file.filepath):
                    name = f'audio_lib_{name}'
                elif '/audio/' in str(file.filepath):
                    name = f'audio_{name}'
                # hacks for manual .bss sections
                elif name == 'fault.bss':
                    name = 'fault'
                elif name == 'fault_drawer.bss':
                    name = 'fault_drawer'

                if prevFile is None:
                    f.write(f'offset,vram,{file.sectionType}\n')
                elif prevFile.sectionType != file.sectionType:
                    f.write('\n')
                    f.write(f'offset,vram,{file.sectionType}\n')

                if prevFile is not None:
                    offset += file.vram - prevFile.vram
                prevFile = file

                f.write(f'{offset:X},{file.vram:X},{name}\n')

            if prevFile is not None:
                f.write(f'{offset + prevFile.size:X},{prevFile.vram + prevFile.size:X},.end\n')

    with open(f'{outputDir}/functions.csv', 'w') as f:
        for symbol in functions:
            f.write(f'{symbol.vram:08X},{symbol.name}\n')

if __name__ == '__main__':
    main()
