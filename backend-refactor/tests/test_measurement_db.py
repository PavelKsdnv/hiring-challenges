"""Unit tests for measurement_db.get_measurements."""
import pytest
from datetime import datetime
from unittest.mock import patch, mock_open
from database.measurement_db import get_measurements
from models.signal import SignalModel

SIGNALS = (
    SignalModel(SignalGId="aaa", SignalId="100", SignalName="S1", AssetId="1", Unit="kV"),
    SignalModel(SignalGId="bbb", SignalId="200", SignalName="S2", AssetId="2", Unit="kW"),
)

FROM = datetime(2021, 11, 1)
TO = datetime(2021, 11, 8)

VALID_CSV = "SignalId|Ts|MeasurementValue\n100|2021-11-02T10:00:00|115,5\n100|2021-11-03T10:00:00|116,0\n"


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", mock_open(read_data=VALID_CSV))
def test_parses_csv_with_european_decimals(_mock_signals):
    results = get_measurements(["100"], FROM, TO)

    assert len(results) == 2
    assert results[0].value == 115.5
    assert results[1].value == 116.0


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", mock_open(read_data=VALID_CSV))
def test_assigns_unit_from_signals(_mock_signals):
    results = get_measurements(["100"], FROM, TO)
    assert all(m.unit == "kV" for m in results)


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", mock_open(read_data=VALID_CSV))
def test_filters_by_signal_id(_mock_signals):
    results = get_measurements(["999"], FROM, TO)
    assert results == []


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", mock_open(read_data=VALID_CSV))
def test_filters_by_date_range(_mock_signals):
    narrow_from = datetime(2021, 11, 2, 9)
    narrow_to = datetime(2021, 11, 2, 11)
    results = get_measurements(["100"], narrow_from, narrow_to)
    assert len(results) == 1


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", side_effect=FileNotFoundError)
def test_missing_file_returns_empty(_mock_open, _mock_signals):
    results = get_measurements(["100"], FROM, TO)
    assert results == []


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", mock_open(
    read_data="SignalId|Ts|MeasurementValue\n100||115,5\n"
))
def test_skips_row_with_missing_timestamp(_mock_signals):
    results = get_measurements(["100"], FROM, TO)
    assert results == []


@patch("database.measurement_db.load_signals", return_value=SIGNALS)
@patch("database.measurement_db.open", mock_open(
    read_data="SignalId|Ts|MeasurementValue\n100|2021-11-02T10:00:00|not_a_number\n"
))
def test_skips_row_with_bad_value(_mock_signals):
    results = get_measurements(["100"], FROM, TO)
    assert results == []
