import requests
from bs4 import BeautifulSoup
import json
import os

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL = "https://en.wikipedia.org/wiki/2025%E2%80%9326_Atlanta_Hawks_season"

# header needed to scrape wikipedia
headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_hawks():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get table with record and standings info
        record_table = soup.find("table", {"class": "infobox vcard"})
        if not record_table:
            print("Error: Could not find the Hawks record or standings on this page.")
        
        for row in record_table.find_all("tr"):
            row_header = row.find("th")
            row_value = row.find("td")

            if row_header and row_value:
                row_label = row_header.get_text(strip=True)
                row_text = row_value.get_text(strip=True)
            
            if not row_header or not row_value:
                continue
            
            if row_label == "Record":
                record_text = row_text
                wins = int(record_text[0])
                losses = int(record_text[2])

            if row_label == "Place":
                standings_text = row_text
                split_standings = standings_text.split(':')
                conf_standings = (split_standings[2])[1:3]
                division_standings = (split_standings[1])[1:3]

        hawks_data = {
            "team": "Atlanta Hawks",
            "wins": wins,
            "losses": losses,
            "record_text": record_text,
            "standings_text": standings_text,
            "conf_standings": conf_standings,
            "division_standings": division_standings
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
        data["falcons"] = hawks_data

        # Write to data.json
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Scraped Hawks data:", hawks_data)
        return hawks_data

    except requests.RequestException as e:
        print("Network error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

if __name__ == "__main__":
    scrape_hawks()
