# AI Agent Pipeline Documentation

## Overview

The LAMDA Supply Chain Risk Analysis System features a sophisticated 7-agent AI pipeline that processes real-time data from multiple external APIs to provide comprehensive supply chain risk assessment.

## Architecture

```
Input Request → Orchestrator → 7 AI Agents → TGN Model → Reporter → Final Output
```

## AI Agents

### 1. Trade Agent (`trade_agent.py`)
**Purpose**: Analyzes trade flows and inventory patterns
**Data Sources**: Gemini AI
**Process**:
- Estimates inventory days based on component type and route
- Calculates past delay patterns from historical data
- Generates trade edge data (exporter→importer flows)
**Output**: `TradeFeatures` with inventory_days, past_delay_days, trade edges

### 2. News Agent (`news_agent.py`)
**Purpose**: Monitors news for supply chain disruptions
**Data Sources**: SERP API → Web scraping → Gemini AI
**Process**:
1. **SERP API**: Searches for disruption-related news using multiple query templates
2. **Web Scraping**: Fetches full article content using BeautifulSoup
3. **Gemini Analysis**: Analyzes text for:
   - News volume in last 7 days
   - Negative sentiment fraction in last 3 days
   - Strike/unrest detection flags
**Output**: `NewsFeatures` with news_vol_7d, neg_tone_frac_3d, strike_flag_7d

### 3. Weather Agent (`weather_agent.py`)
**Purpose**: Detects weather anomalies affecting logistics
**Data Sources**: OpenWeather API or WeatherAPI
**Process**:
1. **Geocoding**: Converts location names to coordinates
2. **Weather API**: Fetches 7-day weather forecast
3. **Anomaly Detection**: Statistical analysis of temperature deviations
**Output**: `WeatherFeatures` with weather_anomaly_7d flag

### 4. Political Agent (`political_agent.py`)
**Purpose**: Assesses geopolitical and sanctions risk
**Data Sources**: Gemini AI
**Process**:
- Evaluates current sanctions affecting the route
- Assesses political risk score (0-1)
- Provides contextual notes on geopolitical factors
**Output**: `PoliticalFeatures` with sanction_flag, political_risk_score, notes

### 5. GSCPI Agent (`gscpi_agent.py`)
**Purpose**: Tracks global supply chain pressure
**Data Sources**: Gemini AI (fetches NY Fed GSCPI data)
**Process**:
- Retrieves latest Global Supply Chain Pressure Index
- Provides timestamp and risk level
**Output**: `GSCPIFeatures` with global_risk score and timestamp

### 6. Normalizer Agent (`normalizer_agent.py`)
**Purpose**: Normalizes features for ML model compatibility
**Process**:
1. **Feature Assembly**: Combines all agent outputs into raw feature vector
2. **Z-Score Normalization**: Converts to standardized scores
3. **Sigmoid Squashing**: Maps to [0,1] range for ML compatibility
4. **Persistent Scaling**: Saves rolling statistics for run-to-run consistency
**Output**: `NormalizedFeatureVector` with standardized features

### 7. TGN Model (`tgn_model.py`)
**Purpose**: Trained AI model for risk prediction
**Process**:
1. **Model Loading**: Attempts to load `tgn_model.pth`
2. **Feature Mapping**: Converts normalized features to model input format
3. **Inference**: Runs forward pass through trained neural network
4. **Fallback**: Uses weighted blending if model unavailable
**Output**: Risk score (0-1) and component contributions

### 8. Reporter Agent (`reporter_agent.py`)
**Purpose**: Generates human-readable reports
**Process**:
1. **Risk Labeling**: Converts scores to High/Medium/Low labels
2. **Contribution Analysis**: Maps component contributions to percentages
3. **Impact Descriptions**: Provides contextual impact explanations
4. **Mitigation Strategies**: Generates actionable recommendations
**Output**: `RiskFactorReport` and `ComprehensiveReport`

## Async Orchestration

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

## API Integration

### External APIs Used

1. **Google Gemini API**
   - Model: `gemini-2.0-flash`
   - Usage: Trade analysis, news sentiment, political risk, GSCPI analysis, report generation
   - Rate Limits: Handled with retry logic

2. **SERP API**
   - Usage: News search and article content retrieval
   - Queries: Multiple disruption-related search terms
   - Rate Limits: Built-in API limits

3. **Weather APIs**
   - OpenWeather API: Primary weather data source
   - WeatherAPI: Alternative provider
   - Usage: 7-day forecast and anomaly detection

4. **Google Maps API**
   - Usage: Geocoding for location-based analysis
   - Rate Limits: Standard Google Maps API limits

## Error Handling

