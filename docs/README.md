# 📘 FinSight AI Documentation

## 🏗️ System Architecture
FinSight uses a **Multi-Agent Architecture** powered by LangGraph.

| Agent | Responsibility | Tools Used |
| :--- | :--- | :--- |
| **Quant Agent** | Mathematical analysis of price trends. | `pandas`, `ta`, `xgboost` |
| **Sentiment Agent** | Psychology analysis of news. | `NewsAPI`, `VADER` |
| **RAG Agent** | Fundamental analysis of documents. | `LangChain`, `ChromaDB` |
| **Manager Agent** | Synthesizes all data into a report. | `Llama-3` (Groq) |

---

## 🚀 Quick Start

### 1. Database Setup
Initialize the SQLite database and download stock data:
```bash
python -m src.data_engine.ingestor_quant