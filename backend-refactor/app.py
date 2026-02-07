"""Application factory and configuration."""
from fastapi import FastAPI
from api.health import health_check
from api.v1.endpoints import assets as assets_v1
from api.v1.endpoints import measurement_legacy as measurements_v1
from api.v2.routes import measurements_router as measurements_v2
from core.config import get_settings
from services.asset_service import AssetService

asset_service = AssetService()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.api_version
    )
    
    assets_v1.set_asset_service(asset_service)
    app.include_router(assets_v1.router, tags=["assets"], prefix="/api/v1")
    app.include_router(assets_v1.router, tags=["assets"], prefix="/api/v2")
    app.include_router(measurements_v1.router, tags=["measurements"], prefix="/api/v1")
    app.include_router(measurements_v2.router, tags=["measurements"], prefix="/api/v2")
    
    app.include_router(health_check.router, tags=['health'], prefix="/api")
    return app
