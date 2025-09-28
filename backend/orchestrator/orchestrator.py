import asyncio
import uuid
from datetime import datetime, timezone
from .agents.trade_agent import fetch_trade_features
from .agents.news_agent import analyze_news
from .agents.weather_agent import weather_features
from .agents.political_agent import political_features
from .agents.gscpi_agent import gscpi_features
from .agents.normalizer_agent import normalize_all
from .agents.reporter_agent import concise_from_contrib, comprehensive, label_from_score
from .utils.geocoding import resolve_pair
from .utils.schema import AnalyzeRequest, AnalyzeResponse, TGNResult
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.tgn_model import tgn
from config.settings import settings

async def run_analysis(inp: AnalyzeRequest) -> AnalyzeResponse:
    request_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    # Resolve coordinates for seller/importer (for weather)
    (seller_latlon, importer_latlon) = await resolve_pair(inp.seller_location, inp.import_location)
    # Fan out
    async def _trade():   return await fetch_trade_features(inp.component_type, inp.seller_location, inp.import_location)
    async def _news():    return await analyze_news(inp.component_type, inp.seller_location, inp.import_location, inp.seller_name)
    async def _weather():
        # For simplicity, consider seller location weather
        if seller_latlon:
            return await weather_features(*seller_latlon)
        return await weather_features(0.0, 0.0)
    async def _pol():     return await political_features(inp.component_type, inp.seller_location, inp.import_location, inp.seller_name)
    async def _gscpi():   return await gscpi_features()

    tasks = [_trade(), _news(), _weather(), _pol(), _gscpi()]
    trade, news, weather, pol, gscpi = await asyncio.wait_for(asyncio.gather(*tasks), timeout=settings.agent_timeout_seconds)

    # Normalize + TGN
    norm = normalize_all(now.isoformat(), trade, news, weather, pol, gscpi)
    risk_score, contrib = tgn.predict(norm.features)
    label = label_from_score(risk_score)

    tgn_out = TGNResult(
        risk_score=risk_score,
        risk_label=label,
        risk_components=contrib
    )
    concise = concise_from_contrib(contrib, risk_score)
    comp = comprehensive(contrib)

    return AnalyzeResponse(
        request_id=request_id,
        created_at=now,
        inputs=inp,
        features=norm.features,
        tgn_result=tgn_out,
        concise=concise,
        comprehensive=comp
    )
