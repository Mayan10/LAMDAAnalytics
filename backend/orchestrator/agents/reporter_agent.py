from typing import List, Dict
from ..utils.schema import TGNResult, RiskFactorReport, ComprehensiveReport

def label_from_score(score: float) -> str:
    if score >= 0.66:
        return "High"
    if score >= 0.33:
        return "Medium"
    return "Low"

def concise_from_contrib(contrib: Dict[str, float], risk_score: float) -> List[RiskFactorReport]:
    # map to percentages and simple language
    out = []
    for k, v in contrib.items():
        pct = round(v * 100, 2)
        level = label_from_score(v)  # local level by contribution
        impact = {
            "weather_anomaly_7d": "Recent weather anomaly near route/plant",
            "strike_flag_7d": "Labor unrest may affect ports/logistics",
            "neg_tone_frac_3d": "Negative news sentiment trending",
            "news_vol_7d": "High volume of disruption mentions",
            "past_delay_days": "Historical delays suggest risk carryover",
            "inventory_days": "Inventory coverage may be tightening",
            "global_risk": "Global chain pressure elevated"
        }.get(k, "Contributing risk factor")
        out.append(RiskFactorReport(name=k, level=level, percent=pct, impact=impact))
    # sort by percent desc
    out.sort(key=lambda x: x.percent, reverse=True)
    return out

def comprehensive(contrib: Dict[str, float]) -> ComprehensiveReport:
    rd = concise_from_contrib(contrib, sum(contrib.values()))
    strategies = {
        "Weather Risk Mitigation": "Plan alternate routes and maintain buffer inventory during severe weather.",
        "Labor Strike Contingency": "Pre-negotiate slots with alternative ports and carriers.",
        "Sanctions Compliance": "Continuously monitor regulations; pre-qualify alternate suppliers."
    }
    return ComprehensiveReport(
        risk_distribution=rd,
        mitigation_strategies=strategies
    )
