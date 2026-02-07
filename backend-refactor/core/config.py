"""Core configuration module."""
from functools import lru_cache
from core.settings import AppSettings

@lru_cache() # maybe use a clearer singleton implementation
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()