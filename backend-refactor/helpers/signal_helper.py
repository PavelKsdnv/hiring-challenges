"""Signal helpers."""
from typing import List, Dict, Optional

def get_signal_by_id(signal_id: str, signals: List[Dict]) -> Optional[Dict]:
    """Get a signal by ID."""
    for signal in signals:
        if signal.get("SignalId") == signal_id:
            return signal
    return None

def find_signal(sid: str, data: List[Dict]) -> Optional[Dict]:
    """Yet another way to find signals."""
    return next((s for s in data if s.get("SignalId") == sid), None)

def filter_signals_by_asset(asset_id: str, signals: List[Dict]) -> List[Dict]:
    """Filter signals by asset ID."""
    return [s for s in signals if s.get("AssetId") == asset_id]
