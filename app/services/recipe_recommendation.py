
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session


SQL_PATH = (
    Path(__file__).resolve().parent.parent
    / "sql"
    / "recommend_recipes.sql"
)

RECOMMEND_QUERY = text(
    SQL_PATH.read_text(encoding="utf-8")
)

def recommend_recipes(
    db: Session,
    ingredient_ids: list[int],
    page: int = 1,
    page_size: int = 10
) -> dict:

    if page < 1:
        raise ValueError("Page must be greater than or equal to 1")

    if not 1 <= page_size <= 10:
        raise ValueError("Page size must be between 1 and 10")

    selected_ids = sorted(set(ingredient_ids))

    if not selected_ids:
        return {
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
            "results": []
        }

    offset = (page - 1) * page_size

    result = db.execute(
        RECOMMEND_QUERY,
        {
            "ingredient_ids": selected_ids,
            "page_size": page_size,
            "offset": offset
        }
    )

    rows = result.mappings().all()

    # Extract total before processing recipes
    total = rows[0]["total"] if rows else 0

    recipes = [
        {
            "recipe_id": row["recipe_id"],
            "recipe_name": row["recipe_name"],
            "match_percentage": float(row["match_percentage"]),
            "matched_ingredients": row["matched_ingredients"],
            "missing_ingredients": row["missing_ingredients"],
            "matched_count": row["matched_count"],
            "missing_count": row["missing_count"],
            "total_ingredients": row["total_ingredients"],
            "can_make_now": row["can_make_now"],
        }
        for row in rows
    ]

    total_pages = (total + page_size - 1) // page_size

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "results": recipes
    }