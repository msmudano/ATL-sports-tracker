# scraper_falcons.py
import requests
from bs4 import BeautifulSoup
import json
import os

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL = "https://www.nfl.com/teams/atlanta-falcons/stats"

def scrape_record():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Select the div with both classes
        record_div = soup.select_one(".nfl-c-team-header__stats.nfl-u-hide-empty")
        if not record_div:
            print("Error: Could not find the Falcons record on the page.")
            return None

        record_text = record_div.get_text(strip=True)
        # Split "3 - 5 - 0" into integers
        parts = [int(x.strip()) for x in record_text.split("-")]
        wins, losses = parts[0], parts[1]
        ties = parts[2] if len(parts) > 2 else 0

        data = {
            "team": "Atlanta Falcons",
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "record_text": record_text
        }

        # Write to data.json
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Scraped record:", data)
        return data

    except requests.RequestException as e:
        print("Network error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

if __name__ == "__main__":
    scrape_record()
