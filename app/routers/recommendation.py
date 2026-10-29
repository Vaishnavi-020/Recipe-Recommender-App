
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ETL.db_connection import get_db
from app.schemas.recommendation_schema import (
    RecipeRecommendationRequest,
    RecipeRecommendationResponse,
)
from app.services.recipe_recommendation import recommend_recipes

router = APIRouter(
    prefix="/recipes",
    tags=["Recipe Recommendations"],
)


@router.post(
    "/recommend",
    response_model=RecipeRecommendationResponse,
)
def get_recommendations(
    payload: RecipeRecommendationRequest,
    db: Session = Depends(get_db),
):
    # Remove duplicate ingredient IDs
    selected_ids = list(set(payload.ingredient_ids))

    # Handle an empty selection
    if not selected_ids:
        raise HTTPException(
            status_code=400,
            detail="Please select at least one ingredient.",
        )

    # Get recommendations using the SQL-based service
    results = recommend_recipes(
        db=db,
        ingredient_ids=selected_ids,
        limit=20,
    )

    # Return the response in the expected schema
    return {
        "selected_ingredient_ids": selected_ids,
        "results": results,
    }
