
WITH selected_ingredients AS (
    SELECT DISTINCT UNNEST(
        CAST(:ingredient_ids AS BIGINT[])
    ) AS ingredient_id
),

recipe_matches AS (
    SELECT DISTINCT
        r.recipe_id,
        r.recipe_title,
        i.ingredient_id,
        i.canonical_name,
        CASE
            WHEN si.ingredient_id IS NOT NULL
            THEN TRUE
            ELSE FALSE
        END AS is_matched

    FROM recipes r

    JOIN recipe_ingredient ri
        ON r.recipe_id = ri.recipe_id

    JOIN ingredients i
        ON ri.ingredient_id = i.ingredient_id

    LEFT JOIN selected_ingredients si
        ON i.ingredient_id = si.ingredient_id
)

SELECT
    recipe_id,
    recipe_title AS recipe_name,

    COUNT(*) AS total_ingredients,

    COUNT(*) FILTER (
        WHERE is_matched = TRUE
    ) AS matched_count,

    COUNT(*) FILTER (
        WHERE is_matched = FALSE
    ) AS missing_count,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE is_matched = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS match_percentage,

    COALESCE(
        ARRAY_AGG(canonical_name ORDER BY canonical_name)
        FILTER (WHERE is_matched = TRUE),
        ARRAY[]::TEXT[]
    ) AS matched_ingredients,

    COALESCE(
        ARRAY_AGG(canonical_name ORDER BY canonical_name)
        FILTER (WHERE is_matched = FALSE),
        ARRAY[]::TEXT[]
    ) AS missing_ingredients,

    BOOL_AND(is_matched) AS can_make_now

FROM recipe_matches

GROUP BY recipe_id, recipe_title

HAVING COUNT(*) FILTER (
    WHERE is_matched = TRUE
) > 0

ORDER BY
    match_percentage DESC,
    missing_count ASC,
    recipe_name ASC

LIMIT :limit;
