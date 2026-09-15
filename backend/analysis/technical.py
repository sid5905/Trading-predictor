import pandas as pd


def _rsi(close: pd.Series, period: int = 14) -> float | None:
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, pd.NA)
    value = 100 - (100 / (1 + rs.iloc[-1]))
    return None if pd.isna(value) else float(value)


def _ema(close: pd.Series, period: int) -> float:
    return float(close.ewm(span=period, adjust=False).mean().iloc[-1])


def _atr(df: pd.DataFrame, period: int = 14) -> float | None:
    prev = df["Close"].shift(1)
    tr = pd.concat([(df["High"] - df["Low"]), (df["High"] - prev).abs(), (df["Low"] - prev).abs()], axis=1).max(axis=1)
    value = tr.rolling(period).mean().iloc[-1]
    return None if pd.isna(value) else float(value)


def analyze(df: pd.DataFrame) -> dict:
    close = df["Close"]
    price = float(close.iloc[-1])
    sma20 = float(close.rolling(20).mean().iloc[-1])
    sma50 = float(close.rolling(50).mean().iloc[-1])
    ema20 = _ema(close, 20)
    ema50 = _ema(close, 50)
    rsi = _rsi(close)
    macd = _ema(close, 12) - _ema(close, 26)
    signal_line = float(pd.Series(close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()).ewm(span=9, adjust=False).mean().iloc[-1])
    atr = _atr(df)
    std20 = float(close.rolling(20).std().iloc[-1])
    upper = sma20 + 2 * std20
    lower = sma20 - 2 * std20

    score = 0
    notes: list[str] = []
    if price > sma20: score += 1
    else: score -= 1
    if sma20 > sma50: score += 1
    else: score -= 1
    if rsi is not None:
        if 50 <= rsi <= 70: score += 1; notes.append("RSI supports positive momentum.")
        elif rsi > 70: notes.append("RSI is elevated; watch for overbought conditions.")
        elif rsi < 30: notes.append("RSI is depressed; watch for oversold conditions.")
    if macd > signal_line: score += 1; notes.append("MACD is above its signal line.")
    else: score -= 1
    if price > upper: notes.append("Price is above the upper Bollinger Band.")
    elif price < lower: notes.append("Price is below the lower Bollinger Band.")

    trend = "Bullish" if price > sma50 and sma20 > sma50 else "Bearish" if price < sma50 and sma20 < sma50 else "Sideways"
    momentum = "Positive" if score >= 2 else "Negative" if score <= -2 else "Mixed"
    volatility = "High" if atr and atr / price > 0.025 else "Moderate" if atr and atr / price > 0.012 else "Low"
    signal = "BUY BIAS" if score >= 3 else "SELL BIAS" if score <= -3 else "NEUTRAL"
    confidence = min(95, max(35, 50 + abs(score) * 10))

    change_pct = float((price / close.iloc[-2] - 1) * 100)
    return {"price": price, "change_pct": change_pct, "trend": trend, "momentum": momentum, "volatility": volatility, "signal": signal, "confidence": confidence,
            "indicators": {"sma20": sma20, "sma50": sma50, "ema20": ema20, "ema50": ema50, "rsi14": rsi, "macd": macd, "macd_signal": signal_line, "atr14": atr, "bb_upper": upper, "bb_lower": lower}, "notes": notes}
