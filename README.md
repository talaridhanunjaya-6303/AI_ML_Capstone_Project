# AI/ML Capstone Project

This repository contains my AI/ML Capstone Project consisting of three modules.

The project covers data pipeline development, data analytics and machine learning, and an AI-powered support assistant.

---

## Project Modules

### 1. Data Pipeline

This module scrapes book data from BooksToScrape, cleans and transforms the data, converts prices from GBP to INR, stores the data in a normalized SQLite database, and performs SQL and Pandas analysis.

**Technologies:** Python, Requests, BeautifulSoup, Pandas, SQLite, SQL

[View Data Pipeline README](./data_pipeline/README.md)

---

### 2. Analytics

This module performs Exploratory Data Analysis and Machine Learning using the Titanic dataset. It includes data preprocessing, visualization, classification, regression, model evaluation, class imbalance handling, hyperparameter tuning, and model comparison.

**Technologies:** Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Joblib, Jupyter Notebook

[View Analytics README](./analytics/README.md)

---

### 3. Support Assistant

This module implements a Retrieval-Augmented Generation (RAG) based customer support assistant using document retrieval, LangGraph, and FastAPI. It also supports mock LLM testing and Docker-based execution.

**Technologies:** Python, LangGraph, FastAPI, Pydantic, RAG, Docker

[View Support Assistant README](./support_assistant/README.md)

---

## Installation

Each module contains its own `requirements.txt` file.

### Data Pipeline

```bash
pip install -r data_pipeline/requirements.txt
```

### Analytics

```bash
pip install -r analytics/requirements.txt
```

### Support Assistant

```bash
pip install -r support_assistant/requirements.txt
```

---

## Running the Project

### Data Pipeline

```bash
cd data_pipeline
python scraper.py
```

For detailed instructions:

[View Data Pipeline README](./data_pipeline/README.md)

---

### Analytics

Open the notebooks inside the `analytics` folder using Jupyter Notebook or JupyterLab.

For detailed instructions:

[View Analytics README](./analytics/README.md)

---

### Support Assistant

Navigate to the `support_assistant` folder and follow the instructions in its README.

```bash
cd support_assistant
```

For detailed instructions:

[View Support Assistant README](./support_assistant/README.md)

---

## Repository Structure

```text
AI-ML-Capstone-Project/
│
├── data_pipeline/
│   ├── README.md
│   ├── requirements.txt
│   └── ...
│
├── analytics/
│   ├── README.md
│   ├── requirements.txt
│   └── ...
│
├── support_assistant/
│   ├── README.md
│   ├── requirements.txt
│   └── ...
│
└── README.md
```

---

## Project Status

| Module | Status |
|---|---|
| Data Pipeline | Completed |
| Analytics | Completed |
| Support Assistant | Completed |

---

## Author

**Dhanunjaya**

AI/ML Capstone Project
