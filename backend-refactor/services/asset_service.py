"""Asset service layer."""
from typing import List
from database.asset_db import get_assets
from models.asset import AssetModel


def valid_assets(assets: List[AssetModel]) -> bool:
    """Validate assets list is non-empty."""
    return len(assets) > 0


class AssetService:
    """Service for managing assets."""

    def get_all_assets(self) -> List[AssetModel]:
        """Get all assets with their signals."""
        assets = get_assets()
        if not valid_assets(assets):
            return []
        return assets

    def post_asset(self) -> List[AssetModel]:
        """Placeholder for posting an asset."""
        return []
