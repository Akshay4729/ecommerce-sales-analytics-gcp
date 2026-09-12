CREATE OR REPLACE TABLE
    `seventh-botany-506408-i1.gold.dim_customer`
AS

SELECT
    ROW_NUMBER() OVER (
        ORDER BY customer_id
    ) AS customer_key,  
    
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state

FROM
    `seventh-botany-506408-i1.silver.customers`;