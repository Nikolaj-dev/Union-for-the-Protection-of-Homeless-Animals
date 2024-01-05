from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/")
async def home():
    text = """You are welcome to Union for the Protection of Homeless Animals!"""
    return {"message": text}


@router.get("/info")
async def get_info():
    text = """The "Union for the Protection of Homeless Animals" is a dedicated initiative aimed at safeguarding and improving the lives of homeless animals. Our mission is to create a unified platform that brings together passionate individuals and organizations committed to the welfare and protection of animals without homes."""
    return {"message": text}


@router.get("/img")
async def img(image_path: str):
    image_path = f"{image_path}"
    return FileResponse(image_path, media_type="image/jpeg")
