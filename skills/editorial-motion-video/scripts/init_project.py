#!/usr/bin/env python3
"""Create an editable starter or extract the bundled approved-film source example."""
import argparse
import shutil
import zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
parser.add_argument("--example", action="store_true", help="Extract approved-film example instead of starter")
args = parser.parse_args()
target = args.destination.expanduser().resolve()
if target.exists():
    parser.error("Destination already exists; choose a new folder")
if args.example:
    with zipfile.ZipFile(SKILL / "assets/attention-example.zip") as archive:
        archive.extractall(target)
else:
    shutil.copytree(SKILL / "assets/starter", target)
    shutil.copy2(SKILL / "assets/runtime/render.mjs", target / "render.mjs")
print(target)
print("Dependencies are not installed automatically. Run doctor.py against this folder.")
