from pathlib import Path

import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PHOTO = BASE_DIR / "source-prepped.png"
OUTPUT_SVG = BASE_DIR / "avi-ascii.svg"

ASCII_RAMP = " .\\`:-=+*cs#%@"
COLUMNS = 160
CHAR_WIDTH = 8
CHAR_HEIGHT = 12


def image_to_ascii(image_path):
    image = Image.open(image_path).convert("L")
    width, height = image.size
    rows = max(1, round(height / width * COLUMNS * CHAR_WIDTH / CHAR_HEIGHT))
    image = image.resize((COLUMNS, rows))

    pixels = np.asarray(image, dtype=np.uint8)
    ramp_max = len(ASCII_RAMP) - 1
    lines = []

    for row in pixels:
        line = "".join(
            " " if int(pixel) > 252
            else ASCII_RAMP[
                min(ramp_max, int(int(pixel) * len(ASCII_RAMP) / 256))
            ]
            for pixel in row
        )
        lines.append(line)

    return lines


def make_svg(lines):
    width = COLUMNS * CHAR_WIDTH
    height = len(lines) * CHAR_HEIGHT
    escaped_lines = []

    for row_index, line in enumerate(lines):
        escaped = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
        escaped_lines.append(
            f'<text x="0" y="{(row_index + 1) * CHAR_HEIGHT}" '
            f'class="ascii-line" style="--row:{row_index}">{escaped}</text>'
        )

    content = "\n".join(escaped_lines)

    return f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <style>
    .ascii-line {{
      font-family: "Courier New", monospace;
      font-size: {CHAR_HEIGHT}px;
      white-space: pre;
      fill: #111111;
      clip-path: inset(0 100% 0 0);
      animation: type-in 0.7s ease-out forwards;
      animation-delay: calc(var(--row) * 0.035s);
    }}
    @keyframes type-in {{
      to {{ clip-path: inset(0 0 0 0); }}
    }}
  </style>
  {content}
</svg>
'''


def main():
    if not INPUT_PHOTO.exists():
        raise FileNotFoundError(f"Prepared photo not found: {INPUT_PHOTO}")

    print("Converting photo to ASCII...")
    lines = image_to_ascii(INPUT_PHOTO)

    print("Creating animated SVG...")
    OUTPUT_SVG.write_text(make_svg(lines), encoding="utf-8")

    print(f"ASCII portrait saved to: {OUTPUT_SVG}")
    print(f"Portrait dimensions: {COLUMNS * CHAR_WIDTH} x {len(lines) * CHAR_HEIGHT}")


if __name__ == "__main__":
    main()



