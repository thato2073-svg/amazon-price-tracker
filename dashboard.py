import pandas as pd
import plotly.express as px
import streamlit as st

from pricewatch.analytics import price_summary
from pricewatch.demo import demo_history
from pricewatch.scraper import ScrapeError
from pricewatch.service import check_product
from pricewatch.storage import history, products

st.set_page_config(page_title="PriceWatch", page_icon="🏷️", layout="wide")
st.title("PriceWatch")
st.caption("Track Amazon product prices, history and target-price opportunities.")

demo_mode = st.toggle("Demo Mode", value=False, help="Explore PriceWatch with synthetic sample history. Demo data is never saved as real observations.")

with st.sidebar:
    st.header("Track a product")
    url = st.text_input("Amazon product URL", placeholder="https://www.amazon.ca/...")
    target = st.number_input("Target price (optional)", min_value=0.0, value=0.0, step=1.0)
    if st.button("Check & save price", type="primary", use_container_width=True):
        try:
            snapshot, reached = check_product(url.strip(), target if target > 0 else None)
            st.success(f"Saved {snapshot.title[:45]} at {snapshot.currency} {snapshot.price:.2f}")
            if reached:
                st.balloons()
                st.success("Target price reached.")
        except (ValueError, ScrapeError) as exc:
            st.error(str(exc))

if demo_mode:
    st.info("DEMO MODE: The history below is synthetic sample data for demonstrating PriceWatch. It is not scraped Amazon history.")
    hist = demo_history()
    summary = price_summary(hist)
    demo_target = 105.00
    st.subheader("Demo: Wireless Gaming Mouse")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Current", f"CAD {summary['current']:.2f}")
    c2.metric("Recorded low", f"CAD {summary['low']:.2f}")
    c3.metric("Recorded high", f"CAD {summary['high']:.2f}")
    c4.metric("Average", f"CAD {summary['average']:.2f}")
    c5.metric("vs average", f"{summary['change_from_average']:.1%}")
    fig = px.line(hist, y="price", markers=True, title="Synthetic 60-day price history")
    fig.add_hline(y=demo_target, line_dash="dash", annotation_text="Demo target")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Synthetic demonstration only. Switch Demo Mode off to track live Amazon products.")
    st.stop()

catalog = products()
if catalog.empty:
    st.info("Add an Amazon product from the sidebar to start building price history.")
    st.stop()

st.subheader("Tracked products")
display = catalog[["title", "currency", "current_price", "target_price"]].copy()
display.columns = ["Product", "Currency", "Current price", "Target"]
st.dataframe(display, use_container_width=True, hide_index=True)

labels = {row.title: row.url for row in catalog.itertuples()}
selected_title = st.selectbox("Explore product", list(labels))
selected_url = labels[selected_title]
hist = history(selected_url)
summary = price_summary(hist)
row = catalog[catalog["url"] == selected_url].iloc[0]

st.subheader(selected_title)
c1, c2, c3, c4, c5 = st.columns(5)
currency = row["currency"]
c1.metric("Current", f"{currency} {summary['current']:.2f}")
c2.metric("Recorded low", f"{currency} {summary['low']:.2f}")
c3.metric("Recorded high", f"{currency} {summary['high']:.2f}")
c4.metric("Average", f"{currency} {summary['average']:.2f}")
c5.metric("vs average", f"{summary['change_from_average']:.1%}")

if not hist.empty:
    fig = px.line(hist, y="price", markers=True, title="Price history")
    target_price = row["target_price"]
    if target_price is not None and not pd.isna(target_price):
        fig.add_hline(y=float(target_price), line_dash="dash", annotation_text="Target")
    st.plotly_chart(fig, use_container_width=True)

st.caption("PriceWatch stores observations locally in SQLite. Amazon page structure and availability can change, so retrieval may occasionally fail.")
