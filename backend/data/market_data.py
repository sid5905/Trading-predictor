import numpy as np
import pandas as pd


def get_demo_data(symbol: str, period: int = 180) -> pd.DataFrame:
    """Generate deterministic OHLCV data for local development."""
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
