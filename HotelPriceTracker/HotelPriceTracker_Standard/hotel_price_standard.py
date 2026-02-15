"""
Date: 2026-01-05
Script Name: hotel_price_standard.py
Author: omegazyph
Updated: 2026-02-15
Description: Multi-target hotel price scraper with CSV logging. 
Supports persistent data storage and Excel/OpenOffice compatibility.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import sys
import io

# Fix Windows terminal encoding for currency symbols
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Global path setup
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, "hotel_list.txt")
output_file = os.path.join(base_dir, "price_history.csv")

def track_prices():
    # Setup default input file if missing
    if not os.path.exists(input_file):
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html\n")
            f.write("https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html")
        print(f"Created {input_file}. Add URLs to proceed.")
        return

    # Load targets
    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    print(f"--- Running tracker on {len(urls)} targets ---")

    results = []
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'html.parser')
                
                # Target price element
                price_tag = soup.find("p", {"class": "price_color"})
                
                if price_tag:
                    raw_price = price_tag.get_text(strip=True)
                    
                    # Numeric extraction for cleaner data processing
                    price = "".join(c for c in raw_price if c.isdigit() or c == '.')
                    
                    timestamp = datetime.now().strftime("%m-%d-%Y %I:%M %p")
                    
                    results.append({
                        "Date": timestamp,
                        "URL": url,
                        "Price": price
                    })
                    print(f"Captured: {price} | {url[:40]}")
            else:
                print(f"Error: {url} returned status {res.status_code}")
                
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    if results:
        save_to_log(output_file, results)

def save_to_log(path, data):
    # Detect if we need to write headers
    exists = os.path.isfile(path)
    
    try:
        # Use utf-8-sig for automatic Excel/OpenOffice encoding detection
        with open(path, "a", newline="", encoding="utf-8-sig") as f:
            fields = ["Date", "URL", "Price"]
            writer = csv.DictWriter(f, fieldnames=fields, dialect='excel')

            if not exists:
                writer.writeheader()
            
            writer.writerows(data)
            
        print(f"--- Log updated: {path} ---")
        
    except PermissionError:
        print("\n!!! Access Denied: Close the CSV file in OpenOffice/Excel before running. !!!\n")

if __name__ == "__main__":
    track_prices()