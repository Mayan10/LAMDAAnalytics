from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

# ----- Request -----
class AnalyzeRequest(BaseModel):
    component_type: str
    seller_location: str
    import_location: str
    seller_name: Optional[str] = None
    additional_factors: Dict[str, Any] = Field(default_factory=dict)

# ----- Agent outputs (intermediate) -----
class TradeEdge(BaseModel):
    exporter: str
    importer: str
    trade_value_usd: float
    timestamp: str  # "YYYY-MM"

class TradeFeatures(BaseModel):
    inventory_days: Optional[float] = None
    past_delay_days: Optional[float] = None
    edges: List[TradeEdge] = Field(default_factory=list)

class NewsFeatures(BaseModel):
    news_vol_7d: int = 0
    neg_tone_frac_3d: float = 0.0
    strike_flag_7d: int = 0
    sources: List[str] = Field(default_factory=list)  # urls

class WeatherFeatures(BaseModel):
    weather_anomaly_7d: int = 0
    details: Dict[str, Any] = Field(default_factory=dict)

class PoliticalFeatures(BaseModel):
    sanction_flag: int = 0
    political_risk_score: float = 0.0
    notes: Optional[str] = None

class GSCPIFeatures(BaseModel):
    global_risk: float = 0.0
    timestamp: Optional[str] = None

class NormalizedFeatureVector(BaseModel):
    ts_iso: str
    features: Dict[str, float]   # normalized comparable feature set

# ----- TGN inference output -----
class TGNResult(BaseModel):
    risk_score: float
    risk_label: str  # "Low" | "Medium" | "High"
    risk_components: Dict[str, float]  # contribution per factor

# ----- Final report (formatted) -----
class RiskFactorReport(BaseModel):
    name: str
    level: str       # High / Medium / Low
    percent: float   # 0-100
    impact: str

class ComprehensiveReport(BaseModel):
    risk_distribution: List[RiskFactorReport]
    mitigation_strategies: Dict[str, str]

class AnalyzeResponse(BaseModel):
    request_id: str
    created_at: datetime
    inputs: AnalyzeRequest
    features: Dict[str, float]                    # normalized feature vector (flattened)
    tgn_result: TGNResult
    concise: List[RiskFactorReport]
    comprehensive: ComprehensiveReport
