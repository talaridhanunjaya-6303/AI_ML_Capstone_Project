# Data Pipeline Module

## Project Overview

This module scrapes book data from https://books.toscrape.com/, cleans the data, converts GBP prices to INR using a fixed exchange rate, stores the data in a SQLite database, executes SQL queries, and demonstrates data retrieval using both SQL and Pandas.

---

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite

---

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
python scraper.py
```

---

## Data Cleaning

The following cleaning steps were performed:

- Removed the £ symbol from prices.
- Removed unwanted encoding characters (Â).
- Converted price to float.
- Converted star ratings from text to integers (1–5).
- Converted stock availability to Boolean values.
- Converted GBP prices to INR.

---

## Currency Conversion

The project uses a fixed conversion rate:

**1 GBP = 105.50 INR**

Price in INR is calculated as:

```
price_inr = price_gbp × 105.50
```

---

## Database Schema

### categories

| Column | Type |
|---------|------|
| category_id | INTEGER PRIMARY KEY |
| category_name | TEXT UNIQUE |

### books

| Column | Type |
|---------|------|
| book_id | INTEGER PRIMARY KEY |
| title | TEXT |
| price_gbp | REAL |
| price_inr | REAL |
| rating | INTEGER |
| in_stock | BOOLEAN |
| category_id | INTEGER |

Foreign Key:

```
books.category_id
↓

categories.category_id
```

---

## SQL Queries Implemented

The project includes SQL queries demonstrating:

- SELECT
- WHERE
- ORDER BY
- LIMIT
- DISTINCT
- BETWEEN
- JOIN

---

## Pandas Operations

The project demonstrates:

- pd.read_sql()
- pd.merge()

The JOIN result from SQL matches the Pandas merge output.

---

## Files

- scraper.py
- books.db
- books_data.csv
- requirements.txt
- README.md

---

## Design Decisions

- Used BeautifulSoup for web scraping.
- Used SQLite for relational database storage.
- Used normalized database design with two tables.
- Used Pandas for data analysis.
- Used SQL JOIN and Pandas Merge to compare outputs.

## Update
Added SQL query documentation.