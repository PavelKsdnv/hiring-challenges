"""Database operations for signals."""
import json
from typing import List, Dict, Optional
from core.config import get_settings

def load_signals() -> List[Dict]:
    """Load signals from JSON file."""
    settings = get_settings()
    with open(settings.data_path, 'r') as f:
        return json.load(f)