"""Database operations for measurements."""
from datetime import datetime
from typing import List, Dict, Optional
import csv
from core.config import get_settings
from utils.date_utils import parse_date

def get_measurements(signal_ids: List[str], from_date: datetime, to_date: datetime) -> List[Dict]:
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

            measurements.append({
                "signal_id": signal_id,
                "timestamp": ts.isoformat(),
                "value": float(value_str),
                "unit": "kV"
            })

    return measurements