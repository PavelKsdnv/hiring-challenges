"""Measurement service."""
from datetime import datetime
from utils.date_utils import validate_date_range
from database.measurement_db import get_measurements
from schemas.measurement_schema import SignalStatsResponse
import statistics

class MeasurementService:
    """Service for managing measurements."""

    def calculate_signal_stats(self, signal_id: str, from_date: datetime, to_date: datetime) -> SignalStatsResponse:
        """Calculate statistics for a signal over a date range."""
        if not validate_date_range(from_date, to_date):
            raise ValueError("Invalid date range")

        measurements = get_measurements([signal_id], from_date, to_date)

        if not measurements:
            return SignalStatsResponse(
                signal_id=signal_id,
                from_date=from_date.isoformat(),
                to_date=to_date.isoformat(),
                count=0,
            )

        values = [m.value for m in measurements]

        return SignalStatsResponse(
            signal_id=signal_id,
            from_date=from_date.isoformat(),
            to_date=to_date.isoformat(),
            count=len(values),
            mean=round(statistics.mean(values), 2),
            min=round(min(values), 2),
            max=round(max(values), 2),
            median=round(statistics.median(values), 2),
            std_dev=round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
        )
