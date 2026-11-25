#!/usr/bin/env python3
"""Write the 25 November 2026 world-news poster to the output directory.

The poster is the PNG file entry.png beside this script: a newspaper
front page drawn from the day's verified news (see research.md for the
sources and build_poster.py for how the image was drawn). This program
only copies those exact bytes to $MAKEFUN_OUTPUT_DIR/entry.png (or
/output when the variable is unset), after checking the file is a whole
1024x1024 PNG of at most 1 MiB whose sha256 matches the verified build.

Standard library only, no network, no clock, no randomness: two runs
write byte-identical output.
"""

import hashlib
import os
import struct
import sys

ASSET = "entry.png"
EXPECTED_SHA256 = (
    "fa1b0070cdc1b7e2dd17763240ce7b31b00184b26aedb8caa6b05af5d0f8c2e4"
)
MAX_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    src = os.path.join(bot_dir, ASSET)
    with open(src, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_SIGNATURE:
        fail("entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail("entry.png is %dx%d, not 1024x1024" % (width, height))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("entry.png sha256 mismatch: " + digest)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as handle:
        handle.write(data)
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), digest))


if __name__ == "__main__":
    main()
