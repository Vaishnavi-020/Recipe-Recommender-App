import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db_connection import engine
from app.models.ingredients import Ingredients
from app.models.recipe_ingredients import RecipeIngredient
from app.models.recipe import Recipe
from app.models.alias_names import AliasNames
from .before_load_process import raw_to_base,aliases_df,attribute_lookup
from .df_prepare import recipes_df

canonical_names=sorted(set(raw_to_base.values()))

with Session(engine) as session:
    try:
        ingredient_objects=[
            Ingredients(canonical_name=name)
            for name in canonical_names
        ]

        session.add_all(ingredient_objects)
        session.flush()

        ingredient_ids={
            obj.canonical_name:obj.ingredient_id
            for obj in ingredient_objects
        }

        existing_aliases=set(session.scalars(
            select(AliasNames.alias_name)
        ).all())
        alias_objects=[]
        for row in aliases_df.itertuples(index=False):
            base=row.base
            alias=row.parenthetical

            if pd.isna(alias) or pd.isna(base):
                continue
            alias=alias.strip().lower()
            if alias in existing_aliases:
                continue
            ingredient_id=ingredient_ids[base]
            alias_objects.append(AliasNames(
                ingredient_id=ingredient_id,
                alias_name=alias
            ))
            existing_aliases.add(alias)
        session.add_all(alias_objects)

        for row in recipes_df.itertuples(index=False):
            recipe=Recipe(
                recipe_title=row.Recipe_title,
                cuisine=row.Cuisine,
                instructions=row.Instructions,
                total_time_minutes=row.TotalTimeInMins,
                url=row.recipe_url,
                image_url=row.image_url
            )

            session.add(recipe)
            session.flush()

            seen=set()
            for raw_name in row.Cleaned_Ingredients:
                if not raw_name or raw_name in seen:
                    continue
                seen.add(raw_name)
                base=raw_to_base.get(raw_name)
                if base is None:
                    print('Unmatched Ingredeint:',raw_name)
                    continue
                ingredient_id=ingredient_ids[base]
                attribute=attribute_lookup.get(raw_name)

                link=RecipeIngredient(
                    recipe_id=recipe.recipe_id,
                    ingredient_id=ingredient_id,
                    raw_ingredient_name=raw_name,
                    ingredient_attribute=(
                        attribute if pd.notna(attribute) else None
                    )
                )
                session.add(link)
        session.commit()

        print("ETL completed successfully :)")
    except:
        session.rollback()
        raise