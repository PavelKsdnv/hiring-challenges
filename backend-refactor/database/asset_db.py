"""Database operations for assets."""
from functools import lru_cache
from typing import Tuple
from database.signal_db import load_signals
from models.asset import AssetModel

@lru_cache
def get_assets() -> Tuple[AssetModel, ...]:
    """Get all assets grouped by asset_id."""
    signals = load_signals()
    assets_dict = {}

    for signal in signals:
        asset_id = signal.asset_id
        if asset_id not in assets_dict:
            assets_dict[asset_id] = []
        assets_dict[asset_id].append(signal)

    return tuple(AssetModel(asset_id=aid, signals=sigs) for aid, sigs in assets_dict.items())
