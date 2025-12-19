import os
import logging
from pathlib import Path
from dotenv import load_dotenv

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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_PATH = MODEL_DIR / "price_predictor.pkl"

# Settings
LLM_MODEL = "llama-3.3-70b-versatile"

LOG_FILE = LOGS_DIR / "app.log"

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE), # Write to file
        logging.StreamHandler()        # Write to terminal
    ]
)
logger = logging.getLogger("FinSight")