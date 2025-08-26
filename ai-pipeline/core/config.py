# notical-flashcards-starter/app/config.py
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from the project root .env (if present)
# Root is one level up from /app
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# ----- App metadata -----
APP_NAME = os.getenv("APP_NAME", "Notical Flashcards")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

# ----- Local-first / offline flags -----
# Keep everything free/offline by default
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "true").lower() == "true"

# Device hint for local models; we’ll wire this up later
DEVICE = os.getenv("DEVICE", "cpu")  # "cpu" | "cuda" (if you have a GPU)

# ----- Paths -----
DATA_DIR = PROJECT_ROOT / "data"
EXPORTS_DIR = PROJECT_ROOT / "exports"
LOG_FILE = PROJECT_ROOT / "notical.log"

# Create required dirs if missing
for d in (DATA_DIR, EXPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ----- Limits / safety -----
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))  # PDF max size
ALLOWED_UPLOAD_EXTS = {".pdf"}  # we’ll add images/audio later

# ----- Deck defaults -----
DEFAULT_DECK_TITLE = os.getenv("DEFAULT_DECK_TITLE", "Notical Deck")

# ----- Feature flags (we’ll implement these gradually) -----
ENABLE_SYLLABUS_MAPPING = os.getenv("ENABLE_SYLLABUS_MAPPING", "false").lower() == "true"
ENABLE_EXPORT_CSV = os.getenv("ENABLE_EXPORT_CSV", "true").lower() == "true"
ENABLE_EXPORT_DOC = os.getenv("ENABLE_EXPORT_DOC", "false").lower() == "true"

# (No API keys here—this project is offline-first on purpose)
