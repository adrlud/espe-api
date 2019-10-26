from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):
    id: int
    name: str
    active: bool
    connected: bool


class Measurement(BaseModel):
    id: int
    created_at: datetime
    device_id: int
    value: float
