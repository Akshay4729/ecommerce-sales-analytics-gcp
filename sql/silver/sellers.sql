CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.sellers` AS

SELECT
    CAST(seller_id AS STRING) AS seller_id,

    SAFE_CAST(seller_zip_code_prefix AS INT64)
        AS seller_zip_code_prefix,

    TRIM(LOWER(seller_city)) AS seller_city,

    UPPER(TRIM(seller_state)) AS seller_state

FROM `seventh-botany-506408-i1.bronze.sellers`;