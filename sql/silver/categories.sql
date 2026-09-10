CREATE OR REPLACE TABLE
  `seventh-botany-506408-i1.silver.categories` AS

SELECT
    TRIM(LOWER(string_field_0)) AS product_category_name,
    TRIM(LOWER(string_field_1)) AS product_category_name_english
FROM
  `seventh-botany-506408-i1.bronze.categories`;