import requests
from bs4 import BeautifulSoup
import json
import os

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
# URL to scrape
TARGET_URL = "https://www.nba.com/stats/team/1610612737/seasons"

def scrape_hawks():
    try:
        # Fetch page
        resp = requests.get(TARGET_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # table with record and standings
        record_table = soup.find("table", {"class": "Crom_table__p1iZz"})
        if not record_table:
            print("Error: Could not find the Hawks record or standings on the page.")
            return None
        
        # parse wins, losses, and standings from table
        hawks_data = None
        rows = record_table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if (cells[0].text.strip() == "2025-26"):
                wins = int(cells[3].text.strip())
                losses = int(cells[4].text.strip())
                conf_rank = cells[10].text.strip()
                hawks_data = {
                    "team": "Atlanta Hawks",
                    "wins": wins,
                    "losses": losses,
                    "standings_text": f"{conf_rank} in East"
                }
                break

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
        data["hawks"] = hawks_data

        # Write to data.json
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Scraped Falcons data:", hawks_data)
        return hawks_data

    except requests.RequestException as e:
        print("Network error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

if __name__ == "__main__":
    scrape_hawks()
