-- Grain: one row per real customer.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.gold.customer_metrics` AS
SELECT
  customer_unique_id,
  COUNT(*) AS delivered_order_count,
  SUM(total_revenue) AS total_revenue,
  SAFE_DIVIDE(SUM(total_revenue), COUNT(*)) AS average_order_value,
  COUNT(*) > 1 AS is_repeat_customer,
  MIN(purchase_date) AS first_purchase_date,
  MAX(purchase_date) AS latest_purchase_date
FROM `seventh-botany-506408-i1.gold.fact_orders`
WHERE order_status = 'delivered'
GROUP BY customer_unique_id;
