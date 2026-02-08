"""Unit tests for signal_db.load_signals."""
import json
import pytest
from unittest.mock import patch, mock_open
from database.signal_db import load_signals

VALID_SIGNALS = json.dumps([
    {"SignalGId": "aaa", "SignalId": "1", "SignalName": "Sig1", "AssetId": "A", "Unit": "kV"},
    {"SignalGId": "bbb", "SignalId": "2", "SignalName": "Sig2", "AssetId": "B", "Unit": "kW"},
])

@pytest.fixture(autouse=True)
def clear_cache():
    load_signals.cache_clear()
    yield
    load_signals.cache_clear()

@patch("database.signal_db.open", mock_open(read_data=VALID_SIGNALS))
def test_load_signals_parses_json():
    signals = load_signals()

    assert len(signals) == 2
    assert signals[0].signal_id == "1"
    assert signals[0].asset_id == "A"
    assert signals[0].unit == "kV"
    assert signals[1].signal_id == "2"

@patch("database.signal_db.open", side_effect=FileNotFoundError)
def test_load_signals_missing_file(mock):
    signals = load_signals()
    assert signals == ()

@patch("database.signal_db.open", mock_open(read_data="not json"))
def test_load_signals_bad_json():
    signals = load_signals()
    assert signals == ()

@patch("database.signal_db.open", mock_open(read_data=json.dumps([{"bad": "data"}])))
def test_load_signals_validation_error():
    signals = load_signals()
    assert signals == ()

@patch("database.signal_db.open", mock_open(read_data=VALID_SIGNALS))
def test_load_signals_returns_tuple():
    signals = load_signals()
    assert isinstance(signals, tuple)

@patch("database.signal_db.open", mock_open(read_data=VALID_SIGNALS))
def test_load_signals_snake_case_fields():
    sig = load_signals()[0]
    assert hasattr(sig, "signal_id")
    assert hasattr(sig, "signal_name")
    assert hasattr(sig, "signal_gid")
    assert hasattr(sig, "asset_id")
    assert hasattr(sig, "unit")
