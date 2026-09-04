-- Grain: one row per source review record.
-- Reviews are aggregated separately in Gold before joining to orders.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.reviews` AS
SELECT
  review_id,
  order_id,
  SAFE_CAST(review_score AS INT64) AS review_score,
  review_comment_title,
  review_comment_message,
  TIMESTAMP(review_creation_date) AS review_created_at,
  TIMESTAMP(review_answer_timestamp) AS review_answered_at,
  NOT SAFE_CAST(review_score AS INT64) BETWEEN 1 AND 5 AS is_invalid_review_score,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.order_reviews`;
