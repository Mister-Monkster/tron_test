from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class InfoSchema(BaseModel):
    address: str
    balance: Decimal
    bandwidth: int
    energy: int


class HistorySchema(BaseModel):
    id: int
    address: str
    date: datetime

    model_config = ConfigDict(from_attributes=True)


class AddressRequest(BaseModel):
    address: str