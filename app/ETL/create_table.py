from .db_connection import engine
from app.models.base import Base

# Import every model so SQLAlchemy registers its tables.
from app.models.recipe import Recipe
from app.models.ingredients import Ingredients
from app.models.alias_names import AliasNames
from app.models.recipe_ingredients import RecipeIngredient


# Create tables that don't already exist.
Base.metadata.create_all(engine)

print("Tables created successfully!")