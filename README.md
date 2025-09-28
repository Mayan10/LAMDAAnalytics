# LAMDA Supply Chain Risk Analysis System

A comprehensive AI-powered supply chain risk analysis system that combines PyTorch machine learning models with a modern React frontend and FastAPI backend.

## 🚀 Features

- **AI-Powered Risk Analysis**: Uses PyTorch models for supply chain risk prediction
- **Real-time Monitoring**: Live tracking of supply chain disruptions and alerts
- **Interactive Route Planning**: Visual route optimization with risk assessment
- **Multi-Agent Architecture**: 8 specialized AI agents for comprehensive analysis
- **Modern Web Interface**: React-based dashboard with real-time updates

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  PyTorch Model  │
│   (Port 5173)   │◄──►│   (Port 8000)   │◄──►│  (tgn_model.pth)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🛠️ Installation & Setup

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Start the backend server
python start_backend.py
```

The backend will be available at: `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd project2

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

### 3. Quick Start (Windows)

```bash
# Start backend (in one terminal)
python start_backend.py

# Start frontend (in another terminal)
start_frontend.bat
```

## 🔧 API Endpoints

### Core Analysis
- `POST /analyze` - Analyze supply chain risk
- `GET /model/info` - Get model information
- `GET /health` - Health check

### Monitoring
- `GET /monitoring/alerts` - Get real-time alerts
- `GET /analytics/overview` - Get analytics overview

## 📊 Usage

1. **Open the Dashboard**: Navigate to `http://localhost:5173/dashboard`
2. **Configure Analysis**: 
   - Select component type (semiconductors, batteries, etc.)
   - Enter seller location (e.g., "China", "Germany")
   - Enter import location (e.g., "USA", "India")
3. **Run Analysis**: Click "Analyze Supply Chain Risk"
4. **View Results**: 
   - Risk score and level
   - Detailed risk factors
   - Recommended routes
   - Real-time monitoring data

## 🧠 Model Integration

The system integrates with your PyTorch model (`tgn_model.pth`) which contains:
- Model state dictionary
- Model class information
- F1 score metrics
- Model name

The backend automatically loads the model and uses it for risk predictions based on:
- Component type
- Geographic locations
- Additional risk factors

## 🎯 Key Components

### Frontend (React)
- **Dashboard.jsx**: Main dashboard with tabs and analytics
- **SupplyChainMap.jsx**: Interactive route visualization
- **services/api.js**: API communication layer

### Backend (FastAPI)
- **main.py**: Core API server with model integration
- **Model Loading**: Automatic PyTorch model loading
- **Risk Analysis**: AI-powered risk assessment
- **Real-time Data**: Live monitoring and alerts

## 🔍 Risk Analysis Features

- **Weather Disruption**: Climate-based risk assessment
- **Political Tensions**: Geopolitical risk evaluation
- **Supply Chain Complexity**: Multi-tier supplier analysis
- **Regulatory Compliance**: Trade regulation monitoring

## 📈 Analytics Dashboard

- Real-time risk scoring
- Route optimization
- Alert management
- Performance metrics
- Model confidence indicators

## 🚨 Troubleshooting

### Backend Issues
- Ensure Python dependencies are installed: `pip install -r backend/requirements.txt`
- Check if model file exists: `tgn_model.pth`
- Verify port 8000 is available

### Frontend Issues
- Ensure Node.js dependencies are installed: `npm install`
- Check if port 5173 is available
- Verify backend is running on port 8000

### Model Issues
- Model file should be in the root directory or backend directory
- Ensure PyTorch is properly installed
- Check model file integrity

## 🔮 Future Enhancements

- Real-time data feeds integration
- Advanced visualization components
- Machine learning model retraining
- Multi-language support
- Mobile responsiveness improvements

## 📝 License

This project is part of the LAMDA Analytics system for supply chain risk management.

## 👥 Team

- **Devansh Behl**: Full Stack Development
- **Mayan Sharma**: AI/ML Engineering
- **Aditya Takuli**: Data Engineering & Analytics
- **Lay Gupta**: Product & Business Model

---

For support or questions, please refer to the API documentation at `http://localhost:8000/docs` when the backend is running.
