# 🤖 AI Agent Pipeline - Complete Orchestrator Flow

This document explains the complete AI agent pipeline that fetches real data, processes it through multiple AI systems, and generates comprehensive risk analysis.

## 🔄 Complete Pipeline Flow

```
Input Request → 7 AI Agents → Gemini Analysis → TGN Model → Gemini Report → Final Output
```

## 📋 Step-by-Step Process

### 1. 🔍 **Trade Agent** (`trade_agent.py`)
- **Purpose**: Analyzes trade flows and inventory patterns
- **Data Sources**: Gemini AI (fallback for trade data)
- **Gemini Analysis**: 
  - Estimates inventory days based on component type and route
  - Calculates past delay patterns
  - Generates trade edge data (exporter→importer flows)
- **Output**: `TradeFeatures` with inventory_days, past_delay_days, trade edges

### 2. 📰 **News Agent** (`news_agent.py`)
- **Purpose**: Monitors news for supply chain disruptions
- **Data Sources**: SERP API → Web scraping → Gemini analysis
- **Process**:
  1. **SERP API**: Searches for disruption-related news using multiple query templates
  2. **Web Scraping**: Fetches full article content using BeautifulSoup
  3. **Gemini Analysis**: Analyzes text for:
     - News volume in last 7 days
     - Negative sentiment fraction in last 3 days
     - Strike/unrest detection flags
- **Output**: `NewsFeatures` with news_vol_7d, neg_tone_frac_3d, strike_flag_7d

### 3. 🌤️ **Weather Agent** (`weather_agent.py`)
- **Purpose**: Detects weather anomalies affecting logistics
- **Data Sources**: OpenWeather API or WeatherAPI
- **Process**:
  1. **Geocoding**: Converts location names to coordinates
  2. **Weather API**: Fetches 7-day weather forecast
  3. **Anomaly Detection**: Statistical analysis of temperature deviations
- **Output**: `WeatherFeatures` with weather_anomaly_7d flag

### 4. 🏛️ **Political Agent** (`political_agent.py`)
- **Purpose**: Assesses geopolitical and sanctions risk
- **Data Sources**: Gemini AI analysis
- **Gemini Analysis**:
  - Evaluates current sanctions affecting the route
  - Assesses political risk score (0-1)
  - Provides contextual notes on geopolitical factors
- **Output**: `PoliticalFeatures` with sanction_flag, political_risk_score, notes

### 5. 🌍 **GSCPI Agent** (`gscpi_agent.py`)
- **Purpose**: Tracks global supply chain pressure
- **Data Sources**: Gemini AI (fetches NY Fed GSCPI data)
- **Gemini Analysis**:
  - Retrieves latest Global Supply Chain Pressure Index
  - Provides timestamp and risk level
- **Output**: `GSCPIFeatures` with global_risk score and timestamp

### 6. ⚖️ **Normalizer Agent** (`normalizer_agent.py`)
- **Purpose**: Normalizes features for ML model compatibility
- **Process**:
  1. **Feature Assembly**: Combines all agent outputs into raw feature vector
  2. **Z-Score Normalization**: Converts to standardized scores
  3. **Sigmoid Squashing**: Maps to [0,1] range for ML compatibility
  4. **Persistent Scaling**: Saves rolling statistics for run-to-run consistency
- **Output**: `NormalizedFeatureVector` with standardized features

### 7. 🤖 **TGN Model** (`tgn_model.py`)
- **Purpose**: Trained AI model for risk prediction
- **Process**:
  1. **Model Loading**: Attempts to load `tgn_model.pth`
  2. **Feature Mapping**: Converts normalized features to model input format
  3. **Inference**: Runs forward pass through trained neural network
  4. **Fallback**: Uses weighted blending if model unavailable
- **Output**: Risk score (0-1) and component contributions

### 8. 📊 **Reporter Agent** (`reporter_agent.py`)
- **Purpose**: Generates human-readable reports
- **Process**:
  1. **Risk Labeling**: Converts scores to High/Medium/Low labels
  2. **Contribution Analysis**: Maps component contributions to percentages
  3. **Impact Descriptions**: Provides contextual impact explanations
  4. **Mitigation Strategies**: Generates actionable recommendations
- **Output**: `RiskFactorReport` and `ComprehensiveReport`

## 🔄 **Async Orchestration** (`orchestrator.py`)

The orchestrator coordinates all agents using async/await patterns:

```python
# Fan-out: Run all agents in parallel
tasks = [
    fetch_trade_features(...),
    analyze_news(...),
    weather_features(...),
    political_features(...),
    gscpi_features(...)
]
trade, news, weather, pol, gscpi = await asyncio.gather(*tasks)

# Fan-in: Combine results
norm = normalize_all(trade, news, weather, pol, gscpi)
risk_score, contrib = tgn.predict(norm.features)
reports = generate_reports(contrib)
```

## 🎯 **Key AI Integration Points**

### **Gemini AI Usage**:
1. **Trade Analysis**: Estimates trade flows and inventory patterns
2. **News Sentiment**: Analyzes scraped news for disruption signals
3. **Political Risk**: Assesses geopolitical factors and sanctions
4. **Global Pressure**: Fetches and interprets GSCPI data
5. **Report Generation**: Simplifies technical outputs for business users

### **TGN Model Integration**:
- **Input**: Normalized feature vector from all agents
- **Processing**: Neural network inference for risk prediction
- **Output**: Risk score and component contributions
- **Fallback**: Weighted blending when model unavailable

## 🚀 **Running the Full Pipeline**

### **Prerequisites**:
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set up API keys in backend/.env
# Google Maps API Configuration
GOOGLE_MAPS_API_KEY=AIzaSyBeju-TfwFR3pTNuffnCgVxnyiu8AvYIow
SERP_API_KEY=33c27e947fc888db75873dae1fbf0d27a1084769c0bbd8c46ce14cd27c04d575
WEATHER_API_KEY=12cdd7b6c0a14759939174503251909
GEMINI_API_KEY=AIzaSyCKsh8435QFEG4AWYbmglqt5iTLtmT5Mf0
```

### **Test the Complete Pipeline**:
```bash
# Run full orchestrator test
python test_full_orchestrator.py

# Or test via API
curl -X POST http://127.0.0.1:8002/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "component_type": "Semiconductor",
    "seller_location": "Hsinchu, Taiwan",
    "import_location": "Los Angeles, USA",
    "seller_name": "TSMC"
  }'
```

## 📊 **Expected Output Structure**

```json
{
  "request_id": "uuid",
  "created_at": "2025-01-01T00:00:00Z",
  "inputs": { /* original request */ },
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
    "risk_components": { /* TGN model contributions */ }
  },
  "concise": [ /* Gemini-simplified risk factors */ ],
  "comprehensive": {
    "risk_distribution": [ /* detailed breakdown */ ],
    "mitigation_strategies": { /* actionable recommendations */ }
  }
}
```

## 🔧 **Performance Characteristics**

- **Total Runtime**: 30-60 seconds (depending on API response times)
- **Parallel Processing**: All agents run concurrently
- **Caching**: 15-minute TTL for news and weather data
- **Error Handling**: Graceful degradation when APIs fail
- **Scalability**: Designed for high-throughput production use

This pipeline represents a complete AI-driven supply chain risk analysis system that combines real-time data fetching, multiple AI models, and comprehensive reporting.
