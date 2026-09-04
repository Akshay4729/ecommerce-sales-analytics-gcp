-- Grain: one row per purchase date for delivered orders.
-- Revenue is item price plus freight value.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.gold.daily_sales`
PARTITION BY purchase_date AS
SELECT
  purchase_date,
  COUNT(*) AS delivered_order_count,
  COUNT(DISTINCT customer_unique_id) AS delivered_customer_count,
  SUM(total_revenue) AS total_revenue,
  SAFE_DIVIDE(SUM(total_revenue), COUNT(*)) AS average_order_value,
  SUM(item_count) AS item_count,
  SUM(CASE WHEN delivery_variance_days <= 0 THEN 1 ELSE 0 END)
    AS delivered_on_or_before_estimate_count,
  SUM(CASE WHEN delivery_variance_days > 0 THEN 1 ELSE 0 END)
    AS delivered_late_count
FROM `seventh-botany-506408-i1.gold.fact_orders`
WHERE order_status = 'delivered'
GROUP BY purchase_date;
