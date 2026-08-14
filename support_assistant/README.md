# Zepto Support Assistant

## Overview

This module implements a Retrieval-Augmented Generation (RAG) based customer support assistant using LangGraph, ChromaDB and FastAPI.

The assistant retrieves relevant Zepto policy documents and generates responses using semantic search.

## Features

* FastAPI REST API
* LangGraph workflow
* ChromaDB vector database
* Sentence Transformers embeddings
* Semantic document retrieval
* Mock LLM support
* Docker support

## Project Structure

```
support_assistant/
│
├── docs/
├── chroma_db/
├── Dockerfile
├── requirements.txt
├── main.py
├── rag_pipeline.py
├── models.py
├── prompt.py
└── README.md
```

## Installation

Create virtual environment

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run API

```bash
uvicorn main:app --reload
```

API will be available at

```
http://localhost:7860
```

Swagger UI

```
http://localhost:7860/docs
```

## Docker

Build image

```bash
docker build -t support-assistant .
```

Run container

```bash
docker run -p 7860:7860 support-assistant
```

## API Endpoint

### POST /ask

Example Request

```json
{
  "query": "How can I cancel my order?"
}
```

Example Response

```json
{
  "answer": "Orders can be cancelled before they are packed.",
  "sources": [
    "doc_05"
  ],
  "confidence": 1.0
}
```

## Technologies

* Python
* FastAPI
* LangGraph
* ChromaDB
* Sentence Transformers
* Docker

## Documents

The assistant indexes Zepto policy documents stored inside the `docs` folder including:

* Delivery Policy
* Refund Policy
* Return Policy
* Membership Policy
* Order Cancellation Policy
* Order Tracking
* Gift Cards
* Customer Support
