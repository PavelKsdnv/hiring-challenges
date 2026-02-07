"""Measurement service."""
from datetime import datetime
from typing import List, Dict
from utils.date_utils import validate_date_range
from db.measurement_db import get_measurements
import statistics
    
class MeasurementService:
    """Service for managing measurements."""

    def calculate_signal_stats(self, signal_id: str, from_date: datetime, to_date: datetime) -> Dict:
        """Calculate statistics for a signal over a date range."""
        if not validate_date_range(from_date, to_date):
            raise ValueError("Invalid date range")
        
        measurements = get_measurements([signal_id], from_date, to_date)
        
        if not measurements:
            return {
                ""
                "": signal_id,
                "from_date": from_date.isoformat(),
                "to_date": to_date.isoformat(),
                "count": 0,
                "mean": None,
                "min": None,
                "max": None,
                "median": None,
                "std_dev": None
            }
        
        values = [m["value"] for m in measurements]
        
        stats = {
            "signal_id": signal_id,
            "from_date": from_date.isoformat(),
            "to_date": to_date.isoformat(),
            "count": len(values),
            "mean": round(statistics.mean(values), 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "median": round(statistics.median(values), 2),
            "std_dev": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0
        }
        
        return stats