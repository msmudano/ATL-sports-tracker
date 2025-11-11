import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
TARGET_URL = "https://www.nba.com/stats/team/1610612737/seasons"

def scrape_hawks():
    try:
        # Set up headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(TARGET_URL)

        # Wait up to 15 seconds for the table to appear
        wait = WebDriverWait(driver, 15)
        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.Crom_table__p1iZz"))
        )

        # Parse table rows
        hawks_data = None
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "2025-26":
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

        driver.quit()

        if not hawks_data:
            print("Error: Could not find Hawks data for 2025-26 season.")
            return None

        # Load existing JSON
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        # Update Hawks section
        data["hawks"] = hawks_data

        # Write to data.json
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Scraped Hawks data:", hawks_data)
        return hawks_data

    except Exception as e:
        print("Unexpected error:", e)
        return None

if __name__ == "__main__":
    scrape_hawks()