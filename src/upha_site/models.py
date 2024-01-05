from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.db_handlers.core.models import SexEnum, SpeciesEnum


class ShelterCreate(BaseModel):
    title: str
    address: str
    phone_number: str
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None


class AnimalCreate(BaseModel):
    name: str
    sex: SexEnum
    age: int
    species: SpeciesEnum
    since_time: datetime = Field(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    shelter_id: int


