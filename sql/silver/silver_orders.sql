-- Grain: one row per order.
-- Preserve source anomalies and expose them as quality flags.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.orders` AS
SELECT
  order_id,
  customer_id,
  LOWER(TRIM(order_status)) AS order_status,
  TIMESTAMP(order_purchase_timestamp) AS order_purchase_at,
  TIMESTAMP(order_approved_at) AS order_approved_at,
  TIMESTAMP(order_delivered_carrier_date) AS order_delivered_carrier_at,
  TIMESTAMP(order_delivered_customer_date) AS order_delivered_customer_at,
  TIMESTAMP(order_estimated_delivery_date) AS order_estimated_delivery_at,
  order_status = 'delivered' AND order_delivered_customer_date IS NULL
    AS is_delivered_missing_delivery_at,
  order_status != 'delivered' AND order_delivered_customer_date IS NOT NULL
    AS is_non_delivered_with_delivery_at,
  order_approved_at < order_purchase_timestamp
    AS is_approval_before_purchase,
  order_delivered_carrier_date < order_approved_at
    AS is_carrier_before_approval,
  order_delivered_customer_date < order_delivered_carrier_date
    AS is_delivery_before_carrier,
  order_delivered_customer_date < order_purchase_timestamp
    AS is_delivery_before_purchase,
  DATE(order_purchase_timestamp) AS purchase_date,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.orders`;
