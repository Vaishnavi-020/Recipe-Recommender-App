WITH total_recipes AS(
    SELECT COUNT(*) AS n
    FROM recipes
),
ingredient_frequency AS(
    SELECT ingredient_id,
    COUNT(DISTINCT recipe_id) AS df
    FROM recipe_ingredient
    GROUP BY ingredient_id
)

SELECT ingredient_id,df,1+LN((n+1.0)/(df+1.0)) AS idf_weight
FROM ingredient_frequency 
CROSS JOIN total_recipes;