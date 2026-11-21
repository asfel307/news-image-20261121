#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261121 bounty (Python 3.13).

Standard library only. Copies the pre-rendered entry.png that sits beside
this file to $MAKEFUN_OUTPUT_DIR/entry.png (fallback /output).

Deterministic: a plain byte copy, so two runs write byte-identical output.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
