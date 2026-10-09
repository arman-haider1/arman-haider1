
from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "arman-haider1"

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "contributions.json"
)

PROFILE_URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_contributions():
    print(f"Fetching contributions for {USERNAME}...")

    response = requests.get(
        PROFILE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    contribution_days = []

    for day in soup.select("td.ContributionCalendar-day"):
        date = day.get("data-date")
        level = day.get("data-level", "0")

        if date:
            contribution_days.append(
                {
                    "date": date,
                    "level": int(level) if level.isdigit() else 0,
                }
            )

    if not contribution_days:
        raise RuntimeError(
            "Contribution data nahi mila. GitHub page ka format check karna hoga."
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(contribution_days, indent=2),
        encoding="utf-8",
    )

    print(f"Success! Saved {len(contribution_days)} contribution days.")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_contributions()