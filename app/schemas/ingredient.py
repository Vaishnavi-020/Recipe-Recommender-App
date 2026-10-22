from pydantic import BaseModel,Field
from typing import List

class IngredientMatch(BaseModel):
    ingredient_id:int
    canonical_name:str
    matched_name:str
    match_type:str

class IngredientSearchResponse(BaseModel):
    query:str
    results:List[IngredientMatch]