import pandas as pd


def detect_patterns(df: pd.DataFrame) -> list[dict]:
    c, o, h, l = df.Close, df.Open, df.High, df.Low
    out: list[dict] = []
    body = (c - o).abs()
    rng = (h - l).replace(0, pd.NA)
    if body.iloc[-1] <= float(rng.iloc[-1]) * 0.12:
        out.append({"name": "Doji", "bias": "Indecision", "confidence": 65})
    if body.iloc[-1] <= float(rng.iloc[-1]) * 0.35:
        lower = min(o.iloc[-1], c.iloc[-1]) - l.iloc[-1]
        upper = h.iloc[-1] - max(o.iloc[-1], c.iloc[-1])
        if lower > body.iloc[-1] * 2 and upper < body.iloc[-1] * 1.2:
            out.append({"name": "Hammer", "bias": "Potential bullish reversal", "confidence": 70})
        if upper > body.iloc[-1] * 2 and lower < body.iloc[-1] * 1.2:
            out.append({"name": "Shooting Star", "bias": "Potential bearish reversal", "confidence": 70})
    if len(c) >= 2:
        if c.iloc[-2] < o.iloc[-2] and c.iloc[-1] > o.iloc[-1] and c.iloc[-1] >= o.iloc[-2] and o.iloc[-1] <= c.iloc[-2]:
            out.append({"name": "Bullish Engulfing", "bias": "Bullish reversal", "confidence": 78})
        if c.iloc[-2] > o.iloc[-2] and c.iloc[-1] < o.iloc[-1] and o.iloc[-1] >= c.iloc[-2] and c.iloc[-1] <= o.iloc[-2]:
            out.append({"name": "Bearish Engulfing", "bias": "Bearish reversal", "confidence": 78})
    return out


def levels(df: pd.DataFrame, window: int = 40) -> dict[str, float]:
    x = df.tail(window)
    return {"support": round(float(x.Low.min()), 2), "resistance": round(float(x.High.max()), 2)}
