## Layered Model

### Bronze

Bronze tables preserve the nine source CSV datasets with explicit BigQuery types:

| Table | Grain | Key or identifying columns |
| --- | --- | --- |
| `customers` | One customer record | `customer_id` |
| `orders` | One order | `order_id` |
| `order_items` | One item within an order | `order_id`, `order_item_id` |
| `order_payments` | One payment sequence within an order | `order_id`, `payment_sequential` |
| `order_reviews` | One source review record | `order_id`, `review_id` when available |
| `products` | One product | `product_id` |
| `sellers` | One seller | `seller_id` |
| `categories` | One category translation row | `product_category_name` |
| `geolocation` | One geographic observation | ZIP prefix is not unique |

### Silver

Silver standardizes names and types, retains source grain, and adds flags such as `is_carrier_before_approval`, `is_invalid_installments`, and `is_invalid_weight`. `geolocation_zip_lookup` is a safe one-row-per-ZIP reference built from distinct observations.

### Gold

| Table | Grain | Purpose |
| --- | --- | --- |
| `fact_orders` | One row per order | Revenue, item, payment, review, and delivery metrics |
| `daily_sales` | One row per purchase date | Delivered sales KPIs and delivery summary |
| `customer_metrics` | One row per real customer | Repeat behavior and customer revenue |

## Important Modeling Rules

- Use `customer_unique_id` for real-customer analysis.
- Aggregate order items, payments, and reviews independently before joining to orders.
- Do not join geolocation directly by ZIP prefix without aggregation.
- Treat missing category translations as retained source values, not dropped products.
