import pytest
from pricewatch.scraper import ScrapeError, parse_price, parse_product_html, validate_amazon_url

HTML = """
<html><span id="productTitle">Test Headphones</span>
<span class="a-price"><span class="a-offscreen">$129.99</span></span></html>
"""

def test_parse_price():
    assert parse_price("$1,299.99") == 1299.99

def test_parse_product_html():
    item = parse_product_html(HTML, "https://www.amazon.ca/dp/TEST")
    assert item.title == "Test Headphones"
    assert item.price == 129.99
    assert item.currency == "CAD"

def test_rejects_non_amazon_url():
    with pytest.raises(ValueError):
        validate_amazon_url("https://example.com/item")

def test_missing_price_raises():
    with pytest.raises(ScrapeError):
        parse_product_html('<span id="productTitle">Test</span>', "https://amazon.ca/dp/TEST")
