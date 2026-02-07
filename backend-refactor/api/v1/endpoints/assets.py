"""Assets endpoint (v1)."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services.asset_service import AssetService, valid_assets
from schemas.asset_schema import AssetResponse

router = APIRouter()

def get_asset_service() -> AssetService:
    return AssetService()

@router.get("/assets", response_model=List[AssetResponse], response_model_by_alias=False)
async def get_assets(asset_service: AssetService = Depends(get_asset_service)):
    """Get all assets with their signals."""
    try:
        assets = asset_service.get_all_assets()

        if not valid_assets(assets):
            raise HTTPException(status_code=404, detail="No assets found")

        return assets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
