# 📈 FinSight AI: Autonomous Financial Analyst

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30-ff4b4b.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**FinSight AI** is a production-grade multi-agent system designed to perform comprehensive investment analysis. It combines **Quantitative Finance** (Technical Analysis), **Machine Learning** (XGBoost Forecasting), and **Generative AI** (Llama-3 via Groq) to deliver actionable insights.

Unlike simple chatbots, FinSight triangulates data from three sources—Price Action, News Sentiment, and Company Filings—to generate professional-grade investment memos.

---

## 🚀 Key Features

* **🤖 Multi-Agent Architecture:**
    * **Quant Agent:** Calculates RSI, MACD, Bollinger Bands, and runs XGBoost price predictions.
    * **Sentiment Agent:** Analyzes market psychology using NewsAPI & VADER (Social Sentiment).
    * **Research (RAG) Agent:** Retrieves fundamental risks from 10-K filings using Vector Search.
    * **Manager Agent:** Synthesizes all data into a cohesive investment report using Llama-3.
* **📊 Interactive Dashboard:** Built with Streamlit & Plotly. Includes Candlestick charts, moving averages, and live metrics.
* **📈 Backtesting Engine:** Simulates historical performance of strategies (e.g., Golden Cross) vs. Buy & Hold.
* **💾 Robust Data Engineering:**
    * **SQLite Database:** Caches stock data for offline access and speed.
    * **Hybrid Fallback:** Tries Database -> Fails to API -> Updates Database.
* **🐳 Production Ready:** Includes Docker support, Pytest suite, and a FastAPI backend.

---

## 🏗️ System Architecture



The system uses **LangGraph** to orchestrate a directed acyclic graph (DAG) of agents:

1.  **User Input:** Ticker Symbol (e.g., AAPL, BTC-USD).
2.  **Parallel Execution:** Quant, Sentiment, and RAG agents run simultaneously.
3.  **Synthesis:** The Manager Agent (LLM) receives structured JSON from all sub-agents.
4.  **Output:** A structured Markdown report + Interactive Visualizations.

---

## 🛠️ Tech Stack

* **LLM & Orchestration:** LangChain, LangGraph, Groq (Llama-3-70b).
* **Machine Learning:** XGBoost, Scikit-Learn.
* **Data & Database:** yfinance, SQLite, SQLAlchemy.
* **Sentiment:** NewsAPI, VADER Sentiment.
* **Vector DB:** ChromaDB / HuggingFace Embeddings.
* **Frontend:** Streamlit, Plotly.
* **Backend API:** FastAPI.

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/finsight-ai.git](https://github.com/yourusername/finsight-ai.git)

cd finsight-ai
```
### 2. Set Up Environment Variables
Create a .env file in the root directory:
```
GROQ_API_KEY=gsk_your_key_here
NEWS_API_KEY=your_newsapi_key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Initialize the Database
Run the ingestor to populate your local SQLite database with initial data:
```bash
python -m src.data_engine.ingestor_quant
```
### 5. Run the Application
Option A: Streamlit Dashboard (UI)
```bash
streamlit run src/ui/app.py
```

Option B: FastAPI Backend
```bash
uvicorn src.api.main:app --reload
```

Option C: Docker
```bash
docker build -t finsight .
docker run -p 8501:8501 --env-file .env finsight
```

---

## 📂 Project Structure
```Plaintext
FinSight/
├── docs/                # Documentation & Architecture diagrams
├── logs/                # Application logs
├── notebooks/           # Jupyter notebooks for research & experiments
├── src/
│   ├── agents/          # LangGraph Agent logic (Quant, RAG, Sentiment)
│   ├── api/             # FastAPI backend endpoints
│   ├── data_engine/     # Database (SQLite) & Ingestion scripts
│   ├── ml_engine/       # XGBoost training, Backtesting, & Feature Engineering
│   └── ui/              # Streamlit Frontend
├── tests/               # Pytest suite
├── Dockerfile           # Containerization setup
└── requirements.txt     # Python dependencies
```

## 🧪 Testing
Run the automated test suite to ensure signal logic and API endpoints are working:
```bash
pytest tests/
```

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any features, bug fixes, or documentation improvements.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.