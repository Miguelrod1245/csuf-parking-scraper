import csv
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://www.fullerton.edu"  # Use the verified canonical hostname
CSV_FILE = "csuf_semester_parking.csv"


def write_csv_row(timestamp, data):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Scrape_Timestamp", "Raw_Web_Data"])

        writer.writerow([timestamp, data])


def scrape_csuf_parking():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36"
        )
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text(separator=" ").strip()
        cleaned_text = " ".join(page_text.split())

        write_csv_row(timestamp, cleaned_text)
        print(f"Parking data successfully logged at {timestamp}")

    except requests.exceptions.RequestException as error:
        write_csv_row(timestamp, f"Request Error: {error}")
        print(f"Request failed: {error}")
        raise

    except Exception as error:
        write_csv_row(timestamp, f"Script Error: {error}")
        print(f"An extraction error occurred: {error}")
        raise


if __name__ == "__main__":
    scrape_csuf_parking()
