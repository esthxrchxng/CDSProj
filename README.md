# 🐻 The Bear Patrol

**S&P 500 Bear Market Early Warning System**

A Streamlit-based dashboard that uses ensemble machine learning and social media sentiment analysis to detect early signs of an S&P 500 bear market.

---

## Overview

The Bear Patrol combines financial time-series features with NLP-driven sentiment signals to produce real-time bear market risk scores. Predictions are pre-computed and visualised through an interactive multi-page dashboard with both public and admin-gated views.

## Features

- **Real-time Risk Scoring** — AI-powered bear market detection with 85%+ accuracy
- **Social Sentiment Analysis** — Fine-tuned transformer model (FinBERT-style) classifying social media posts as positive, neutral, or negative
- **Ensemble ML Models** — Random Forest, SVM, Voting Ensemble, and TabNet combined for robust predictions
- **Public Dashboard** — Live S&P 500 metrics, risk indicators, and forward predictions
- **Admin Dashboard** — Sentiment & Momentum Analysis, Ensemble Model Confidence, and deeper analytics (login-gated)

---

## Project Structure

```
CDSProj/
├── app.py                                  # Landing page (Streamlit entry point)
├── requirements.txt
├── jan_apr_2026_predictions.csv            # Pre-computed bear market predictions (Jan–Apr 2026)
│
├── pages/
│   ├── Dashboard.py                        # Public-facing dashboard
│   ├── Admin_Login.py                      # Admin authentication page
│   └── Admin_Dashboard.py                  # Admin-only analytics dashboard
│
├── Model PKL Files/
│   ├── rf_base.pkl                         # Random Forest base model
│   ├── svm_base.pkl                        # SVM base model
│   ├── voting_base.pkl                     # Voting Ensemble base model
│   ├── meta_learner.pkl                    # Meta-learner (stacking)
│   ├── financial_scaler.pkl                # Scaler for financial features
│   ├── meta_scaler.pkl                     # Scaler for meta-learner inputs
│   ├── jan_apr_2026_predictions.csv        # Predictions used by admin upload
│   └── API_Feature_Contract.txt           # Full ordered feature list (114 features)
│
├── sentiment_model/
│   ├── config.json                         # Fine-tuned sentiment model config
│   ├── tokenizer.json                      # Tokenizer vocabulary & rules
│   └── tokenizer_config.json              # Tokenizer settings
│
├── SocialMediaDataset/
│   ├── sentiment_analysis.ipynb            # Sentiment model training notebook
│   ├── sentiment_analysis_model.ipynb      # Model experimentation notebook
│   └── real_time_sentiment_prediction.ipynb# Live prediction pipeline notebook
│
├── Raw Data/
│   ├── Financial Data/                     # Historical market data (Bloomberg/yfinance)
│   │   ├── SPX Last Open val.xlsx          # S&P 500 open/last prices
│   │   ├── SPX Volume.xlsx                 # S&P 500 volume
│   │   ├── VIX Index.xlsx                  # CBOE VIX volatility index
│   │   ├── USGG2YR.xlsx                    # US 2-year Treasury yield
│   │   ├── USGG10YR.xlsx                   # US 10-year Treasury yield
│   │   ├── USGG3M.xlsx                     # US 3-month Treasury yield
│   │   ├── DowJones Last Open.xlsx         # Dow Jones open/last prices
│   │   ├── DowJones High Low.xlsx          # Dow Jones high/low prices
│   │   ├── Nasdaq Last Open.xlsx           # Nasdaq open/last prices
│   │   ├── Nasdaq High Low.xlsx            # Nasdaq high/low prices
│   │   ├── MXWO Last Open val.xlsx         # MSCI World open/last prices
│   │   ├── MXWO High Low val.xlsx          # MSCI World high/low prices
│   │   ├── ES1.xlsx / ES2.xlsx             # S&P 500 futures (front & second month)
│   │   ├── CL1 Comodity.xlsx               # Crude oil (WTI) front month
│   │   ├── CO1 Comodity.xlsx               # Crude oil (Brent) front month
│   │   └── XAUUSD Last.xlsx                # Gold spot price
│   │
│   └── Sentiment Data/
│       ├── 2008/ … 2025/                   # Annual Reddit sentiment outputs
│       │   ├── daily.csv                   # Daily aggregated sentiment scores
│       │   ├── daily_sentiment_results.csv # Per-post sentiment classifications
│       │   ├── predictions.csv             # Model predictions for that year
│       │   ├── test_predictions.csv        # Held-out test predictions
│       │   ├── model_performance_summary.txt
│       │   └── sentiment_trend.png
│       ├── 2026/
│       │   └── Jan 2026 to Apr 2026/       # 2026 sentiment data (prediction window)
│       │       ├── daily.csv
│       │       ├── daily_sentiment_results.csv
│       │       ├── predictions.csv
│       │       ├── test_predictions_full.csv
│       │       ├── model_performance_summary.txt
│       │       └── sentiment_trend.png
│       ├── Combined 2008-2025/             # Full historical combined dataset
│       │   ├── combined_daily.csv
│       │   ├── combined_daily_sentiment_results.csv
│       │   ├── combined_test_predictions.csv
│       │   └── combined_data.py
│       └── JSON files for Live Prediction/ # Reddit subreddit scraped data (JSON)
│           ├── StockMarket.json
│           ├── wallstreetbets.json
│           ├── investing.json
│           ├── economy.json
│           ├── Cryptocurrency.json
│           └── … (22 subreddits total)
│
└── CDS_Project_Modelling.ipynb             # End-to-end modelling notebook
```

---

## ML Feature Contract

The prediction pipeline expects **114 features** in strict order:
- **111 financial features** — S&P 500 price/volume, VIX, yield curve (2Y/10Y/3M), gold, crude oil, rolling returns, volatility, drawdowns, moving averages, and more
- **3 sentiment features** — aggregated positive, neutral, and negative scores from social media

See [`Model PKL Files/API_Feature_Contract.txt`](Model%20PKL%20Files/API_Feature_Contract.txt) for the full ordered feature list.

---

## Setup

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## Dashboard Pages

| Page | Access | Description |
|---|---|---|
| `app.py` | Public | Landing / home page |
| `pages/Dashboard.py` | Public | S&P 500 risk score, crash warnings, price chart. Unlocks Sentiment & Ensemble charts when logged in as admin |
| `pages/Admin_Login.py` | Public | Admin login form |
| `pages/Admin_Dashboard.py` | Admin only | Full analytics — sentiment trend, social media activity, model confidence, model metrics |

---

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit, Plotly |
| ML Models | PyTorch, TabNet (`pytorch-tabnet`), scikit-learn |
| Sentiment NLP | HuggingFace Transformers |
| Market Data | yfinance, openpyxl |

---

## Team
Group 13

| Name | Student ID |
|---|---|
| Boh Chue Yee Shani | 1008154 |
| Esther Ching Jing Xuan | 1008145 |
| Matthew Phua Tai Kit | 1008016 |
| Desmond Ngui You Hong | 1008059 |

*Singapore University of Technology and Design — Term 6 CDS Project*
