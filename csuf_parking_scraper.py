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
        response = requests.get(URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Failed to fetch data: HTTP {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for table data rows on the CSUF parking site
        rows = soup.find_all('tr')
        if not rows:
            # Fallback if they use general tables or generic divs
            rows = soup.find_all(class_="parking-lot")

        csv_file = "csuf_semester_parking.csv"
        file_exists = os.path.isfile(csv_file)
        
        scraped_any = False
        
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Scrape_Timestamp", "Location_Name", "Available_Spots"])
            
            # Simple text parsing fallback that loops rows and finds text numbers
            for row in rows:
                text_content = row.get_text(separator=" ").strip()
                if any(structure in text_content for structure in ["Nutwood", "State College", "Eastside", "S8", "S10"]):
                    # Clean up space characters to log cleanly
                    cleaned_line = " ".join(text_content.split())
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cleaned_line])
                    scraped_any = True
                    
        if scraped_any:
            print(f"Parking data successfully logged at {datetime.now()}")
        else:
            # Fallback block to capture raw content structure if layouts mismatch
            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                main_content = soup.get_text(separator=" ").strip()
                summary = " ".join(main_content.split())[:200]
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Raw snapshot: {summary}"])
            print("Logged web page snapshot data.")
            
    except Exception as e:
        print(f"An extraction error occurred: {e}")

if __name__ == "__main__":
    scrape_csuf_parking()
