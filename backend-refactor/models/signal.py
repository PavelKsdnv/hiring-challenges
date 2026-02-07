"""Signal model definitions."""
from pydantic import BaseModel

class SignalModel(BaseModel):
    """Signal model."""
    SignalGId: str
    SignalId: str
    SignalName: str
    AssetId: str
    Unit: str
