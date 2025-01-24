-- flattened restrictions, children first
WITH RECURSIVE restriction_hierarchy AS (
    SELECT
        c.id AS child_id,
        c.first_name AS child_name,
        c_rstr.dietaryrestriction_id AS rstr_id,
        rstr.name_it AS rstr_name
    FROM mealplanner_child c
    INNER JOIN mealplanner_child_dietary_restrictions c_rstr
        ON c.id = c_rstr.child_id
    INNER JOIN mealplanner_dietaryrestriction rstr
        ON c_rstr.dietaryrestriction_id = rstr.id

    UNION

    SELECT
        rh.child_id,
        rh.child_name,
        rstr_incl.to_dietaryrestriction_id,
        rstr.name_it
    FROM restriction_hierarchy rh
    INNER JOIN mealplanner_dietaryrestriction_included_restrictions rstr_incl
        ON rh.rstr_id = rstr_incl.from_dietaryrestriction_id
    INNER JOIN mealplanner_dietaryrestriction rstr
        ON rstr_incl.to_dietaryrestriction_id = rstr.id
)
SELECT DISTINCT
    child_id,
    child_name,
    rstr_id,
    rstr_name
FROM restriction_hierarchy
ORDER BY child_id, rstr_name;

-- flattened restrictions, children first, only IDs
WITH RECURSIVE restriction_hierarchy AS (
    SELECT
        c.id AS child_id,
        c_rstr.dietaryrestriction_id AS rstr_id
    FROM mealplanner_child c
    INNER JOIN mealplanner_child_dietary_restrictions c_rstr
        ON c.id = c_rstr.child_id

    UNION

    SELECT
        rh.child_id,
        rstr_incl.to_dietaryrestriction_id
    FROM restriction_hierarchy rh
    INNER JOIN mealplanner_dietaryrestriction_included_restrictions rstr_incl
        ON rh.rstr_id = rstr_incl.from_dietaryrestriction_id
)
SELECT DISTINCT
    child_id,
    rstr_id
FROM restriction_hierarchy
ORDER BY child_id, rstr_id;

-- flattened restrictions, restrictions first, only IDs
WITH RECURSIVE restriction_hierarchy AS (
    SELECT
        rstr.id AS rstr_id,
        c_rstr.child_id
    FROM mealplanner_dietaryrestriction rstr
    INNER JOIN mealplanner_child_dietary_restrictions c_rstr
        ON rstr.id = c_rstr.dietaryrestriction_id

    UNION

    SELECT
        rstr_incl.to_dietaryrestriction_id,
        rh.child_id
    FROM restriction_hierarchy rh
    INNER JOIN mealplanner_dietaryrestriction_included_restrictions rstr_incl
        ON rh.rstr_id = rstr_incl.from_dietaryrestriction_id
)
SELECT DISTINCT
    rstr_id,
    child_id
FROM restriction_hierarchy
ORDER BY rstr_id, child_id;

-- flattened restrictions, restrictions first, only IDs, starting from a subset of restrictions
WITH RECURSIVE restriction_hierarchy AS (
    SELECT
        rstr.id AS rstr_id,
        c_rstr.child_id
    FROM mealplanner_dietaryrestriction rstr
    INNER JOIN mealplanner_child_dietary_restrictions c_rstr
        ON rstr.id = c_rstr.dietaryrestriction_id
    WHERE rstr.id IN (
        '6d7587c807954a059b29d6e4707667e4'
    )

    UNION

    SELECT
        rstr_incl.to_dietaryrestriction_id,
        rh.child_id
    FROM restriction_hierarchy rh
    INNER JOIN mealplanner_dietaryrestriction_included_restrictions rstr_incl
        ON rh.rstr_id = rstr_incl.from_dietaryrestriction_id
)
SELECT DISTINCT
    rstr_id,
    child_id
FROM restriction_hierarchy
ORDER BY rstr_id, child_id;