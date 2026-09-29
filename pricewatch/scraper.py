from __future__ import annotations
import re
from datetime import datetime, timezone
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from pricewatch.models import ProductSnapshot

class ScrapeError(RuntimeError):
    pass

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PriceWatch/2.0; +educational-price-monitor)",
    "Accept-Language": "en-CA,en;q=0.9",
}

def validate_amazon_url(url: str) -> None:
    host = urlparse(url).hostname or ""
    if host not in {"amazon.ca", "www.amazon.ca", "amazon.com", "www.amazon.com"}:
        raise ValueError("PriceWatch currently supports Amazon Canada and Amazon US URLs.")

def parse_price(text: str) -> float:
    cleaned = re.sub(r"[^0-9.,]", "", text).strip()
    if not cleaned:
        raise ScrapeError("Price text did not contain a numeric value.")
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        parts = cleaned.split(",")
        cleaned = ".".join(parts) if len(parts[-1]) == 2 else "".join(parts)
    return float(cleaned)

def parse_product_html(html: str, url: str) -> ProductSnapshot:
    soup = BeautifulSoup(html, "html.parser")
    title_node = soup.select_one("#productTitle")
    price_node = (
        soup.select_one(".a-price .a-offscreen")
        or soup.select_one("#priceblock_ourprice")
        or soup.select_one("#priceblock_dealprice")
    )
    if not title_node:
        raise ScrapeError("Product title was not found. Amazon may have changed the page.")
    if not price_node:
        raise ScrapeError("Product price was not found. The item may be unavailable.")
    text = price_node.get_text(" ", strip=True)
    currency = "CAD" if "CDN" in text or "$" in text and ".ca" in url else "USD"
    return ProductSnapshot(
        url=url,
        title=title_node.get_text(" ", strip=True),
        price=parse_price(text),
        currency=currency,
        captured_at=datetime.now(timezone.utc),
    )

def fetch_product(url: str) -> ProductSnapshot:
    validate_amazon_url(url)
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ScrapeError("Unable to retrieve the product page.") from exc
    return parse_product_html(response.text, url)
