
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
    limit: int = 20,
) -> list[dict]:

    # Remove duplicate selections
    selected_ids = list(set(ingredient_ids))

    if not selected_ids:
        return []

    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")

    # Execute the SQL query
    result = db.execute(
        RECOMMEND_QUERY,
        {
            "ingredient_ids": selected_ids,
            "limit": limit,
        },
    )

    # Convert database rows to dictionaries
    rows = result.mappings().all()

    return [
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
