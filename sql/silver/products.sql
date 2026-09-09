CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.products` AS

SELECT
    CAST(product_id AS STRING) AS product_id,

    TRIM(LOWER(product_category_name)) AS product_category_name,

    SAFE_CAST(product_name_lenght AS INT64) AS product_name_length,

    SAFE_CAST(product_description_lenght AS INT64)
        AS product_description_length,

    SAFE_CAST(product_photos_qty AS INT64) AS product_photos_qty,

    SAFE_CAST(product_weight_g AS NUMERIC) AS product_weight_g,

    SAFE_CAST(product_length_cm AS NUMERIC) AS product_length_cm,

    SAFE_CAST(product_height_cm AS NUMERIC) AS product_height_cm,

    SAFE_CAST(product_width_cm AS NUMERIC) AS product_width_cm

FROM `seventh-botany-506408-i1.bronze.products`;