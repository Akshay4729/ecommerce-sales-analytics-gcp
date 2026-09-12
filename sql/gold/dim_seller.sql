CREATE OR REPLACE TABLE
    `seventh-botany-506408-i1.gold.dim_seller`
AS

SELECT
    ROW_NUMBER() OVER (
        ORDER BY seller_id
    ) AS seller_key,
    seller_id,
    seller_city,
    seller_zip_code_prefix,
    seller_state

FROM
    `seventh-botany-506408-i1.silver.sellers`;