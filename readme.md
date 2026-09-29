# PriceWatch

An e-commerce **price monitoring and historical price intelligence dashboard** built with Python, Streamlit, Beautiful Soup, Plotly and SQLite.

PriceWatch tracks Amazon product prices over time, stores observations, compares current prices with recorded history and highlights when a user-defined target price has been reached.

## Features

- Track multiple Amazon Canada and Amazon US product URLs
- Extract product title and current displayed price
- SQLite-backed persistent price history
- User-defined target prices
- Current, minimum, maximum and average recorded price
- Percentage difference from historical average
- Interactive historical price charts
- Target-price reference line
- URL validation and explicit retrieval/parsing errors
- Modular scraper, service, analytics and storage layers
- Unit tests for parsing, analytics and persistence
- GitHub Actions continuous integration
- Streamlit dashboard

## Architecture

```text
Amazon product page
       |
       v
pricewatch/scraper.py
 validation + parsing
       |
       v
pricewatch/service.py
       |
   +---+---+
   |       |
   v       v
storage  analytics
SQLite   price intelligence
   |       |
   +---+---+
       |
       v
  dashboard.py
Streamlit + Plotly
```

## Project structure

```text
.
├── pricewatch/
│   ├── analytics.py
│   ├── models.py
│   ├── scraper.py
│   ├── service.py
│   └── storage.py
├── tests/
│   ├── test_analytics.py
│   ├── test_scraper.py
│   └── test_storage.py
├── .github/workflows/ci.yml
├── dashboard.py
├── pyproject.toml
└── requirements.txt
```

## Run locally

```bash
git clone https://github.com/thato2073-svg/amazon-price-tracker.git
cd amazon-price-tracker
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run dashboard.py
```

## Testing

```bash
pytest -q
```

## Design notes

PriceWatch intentionally separates HTTP retrieval from HTML parsing so parsing behavior can be tested with local fixtures instead of repeatedly requesting a live retailer page.

The application stores observations in SQLite rather than a flat CSV, allowing multiple products and historical queries while keeping local setup simple.

## Limitations and responsible use

- Amazon can change its HTML structure at any time, which may require parser updates.
- Automated requests can be rate-limited or blocked. PriceWatch does not attempt to defeat CAPTCHAs or access controls.
- Availability, coupons, shipping, taxes, regional pricing and personalized offers may not be represented by the displayed scraped price.
- Use responsibly and comply with applicable website terms and policies.
- Price history begins when a product is first tracked by the user.

## Roadmap

- Optional email notifications
- Scheduled checks in an appropriate hosted environment
- Additional retailer adapters
- Product-level price-drop event timeline

## Author

**Thato Olayinka**  
Computing Science + Economics, University of Alberta
