#!/usr/bin/env python3
"""news-image-20261124 entry (Python 3.13, standard library only).

Copies the front-page image this repository holds (entry.png, drawn by
draw.py) to /output/entry.png. The grader runs this program twice with no
network; a byte copy is deterministic, so both runs write identical bytes.

Local test:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
