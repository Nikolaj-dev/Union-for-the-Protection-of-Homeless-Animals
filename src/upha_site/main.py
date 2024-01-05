from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.upha_site.routes.routes import router as base_route
from src.upha_site.routes.ad_routes import router as ad_route
from src.upha_site.routes.shelter_routes import router as shelter_route
from src.upha_site.routes.animal_routes import router as animal_route


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(base_route, tags=["base"])
app.include_router(ad_route, prefix="/ads", tags=["advertisement"])
app.include_router(shelter_route, prefix="/shelters", tags=["shelters"])
app.include_router(animal_route, prefix="/animals", tags=["animals"])
