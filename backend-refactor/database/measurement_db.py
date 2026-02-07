"""Database operations for measurements."""
from datetime import datetime
from typing import List
import csv
from core.config import get_settings
from utils.date_utils import parse_date
from models.measurement import MeasurementModel

def get_measurements(signal_ids: List[str], from_date: datetime, to_date: datetime) -> List[MeasurementModel]:
    """Get measurements for given signal IDs and date range."""
    settings = get_settings()
    measurements = []

    with open(settings.measurements_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            signal_id = row.get("SignalId")
            if signal_id not in signal_ids:
                continue

            ts = parse_date(row.get("Ts"))
            if ts < from_date or ts > to_date:
                continue

            # Parse value (European format uses comma as decimal separator)
            value_str = row.get("MeasurementValue", "0").replace(",", ".")

            measurements.append(MeasurementModel(
                signal_id=signal_id,
                timestamp=ts,
                value=float(value_str),
                unit="kV" # todo add proper unit retrieval
            ))

    return measurements
