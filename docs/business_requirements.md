# Business Requirements

## Objective

Build an end-to-end analytics platform that enables business stakeholders to monitor sales performance, customer behavior, seller performance, and operational efficiency using Google Cloud Platform.

## Key Metrics

- Total Revenue
- Total Orders
- Average Order Value
- Repeat Customers
- Monthly Sales
- Top Categories
- Top Products
- Seller Performance
- Delivery Performance

## KPI Definitions

The primary sales view uses orders with `order_status = 'delivered'`.

| KPI | Definition |
| --- | --- |
| Total Revenue | Sum of `price + freight_value` from order items belonging to delivered orders |
| Total Orders | Count of delivered orders |
| Average Order Value | Total Revenue divided by delivered order count |
| Repeat Customers | Real customers (`customer_unique_id`) with more than one delivered order |
| Monthly Sales | Delivered revenue grouped by the order purchase date month |
| Top Categories | Delivered item revenue grouped by translated product category |
| Top Products | Delivered item revenue grouped by product |
| Seller Performance | Delivered item count and revenue grouped by seller |
| Delivery Performance | Delivered orders with usable delivery timestamps; late means delivery after the estimated date |

Payment values are retained for reconciliation but are not added to item revenue. Payments can have multiple records per order.

## Data-Quality Policy

The Silver layer preserves source records and adds quality flags. It does not silently delete anomalous rows. Gold models apply explicit business filters, such as delivered status, and expose exception counts for review.

Known conditions include timestamp ordering anomalies, status/timestamp mismatches, invalid installments, non-positive product dimensions, unmatched product categories, and multiple geographic observations per ZIP prefix.

## Reporting Grain

Power BI should connect to Gold tables rather than joining raw or Silver one-to-many tables directly. `fact_orders` is one row per order; `daily_sales` is one row per purchase date; and `customer_metrics` is one row per `customer_unique_id`.