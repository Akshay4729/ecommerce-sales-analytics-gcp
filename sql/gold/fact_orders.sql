-- Grain: one row per order.
-- Items, payments, and reviews are aggregated independently before joining.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.gold.fact_orders`
PARTITION BY purchase_date
CLUSTER BY order_status, customer_unique_id AS
WITH item_totals AS (
  SELECT
    order_id,
    SUM(item_price) AS item_revenue,
    SUM(freight_value) AS freight_revenue,
    SUM(line_revenue) AS total_revenue,
    COUNT(*) AS item_count
  FROM `seventh-botany-506408-i1.silver.order_items`
  GROUP BY order_id
), payment_totals AS (
  SELECT
    order_id,
    SUM(payment_value) AS payment_value,
    COUNT(*) AS payment_record_count
  FROM `seventh-botany-506408-i1.silver.payments`
  GROUP BY order_id
), review_totals AS (
  SELECT
    order_id,
    COUNT(*) AS review_count,
    AVG(review_score) AS average_review_score
  FROM `seventh-botany-506408-i1.silver.reviews`
  WHERE NOT is_invalid_review_score
  GROUP BY order_id
)
SELECT
  orders.order_id,
  orders.customer_id,
  customers.customer_unique_id,
  orders.order_status,
  orders.purchase_date,
  orders.order_purchase_at,
  orders.order_approved_at,
  orders.order_delivered_carrier_at,
  orders.order_delivered_customer_at,
  orders.order_estimated_delivery_at,
  item_totals.item_revenue,
  item_totals.freight_revenue,
  item_totals.total_revenue,
  item_totals.item_count,
  payment_totals.payment_value,
  payment_totals.payment_record_count,
  review_totals.review_count,
  review_totals.average_review_score,
  DATE_DIFF(DATE(orders.order_delivered_customer_at), orders.purchase_date, DAY)
    AS purchase_to_delivery_days,
  DATE_DIFF(DATE(orders.order_delivered_customer_at), DATE(orders.order_estimated_delivery_at), DAY)
    AS delivery_variance_days,
  orders.is_delivered_missing_delivery_at,
  orders.is_non_delivered_with_delivery_at,
  orders.is_carrier_before_approval,
  orders.is_delivery_before_carrier,
  orders.is_delivery_before_purchase
FROM `seventh-botany-506408-i1.silver.orders` AS orders
LEFT JOIN `seventh-botany-506408-i1.silver.customers` AS customers
  ON orders.customer_id = customers.customer_id
LEFT JOIN item_totals
  ON orders.order_id = item_totals.order_id
LEFT JOIN payment_totals
  ON orders.order_id = payment_totals.order_id
LEFT JOIN review_totals
  ON orders.order_id = review_totals.order_id;
