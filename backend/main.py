from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .analysis.technical import analyze
from .config import APP_NAME
from .data.market_data import get_demo_data
from .schemas import AnalyzeRequest, AnalyzeResponse

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title=APP_NAME, version="1.0.0", description="Indian-market technical analysis dashboard")
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": APP_NAME, "version": "1.0.0"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_symbol(request: AnalyzeRequest):
    try:
        symbol = request.symbol.strip().upper()
        df = get_demo_data(symbol, request.period)
        result = analyze(df)
        result["chart"] = [
            {"date": idx.strftime("%Y-%m-%d"), "open": round(float(row.Open), 2), "high": round(float(row.High), 2), "low": round(float(row.Low), 2), "close": round(float(row.Close), 2), "volume": int(row.Volume)}
            for idx, row in df.tail(120).iterrows()
        ]
        return {"symbol": symbol, **result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to analyze this symbol") from exc
