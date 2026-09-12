import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")


class Config:
    """Central configuration for the ORCA application."""

    APP_NAME = "ORCA"
    APP_VERSION = "1.0.0"

    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_PORT", "5000"))

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.1-flash-lite",
    )

    OLLAMA_HOST = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434",
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "mistral:latest",
    )

    DATA_DIR = ROOT_DIR / "data"
    SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"

    SYNTHETIC_DATA_FILE = (
        SYNTHETIC_DATA_DIR / "india_coastal.csv"
    )

    DATA_MODE = "SYNTHETIC_DEMO_DATA"


config = Config()