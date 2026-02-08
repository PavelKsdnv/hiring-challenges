"""Application settings and environment variables."""
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    """Application settings loaded from environment."""
    app_name: str = "AssetAPI"
    debug_mode: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    data_path: str = "data/signal.json"
    measurements_path: str = "data/measurements.csv"
    
    class Config:
        env_file = ".env"
