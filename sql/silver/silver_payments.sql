-- Grain: one row per order and payment sequence.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.payments` AS
SELECT
  order_id,
  SAFE_CAST(payment_sequential AS INT64) AS payment_sequential,
  LOWER(TRIM(payment_type)) AS payment_type,
  SAFE_CAST(payment_installments AS INT64) AS payment_installments,
  SAFE_CAST(payment_value AS NUMERIC) AS payment_value,
  SAFE_CAST(payment_installments AS INT64) <= 0 AS is_invalid_installments,
  SAFE_CAST(payment_value AS NUMERIC) < 0 AS is_invalid_payment_value,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.order_payments`;
