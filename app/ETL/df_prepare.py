import json
import pandas as pd
from .db_connection import engine

recipes_df=pd.read_pickle('recipes_processed.pkl')
metadata_df=pd.read_pickle('ingredient_metadata_processed.pkl')

def prepare_for_postgres(df):
    df=df.copy()

    for col in df.columns:
        def convert(value):
            if isinstance(value,(list,dict)):
                return json.dumps(value,ensure_ascii=False)
            return value
        df[col]=df[col].map(convert)
    return df

final_recipe=recipes_df.drop(
    columns=['ingredient_metadata'],
    errors='ignore'
)

recipes_to_load=prepare_for_postgres(final_recipe)
metadata_to_load=prepare_for_postgres(metadata_df)

recipes_to_load.to_sql(
    name='recipes_staging',
    con=engine,
    if_exists='replace',
    index=False,
    chunksize=1000
)

metadata_to_load.to_sql(
    name='ingredient_metadata_staging',
    con=engine,
    if_exists='replace',
    index=False,
    chunksize=1000
)

print('Both Dataframes loaded successfully!')