# ATL-sports-tracker
## Overview
Automated web scraped sports data from all your favorite Atlanta sports teams!

Built with Python, Flask, BeautifulSoup, and HTML/CSS

This site uses multiple python scripts that incorporate the BeautifulSoup library in order to web scrape relevant information for the following Atlanta sports teams:
- Atlanta Falcons
- Atlanta Hawks
- Georgia Tech Football
- Georgia Tech Basketball

The web scraping scripts are run twice a day via a GitHub Workflow.

## Features in Detail
### Web Scraping
- Use of requests, BeautifulSoup libraries to scrape data from teamrankings.com and WikiPedia for each of the teams
- Extracts team record, team standings, team statistics, and team statisitic rankings for each of the teams
- Automatically updates and maintains all data in a data.json file

### Flask Backend
- Handles routes to each of the subpages (/falcons, /hawks, etc)
- Robust load_data() function that supports error handling if JSON content is missing or inproper
- Includes API endpoint route (/api/data), which returns the full JSON dataset

### Simple, but theme-aligned Front-End UI
- Leverages HTML/CSS in order to present data in a readable format as well as incorporating color schemes and design choices to evoke a "sports" theme
- Includes page navigation buttons with interactive hover animations

## Accessing the site
### Option 1: Access via Render
The site is hosted on Render at the link below. Please note this web app is running on the free version of Render, so it may take roughly 1 minute to load
<https://atl-sports-tracker.onrender.com>  

### Option 2: Run Locally
Run these commands in your terminal: 
1. Clone repository
```shell
    git clone https://github.com/YOUR_USERNAME/atl-sports-tracker.git
    d atl-sports-tracker
```
2. Set up virtual environment
```shell
    python3 -m venv venv
    source venv/bin/activate   # if on macOS/Linux
    venv\Scripts\activate      # if on Windows
```
3. Install dependencies
```shell
    pip install -r requirements.txt
```
4. Run all scrapers
```shell
    python scrapers/scraper_falcons.py
    python scrapers/scraper_hawks.py
    python scrapers/scraper_gt.py
    python scrapers/scraper_gt_bb.py
```
5. Run local server
```shell
    python app.py
```
6. Access site
<http://127.0.0.1:5000>
