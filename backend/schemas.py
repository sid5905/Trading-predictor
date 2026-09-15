from typing import Any
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=30)
    period: int = Field(default=180, ge=60, le=2000)

class AnalyzeResponse(BaseModel):
    symbol: str
    price: float
    change_pct: float
    trend: str
    momentum: str
    volatility: str
    signal: str
    confidence: int
    indicators: dict[str, float | None]
    notes: list[str]
    patterns: list[dict[str, Any]] = Field(default_factory=list)
    levels: dict[str, float] = Field(default_factory=dict)
    chart: list[dict[str, Any]] = Field(default_factory=list)
    data_source: str = "Demo fallback"
    is_live: bool = False
