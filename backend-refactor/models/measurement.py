"""Measurement model."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MeasurementModel(BaseModel):
    """Measurement data model."""
    signal_id: str
    timestamp: datetime
    value: float
    unit: Optional[str] = None
