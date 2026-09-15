from __future__ import annotations

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    yf = None


def get_demo_data(symbol: str, period: int = 180) -> pd.DataFrame:
    """Deterministic fallback so the UI remains usable without a provider."""
    seed = sum(ord(c) for c in symbol.upper())
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=period)
    drift = rng.normal(0.0005, 0.0004)
    returns = rng.normal(drift, 0.018, period)
    close = 100 * np.exp(np.cumsum(returns))
    open_ = close * (1 + rng.normal(0, 0.006, period))
    high = np.maximum(open_, close) * (1 + rng.uniform(0.001, 0.018, period))
    low = np.minimum(open_, close) * (1 - rng.uniform(0.001, 0.018, period))
    volume = rng.integers(100_000, 2_000_000, period)
    return pd.DataFrame({"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume}, index=dates)


def normalize_symbol(symbol: str) -> str:
    value = symbol.upper().strip().replace("NSE:", "").replace("BSE:", "")
    return value if value.endswith(".NS") else f"{value}.NS"


def get_market_data(symbol: str, period: int = 180) -> tuple[pd.DataFrame, bool, str]:
    """Fetch Indian-market daily data; fall back to deterministic data on provider failure."""
    clean = normalize_symbol(symbol)
    if yf is not None:
        try:
            data = yf.Ticker(clean).history(period="1y", interval="1d", auto_adjust=False)
            if not data.empty:
                data = data[[c for c in ["Open", "High", "Low", "Close", "Volume"] if c in data]].dropna(subset=["Close"])
                return data.tail(max(period, 60)), True, "Yahoo Finance"
        except Exception:
            pass
    return get_demo_data(clean, period), False, "Demo fallback"
