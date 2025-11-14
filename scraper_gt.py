import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL = "https://en.wikipedia.org/wiki/2025_Georgia_Tech_Yellow_Jackets_football_team"

# header needed to scrape wikipedia
headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_gt():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get table with record and ranking info
        record_table = soup.find("table", {"class": "infobox vevent"})
        if not record_table:
            print("Error: Could not find the Georgia Tech record or standings on this page.")
        
        for row in record_table.find_all("tr"):
            row_header = row.find("th")
            row_value = row.find("td")

            if row_header and row_value:
                row_label = row_header.get_text(strip=True)
                row_text = row_value.get_text(strip=True)
            
            if not row_header or not row_value:
                continue

            if row_label == "CFP":
                ranking = row_text

            if row_label == "Record":
                record_text = row_text.split(" ")[0]
                parts = [int(x.strip()) for x in record_text.split("–")]
                wins, losses = parts[0], parts[1]

                conf_record_text = row_text.split(" ")[1][1:]            

        # get table with conf standings
        standings_table = soup.find("table", {"class": "standings-box"})
        if not standings_table:
            print("Error: Could not find the Georgia Tech record or standings on this page.")

        standings = 0
        for row in standings_table.find_all("tr"):
            if row.find("td") == None:
                continue

            standings += 1
            row_value = row.find("td").find("a")
            if (row_value.get_text(strip=True) == "Georgia Tech"):
                break
            

        # set season_ongoing field
        today = datetime.today().date()
        gt_end_date_str = "2026-01-19"
        gt_end_date = datetime.strptime(gt_end_date_str, "%Y-%m-%d").date()
        if (today <= gt_end_date):
            season_ongoing = "YES"
        else:
            season_ongoing = "NO"

        gt_data = {
            "team": "Georgia Tech Yellow Jackets (Football)",
            "wins": wins,
            "losses": losses,
            "record_text": record_text,
            "ranking": ranking,
            "conf_record": conf_record_text,
            "conf_standings": standings,
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

        # Update only the GT section
        data["gt"] = gt_data

        # Write to data.json
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Scraped GT data:", gt_data)
        return gt_data

    except requests.RequestException as e:
        print("Network error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

if __name__ == "__main__":
    scrape_gt()
