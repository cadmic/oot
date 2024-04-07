#!/usr/bin/env python3

import os
import tempfile
import shutil
import subprocess
import sys


BUFFER_SIZE = 128 * 1024


def main():
    filename = sys.argv[-1]
    with tempfile.NamedTemporaryFile(
        mode="w", prefix="oot_", suffix=".c", encoding="euc-jp"
    ) as tmp:
        with open(filename, "r", encoding="utf-8") as f:
            tmp.write(f'#line 1 "{filename}"\n')
            shutil.copyfileobj(f, tmp, BUFFER_SIZE)
            tmp.flush()

        compile_command = sys.argv[1:-1] + ["-I", os.path.dirname(filename), tmp.name]
        process = subprocess.run(compile_command)
        sys.exit(process.returncode)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
