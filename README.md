# Supermarket Sales Pulse

A Streamlit dashboard for a **supermarket store manager**, built as Part 1 of the
BANA409 Assignment 4 Data App exercise.

- **Dataset:** [Supermarket sales](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales) (Kaggle, 1,000 transactions, Jan–Mar 2019)
- **App:** `app.py` (Streamlit), reads `sales_daily.csv` and `sales_product_line.csv`

---

## Step 1 — Dataset and decision-maker

**Dataset.** The Kaggle "Supermarket sales" dataset records 1,000 checkout transactions
from three branches (A, B, C) of a supermarket chain, covering January to March 2019.
Each row is one receipt, with the branch, city, customer type, product line, quantities,
total paid, and customer rating. Because the dashboard only needs sales *totals*, I
aggregated the 1,000 receipts into two small files in a short prep step:

- `sales_daily.csv` — revenue and transaction count per day per branch (263 rows)
- `sales_product_line.csv` — revenue and transaction count per branch and product line (18 rows)

**Decision-maker.** The **store manager** of one branch — the person responsible for
day-to-day staffing, ordering stock, and running in-store promotions.

## Step 2 — Justify the dashboard

1. **Who, and how often?** The store manager, every morning, with a fuller review each Monday.
2. **What decision does it support?** *"If the store manager sees a product line's daily
   revenue fall below its recent average, or the branch's daily total dip sharply, they
   will adjust staffing, reorder that line, or run a promotion."*
3. **What do they do today?** They pull the previous day's sales out of the point-of-sale
   system into a spreadsheet by hand — time-consuming, and it is easy to miss a slowing
   product line until it is too late to react.
4. **Why a dashboard?** The same questions ("how did we do yesterday? which lines are
   moving?") come up every single day; a dashboard that refreshes itself answers them in
   five seconds instead of a manual spreadsheet.

## Step 3 — Decide what matters

**Headline numbers (top).**

- **Total revenue** — the first "are we on track?" number.
- **Transactions** — foot traffic.
- **Average transaction value** — basket size; with transactions, it explains revenue.

**Supporting charts (middle).**

- **Daily revenue** (line chart) — whether revenue is trending up or down, and which days fell short.
- **Revenue by product line** (bar chart) — which lines drive (or drag) revenue, so the manager knows what to reorder or promote.

**Filters.** A **branch** selector (so the manager sees their own store) and a **date
range** (to zoom into a week or a single bad day). Nothing else.

**What I chose *not* to show, and why.**

1. **Customer gender and customer type.** Interesting in the EDA, but a store manager
   cannot act on the gender or member/non-member split of a day's sales — it changes no
   staffing, ordering, or promotion decision.
2. **Payment method.** Also interesting, but the payment mix does not change any
   store-level decision.

**What could mislead, and how I handle it.**

- The data covers only **three months (Jan–Mar 2019)**, so there is no year-over-year
  comparison and no holiday seasonality. The dashboard states the period explicitly so the
  manager does not read a three-month pattern as a full year.
- The raw file's **"gross margin percentage" is identical (4.76%) on every row**, so it is
  a constant, not a signal. I deliberately do not show a profit/margin KPI because it would
  look meaningful while carrying no information.
- "Total" includes the 5% tax, so the headline "revenue" is gross sales, not net income.

**Order.** Headline numbers at the top (answer *"is anything wrong right now?"*), then the
trend chart and the product-line breakdown (answer *"why?"*). No detail table — the manager
does not need to inspect individual receipts on this dashboard.

## Step 4 — Refresh frequency

1. **How often should the data refresh?** **Nightly**, from the point-of-sale system. Sales
   change continuously, but the manager acts on them at most once a day.
2. **How often should someone review it?** **Every morning** for a quick check, plus a fuller
   review **every Monday morning** when weekly staffing and restock orders are placed.
3. **What to track, and what should trigger action?** Track daily revenue per product line;
   if a top line's daily revenue falls below 70% of its four-week average, the manager should
   check stock and consider a promotion the same day.
4. **What does stale data cost?** A day's lag hides a sudden drop or a stock-out, so a hot
   product can sit out of stock for a full day of lost sales before anyone notices.
