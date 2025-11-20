import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL_1 = "https://en.wikipedia.org/wiki/2025_Georgia_Tech_Yellow_Jackets_football_team"
TARGET_URL_2 = "https://www.teamrankings.com/college-football/team/georgia-tech-yellow-jackets/stats"

# header needed to scrape wikipedia
headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_gt():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL_1, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get table with record and ranking info
        record_table = soup.find("table", {"class": "infobox vevent"})
        if not record_table:
            print("Error: Could not find the Georgia Tech record or standings on this page.")
        
        # get CFP ranking, record, wins, losses, conference record
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

        # get conference standings
        standings = 0
        for row in standings_table.find_all("tr"):
            if row.find("td") == None:
                continue

            standings += 1
            row_value = row.find("td").find("a")
            if (row_value.get_text(strip=True) == "Georgia Tech"):
                break

        # Fetch page for team stats
        resp = requests.get(TARGET_URL_2, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # get tables with team stats
        stats_tables = soup.find_all("table", {"class": "tr-table scrollable"})
        overall_stats_table = stats_tables[0]
        rushing_stats_table = stats_tables[1]
        passing_stats_table = stats_tables[2]

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

        # get rush yds/game, oppoenent rush yds/game
        for row in rushing_stats_table.find_all("tr"):
            cells = row.find_all(["td"])

            if (len(cells) < 4):
                continue

            if cells[0].get_text(strip=True) == "Rush Yards/Game":
                rpg = cells[1].get_text(strip=True).split("(")[0]
                rpg_rank = cells[1].get_text(strip=True).split("(")[1][:-1]

            if cells[2].get_text(strip=True) == "Opp Rush Yards/Game":
                opp_rpg = cells[3].get_text(strip=True).split("(")[0]
                opp_rpg_rank = cells[3].get_text(strip=True).split("(")[1][:-1]

        # get pass yds/game, opponent pass yds/game
        for row in passing_stats_table.find_all("tr"):
            cells = row.find_all(["td"])

            if (len(cells) < 4):
                continue

            if cells[0].get_text(strip=True) == "Pass Yards/Game":
                papg = cells[1].get_text(strip=True).split("(")[0]
                papg_rank = cells[1].get_text(strip=True).split("(")[1][:-1]

            if cells[2].get_text(strip=True) == "Opp Pass Yards/Game":
                opp_papg = cells[3].get_text(strip=True).split("(")[0]
                opp_papg_rank = cells[3].get_text(strip=True).split("(")[1][:-1]
            

        # set season_ongoing field
        today = datetime.today().date()
        gt_playoff_str = "2026-11-29"
        gt_playoff_date = datetime.strptime(gt_playoff_str, "%Y-%m-%d").date()
        gt_season_str = "2026-01-19"
        gt_season_date = datetime.strptime(gt_season_str, "%Y-%m-%d").date()

        if (today <= gt_playoff_date):
            season_status = "Regular Season"
        elif (today <= gt_season_date):
            season_status = "12 Team Playoff / Bowl Season"
        else:
            season_status = "Season is Over"

        gt_data = {
            "team": "Georgia Tech Yellow Jackets",
            "wins": wins,
            "losses": losses,
            "record_text": record_text,
            "ranking": ranking,
            "conf_record": conf_record_text,
            "conf_standings": standings,
            "season_status": season_status,
            "ppg": ppg,
            "opp_ppg": opp_ppg,
            "ppg_rank": ppg_rank,
            "opp_ppg_rank": opp_ppg_rank,
            "rpg": rpg,
            "opp_rpg": opp_rpg,
            "rpg_rank": rpg_rank,
            "opp_rpg_rank": opp_rpg_rank,
            "papg": papg,
            "opp_papg": opp_papg,
            "papg_rank": papg_rank,
            "opp_papg_rank": opp_papg_rank
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
