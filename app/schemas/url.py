from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    original_url: str

    # expiration_time: Optional[int] = None  # Expiration in days, optional
    expiration_time: Optional[datetime] = None  # Expiration in days, optional


class URLResponse(BaseModel):
    short_url: str
    original_url: str
    expiration_time: Optional[datetime] = None

    class Config:
        orm_mode = True # This tells Pydantic to work with SQLAlchemy models