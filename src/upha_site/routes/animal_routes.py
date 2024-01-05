from fastapi import APIRouter
from src.upha_site.models import AnimalCreate
from src.db_handlers.core.orm import AnimalRepository

router = APIRouter()


@router.get("")
async def get_all_animals():
    data = await AnimalRepository().retrieve_all()
    return data


@router.post("/filter")
async def filter_animals(filter_condition: dict):
    data = await AnimalRepository().filter_all(filter_condition)
    return data


@router.post("/create")
async def create_animal(new_ad: AnimalCreate):
    data = await AnimalRepository().create(**new_ad.dict())
    return data


@router.get("/{pk}")
async def get_one_animal(pk: int):
    data = await AnimalRepository().retrieve_one(pk=pk)
    return data


@router.delete("/{pk}/delete")
async def delete_animal(pk: int):
    data = await AnimalRepository().delete(pk=pk)
    return data


@router.patch("/{pk}/update")
async def update_animal(pk: int, new_data: dict):
    data = await AnimalRepository().update(pk=pk, new_data=new_data)
    return data
