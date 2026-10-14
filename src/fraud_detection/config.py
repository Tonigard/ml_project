from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "artifacts" / "fraud_detection.pkl"


class Settings(BaseSettings):
    model_path: str = str(DEFAULT_MODEL_PATH)
    database_url: str | None = None
    log_level: str = "INFO"
    FEATURE_LIST: ClassVar[list[str]] = joblib.load(DEFAULT_MODEL_PATH)["selected_features"]


settings = Settings()
