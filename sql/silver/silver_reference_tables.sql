-- Customer and seller records retain source identity while using the safe ZIP lookup.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.customers` AS
SELECT
  customer_id,
  customer_unique_id,
  SAFE_CAST(customer_zip_code_prefix AS INT64) AS customer_zip_code_prefix,
  LOWER(TRIM(customer_city)) AS customer_city,
  UPPER(TRIM(customer_state)) AS customer_state,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.customers`;

CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.sellers` AS
SELECT
  seller_id,
  SAFE_CAST(seller_zip_code_prefix AS INT64) AS seller_zip_code_prefix,
  LOWER(TRIM(seller_city)) AS seller_city,
  UPPER(TRIM(seller_state)) AS seller_state,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.sellers`;

CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.categories` AS
SELECT
  NULLIF(TRIM(product_category_name), '') AS product_category_name,
  NULLIF(LOWER(TRIM(product_category_name_english)), '') AS product_category_name_english,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.categories`;
