import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTOR_DB_DIR = DATA_DIR / "vector_store"
MODEL_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure they exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Config
MODEL_PATH = MODEL_DIR / "price_predictor.pkl"

# Settings
LLM_MODEL = "llama-3.3-70b-versatile"

# --- UNIVERSAL KEY FETCHER ---
def get_api_key(key_name):
    """
    Tries to find the API Key in:
    1. Streamlit Cloud Secrets (Production)
    2. Local Environment Variables (Local Development/Docker)
    """
    # Check Streamlit Secrets first
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except FileNotFoundError:
        pass # Not running on Streamlit Cloud

    # Fallback to OS Environment
    return os.getenv(key_name)

# Export Keys for other modules to use
GROQ_API_KEY = get_api_key("GROQ_API_KEY")
NEWS_API_KEY = get_api_key("NEWS_API_KEY")

# Configure Logging
LOG_FILE = LOGS_DIR / "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE), # Write to file
        logging.StreamHandler()        # Write to terminal
    ]
)
logger = logging.getLogger("FinSight")