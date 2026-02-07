"""Database operations for measurements."""
from datetime import datetime
from typing import List
import csv
import logging
from core.config import get_settings
from utils.date_utils import parse_date
from models.measurement import MeasurementModel
from database.signal_db import load_signals

logger = logging.getLogger(__name__)

def get_measurements(signal_ids: List[str], from_date: datetime, to_date: datetime) -> List[MeasurementModel]:
    """Get measurements for given signal IDs and date range."""
    settings = get_settings()

    # Get correct units per signal (kV/kW)
    unit_map = {s.signal_id: s.unit for s in load_signals()}

    try:
        file = open(settings.measurements_path, 'r', encoding='utf-8-sig')
    except FileNotFoundError:
        logger.warning("Measurements file not found: %s", settings.measurements_path)
        return []

    measurements = []
    with file:
        reader = csv.DictReader(file, delimiter='|')
        for row in reader:
            signal_id = row.get("SignalId")
            if signal_id not in signal_ids:
                continue

            ts_raw = row.get("Ts")
            if not ts_raw:
                continue
            try:
                ts = parse_date(ts_raw)
            except (ValueError, TypeError):
                continue

            if ts < from_date or ts > to_date:
                continue

            value_str = row.get("MeasurementValue", "").replace(",", ".")
            try:
                value = float(value_str)
            except (ValueError, TypeError):
                continue

            measurements.append(MeasurementModel(
                signal_id=signal_id,
                timestamp=ts,
                value=value,
                unit=unit_map.get(signal_id, ""),
            ))

    return measurements
