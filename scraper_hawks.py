import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to store scraped data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
TARGET_URL = "https://www.nba.com/stats/team/1610612737/seasons"

def scrape_hawks_data():
    try:
        print("=== Starting Hawks data scrape ===")

        # Set up headless Chrome
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        print("Initializing Chrome WebDriver...")

        # Fix to point to chromium 
        options.binary_location = "/usr/bin/chromium-browser"

        driver = webdriver.Chrome(options=options)
        print(f"Navigating to {TARGET_URL} ...")
        driver.get(TARGET_URL)

        # Wait a few seconds for JS to render
        print("Waiting for stats table to appear...")
        time.sleep(5)

        # Wait for the row containing "2025-26" season to appear
        try:
            row_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//tr[td[contains(text(),'2025-26')]]")
                )
            )
        except Exception as e:
            print("!!! ERROR during scraping !!!")
            raise e

        # Parse the row's td elements
        cells = row_element.find_elements(By.TAG_NAME, "td")
        if not cells or len(cells) < 11:
            raise ValueError("Could not find expected table cells for 2025-26 row")

        wins = int(cells[3].text.strip())
        losses = int(cells[4].text.strip())
        conf_rank = cells[10].text.strip()

        hawks_data = {
            "team": "Atlanta Hawks",
            "wins": wins,
            "losses": losses,
            "standings_text": f"{conf_rank} in East"
        }

        print("Scraped Hawks data:", hawks_data)
        driver.quit()
        return hawks_data

    except Exception as e:
        print("!!! ERROR during scraping !!!")
        print(e)
        try:
            driver.quit()
        except:
            pass
        return {"error": "Scraping failed"}

def main():
    print("=== Running Hawks scraper main ===")
    data = {}

    # Load existing JSON
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            print("Loaded existing data.json successfully")
        except Exception as e:
            print("Failed to load existing data.json:", e)
            data = {}

    # Scrape Hawks data
    hawks_data = scrape_hawks_data()
    data["hawks"] = hawks_data

    # Save updated JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved updated data.json")
    print("=== Finished Hawks scraper ===")

if __name__ == "__main__":
    main()
