-- Grain: one row per product.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.products` AS
SELECT
  product_id,
  NULLIF(TRIM(product_category_name), '') AS product_category_name,
  NULLIF(TRIM(product_category_name), '') IS NULL AS is_missing_category,
  SAFE_CAST(product_name_lenght AS INT64) AS product_name_length,
  SAFE_CAST(product_description_lenght AS INT64) AS product_description_length,
  SAFE_CAST(product_photos_qty AS INT64) AS product_photos_qty,
  SAFE_CAST(product_weight_g AS FLOAT64) AS product_weight_g,
  SAFE_CAST(product_length_cm AS FLOAT64) AS product_length_cm,
  SAFE_CAST(product_height_cm AS FLOAT64) AS product_height_cm,
  SAFE_CAST(product_width_cm AS FLOAT64) AS product_width_cm,
  SAFE_CAST(product_weight_g AS FLOAT64) <= 0 AS is_invalid_weight,
  SAFE_CAST(product_length_cm AS FLOAT64) <= 0 AS is_invalid_length,
  SAFE_CAST(product_height_cm AS FLOAT64) <= 0 AS is_invalid_height,
  SAFE_CAST(product_width_cm AS FLOAT64) <= 0 AS is_invalid_width,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.products`;
