"""Database operations for signals."""
import json
from typing import List
from core.config import get_settings
from models.signal import SignalModel

def load_signals() -> List[SignalModel]:
    """Load signals from JSON file."""
    settings = get_settings()
    with open(settings.data_path, 'r') as f:
        data = json.load(f)
    return [SignalModel(**item) for item in data]
