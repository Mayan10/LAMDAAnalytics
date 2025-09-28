# Supply Chain Risk Prediction Orchestrator

This implementation provides a comprehensive multi-agent system for real-time supply chain risk analysis using async orchestration, external API integration, and machine learning inference.

## 🏗️ Architecture Overview

The system consists of:
- **7 Specialized Agents**: Trade, News, Weather, Political, GSCPI, Normalizer, Reporter
- **Async Orchestrator**: Fan-out/fan-in pattern for parallel processing
- **TGN Model Wrapper**: Safe fallback to weighted scoring if model unavailable
- **External API Integration**: Gemini, SERP, Weather, Google Maps
- **Feature Normalization**: Persistent z-score scaling for comparability

## 📁 Directory Structure

```
backend/
├── main.py                      # FastAPI application with new routes
├── requirements.txt             # Updated dependencies
├── .env.example                 # Environment variables template
├── tgn_model.pth                # Your existing TGN model
├── config/
│   ├── __init__.py
│   └── settings.py              # Pydantic settings for env vars
├── models/
│   ├── __init__.py
│   └── tgn_model.py             # TGN wrapper with safe fallback
├── orchestrator/
│   ├── __init__.py
│   ├── orchestrator.py          # Main async orchestrator
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── trade_agent.py       # Trade flow analysis
│   │   ├── news_agent.py        # News sentiment & disruption detection
│   │   ├── weather_agent.py     # Weather anomaly detection
│   │   ├── political_agent.py   # Political risk assessment
│   │   ├── gscpi_agent.py       # Global supply chain pressure
│   │   ├── normalizer_agent.py  # Feature normalization
│   │   └── reporter_agent.py    # Report generation
│   └── utils/
│       ├── __init__.py
│       ├── api_clients.py       # HTTP clients & API wrappers
│       ├── geocoding.py         # Location resolution
│       ├── scoring.py           # Feature scaling & persistence
│       ├── cache.py             # TTL caching for API calls
│       ├── schema.py            # Pydantic models
│       └── timeutils.py         # Time utilities
└── data/
    └── scoring_state.json       # Persistent normalization state
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys:
# - GOOGLE_MAPS_API_KEY (for geocoding)
# - SERP_API_KEY (for news search)
# - WEATHER_API_KEY (for weather data)
# - GEMINI_API_KEY (for AI analysis)
```

### 3. Start the Backend

```bash
# From project root
python start_backend.py

# Or directly
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the System

```bash
# Run the test script
python test_orchestrator.py

# Or test with curl
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "component_type": "Semiconductor",
    "seller_location": "Hsinchu, Taiwan",
    "import_location": "Los Angeles, USA",
    "seller_name": "TSMC"
  }'
