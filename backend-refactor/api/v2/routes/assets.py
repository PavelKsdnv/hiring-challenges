"""Assets endpoint (v1)."""
from fastapi import APIRouter, HTTPException
from typing import List
from services.asset_service import AssetService
from schemas.asset_schema import AssetResponse
from utils.helpers import validate_data

router = APIRouter()

asset_service = None
def set_asset_service(service: AssetService):
    asset_service = service

@router.get("/assets", response_model=List[AssetResponse])
async def get_assets():
    """Get all assets with their signals."""
    try:
        assets = asset_service.get_all_assets()
        
        if not validate_data(assets):
            raise HTTPException(status_code=404, detail="No assets found")
        
        return assets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))