"""Asset model definition."""
from typing import List
from pydantic import BaseModel
from models.signal import SignalModel

class AssetModel(BaseModel):
    """Asset model with signals."""
    asset_id: str
    signals: List[SignalModel]
