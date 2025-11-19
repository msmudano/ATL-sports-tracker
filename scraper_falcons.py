import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URLs to scrape
TARGET_URL_1 = "https://en.wikipedia.org/wiki/2025_Atlanta_Falcons_season"
TARGET_URL_2 = "https://www.teamrankings.com/nfl/team/atlanta-falcons/stats"

# header needed to scrape wikipedia
headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_falcons():
    try:
        # Fetch page for record, standings info
        resp = requests.get(TARGET_URL_1, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get table with record and division standings info
        record_table = soup.find("table", {"class": "infobox vcard"})
        if not record_table:
            print("Error: Could not find the Falcons record or standings on this page")

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
                parts = [x.strip() for x in record_text.split("–")]
                wins = parts[0]
                losses = parts[1]

            if row_label == "Division place":
                division_standing = row_text[0:3]

        # get table with conf standing
        conf_table = soup.find("table", {"class": "wikitable defaultcenter col2left"})
        for row in conf_table.find_all("tr"):
            cells = row.find_all(["td"])

            if (len(cells) < 5):
                continue

            if cells[1].get_text(strip=True) == "Atlanta Falcons":
                conf_standing = cells[0].get_text(strip=True)

                if ("[" in conf_standing):
                    conf_standing = conf_standing[0 : conf_standing.index("[")]

            if cells[0].get_text(strip=True) == "7":
                next_team_in_wins = cells[3].get_text(strip=True)
                next_team_in_losses = cells[4].get_text(strip=True)
                wins_away = ((int(next_team_in_wins) - int(wins)) + (int(losses) - int(next_team_in_losses))) * 0.5

        # Fetch page for team stats
        # resp = requests.get(TARGET_URL_2, timeout=15, headers=headers)
        # resp.raise_for_status()
        # soup = BeautifulSoup(resp.text, "html.parser")

        # get table with team stats
        # stats_table = soup.find("table", {"class"}: "")

                

        # set season_status field
        today = datetime.today().date()
        falcons_playoff_str = "2026-01-10"
        falcons_playoff_date = datetime.strptime(falcons_playoff_str, "%Y-%m-%d").date()
        falcons_season_str = "2026-02-08"
        falcons_season_date = datetime.strptime(falcons_season_str, "%Y-%m-%d").date()

        if (today <= falcons_playoff_date):
            season_status = "Regular Season"
        elif (today <= falcons_season_date):
            season_status = "Playoffs"
        else:
            season_status = "Season is Over"

        falcons_data = {
            "team": "Atlanta Falcons",
            "wins": wins,
            "losses": losses,
            "record_text": record_text,
            "division_standing": division_standing,
            "conf_standing": conf_standing,
            "season_status": season_status,
            "wins_away": wins_away
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
