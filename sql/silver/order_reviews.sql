CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.order_reviews` AS

SELECT
    CAST(review_id AS STRING) AS review_id,

    CAST(order_id AS STRING) AS order_id,

    SAFE_CAST(review_score AS INT64) AS review_score,

    SAFE_CAST(review_comment_title AS STRING) AS review_comment_title,

    SAFE_CAST(review_comment_message AS STRING) AS review_comment_message,

    SAFE_CAST(review_creation_date AS TIMESTAMP) AS review_creation_date,

    SAFE_CAST(review_answer_timestamp AS TIMESTAMP) AS review_answer_timestamp

FROM `seventh-botany-506408-i1.bronze.reviews`;