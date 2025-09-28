from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import torch
import torch.nn as nn
import numpy as np
import json
import logging
from datetime import datetime
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LAMDA Supply Chain Risk Analysis API",
    description="AI-powered supply chain risk analysis and route optimization",
    version="1.0.0"
)

# CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None
model_info = {}

# Pydantic models for request/response
class SupplyChainAnalysisRequest(BaseModel):
    component_type: str
    seller_location: str
    import_location: str
    additional_factors: Optional[Dict[str, Any]] = {}

class RiskFactor(BaseModel):
    id: int
    name: str
    level: str
    impact: float
    description: str

class Route(BaseModel):
    id: int
    name: str
    risk: str
    duration: str
    cost: str
    reliability: float

class AnalysisResponse(BaseModel):
    risk_score: float
    risk_level: str
    risk_factors: List[RiskFactor]
    recommended_routes: List[Route]
    model_confidence: float
    analysis_timestamp: str

class ModelInfo(BaseModel):
    model_name: str
    model_class: str
    f1_score: float
    loaded_at: str

# Load the PyTorch model
def load_model():
    global model, model_info
    try:
        # Load the model checkpoint
        checkpoint = torch.load('tgn_model.pth', map_location='cpu', weights_only=False)
        
        model_info = {
            'model_name': checkpoint.get('model_name', 'Unknown'),
            'model_class': checkpoint.get('model_class', 'Unknown'),
            'f1_score': checkpoint.get('f1_score', 0.0),
            'loaded_at': datetime.now().isoformat()
        }
        
        # For now, we'll use the model info for predictions
        # In a real implementation, you'd reconstruct the model architecture
        # and load the state dict
        model = checkpoint
        
        logger.info(f"Model loaded successfully: {model_info['model_name']}")
        logger.info(f"Model F1 Score: {model_info['f1_score']}")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e

# Initialize model on startup
@app.on_event("startup")
async def startup_event():
    load_model()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None
    }

# Model information endpoint
@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return ModelInfo(**model_info)

