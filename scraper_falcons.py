# scraper_falcons_record.py
import requests
from bs4 import BeautifulSoup
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
TARGET_URL = "https://www.nfl.com/teams/atlanta-falcons/stats"  # or whichever page you use

def scrape_record():
    resp = requests.get(TARGET_URL, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Example: find where the record is shown; you’ll need to inspect the page HTML
    # For demo: suppose there’s an element <div class="team-record">3-5-0</div>
    record_div = soup.select_one(".nfl-c-team-header__stats nfl-u-hide-empty")  # adjust selector
    record_text = record_div.get_text(strip=True)

    # Might be something like "3-5-0" meaning wins-losses-ties
    wins, losses, ties = record_text.split("-")
    result = {
        "team": "Atlanta Falcons",
        "wins": int(wins),
        "losses": int(losses),
        "ties": int(ties) if ties.isdigit() else 0,
        "record_text": record_text
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("Scraped record:", result)
    return result

if __name__ == "__main__":
    scrape_record()
