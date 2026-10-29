from fastapi import FastAPI
from app.routers.search_ingredeint import router as ingredient_router
from app.routers.recommendation import router as recommender_router

app=FastAPI(title="Recipe Recommender API")

app.include_router(ingredient_router)
app.include_router(recommender_router)