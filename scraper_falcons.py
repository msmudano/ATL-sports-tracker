import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL = "https://www.nfl.com/teams/atlanta-falcons/stats"

def scrape_falcons():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # team record
        record_div = soup.select_one(".nfl-c-team-header__stats.nfl-u-hide-empty")
        if not record_div:
            print("Error: Could not find the Falcons record on the page.")
            return None
        
        # team standings
        standings_div = soup.select_one(".nfl-c-team-header__ranking.nfl-u-hide-empty")
        if not standings_div:
            print("Error: Could not find the Falcons standings on the page.")
            return None

        # convert record into ints
        record_text = record_div.get_text(strip=True)
        parts = [int(x.strip()) for x in record_text.split("-")]
        wins, losses = parts[0], parts[1]
        ties = parts[2] if len(parts) > 2 else 0

        # convert standings into text
        standings_text = standings_div.get_text(strip=True)

        # set season_ongoing field
        today = datetime.today().date()
        falcons_end_date = "02-08-2026"
        if (today <= falcons_end_date):
            season_ongoing = "YES"
        else:
            season_ongoing = "NO"

        falcons_data = {
            "team": "Atlanta Falcons",
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "record_text": record_text,
            "standings_text": standings_text,
            "season_ongoing": season_ongoing
        }

        # Load existing JSON if available
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        # Update only the Falcons section
        data["falcons"] = falcons_data

        # Write to data.json
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Scraped Falcons data:", falcons_data)
        return falcons_data

    except requests.RequestException as e:
        print("Network error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

if __name__ == "__main__":
    scrape_falcons()
