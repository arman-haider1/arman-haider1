
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "info-card.svg"

STATIC = os.getenv("STATIC") == "1"

rows = [
    ("Now", "Learning Cyber Security"),
    ("Prev", "Web Security Auditing"),
    ("Stack", "Python | Git | GitHub"),
    ("Highlights", "OWASP | Security Labs"),
]

row_markup = []

for index, (label, value) in enumerate(rows):
    y = 94 + index * 34
    delay = index * 0.35

    animation = ""
    if not STATIC:
        animation = (
            f'opacity="0" '
            f'style="animation: reveal 0.5s ease-out '
            f'{delay}s forwards"'
        )

    row_markup.append(
        f'<text x="32" y="{y}" fill="#39d353" '
        f'font-family="monospace" font-size="15" '
        f'font-weight="bold" {animation}>{label:12}</text>'
        f'<text x="175" y="{y}" fill="#c9d1d9" '
        f'font-family="monospace" font-size="14" '
        f'{animation}>{value}</text>'
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="490" height="235" viewBox="0 0 490 235">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#161b22"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <style>
    @keyframes reveal {{
      from {{ opacity: 0; transform: translateY(7px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</defs>
<rect width="490" height="235" rx="12"
fill="url(#bg)" stroke="#30363d"/>
<path d="M12 0 H478 Q490 0 490 12 V43 H0 V12 Q0 0 12 0"
fill="#21262d"/>
<circle cx="20" cy="21" r="5" fill="#ff5f56"/>
<circle cx="38" cy="21" r="5" fill="#ffbd2e"/>
<circle cx="56" cy="21" r="5" fill="#27c93f"/>
<text x="245" y="26" fill="#8b949e" font-family="monospace"
font-size="12" text-anchor="middle">arman@github ~</text>
<text x="24" y="68" fill="#58a6ff" font-family="monospace"
font-size="15" font-weight="bold">profile.conf</text>
{''.join(row_markup)}
</svg>
"""

OUTPUT_FILE.write_text(svg, encoding="utf-8")
print(f"Info card generated: {OUTPUT_FILE}")
print(f"Static preview mode: {STATIC}")