# Trading Predictor

AURA Trading Predictor is a modular Indian-market analysis assistant. The repository is designed to become the trading intelligence layer of AURA.

## Current MVP

- FastAPI backend
- Web dashboard with stock symbol input
- Technical-analysis engine using OHLCV data
- SMA, EMA, RSI, MACD, Bollinger Bands, ATR
- Trend / momentum / volatility summary
- Rule-based signal scoring (not financial advice)
- Demo mode with generated OHLCV data so the app works without an API key
- Clean separation between market data, analysis, and API layers

## Architecture

```text
Trading-predictor/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── data/
│   │   └── market_data.py
│   └── analysis/
│       └── technical.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Data providers

The MVP defaults to deterministic demo data. The market-data adapter is intentionally isolated so a live Indian-market provider can be added without rewriting the analysis engine.

## Safety

This project is an analysis tool. It does not place trades. Broker execution should be introduced only as a separate, explicitly authorized module with paper trading, validation, limits, confirmations, audit logs, and kill switches.
