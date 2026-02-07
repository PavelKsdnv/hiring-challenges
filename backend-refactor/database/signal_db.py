"""Database operations for signals."""
import json
import logging
from functools import lru_cache
from typing import Tuple
from pydantic import ValidationError
from core.config import get_settings
from models.signal import SignalModel

logger = logging.getLogger(__name__)

@lru_cache
def load_signals() -> Tuple[SignalModel, ...]:
    """Load signals from JSON file."""
    settings = get_settings()
    try:
        with open(settings.data_path, 'r') as f:
            data = json.load(f)
        return tuple(SignalModel(**item) for item in data)
    except FileNotFoundError:
        logger.warning("Signal data file not found: %s", settings.data_path)
        return ()
    except json.JSONDecodeError:
        logger.warning("Invalid JSON in signal data file: %s", settings.data_path)
        return ()
    except ValidationError as e:
        logger.warning("Signal data validation error: %s", e)
        return ()
