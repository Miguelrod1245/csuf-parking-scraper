import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

URL = "https://fullerton.edu"

def scrape_csuf_parking():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=15)
        
        csv_file = "csuf_semester_parking.csv"
        file_exists = os.path.isfile(csv_file)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Scrape_Timestamp", "Raw_Web_Data"])
            
            if response.status_code != 200:
                writer.writerow([timestamp, f"Failed to fetch data: HTTP {response.status_code}"])
                print(f"HTTP Error {response.status_code}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Grabs ALL text from the page, removes excess spaces, and cleans it up
            page_text = soup.get_text(separator=" ").strip()
            cleaned_text = " ".join(page_text.split())
            
            # Save the text directly to the CSV
            writer.writerow([timestamp, cleaned_text])
                
        print(f"Parking data successfully logged at {timestamp}")
        
    except Exception as e:
        # If an error happens, write the error to the CSV so a file is ALWAYS created
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not os.path.isfile(csv_file):
                writer.writerow(["Scrape_Timestamp", "Raw_Web_Data"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Script Error: {str(e)}"])
        print(f"An extraction error occurred: {e}")

if __name__ == "__main__":
    scrape_csuf_parking()
