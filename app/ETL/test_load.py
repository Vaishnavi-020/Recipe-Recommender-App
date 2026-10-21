import pandas as pd
from .db_connection import engine

recipes = pd.read_sql_table("recipes_staging", engine)
metadata = pd.read_sql_table(
    "ingredient_metadata_staging", engine
)

print("Recipes shape:", recipes.shape)
print("Metadata shape:", metadata.shape)

print(recipes.head())
print(metadata.head())