from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):
    id: int
    name: str


class Measurement(BaseModel):
    id: int
    created_at: datetime
    device_id: int
    value: float
