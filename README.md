# 🐻 The Bear Patrol

**S&P 500 Bear Market Early Warning System**

A Streamlit-based dashboard that uses ensemble machine learning and social media sentiment analysis to detect early signs of an S&P 500 bear market.

---

## Overview

The Bear Patrol combines financial time-series features with NLP-driven sentiment signals to produce real-time bear market risk scores. Predictions are served through a FastAPI backend and visualised in an interactive dashboard.

## Features

- **Real-time Risk Scoring** — AI-powered bear market detection with 85%+ accuracy
- **Social Sentiment Analysis** — Fine-tuned transformer model (FinBERT-style) classifying social media posts as positive, neutral, or negative
- **Ensemble ML Models** — TabNet + additional models combined for robust predictions
- **Public Dashboard** — Live S&P 500 metrics, risk indicators, and forward predictions
- **Admin Dashboard** — Deeper analytics accessible after login

## Project Structure

```
app.py                         # Landing page (Streamlit entry point)
pages/
  Dashboard.py                 # Public-facing dashboard
  Admin_Login.py               # Admin authentication page
  Admin_Dashboard.py           # Admin-only analytics
sentiment_model/               # Fine-tuned sentiment transformer
Model_PKL_Files/               # Trained ML model files & API feature contract
jan_apr_2026_predictions.csv   # Pre-computed bear market predictions
requirements.txt
```

## ML Feature Contract

The prediction API expects **114 features** in strict order:
- **111 financial features** — S&P 500 price/volume, VIX, yield curve (2Y/10Y/3M), gold, crude oil, rolling returns, volatility, drawdowns, moving averages, and more
- **3 sentiment features** — aggregated positive, neutral, and negative scores from social media

See [`Model_PKL_Files/API_Feature_Contract.txt`](Model_PKL_Files/API_Feature_Contract.txt) for the full ordered feature list.

## Setup

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit, Plotly |
| ML Models | PyTorch, TabNet (`pytorch-tabnet`), scikit-learn |
| Sentiment NLP | HuggingFace Transformers |
| Market Data | yfinance |
| API | FastAPI, Uvicorn, Pydantic |

## Team

Shani · Esther · Matthew · Desmond  
*Singapore University of Technology and Design — Term 6 CDS Project*
