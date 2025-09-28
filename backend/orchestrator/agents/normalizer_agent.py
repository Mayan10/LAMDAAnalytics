from ..utils.schema import (TradeFeatures, NewsFeatures, WeatherFeatures, PoliticalFeatures, GSCPIFeatures, NormalizedFeatureVector)
from ..utils.scoring import normalize_features

def assemble_raw(trade: TradeFeatures, news: NewsFeatures, weather: WeatherFeatures, pol: PoliticalFeatures, g: GSCPIFeatures):
    return {
        "inventory_days": trade.inventory_days if trade.inventory_days is not None else 30.0,
        "past_delay_days": trade.past_delay_days if trade.past_delay_days is not None else 5.0,
        "news_vol_7d": float(news.news_vol_7d),
        "neg_tone_frac_3d": news.neg_tone_frac_3d,
        "strike_flag_7d": float(news.strike_flag_7d),
        "weather_anomaly_7d": float(weather.weather_anomaly_7d),
        "global_risk": g.global_risk
    }

def normalize_all(ts_iso: str, trade, news, weather, pol, g) -> NormalizedFeatureVector:
    raw = assemble_raw(trade, news, weather, pol, g)
    norm = normalize_features(raw)
    return NormalizedFeatureVector(ts_iso=ts_iso, features=norm)
