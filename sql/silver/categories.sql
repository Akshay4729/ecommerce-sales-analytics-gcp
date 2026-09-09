CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.categories` AS

SELECT
    TRIM(LOWER(product_category_name)) AS product_category_name,

    TRIM(LOWER(product_category_name_english))
        AS product_category_name_english

FROM `seventh-botany-506408-i1.bronze.categories`;