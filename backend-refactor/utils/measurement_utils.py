"""Measurement utilities."""
from typing import List, Dict
from datetime import datetime

def filter_measurements_by_date(measurements: List[Dict], from_date: datetime, to_date: datetime) -> List[Dict]:
    """Filter measurements by date range."""
    filtered = []
    for m in measurements:
        ts = datetime.fromisoformat(m["timestamp"])
        if from_date <= ts <= to_date:
            filtered.append(m)
    return filtered