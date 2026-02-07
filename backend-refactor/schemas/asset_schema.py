"""Asset schema definitions."""
from typing import List
from pydantic import BaseModel
from models.signal import SignalModel

class AssetResponse(BaseModel):
    """Schema for asset API response."""
    asset_id: str
    signals: List[SignalModel]
