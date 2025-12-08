import requests
import csv
from datetime import datetime

CSV_FILE = "metar_history_wsss.csv"
URL = "https://aviationweather.gov/api/data/metar?ids=WSSS&format=raw"

def fetch_metar():
    r = requests.get(URL)
    if r.status_code == 200:
        metar = r.text.strip()
        print("Fetched METAR:", metar)
        return metar
    else:
        print("Failed to fetch METAR:", r.status_code)
        return None

def append_metar(metar):
    if not metar:
        return False
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open(CSV_FILE, "a") as f:
        f.write(f"{timestamp},{metar}\n")
    print("Appended to CSV")
    return True

if __name__ == "__main__":
    metar = fetch_metar()
    append_metar(metar)
