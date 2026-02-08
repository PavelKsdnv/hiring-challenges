"""Unit tests for MeasurementService.calculate_signal_stats."""
import pytest
from datetime import datetime
from unittest.mock import patch
from models.measurement import MeasurementModel
from services.measurement_service import MeasurementService

FROM = datetime(2021, 11, 1)
TO = datetime(2021, 11, 8)

def _make_measurements(values, signal_id="1", unit="kV"):
    """Helper to build a list of MeasurementModel from raw values."""
    return [
        MeasurementModel(
            signal_id=signal_id,
            timestamp=datetime(2021, 11, 1, i),
            value=v,
            unit=unit,
        )
        for i, v in enumerate(values)
    ]

@patch("services.measurement_service.get_measurements")
def test_stats_basic(mock_get):
    mock_get.return_value = _make_measurements([10.0, 20.0, 30.0])
    svc = MeasurementService()

    result = svc.calculate_signal_stats("1", FROM, TO)

    assert result.count == 3
    assert result.mean == 20.0
    assert result.min == 10.0
    assert result.max == 30.0
    assert result.median == 20.0
    assert result.std_dev == 10.0

@patch("services.measurement_service.get_measurements")
def test_stats_single_value(mock_get):
    mock_get.return_value = _make_measurements([42.0])
    svc = MeasurementService()

    result = svc.calculate_signal_stats("1", FROM, TO)

    assert result.count == 1
    assert result.mean == 42.0
    assert result.min == 42.0
    assert result.max == 42.0
    assert result.median == 42.0
    assert result.std_dev == 0.0

@patch("services.measurement_service.get_measurements")
def test_stats_empty(mock_get):
    mock_get.return_value = []
    svc = MeasurementService()

    result = svc.calculate_signal_stats("1", FROM, TO)

    assert result.count == 0
    assert result.mean is None
    assert result.min is None
    assert result.max is None

def test_stats_invalid_date_range():
    svc = MeasurementService()

    with pytest.raises(ValueError, match="Invalid date range"):
        svc.calculate_signal_stats("1", TO, FROM)

@patch("services.measurement_service.get_measurements")
def test_stats_rounding(mock_get):
    mock_get.return_value = _make_measurements([1.111, 2.222, 3.333])
    svc = MeasurementService()

    result = svc.calculate_signal_stats("1", FROM, TO)

    assert result.mean == 2.22
    assert result.min == 1.11
    assert result.max == 3.33
