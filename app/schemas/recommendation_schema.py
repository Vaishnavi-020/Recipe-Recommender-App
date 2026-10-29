from pydantic import BaseModel,Field

class RecipeRecommendationRequest(BaseModel):
    ingredient_ids:list[int]=Field(
        min_length=1,
        max_length=100,
        description='IDs of ingredients selected by the user'
    )

class RecipeRecommendationItem(BaseModel):
    recipe_id:int
    recipe_name:str
    match_percentage: float
    matched_ingredients: list[str]
    missing_ingredients: list[str]
    matched_count: int
    missing_count: int
    total_ingredients: int
    can_make_now: bool

class RecipeRecommendationResponse(BaseModel):
    selected_ingredient_ids: list[int]
    results: list[RecipeRecommendationItem]