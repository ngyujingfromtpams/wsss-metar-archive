import requests
from datetime import datetime
import os
import sys

# ---------------- CONFIG ----------------
URL = "https://aviationweather.gov/api/data/metar?ids=WSSS&format=raw"
CSV_FILE = "metar_history_wsss.csv"
# ----------------------------------------

def fetch_metar():
    """Fetch latest METAR from aviationweather.gov API."""
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            return r.text.strip()
        print(f"Failed to fetch METAR: HTTP {r.status_code}")
        return None
    except Exception as e:
        print(f"Error fetching METAR: {e}")
        return None

def append_metar(metar):
    """Append METAR to CSV if it's not a duplicate. Return True if new METAR added."""
    if metar is None:
        return None

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Create CSV if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w") as f:
            f.write("timestamp,metar\n")

    # Avoid duplicates
    with open(CSV_FILE, "r") as f:
        existing = f.read().splitlines()
    if any(metar in line for line in existing):
        print("Duplicate METAR — skipped")
        return None  # Nothing appended

    # Append new METAR
    with open(CSV_FILE, "a") as f:
        f.write(f"{timestamp},{metar}\n")
    print("Saved METAR:", metar)
    return True  # New METAR appended

    if __name__ == "__main__":
        metar = fetch_metar()
        appended = append_metar(metar)
    
        if appended:
            print("New METAR appended — ready to commit.")
        else:
            print("No new METAR — nothing to commit.")
    
        # Always exit 0 so GitHub Actions doesn't mark as failure
        sys.exit(0)
