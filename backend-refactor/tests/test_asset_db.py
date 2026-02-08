"""Unit tests for asset_db.get_assets."""
import pytest
from unittest.mock import patch
from database.asset_db import get_assets
from models.signal import SignalModel

@pytest.fixture(autouse=True)
def clear_cache():
    get_assets.cache_clear()
    yield
    get_assets.cache_clear()

def _signal(signal_id, asset_id):
    return SignalModel(
        SignalGId=f"gid-{signal_id}",
        SignalId=signal_id,
        SignalName=f"Signal {signal_id}",
        AssetId=asset_id,
        Unit="kV",
    )

@patch("database.asset_db.load_signals")
def test_groups_signals_by_asset_id(mock_load):
    mock_load.return_value = (
        _signal("1", "A"),
        _signal("2", "A"),
        _signal("3", "B"),
    )
    assets = get_assets()

    assert len(assets) == 2
    asset_a = next(a for a in assets if a.asset_id == "A")
    asset_b = next(a for a in assets if a.asset_id == "B")
    assert len(asset_a.signals) == 2
    assert len(asset_b.signals) == 1

@patch("database.asset_db.load_signals")
def test_empty_signals_returns_empty(mock_load):
    mock_load.return_value = ()
    assets = get_assets()
    assert assets == ()

@patch("database.asset_db.load_signals")
def test_returns_tuple(mock_load):
    mock_load.return_value = (_signal("1", "A"),)
    assets = get_assets()
    assert isinstance(assets, tuple)
