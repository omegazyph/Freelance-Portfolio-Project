"""
Date: 2026-01-05
Script Name: hotel_price_basic_us.py
Author: omegazyph
Updated: 2026-02-15
Description: A professional Python scraping utility optimized for the US 
market. Specifically configured for UTF-8 character encoding to handle 
USD currency symbols correctly in Windows environments.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import io

# Forces the terminal to support UTF-8 encoding for the US Dollar symbol ($)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_hotel_price_us():
    # Example Target: This should be replaced with a US-based hotel URL
    target_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" 
    
    # Professional headers to mimic a US-based Windows user
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    print(f"Initializing connection to: {target_url}")

    try:
        # Performing the request with a 15-second timeout for stability
        response = requests.get(target_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This class must be updated based on the specific hotel's website structure
            price_element = soup.find("p", {"class": "price_color"})
            
            if price_element:
                # Cleaning the data and removing extra whitespace
                raw_price = price_element.get_text(strip=True)
                
                # Timestamp formatted for US Standard (MM-DD-YYYY)
                timestamp = datetime.now().strftime("%m-%d-%Y %I:%M %p")
                
                print("=========================================")
                print("US DATA EXTRACTION SUCCESSFUL")
                print(f"Timestamp: {timestamp}")
                print(f"Current Rate: {raw_price}")
                print("=========================================")
            else:
                print("Notification: Target price element not found on page.")
        else:
            print(f"Network Error: Received status code {response.status_code}")

    except Exception as error:
        print(f"A critical system error has occurred: {error}")

if __name__ == "__main__":
    get_hotel_price_us()