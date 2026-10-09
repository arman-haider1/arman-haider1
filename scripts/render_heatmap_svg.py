
import json
from pathlib import Path
from datetime import date
from html import escape

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "contributions.json"
OUTPUT_FILE = ROOT / "contrib-heatmap.svg"

CELL_SIZE = 12
GAP = 3
STEP = CELL_SIZE + GAP

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


def render_heatmap():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Contribution data not found: {INPUT_FILE}"
        )

    contributions = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    if not contributions:
        raise ValueError("Contribution data file is empty.")

    days = {}

    for item in contributions:
        day = date.fromisoformat(item["date"])
        days[day] = max(0, min(4, int(item.get("level", 0))))

    first_day = min(days)
    last_day = max(days)

    start = date.fromordinal(
        first_day.toordinal() - first_day.weekday()
    )
    end = date.fromordinal(
        last_day.toordinal() + (6 - last_day.weekday())
    )

    weeks = (end - start).days // 7 + 1
    width = weeks * STEP - GAP
    height = 7 * STEP - GAP

    rects = []

    for day, level in sorted(days.items()):
        week = (day - start).days // 7
        weekday = day.weekday()

        x = week * STEP
        y = weekday * STEP

        rects.append(
            f'<rect x="{x}" y="{y}" '
            f'width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="3" fill="{COLORS[level]}">'
            f'<title>{escape(day.isoformat())}: '
            f'contribution level {level}</title></rect>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <rect width="100%" height="100%" fill="#0d1117" rx="6"/>
    {''.join(rects)}
    </svg>
    """

    OUTPUT_FILE.write_text(svg, encoding="utf-8")

    print(f"Heatmap created: {OUTPUT_FILE}")
    print(f"Days: {len(days)}")
    print(f"Dimensions: {width} x {height}")


if __name__ == "__main__":
    render_heatmap()