"""Main entry point for the application."""
import uvicorn
from app import create_app
from core.config import get_settings

app = create_app()
if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host=settings.host, port=settings.port, log_level=settings.log_level, reload=True)