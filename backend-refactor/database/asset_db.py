"""Database operations for assets."""
from typing import List
from database.signal_db import load_signals
from models.asset import AssetModel

def get_assets() -> List[AssetModel]:
    """Get all assets grouped by asset_id."""
    signals = load_signals()
    assets_dict = {}

    for signal in signals:
        asset_id = signal.AssetId
        if asset_id not in assets_dict:
            assets_dict[asset_id] = []
        assets_dict[asset_id].append(signal)

    return [AssetModel(asset_id=aid, signals=sigs) for aid, sigs in assets_dict.items()]
