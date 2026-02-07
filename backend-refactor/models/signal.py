"""Signal model definitions."""
from pydantic import BaseModel, ConfigDict, Field

class SignalModel(BaseModel):
    """Signal model."""
    model_config = ConfigDict(populate_by_name=True)

    signal_gid: str = Field(alias="SignalGId")
    signal_id: str = Field(alias="SignalId")
    signal_name: str = Field(alias="SignalName")
    asset_id: str = Field(alias="AssetId")
    unit: str = Field(alias="Unit")
