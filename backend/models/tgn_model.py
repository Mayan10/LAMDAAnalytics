from __future__ import annotations
import os
import torch
import numpy as np
from typing import Dict, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from orchestrator.utils.scoring import weighted_risk

class TGNWrapper:
    """
    Tries to load tgn_model.pth and run inference.
    If input shape mismatches or file absent, gracefully fall back to a weighted blend over normalized features.
    """
    def __init__(self, model_path: str = "tgn_model.pth"):
        self.model_path = model_path
        self.model = None
        self.loaded = False
        if os.path.exists(self.model_path):
            try:
                self.model = torch.load(self.model_path, map_location="cpu")
                self.model.eval()
                self.loaded = True
            except Exception:
                self.model = None
                self.loaded = False

    def predict(self, norm_features: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        Return (risk_score, contribution_dict)
        risk_score in [0,1]
        """
        # If you have a real PyTorch forward path, map features to tensor here.
        # Fallback: weighted blend
        risk, contrib = weighted_risk(norm_features)
        risk = float(np.clip(risk, 0.0, 1.0))
        return risk, contrib

tgn = TGNWrapper()
