import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_hawks_data():
    print("=== Starting Hawks data scrape ===")

    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.binary_location = "/usr/bin/chromium-browser"

    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)

    url = "https://www.nba.com/stats/team/1610612737/seasons"
    print(f"Navigating to {url} ...")
    driver.get(url)

    try:
        # Wait for main table to load
        print("Waiting for stats table to appear...")
        table = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        print("Stats table found!")

        # Grab headers
        headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, "thead th")]
        print(f"Found headers: {headers}")

        # Grab rows
        rows = []
        for tr in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
            cells = [td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")]
            if cells:
                rows.append(dict(zip(headers, cells)))

        print(f"Collected {len(rows)} rows of data")

        driver.quit()
        return rows

    except Exception as e:
        print("!!! ERROR during scraping !!!")
        print(traceback.format_exc())
        driver.quit()
        return None


def save_data_to_json(new_data):
    print("=== Updating data.json ===")
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            print("Loaded existing data.json successfully")
    except FileNotFoundError:
        print("data.json not found, creating a new one...")
        data = {}

    data["hawks"] = new_data if new_data else {"error": "Scraping failed"}

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
        print("Saved updated data.json")

def main():
    print("=== Running Hawks scraper main ===")
    hawks_data = scrape_hawks_data()
    save_data_to_json(hawks_data)
    print("=== Finished Hawks scraper ===")

if __name__ == "__main__":
    main()
