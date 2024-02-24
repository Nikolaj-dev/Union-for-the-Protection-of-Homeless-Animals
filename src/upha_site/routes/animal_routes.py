from datetime import datetime
from fastapi import APIRouter, Form, File, UploadFile
from src.db_handlers.core.orm import AnimalRepository
from uuid import uuid4
from src.upha_site.services import is_empty, upload_image, delete_image
import logging
from src.db_handlers.core.models import SexEnum, SpeciesEnum


router = APIRouter()
logger = logging.getLogger("animals-route")


@router.get("")
async def get_all_animals():
    data = await AnimalRepository().retrieve_all()
    return data


@router.post("/filter")
async def filter_animals(filter_condition: dict):
    data = await AnimalRepository().filter_all(filter_condition)
    return data


@router.post("/create")
async def create_animal(
        name: str = Form(),
        sex: SexEnum = Form(),
        age: int = Form(),
        species: SpeciesEnum = Form(),
        since_time: datetime = Form(),
        shelter_id: int = Form(),
        file: UploadFile = File(...)
):
    try:
        # Generate a unique filename for the uploaded image
        generated_filename = f"{uuid4()}{file.filename}"

        # Prepare data for validation and creation
        data = {
            "name": name,
            "sex": sex,
            "image_path": f"static/animals-images/{generated_filename}",
            "age": age,
            "species": species,
            "since_time": since_time,
            "shelter_id": shelter_id
        }

        # Validate input data
        validation_result = await is_empty(**data)

        if "error" in validation_result:
            return validation_result
        else:
            try:
                # Upload the image
                image_upload_result = await upload_image(
                    file=file,
                    folder="animals-images",
                    generated_filename=generated_filename
                )

                if "error" in image_upload_result:
                    return image_upload_result
                else:
                    # Create a new animal in the repository
                    adv = await AnimalRepository().create(**data)

                    if "error" in adv:
                        # If there's an error in animal creation, delete the uploaded image
                        await delete_image(f"static/animals-images/{generated_filename}")
                        return adv
                    else:
                        return adv
            except Exception as ex:
                await delete_image(f"static/animals-images/{generated_filename}")
                logger.exception(f"{ex.add_note('An error occurred during animal creation')}")
                return {"error": "An error occurred while uploading the image."}
    except Exception as ex:
        logger.exception(f"{ex.add_note('An error occurred during animal creation')}")
        return {"error": "Internal error."}


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
