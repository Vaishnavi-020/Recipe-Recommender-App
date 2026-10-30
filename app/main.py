from fastapi import FastAPI
from app.routers.search_ingredeint import router as ingredient_router
from app.routers.recommendation import router as recommender_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="Recipe Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ingredient_router)
app.include_router(recommender_router)