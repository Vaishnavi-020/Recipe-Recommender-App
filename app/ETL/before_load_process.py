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
]

for col in text_cols:
    metadata[col] = metadata[col].map(
        lambda x: x.strip().lower()
        if isinstance(x, str) else x
    )

metadata = metadata.replace(r"^\s*$", pd.NA, regex=True)

# ----------------------------------------
# 1. VALID METADATA
# ----------------------------------------

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

# ----------------------------------------
# 2. RAW TO BASE MAPPING
# ----------------------------------------

# IMPORTANT:
# Include ALL classifications, including 'not sure'.
# Every valid raw ingredient must map to its base name.

raw_to_base = (
    metadata_valid
    .drop_duplicates("raw")
    .set_index("raw")["base"]
    .to_dict()
)

# ----------------------------------------
# 3. ALIAS MAPPINGS
# ----------------------------------------

# Only explicitly classified aliases are included.

aliases_df = metadata_valid[
    (metadata_valid["parenthetical_type"] == "alias")
    & metadata_valid["parenthetical"].notna()
][["base", "parenthetical"]].drop_duplicates()

# ----------------------------------------
# 4. ATTRIBUTE MAPPINGS
# ----------------------------------------

attribute_df = metadata_valid[
    (metadata_valid["parenthetical_type"] == "attribute")
    & metadata_valid["parenthetical"].notna()
][["base", "parenthetical"]].drop_duplicates()

# Create lookup for raw ingredient -> attribute.
attribute_lookup = (
    metadata_valid[
        metadata_valid["parenthetical_type"] == "attribute"
    ]
    .drop_duplicates("raw")
    .set_index("raw")["parenthetical"]
    .to_dict()
)

# ----------------------------------------
# 5. VALIDATION
# ----------------------------------------

print("Converted successfully")

print("Unique raw ingredients:", len(raw_to_base))
print("Alias mappings:", len(aliases_df))
print(
    "Attribute mappings:",
    len(attribute_df)
)

print(
    "Not sure rows:",
    metadata_valid["parenthetical_type"].eq("not sure").sum()
)

