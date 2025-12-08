import requests
from datetime import datetime
import os

# METAR API URL for WSSS
URL = "https://aviationweather.gov/api/data/metar?ids=WSSS&format=raw"

# File to store METAR
CSV_FILE = "metar_history_wsss.csv"

def fetch_metar():
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            return r.text.strip()
        return None
    except:
        return None

def append_metar(metar):
    if metar is None:
        return

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Avoid duplicates
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as f:
            existing = f.read().splitlines()
        if any(metar in line for line in existing):
            print("Duplicate METAR — skipped")
            return

    with open(CSV_FILE, "a") as f:
        f.write(f"{timestamp},{metar}\n")
    print("Saved METAR:", metar)
