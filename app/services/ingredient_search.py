from fastapi import HTTPException
from sqlalchemy import select,func
from sqlalchemy.orm import Session

from app.models.ingredients import Ingredients
from app.models.alias_names import AliasNames
from app.models.recipe_ingredients import RecipeIngredient
from app.models.recipe import Recipe

def search_ingredients(db:Session,query:str,limit:int=10,)->list[dict]:
    """
    Search ingredients using:
    1. Exact canonical name
    2. Exact alternative name (alias)
    3. Partial canonical name
    4. Partial alias

    Returns normalized ingredient search results.
    """
    query=query.strip().lower()
    if not query:
        return []
    if limit<1:
        raise ValueError("Limit must be greater than zero")
    results=[]
    seen_ids=set()

    # 1. Exact canonical name match
    exact_canonical=db.execute(
        select(Ingredients).where(
            func.lower(Ingredients.canonical_name)==query
            ).limit(limit)
    ).scalars().all()
    for ingredient in exact_canonical:
        if ingredient.ingredient_id not in seen_ids:
            results.append({
                "ingredient_id":ingredient.ingredient_id,
                "canonical_name":ingredient.canonical_name,
                "matched_name":ingredient.canonical_name,
                "match_type":'exact',
            })
            seen_ids.add(ingredient.ingredient_id)
        
    # 2. Exact alias match
    if len(results)<limit:
        exact_aliases=db.execute(
            select(Ingredients,AliasNames).join(AliasNames,AliasNames.ingredient_id==Ingredients.ingredient_id)
            .where(
                func.lower(AliasNames.alias_name)==query
            ).limit(limit)                       
        ).all()
        for ingredient,alias in exact_aliases:
            if ingredient.ingredient_id not in seen_ids:
                results.append({
                    "ingredient_id":ingredient.ingredient_id,
                    "canonical_name":ingredient.canonical_name,
                    "matched_name":alias.alias_name,
                    "match_type":"alias",
                })
                seen_ids.add(ingredient.ingredient_id)

        # 3. Partial canonical name match
        if len(results)<limit:
            pattern=f"{query}%"
            partial_canonical=db.execute(
                select(Ingredients).where(
                    func.lower(Ingredients.canonical_name).like(pattern)
                ).limit(limit)
            ).scalars().all()

            for ingredient in partial_canonical:
                if ingredient.ingredient_id not in seen_ids:
                    results.append({
                        "ingredient_id":ingredient.ingredient_id,
                        "canonical_name":ingredient.canonical_name,
                        "matched_name":ingredient.canonical_name,
                        "match_type":"partial",
                    })
                    seen_ids.add(ingredient.ingredient_id)
        
        # 4. Partial alias match
        if len(results)<limit:
            partial_alias=db.execute(select(Ingredients,AliasNames)
                                     .join(AliasNames,AliasNames.ingredient_id==Ingredients.ingredient_id)
                                     .where(func.lower(AliasNames.alias_name).like(f"{query}%"))
                                     .limit(limit)).all()
            for ingredient,alias in partial_alias:
                if ingredient.ingredient_id not in seen_ids:
                    results.append({
                        "ingredient_id":ingredient.ingredient_id,
                        "canonical_name":ingredient.canonical_name,
                        "matched_name":alias.alias_name,
                        "match_type":"partial_alias",
                    })
                    seen_ids.add(ingredient.ingredient_id)

    return results[:limit]