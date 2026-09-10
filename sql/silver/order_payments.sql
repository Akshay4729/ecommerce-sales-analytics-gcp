CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.order_payments` AS

SELECT
    CAST(order_id AS STRING) AS order_id,

    SAFE_CAST(payment_sequential AS INT64) AS payment_sequential,

    TRIM(LOWER(payment_type)) AS payment_type,

    SAFE_CAST(payment_installments AS INT64) AS payment_installments,

    SAFE_CAST(payment_value AS NUMERIC) AS payment_value

FROM `seventh-botany-506408-i1.bronze.order_payments`;