from fastapi import APIRouter
from src.db_handlers.core.orm import ShelterRepository
from src.upha_site.models import ShelterCreate


router = APIRouter()


@router.get("")
async def get_all_shelters():
    data = await ShelterRepository().retrieve_all()
    return data


@router.post("/filter")
async def filter_shelter(filter_condition: dict):
    data = await ShelterRepository().filter_all(filter_condition)
    return data


@router.post("/create")
async def create_shelter(new_shelter: ShelterCreate):
    data = await ShelterRepository().create(**new_shelter.dict())
    return data


@router.get("/{pk}")
async def get_one_shelter(pk: int):
    data = await ShelterRepository().retrieve_one(pk=pk)
    return data


@router.delete("/{pk}/delete")
async def delete_shelter(pk: int):
    data = await ShelterRepository().delete(pk=pk)
    return data


@router.patch("/{pk}/update")
async def update_shelter(pk: int, new_data: dict):
    data = await ShelterRepository().update(pk=pk, new_data=new_data)
    return data
