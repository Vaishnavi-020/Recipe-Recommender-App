from fastapi import APIRouter,Query,Depends
from sqlalchemy.orm import Session
from app.ETL.db_connection import get_db
from app.schemas.ingredient import IngredientSearchResponse
from app.services.ingredient_search import search_ingredients

router=APIRouter(prefix='/ingredients',tags=['Ingredients'])

@router.get("/search",response_model=IngredientSearchResponse)
def search_ingredient(q:str=Query(...,min_length=1,max_length=100,description="Ingredient name to search"),
                      limit:int=Query(10,ge=1,le=50,description="Maximum number of results"),
                      db:Session=Depends(get_db)):
    results=search_ingredients(db=db,query=q,limit=limit)
    return {
        "query":q.strip(),
        "results":results
    }
