import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL_1 = "https://en.wikipedia.org/wiki/2025%E2%80%9326_Atlanta_Hawks_season"
TARGET_URL_2 = "https://www.teamrankings.com/nba/team/atlanta-hawks/stats"

# header needed to scrape wikipedia
headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_hawks():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL_1, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get table with record and standings info
        record_table = soup.find("table", {"class": "infobox vcard"})
        if not record_table:
            print("Error: Could not find the Hawks record or standings on this page.")
        
        # get record, wins, losses, conference standings, division standing
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
                losses = parts[1].split(" ")[0]

            if row_label == "Place":
                standings_text = row_text
                split_standings = standings_text.split(':')
                conf_standings = (split_standings[2])[1:4]
                division_standings = (split_standings[1])[1:4]
        
        # Fetch page for team stats
        resp = requests.get(TARGET_URL_2, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get tables with team stats
        stats_tables = soup.find_all("table", {"class": "tr-table scrollable"})
        overall_stats_table = stats_tables[0]
        shooting_stats_table = stats_tables[1]

        # get points/game, opponent points/game
        for row in overall_stats_table.find_all("tr"):
            cells = row.find_all(["td"])

            if (len(cells) < 4):
                continue

            if cells[0].get_text(strip=True) == "Points/Game":
                ppg = cells[1].get_text(strip=True).split("(")[0]
                ppg_rank = cells[1].get_text(strip=True).split("(")[1][:-1]

            if cells[2].get_text(strip=True) == "Opp Points/Game":
                opp_ppg = cells[3].get_text(strip=True).split("(")[0]
                opp_ppg_rank = cells[3].get_text(strip=True).split("(")[1][:-1]

        # get shooting percentage, opponent shooting percentage
        for row in shooting_stats_table.find_all("tr"):
            cells = row.find_all(["td"])

            if (len(cells) < 4):
                continue

            if cells[0].get_text(strip=True) == "Shooting %":
                sppg = cells[1].get_text(strip=True).split("(")[0]
                sppg_rank = cells[1].get_text(strip=True).split("(")[1][:-1]

            if cells[2].get_text(strip=True) == "Opp Shooting %":
                opp_sppg = cells[3].get_text(strip=True).split("(")[0]
                opp_sppg_rank = cells[3].get_text(strip=True).split("(")[1][:-1]

        # set season_ongoing field
        today = datetime.today().date()
        hawks_playoff_str = "2026-04-12"
        hawks_playoff_date = datetime.strptime(hawks_playoff_str, "%Y-%m-%d").date()
        hawks_season_str = "2026-06-30"
        hawks_season_date = datetime.strptime(hawks_season_str, "%Y-%m-%d").date()
        if (today <= hawks_playoff_date):
            season_status = "Regular Season"
        elif (today <= hawks_season_date):
            season_status = "Playoffs"
        else:
            season_status = "Season is Over"

        hawks_data = {
            "team": "Atlanta Hawks",
            "wins": wins,
            "losses": losses,
            "record_text": record_text,
            "standings_text": standings_text,
            "conf_standings": conf_standings,
            "division_standings": division_standings,
            "season_status": season_status,
            "ppg": ppg,
            "opp_ppg": opp_ppg,
            "ppg_rank": ppg_rank,
            "opp_ppg_rank": opp_ppg_rank,
            "sppg": sppg,
            "opp_sppg": opp_sppg,
            "sppg_rank": sppg_rank,
            "opp_sppg_rank": opp_sppg_rank
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

        # Update only the Hawks section
        data["hawks"] = hawks_data

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
