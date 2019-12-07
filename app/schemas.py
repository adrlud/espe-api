from datetime import datetime

from pydantic import BaseModel
from typing import Optional

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

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None

