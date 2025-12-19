import os
import sys
import logging
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Project Paths
# Using resolve() ensures we get the absolute path on the Cloud server
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTOR_DB_DIR = DATA_DIR / "vector_store"
MODEL_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "app.log"

# 3. Create Directories (CRITICAL STEP)
# We must create these before trying to write files to them
try:
    for d in [RAW_DATA_DIR, VECTOR_DB_DIR, MODEL_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"⚠️ Warning: Could not create directories: {e}")

# 4. Universal Key Fetcher
def get_api_key(key_name):
    """
    Tries to find the API Key in:
    1. Streamlit Cloud Secrets (Production)
    2. Local Environment Variables (Local Development/Docker)
    """
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except FileNotFoundError:
        pass 
    return os.getenv(key_name)

# Export Keys
GROQ_API_KEY = get_api_key("GROQ_API_KEY")
NEWS_API_KEY = get_api_key("NEWS_API_KEY")

# 5. Robust Logging Setup
# We define handlers list. We ALWAYS want to log to Console (StreamHandler).
# We ONLY log to file if we successfully created the logs directory.
handlers = [logging.StreamHandler(sys.stdout)]

if LOGS_DIR.exists():
    try:
        handlers.append(logging.FileHandler(LOG_FILE))
    except IOError:
        print("⚠️ Warning: Could not write to log file. Using console logging only.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=handlers
)

# Create a global logger
logger = logging.getLogger("FinSight")