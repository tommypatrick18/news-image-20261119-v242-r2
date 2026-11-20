#!/usr/bin/env python3
"""main.py — news-image-20261119 v242-R2 ("The World in One Day").

Entry program: place the finished page image where the harness expects it.
The image is drawn at build time (page.html rendered in headless Chromium);
this program only carries the finished bytes to the output directory, so
every run produces the exact same file. Standard library only.

Expects MAKEFUN_OUTPUT_DIR in the environment. Writes entry.png there
and prints its size and sha256 so the run can be checked at a glance.
"""
import hashlib
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def digest_of(data):
    return hashlib.sha256(data).hexdigest()


def run():
    source = HERE / "entry.png"
    if not source.is_file():
        print("entry.png is missing from the repository", file=sys.stderr)
        return 1
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not target_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    payload = source.read_bytes()
    destination = pathlib.Path(target_dir) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    back = destination.read_bytes()
    if back != payload:
        print("output bytes differ from entry.png", file=sys.stderr)
        return 1
    print(f"entry.png: {len(payload)} bytes sha256 {digest_of(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
