#!/usr/bin/env python3
"""finalize.py — news-image-20261119 v242-R2 ("The World in One Day").

Turns the deterministic Chromium screenshot into the entry files:
  entry.png       (1024x1024, the submission image)
  render-600.png  (Lanczos downscale of the same entry.png)
  render-300.png  (Lanczos downscale of the same entry.png)

Rules enforced here: entry.png is a copy of build/raw-1024.png when its
PNG chunks are exactly IHDR/IDAT/IEND (otherwise it is re-encoded with
Pillow, which writes those three chunks only); every output must stay
under 1 MiB; the two downscales always come from the final entry.png;
rerunning this script must reproduce identical hashes.

Run: python3 finalize.py   (from this directory)
"""
import hashlib
import os
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
RAW = os.path.join(BUILD, "raw-1024.png")
LIMIT = 1024 * 1024


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def chunk_names(path):
    names = []
    with open(path, "rb") as fh:
        head = fh.read(8)
        assert head == b"\x89PNG\r\n\x1a\n", "not a PNG file"
        while True:
            raw = fh.read(8)
            if len(raw) < 8:
                break
            size = struct.unpack(">I", raw[:4])[0]
            names.append(raw[4:8].decode("ascii", "replace"))
            fh.seek(size + 4, 1)
    return names


def main():
    if not os.path.exists(RAW):
        print("missing build/raw-1024.png — run node render.js first")
        return 1
    chunks = chunk_names(RAW)
    print("raw chunks:", chunks)
    entry = os.path.join(HERE, "entry.png")
    if chunks == ["IHDR", "IDAT", "IEND"]:
        with open(RAW, "rb") as src, open(entry, "wb") as dst:
            dst.write(src.read())
        print("entry.png: copied raw screenshot (chunks already minimal)")
    else:
        img = Image.open(RAW).convert("RGB")
        img.save(entry, format="PNG")
        print("entry.png: re-encoded with Pillow (raw had extra chunks)")
    img = Image.open(entry)
    print(f"entry.png: {img.size[0]}x{img.size[1]} {img.mode}, "
          f"{os.path.getsize(entry)} bytes, sha256 {sha256_of(entry)}")
    if img.size != (1024, 1024):
        print("SIZE FAIL: entry is not 1024x1024")
        return 1
    if os.path.getsize(entry) > LIMIT:
        print("SIZE FAIL: entry is over 1 MiB")
        return 1
    for side in (600, 300):
        out = os.path.join(HERE, f"render-{side}.png")
        small = img.resize((side, side), Image.LANCZOS)
        small.save(out, format="PNG")
        print(f"render-{side}.png: {os.path.getsize(out)} bytes, "
              f"sha256 {sha256_of(out)}")
        if os.path.getsize(out) > LIMIT:
            print(f"SIZE FAIL: render-{side} is over 1 MiB")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
