from fastapi import APIRouter, UploadFile, File, Form
from src.db_handlers.core.orm import AdvertisementRepository
from uuid import uuid4
from src.upha_site.services import upload_image, delete_image, is_empty
import logging


router = APIRouter()
logger = logging.getLogger("ads-route")


@router.get("")
async def get_all_ads():
    data = await AdvertisementRepository().retrieve_all()
    return data


@router.post("/filter")
async def filter_ads(filter_condition: dict):
    data = await AdvertisementRepository().filter_all(filter_condition)
    return data


@router.post("/filter-by-time")
async def filter_ads_by_time(days: int):
    data = await AdvertisementRepository().filter_by_time(days)
    return data


@router.post("/create")
async def create_ad(title: str = Form(), body: str = Form(), file: UploadFile = File(...)):
    try:
        # Generate a unique filename for the uploaded image
        generated_filename = f"{uuid4()}{file.filename}"

        # Prepare data for validation and creation
        data = {
            "title": title,
            "body": body,
            "image_path": f"static/ads-images/{generated_filename}"
        }

        # Validate input data
        validation_result = await is_empty(**data)

        if "error" in validation_result:
            return validation_result
        else:
            try:
                # Upload the image
                image_upload_result = await upload_image(file=file, generated_filename=generated_filename)

                if "error" in image_upload_result:
                    return image_upload_result
                else:
                    # Create a new advertisement in the repository
                    adv = await AdvertisementRepository().create(**{
                        "title": title,
                        "body": body,
                        "image_path": f"static/ads-images/{generated_filename}"
                    })

                    if "error" in adv:
                        # If there's an error in advertisement creation, delete the uploaded image
                        await delete_image(f"static/ads-images/{generated_filename}")
                        return adv
                    else:
                        return adv
            except Exception as ex:
                logger.exception(f"An error occurred during ad creation: {ex}")
                return {"error": "Internal error."}
    except Exception as ex:
        logger.exception(f"An error occurred during ad creation: {ex}")
        return {"error": "Internal error."}


@router.get("/{pk}")
async def get_one_ad(pk: int):
    data = await AdvertisementRepository().retrieve_one(pk=pk)
    return data


@router.delete("/{pk}/delete")
async def delete_ad(pk: int):
    data = await AdvertisementRepository().delete(pk=pk)
    return data


@router.patch("/{pk}/update")
async def update_ad(pk: int, new_data: dict):
    data = await AdvertisementRepository().update(pk=pk, new_data=new_data)
    return data
