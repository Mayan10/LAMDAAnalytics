import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from orchestrator.utils.api_clients import get_gemini
from ..utils.schema import GSCPIFeatures
from ..utils.timeutils import utc_now_iso

async def gscpi_features() -> GSCPIFeatures:
    prompt = """
Fetch the latest NY Fed Global Supply Chain Pressure Index (GSCPI) value (monthly).
Return strict JSON: {"global_risk": float, "timestamp": "YYYY-MM"}.
If you cannot fetch today, return last known recent value (e.g., 0.0 to 1.0 range).
"""
    model = get_gemini()
    try:
        resp = model.generate_content(prompt)
        import json, re
        s = (resp.text or "{}")
        s = re.sub(r"```json|```", "", s).strip()
        data = json.loads(s)
        return GSCPIFeatures(
            global_risk=float(data.get("global_risk", 0.2)),
            timestamp=data.get("timestamp", utc_now_iso()[:7])
        )
    except Exception:
        return GSCPIFeatures(global_risk=0.2, timestamp=utc_now_iso()[:7])
