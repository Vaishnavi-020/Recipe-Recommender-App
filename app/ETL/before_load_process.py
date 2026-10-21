import pandas as pd
from .db_connection import engine

recipes = pd.read_sql_table("recipes_staging", engine)
metadata = pd.read_sql_table("ingredient_metadata_staging", engine)

print(recipes.shape)
print(metadata.shape)
print(recipes.columns.tolist())
print(metadata.columns.tolist())

metadata = metadata.copy()

text_cols = [
    "raw",
    "base",
    "parenthetical",
    "parenthetical_type",
    "ingredient_attribute",
]

for col in text_cols:
    metadata[col] = metadata[col].map(
        lambda x: x.strip().lower()
        if isinstance(x, str) else x
    )

metadata = metadata.replace(r"^\s*$", pd.NA, regex=True)

metadata_valid = metadata.dropna(
    subset=["raw", "base"]
).copy()

# Check whether a raw name maps to multiple canonical names.
conflicts = (
    metadata_valid.groupby("raw")["base"].nunique()
)

if (conflicts > 1).any():
    raise ValueError(
        "Resolve raw-to-base conflicts before loading."
    )

# One raw ingredient name -> one canonical ingredient.
raw_to_base = (
    metadata_valid
    .drop_duplicates("raw")
    .set_index("raw")["base"]
    .to_dict()
)

print("Converted successfully")

# Only parentheticals explicitly classified as aliases.
aliases_df = metadata_valid[
    (metadata_valid["parenthetical_type"] == "alias")
    & metadata_valid["parenthetical"].notna()
][["base", "parenthetical"]].drop_duplicates()

# Determine the effective attribute.
metadata_valid["effective_attribute"] = (
    metadata_valid["ingredient_attribute"]
)

mask = (
    metadata_valid["parenthetical_type"].eq("attribute")
    & metadata_valid["parenthetical"].notna()
)

# If the parenthetical itself is an attribute, use it.
metadata_valid.loc[mask, "effective_attribute"] = (
    metadata_valid.loc[mask, "parenthetical"]
)

attribute_lookup = (
    metadata_valid
    .drop_duplicates("raw")
    .set_index("raw")["effective_attribute"]
    .to_dict()
)
