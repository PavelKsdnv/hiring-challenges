"""Asset service layer."""
from typing import List, Dict
from database.asset_db import get_assets


def valid_assets(assets: List[Dict]) -> bool:
    """Validate assets have required fields."""
    if not assets:
        return False
    for asset in assets:
        if "asset_id" not in asset:
            return False
        if "signals" not in asset or not isinstance(asset["signals"], list):
            return False
    return True


class AssetService:
    """Service for managing assets."""

    def get_all_assets(self) -> List[Dict]:
        """Get all assets with their signals."""
        assets = get_assets()
        if not valid_assets(assets):
            return []
        return assets
    
    def post_asset(self) -> List[Dict]:
        """Placeholder for posting an asset."""
        # Implementation would go here
        return []
