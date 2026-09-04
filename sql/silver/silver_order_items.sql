-- Grain: one row per order line item.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.order_items` AS
SELECT
  order_id,
  SAFE_CAST(order_item_id AS INT64) AS order_item_id,
  product_id,
  seller_id,
  TIMESTAMP(shipping_limit_date) AS shipping_limit_at,
  SAFE_CAST(price AS NUMERIC) AS item_price,
  SAFE_CAST(freight_value AS NUMERIC) AS freight_value,
  SAFE_CAST(price AS NUMERIC) + SAFE_CAST(freight_value AS NUMERIC) AS line_revenue,
  SAFE_CAST(price AS NUMERIC) < 0 AS is_invalid_price,
  SAFE_CAST(freight_value AS NUMERIC) < 0 AS is_invalid_freight,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.order_items`;