### Graceful Degradation
- **API Failures**: Fallback to mock data with clear indicators
- **Model Failures**: Weighted risk scoring as backup
- **Network Issues**: Retry logic with exponential backoff
- **Invalid Responses**: JSON parsing with error recovery

### Caching Strategy
- **News Data**: 15-minute TTL cache
- **Weather Data**: 15-minute TTL cache
- **Geocoding**: Persistent cache for repeated locations
- **Model Results**: In-memory caching for identical requests

## Performance Characteristics

- **Total Runtime**: 30-60 seconds (depending on API response times)
- **Parallel Processing**: All agents run concurrently
- **Memory Usage**: Optimized for production deployment
- **Scalability**: Designed for high-throughput use

## Configuration

### Environment Variables

```bash
# Required API Keys
GOOGLE_MAPS_API_KEY=your_key
SERP_API_KEY=your_key
WEATHER_API_KEY=your_key
GEMINI_API_KEY=your_key

# Optional Settings
WEATHER_PROVIDER=openweather
HTTP_TIMEOUT_SECONDS=30
AGENT_TIMEOUT_SECONDS=40
SCORING_STATE_PATH=./data/scoring_state.json
LOG_LEVEL=INFO
ENABLE_GDELT=false
ENABLE_COMTRADE=false
ALLOW_GEMINI_FALLBACK=true
```

## Testing

### Test Scripts

1. **`run_orchestrator_realtime.py`**: Complete pipeline test
2. **`test_google_api.py`**: API connectivity test
3. **`test_simple_orchestrator.py`**: Simplified pipeline test
4. **`test_api_keys.py`**: Individual API key validation

### Running Tests

```bash
# Test complete pipeline
python run_orchestrator_realtime.py

# Test API connectivity
python test_google_api.py

# Test with mock data
python test_simple_orchestrator.py
```

## Output Format

### Analysis Response

```json
{
  "request_id": "uuid",
  "created_at": "2025-01-01T00:00:00Z",
  "inputs": {
    "component_type": "Semiconductor",
    "seller_location": "Hsinchu, Taiwan",
    "import_location": "Los Angeles, USA",
    "seller_name": "TSMC"
  },
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
    "risk_components": {
      "inventory_days": 0.13,
      "past_delay_days": 0.08,
      "news_vol_7d": 0.12,
      "neg_tone_frac_3d": 0.03,
      "strike_flag_7d": 0.0,
      "weather_anomaly_7d": 0.02,
      "global_risk": 0.02
    }
  },
  "concise": [
    {
      "name": "news_vol_7d",
      "level": "High",
      "percent": 26.7,
      "impact": "High volume of disruption mentions"
    }
  ],
  "comprehensive": {
    "risk_distribution": [...],
    "mitigation_strategies": {
      "Weather Risk Mitigation": "Plan alternate routes...",
      "Labor Strike Contingency": "Pre-negotiate slots...",
      "Sanctions Compliance": "Continuously monitor..."
    }
  }
}
```

## Monitoring and Logging

### Log Levels
- **INFO**: Normal operation logs
- **WARNING**: API failures, fallback usage
- **ERROR**: Critical failures, model errors
- **DEBUG**: Detailed execution traces

### Metrics
- **Execution Time**: Per-agent and total pipeline time
- **API Response Times**: Individual API performance
- **Success Rates**: Agent completion rates
- **Error Rates**: Failure tracking and analysis

## Security Considerations

### API Key Management
- Environment variable storage
- No hardcoded credentials
- Secure key rotation support

### Data Privacy
- No persistent storage of sensitive data
- Temporary caching only
- GDPR compliance considerations

### Rate Limiting
- Built-in API rate limit handling
- Exponential backoff for retries
- Circuit breaker patterns for failures

## Deployment

### Production Considerations
- **Load Balancing**: Multiple backend instances
- **Database**: Persistent storage for scoring state
- **Monitoring**: Application performance monitoring
- **Scaling**: Horizontal scaling support

### Docker Support
```dockerfile
FROM python:3.13-slim
COPY backend/ /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"]
```

## Future Enhancements

1. **Real-time Streaming**: WebSocket support for live updates
2. **Advanced Caching**: Redis-based distributed caching
3. **Model Versioning**: A/B testing for model improvements
4. **Custom Agents**: Plugin architecture for new agents
5. **Batch Processing**: Bulk analysis capabilities
6. **API Gateway**: Centralized API management
7. **Analytics**: Advanced performance analytics
8. **Alerting**: Proactive failure notifications

---

This documentation provides a comprehensive overview of the AI agent pipeline system. For specific implementation details, refer to the individual agent files and the orchestrator implementation.
