from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .analysis.patterns import detect_patterns, levels
from .analysis.technical import analyze
from .config import APP_NAME
from .data.market_data import get_market_data
from .schemas import AnalyzeRequest, AnalyzeResponse

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title=APP_NAME, version="2.0.0", description="AURA Indian-market technical analysis platform")
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend"), name="static")

@app.get("/")
def index():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

@app.get("/health")
def health():
    return {"status": "ok", "service": APP_NAME, "version": "2.0.0"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_symbol(request: AnalyzeRequest):
    symbol = request.symbol.strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Enter an NSE stock symbol")
    try:
        df, live, provider = get_market_data(symbol, request.period)
        if len(df) < 60:
            raise HTTPException(status_code=422, detail="Not enough price history for analysis")
        result = analyze(df)
        result["patterns"] = detect_patterns(df)
        result["levels"] = levels(df)
        result["data_source"] = provider
        result["is_live"] = live
        result["chart"] = [{"date": idx.strftime("%Y-%m-%d"), "open": round(float(row.Open), 2), "high": round(float(row.High), 2), "low": round(float(row.Low), 2), "close": round(float(row.Close), 2), "volume": int(row.Volume)} for idx, row in df.tail(180).iterrows()]
        return {"symbol": symbol.replace(".NS", ""), **result}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to analyze {symbol}: {exc}") from exc
