import requests
from bs4 import BeautifulSoup

print("--- STARTING HUMAN-MIMIC SCRAPER ---")

URL = "https://www.amazon.ca/Jacked-Factory-Creatine-Monohydrate-Powder/dp/B08DH161T6/"

# These headers tell Amazon you are a real Chrome browser
headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# ... (keep your URL and headers the same as before) ...

def get_amazon_data():
    session = requests.Session()
    try:
        response = session.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id="productTitle")
        
        if title:
            name = title.get_text().strip()[:40] # Shorten name
            price_whole = soup.find(class_="a-price-whole")
            price_fraction = soup.find(class_="a-price-fraction")
            
            # Clean the price string
            price_val = price_whole.get_text().replace('.', '').strip() if price_whole else "0"
            cents_val = price_fraction.get_text().strip() if price_fraction else "00"
            final_price = f"{price_val}.{cents_val}"
            
            # --- NEW: SAVE TO CSV ---
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open('price_history.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # If you want to add a header row manually later, you can.
                writer.writerow([current_time, name, final_price])
            
            print(f"Logged: {current_time} | ${final_price}")
            # ------------------------
            
        else:
            print("Failed to find data this time.")
    except Exception as e:
        print(f"Error: {e}")

get_amazon_data()