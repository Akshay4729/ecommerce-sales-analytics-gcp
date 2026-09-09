CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.customer` AS

SELECT
    CAST(customer_id AS STRING) AS customer_id,

    CAST(customer_unique_id AS STRING) AS customer_unique_id,

    SAFE_CAST(customer_zip_code_prefix AS INT64)
        AS customer_zip_code_prefix,

    TRIM(LOWER(customer_city)) AS customer_city,

    UPPER(TRIM(customer_state)) AS customer_state

FROM `seventh-botany-506408-i1.bronze.customers`;