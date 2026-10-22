from fastapi import FastAPI
from app.routers.search_ingredeint import router as ingredient_router

app=FastAPI(title="Recipe Recommender API")

app.include_router(ingredient_router)