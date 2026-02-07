"""Measurements router (v2 style but registered as v1)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from services.measurement_service import MeasurementService
from schemas.measurement_schema import SignalStatsResponse

router = APIRouter()

def get_measurement_service() -> MeasurementService:
    return MeasurementService()

@router.get("/measurements/stats/{signal_id}", response_model=SignalStatsResponse)
async def get_signal_stats(
    signal_id: str,
    from_date: str = Query(..., alias="from", description="Start date (ISO format)"),
    to_date: str = Query(..., alias="to", description="End date (ISO format)"),
    measurement_service: MeasurementService = Depends(get_measurement_service),
):
    """Calculate statistics for a signal over a date range.

    Returns:
        - count: Number of measurements
        - mean: Average value
        - min: Minimum value
        - max: Maximum value
        - median: Median value
        - std_dev: Standard deviation
    """
    try:
        from_dt = datetime.fromisoformat(from_date)
        to_dt = datetime.fromisoformat(to_date)

        return measurement_service.calculate_signal_stats(signal_id, from_dt, to_dt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating stats: {str(e)}")
