# Amazon Price Tracker 🏷️

A Python web scraper that monitors the price of **Jacked Factory Creatine** (or any Amazon product) and logs the data to a CSV file. It uses custom headers to mimic a real browser, helping to bypass Amazon's anti-bot security.



## How It Works
1. **Request:** Sends an HTTP request to Amazon using a "Human-Mimic" User-Agent.
2. **Scrape:** Uses `BeautifulSoup` to find the specific HTML tags for Product Title and Price.
3. **Log:** Saves the current timestamp and price into `price_history.csv`.
4. **Alert:** Prints a special notification to the terminal if the price drops below a set target.

##  Tech Stack
* **Language:** Python 3.14
* **Libraries:** `requests`, `beautifulsoup4`
* **Storage:** CSV (Comma Separated Values)

##  Installation & Usage
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/amazon-price-tracker.git](https://github.com/thato2073-svg/amazon-price-tracker.git)