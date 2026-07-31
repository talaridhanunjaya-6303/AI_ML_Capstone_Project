# AI ML Capstone Project

This repository contains three modules:

- data_pipeline
- analytics
- support_assistant

## Module 1

The Data Pipeline module scrapes book data from BooksToScrape, cleans the data, converts prices from GBP to INR, stores the data in SQLite, executes SQL queries, and demonstrates Pandas data analysis.

## Requirements

Each module contains its own requirements.txt file.

Install dependencies:

```bash
pip install -r data_pipeline/requirements.txt
```

Run Module 1:

```bash
cd data_pipeline

python scraper.py
```

The remaining modules (analytics and support_assistant) will be added in subsequent parts of the project.