from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScanInput(BaseModel):
serial_number: str
vendor: Optional[str] = None
model: Optional[str] = None
user_id: int


class DeviceOut(BaseModel):
id: int
serial_number: str
vendor: Optional[str]
model: Optional[str]
category: Optional[str]
user_id: int
date_added: datetime


class Config:
orm_mode = True