# Supply chain risk analysis endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_supply_chain(request: SupplyChainAnalysisRequest):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Simulate model prediction based on input parameters
        # In a real implementation, you would:
        # 1. Preprocess the input data
        # 2. Run inference with the loaded model
        # 3. Post-process the results
        
        # Calculate risk score based on component type and locations
        base_risk = calculate_base_risk(request.component_type, request.seller_location, request.import_location)
        
        # Generate risk factors based on analysis
        risk_factors = generate_risk_factors(request, base_risk)
        
        # Generate recommended routes
        routes = generate_routes(request, base_risk)
        
        # Calculate overall risk score
        risk_score = min(100, max(0, base_risk + np.random.normal(0, 5)))
        risk_level = get_risk_level(risk_score)
        
        # Model confidence based on F1 score
        model_confidence = model_info.get('f1_score', 0.85) * 100
        
        return AnalysisResponse(
            risk_score=round(risk_score, 1),
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommended_routes=routes,
            model_confidence=round(model_confidence, 1),
            analysis_timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

def calculate_base_risk(component_type: str, seller_location: str, import_location: str) -> float:
    """Calculate base risk score based on component type and locations"""
    base_risk = 50.0  # Start with medium risk
    
    # Component type risk factors
    component_risks = {
        'semiconductors': 75.0,  # High risk due to supply chain complexity
        'batteries': 70.0,       # High risk due to regulations
        'steel': 40.0,           # Lower risk
        'electronics': 65.0,     # Medium-high risk
        'textiles': 30.0         # Lower risk
    }
    
    base_risk = component_risks.get(component_type.lower(), 50.0)
    
    # Location-based risk adjustments
    high_risk_locations = ['china', 'russia', 'iran', 'north korea']
    medium_risk_locations = ['india', 'brazil', 'mexico', 'thailand']
    
    seller_lower = seller_location.lower()
    import_lower = import_location.lower()
    
    if any(loc in seller_lower for loc in high_risk_locations):
        base_risk += 15.0
    elif any(loc in seller_lower for loc in medium_risk_locations):
        base_risk += 8.0
    
    if any(loc in import_lower for loc in high_risk_locations):
        base_risk += 10.0
    elif any(loc in import_lower for loc in medium_risk_locations):
        base_risk += 5.0
    
    # Add some randomness to simulate real-world variability
    base_risk += np.random.normal(0, 8)
    
    return max(0, min(100, base_risk))

def generate_risk_factors(request: SupplyChainAnalysisRequest, base_risk: float) -> List[RiskFactor]:
    """Generate risk factors based on analysis"""
    factors = []
    
    # Weather risk
    weather_impact = min(90, max(10, base_risk * 0.8 + np.random.normal(0, 10)))
    factors.append(RiskFactor(
        id=1,
        name="Weather Disruption",
        level="High" if weather_impact > 70 else "Medium" if weather_impact > 40 else "Low",
        impact=round(weather_impact, 1),
        description="Severe weather patterns affecting shipping routes"
    ))
    
    # Political risk
    political_impact = min(85, max(15, base_risk * 0.6 + np.random.normal(0, 12)))
    factors.append(RiskFactor(
        id=2,
        name="Political Tensions",
        level="High" if political_impact > 70 else "Medium" if political_impact > 40 else "Low",
        impact=round(political_impact, 1),
        description="Geopolitical tensions affecting trade routes"
    ))
    
    # Supply chain complexity
    complexity_impact = min(80, max(20, base_risk * 0.7 + np.random.normal(0, 8)))
    factors.append(RiskFactor(
        id=3,
        name="Supply Chain Complexity",
        level="High" if complexity_impact > 65 else "Medium" if complexity_impact > 35 else "Low",
        impact=round(complexity_impact, 1),
        description="Complex multi-tier supplier networks"
    ))
    
    # Regulatory compliance
    regulatory_impact = min(75, max(25, base_risk * 0.5 + np.random.normal(0, 10)))
    factors.append(RiskFactor(
        id=4,
        name="Regulatory Compliance",
        level="High" if regulatory_impact > 60 else "Medium" if regulatory_impact > 35 else "Low",
        impact=round(regulatory_impact, 1),
        description="International trade regulations and compliance requirements"
    ))
    
    return factors

def generate_routes(request: SupplyChainAnalysisRequest, base_risk: float) -> List[Route]:
    """Generate recommended routes based on analysis"""
    routes = []
    
    # Primary route
    primary_reliability = max(60, 95 - base_risk * 0.3)
    routes.append(Route(
        id=1,
        name="Primary Route",
        risk="Low" if base_risk < 40 else "Medium" if base_risk < 70 else "High",
        duration=f"{int(10 + base_risk * 0.1)} days",
        cost=f"${int(2000 + base_risk * 20):,}",
        reliability=round(primary_reliability, 1)
    ))
    
    # Alternative route A
    alt_a_reliability = max(50, 90 - base_risk * 0.4)
    routes.append(Route(
        id=2,
        name="Alternative Route A",
        risk="Medium" if base_risk < 50 else "High",
        duration=f"{int(12 + base_risk * 0.15)} days",
        cost=f"${int(1800 + base_risk * 25):,}",
        reliability=round(alt_a_reliability, 1)
    ))
    
    # Alternative route B
    alt_b_reliability = max(40, 85 - base_risk * 0.5)
    routes.append(Route(
        id=3,
        name="Alternative Route B",
        risk="High",
        duration=f"{int(8 + base_risk * 0.2)} days",
        cost=f"${int(2500 + base_risk * 30):,}",
        reliability=round(alt_b_reliability, 1)
    ))
    
    return routes

def get_risk_level(risk_score: float) -> str:
    """Convert risk score to risk level"""
    if risk_score < 30:
        return "Low"
    elif risk_score < 60:
        return "Medium"
    elif risk_score < 80:
        return "High"
    else:
        return "Critical"

# Real-time monitoring endpoint
@app.get("/monitoring/alerts")
async def get_alerts():
    """Get real-time alerts and monitoring data"""
    alerts = [
        {
            "id": 1,
            "type": "weather",
            "severity": "high",
            "title": "Severe Weather Alert",
            "description": "Tropical storm affecting shipping routes in Southeast Asia",
            "timestamp": datetime.now().isoformat(),
            "affected_routes": ["Route A", "Route B"]
        },
        {
            "id": 2,
            "type": "political",
            "severity": "medium",
            "title": "Trade Policy Update",
            "description": "New trade restrictions announced for electronic components",
            "timestamp": datetime.now().isoformat(),
            "affected_routes": ["Route C"]
        }
    ]
    
    return {"alerts": alerts, "timestamp": datetime.now().isoformat()}

# Analytics endpoint
@app.get("/analytics/overview")
async def get_analytics_overview():
    """Get overall analytics and metrics"""
    return {
        "total_suppliers": 10000,
        "active_routes": 24,
        "active_alerts": 7,
        "reliability_score": 89.2,
        "risk_trend": "decreasing",
        "last_updated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
