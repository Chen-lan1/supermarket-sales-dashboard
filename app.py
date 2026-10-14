import pandas as pd
import streamlit as st

st.set_page_config(page_title="Supermarket Sales Pulse", page_icon="🛒", layout="wide")


@st.cache_data
def load_data():
    daily = pd.read_csv("sales_daily.csv")
    daily["Date"] = pd.to_datetime(daily["Date"])
    by_line = pd.read_csv("sales_product_line.csv")
    return daily, by_line


daily, by_line = load_data()

# ---- Title ----
st.title("🛒 Supermarket Sales Pulse")
st.caption(
    "For the store manager: watch daily revenue and the product-line mix to decide "
    "staffing, restocking, and promotions."
)

# ---- Filters ----
col1, col2 = st.columns(2)
with col1:
    branch = st.selectbox(
        "Branch", ["All branches"] + sorted(daily["Branch"].unique().tolist())
    )
with col2:
    dmin, dmax = daily["Date"].min().date(), daily["Date"].max().date()
    date_range = st.date_input(
        "Date range", value=(dmin, dmax), min_value=dmin, max_value=dmax
    )

# Apply the branch filter.
d = daily.copy()
if branch != "All branches":
    d = d[d["Branch"] == branch]
p = by_line.copy()
if branch != "All branches":
    p = p[p["Branch"] == branch]

# Apply the date-range filter (daily file only; product-line totals are for the period).
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    d = d[(d["Date"].dt.date >= start) & (d["Date"].dt.date <= end)]

# ---- Headline metrics ----
revenue = d["revenue"].sum()
orders = d["transactions"].sum()
avg_basket = revenue / orders if orders else 0.0

m1, m2, m3 = st.columns(3)
m1.metric("Total revenue", f"${revenue:,.0f}")
m2.metric("Transactions", f"{orders:,}")
m3.metric("Avg. transaction", f"${avg_basket:,.2f}")

st.divider()

# ---- Supporting charts ----
st.subheader("Daily revenue")
st.line_chart(d.groupby("Date")["revenue"].sum())

st.subheader("Revenue by product line")
st.bar_chart(p.groupby("Product line")["revenue"].sum().sort_values())

# ---- Data period / refresh note ----
st.caption(
    "Data: Jan–Mar 2019, Kaggle 'Supermarket sales' snapshot (aggregated from 1,000 "
    "transactions). In production this would refresh nightly from the point-of-sale "
    "system; the store manager reviews it every Monday morning for weekly staffing "
    "and ordering decisions."
)
