from pydantic import BaseModel
from typing import Optional


class ShelterCreate(BaseModel):
    title: str
    address: str
    phone_number: str
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None
