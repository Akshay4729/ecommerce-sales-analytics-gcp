CREATE OR REPLACE TABLE
  `seventh-botany-506408-i1.silver.orders` AS

SELECT
    -- Original source columns
    order_id,
    customer_id,
    order_status,

    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,

    -- Date dimensions
    DATE(order_purchase_timestamp) AS purchase_date,

    EXTRACT(YEAR FROM order_purchase_timestamp) AS purchase_year,

    EXTRACT(MONTH FROM order_purchase_timestamp) AS purchase_month,

    -- Delivery duration
    CASE
        WHEN order_purchase_timestamp IS NOT NULL
             AND order_delivered_customer_date IS NOT NULL
        THEN TIMESTAMP_DIFF(
            order_delivered_customer_date,
            order_purchase_timestamp,
            DAY
        )
        ELSE NULL
    END AS delivery_days,

    -- Estimated delivery duration
    CASE
        WHEN order_purchase_timestamp IS NOT NULL
             AND order_estimated_delivery_date IS NOT NULL
        THEN TIMESTAMP_DIFF(
            order_estimated_delivery_date,
            order_purchase_timestamp,
            DAY
        )
        ELSE NULL
    END AS estimated_delivery_days,

    -- Actual delivery delay compared with estimated delivery
    CASE
        WHEN order_delivered_customer_date IS NOT NULL
             AND order_estimated_delivery_date IS NOT NULL
        THEN TIMESTAMP_DIFF(
            order_delivered_customer_date,
            order_estimated_delivery_date,
            DAY
        )
        ELSE NULL
    END AS delivery_delay_days,

    -- Order lifecycle validation
    CASE
        WHEN order_purchase_timestamp IS NOT NULL
             AND order_approved_at IS NOT NULL
             AND order_purchase_timestamp > order_approved_at
            THEN FALSE

        WHEN order_approved_at IS NOT NULL
             AND order_delivered_carrier_date IS NOT NULL
             AND order_approved_at > order_delivered_carrier_date
            THEN FALSE

        WHEN order_delivered_carrier_date IS NOT NULL
             AND order_delivered_customer_date IS NOT NULL
             AND order_delivered_carrier_date > order_delivered_customer_date
            THEN FALSE

        ELSE TRUE
    END AS is_lifecycle_valid,

    -- Order status vs customer delivery date validation
    CASE
        WHEN LOWER(order_status) = 'delivered'
             AND order_delivered_customer_date IS NULL
            THEN FALSE

        WHEN LOWER(order_status) != 'delivered'
             AND order_delivered_customer_date IS NOT NULL
            THEN FALSE

        ELSE TRUE
    END AS is_status_delivery_date_consistent

FROM
  `seventh-botany-506408-i1.bronze.orders`;