```

## 🔧 API Endpoints

### POST /analyze
Main analysis endpoint that orchestrates all agents.

**Request:**
```json
{
  "component_type": "Semiconductor",
  "seller_location": "Hsinchu, Taiwan", 
  "import_location": "Los Angeles, USA",
  "seller_name": "TSMC",
  "additional_factors": {}
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "inputs": { /* request data */ },
  "features": {
    "inventory_days": 0.65,
    "past_delay_days": 0.42,
    "news_vol_7d": 0.78,
    "neg_tone_frac_3d": 0.23,
    "strike_flag_7d": 0.0,
    "weather_anomaly_7d": 0.15,
    "global_risk": 0.31
  },
  "tgn_result": {
    "risk_score": 0.45,
    "risk_label": "Medium",
    "risk_components": { /* factor contributions */ }
  },
  "concise": [
    {
      "name": "news_vol_7d",
      "level": "High", 
      "percent": 23.4,
      "impact": "High volume of disruption mentions"
    }
  ],
  "comprehensive": {
    "risk_distribution": [ /* detailed factors */ ],
    "mitigation_strategies": { /* recommendations */ }
  }
}
```

### GET /model/info
Returns TGN model status and configuration.

### GET /analytics/overview
Returns system analytics and metrics.

### GET /monitoring/alerts
Returns real-time alerts and monitoring data.

## 🤖 Agent Details

### Trade Agent
- **Purpose**: Analyzes trade flows and inventory patterns
- **Data Sources**: Gemini (fallback), Comtrade (future)
- **Features**: `inventory_days`, `past_delay_days`, trade edges

### News Agent  
- **Purpose**: Monitors news for disruptions and sentiment
- **Data Sources**: SERP API → web scraping → Gemini analysis
- **Features**: `news_vol_7d`, `neg_tone_frac_3d`, `strike_flag_7d`

### Weather Agent
- **Purpose**: Detects weather anomalies affecting logistics
- **Data Sources**: OpenWeather/WeatherAPI
- **Features**: `weather_anomaly_7d`

### Political Agent
- **Purpose**: Assesses geopolitical and sanctions risk
- **Data Sources**: Gemini analysis
- **Features**: `sanction_flag`, `political_risk_score`

### GSCPI Agent
- **Purpose**: Tracks global supply chain pressure
- **Data Sources**: Gemini (fetches NY Fed GSCPI)
- **Features**: `global_risk`

### Normalizer Agent
- **Purpose**: Normalizes features for ML compatibility
- **Process**: Z-score → sigmoid → [0,1] range
- **Persistence**: Rolling stats saved to `scoring_state.json`

### Reporter Agent
- **Purpose**: Generates human-readable reports
- **Output**: Risk factors, mitigation strategies, impact descriptions

## 🧠 TGN Model Integration

The system includes a safe TGN model wrapper that:
1. Attempts to load `tgn_model.pth`
2. Falls back to weighted feature blending if model unavailable
3. Provides consistent risk scoring interface
4. Handles input shape mismatches gracefully

## ⚡ Performance Features

- **Async Processing**: All agents run in parallel using `asyncio.gather()`
- **Caching**: 15-minute TTL cache for news and weather data
- **Timeouts**: Configurable timeouts for API calls and agent execution
- **Retry Logic**: Exponential backoff for failed API calls
- **Feature Scaling**: Persistent normalization ensures run-to-run comparability

## 🔒 Security & Configuration

- **Environment Variables**: All API keys loaded from `.env`
- **CORS**: Configured for development (tighten for production)
- **Error Handling**: Graceful degradation when APIs fail
- **Logging**: Configurable log levels

## 🧪 Testing

```bash
# Test the orchestrator
python test_orchestrator.py

# Test individual endpoints
curl http://localhost:8000/model/info
curl http://localhost:8000/analytics/overview
curl http://localhost:8000/monitoring/alerts
```

## 🔮 Extensibility

### Adding New Agents
1. Create agent in `orchestrator/agents/`
2. Add to orchestrator's fan-out tasks
3. Update normalizer to include new features
4. Add feature weights in `scoring.py`

### Direct API Integration
- Set `ENABLE_COMTRADE=true` for direct trade data
- Set `ENABLE_GDELT=true` for direct news data
- Replace Gemini fallbacks with direct API calls

### Custom Models
- Replace TGN wrapper with your model
- Implement `predict()` method returning `(score, contributions)`
- Update feature mapping as needed

## 📊 Monitoring

The system provides:
- Request tracking with UUIDs
- Feature normalization persistence
- API call caching and retry metrics
- Error logging and graceful degradation

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all keys are set in `.env`
2. **Import Errors**: Run from project root or add to Python path
3. **Timeout Errors**: Increase `AGENT_TIMEOUT_SECONDS` in `.env`
4. **Model Loading**: Check `tgn_model.pth` exists and is readable

### Debug Mode

Set `LOG_LEVEL=DEBUG` in `.env` for detailed logging.

## 📈 Next Steps

1. **Add Real APIs**: Integrate Comtrade, GDELT for direct data
2. **Enhanced Caching**: Redis for distributed caching
3. **Model Training**: Retrain TGN with new feature set
4. **Dashboard**: Real-time monitoring and alerting
5. **Batch Processing**: Handle multiple analyses efficiently

---

This orchestrator provides a robust foundation for supply chain risk analysis with room for customization and scaling based on your specific needs.
