CREATE OR REPLACE TABLE
    `seventh-botany-506408-i1.gold.dim_category`
AS

SELECT
    ROW_NUMBER() OVER (
        ORDER BY product_category_name,
                 product_category_name_english
    ) AS category_key,
    product_category_name,
    product_category_name_english

FROM
    `seventh-botany-506408-i1.silver.categories`;