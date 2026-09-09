CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.order_items` AS

SELECT
    CAST(order_id AS STRING) AS order_id,

    SAFE_CAST(order_item_id AS INT64) AS order_item_id,

    CAST(product_id AS STRING) AS product_id,

    CAST(seller_id AS STRING) AS seller_id,

    SAFE_CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_date,

    SAFE_CAST(price AS NUMERIC) AS price,

    SAFE_CAST(freight_value AS NUMERIC) AS freight_value

FROM `seventh-botany-506408-i1.bronze.order_items`;