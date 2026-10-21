import pandas as pd

recipes_df=pd.read_pickle('recipes_processed.pkl')
metadata_df=pd.read_pickle('ingredient_metadata_processed.pkl')

print('Recipes:',recipes_df.shape)
print('Metadata:',metadata_df.shape)

print(recipes_df.head())
print(metadata_df.head())