# Cloud Resources

## Project
- Name: ecommerce-sales-analytics

## Cloud Storage
- Bucket: akshay-ecommerce-data-lake
- Purpose:
  - raw/
  - processed/
  - archive/

## BigQuery
- bronze
- silver
- gold

## Region
- us-central1


Customer Identity
(customer_unique_id)
       │
       │ 1:M
       ▼
Customer Record
(customer_id)
       │
       │ 1:1
       ▼
Orders
   │
   ├── 1:M ──> Order Items
   │                │
   │                ├── M:1 → Products
   │                └── M:1 → Sellers
   │
   ├── 1:M ──> Payments
   │
   └── 1:M ──> Reviews



   Customers
    │
    └── Orders
          │
          ├── Order Items ── Products ── Categories
          │       │
          │       └── Sellers
          │
          ├── Payments
          │
          └── Reviews



Customers
    │
    │ 1:M
    ▼
Orders
    │
    ├────────────── 1:M ──────────────► Order Payments
    │
    ├────────────── 1:M ──────────────► Order Reviews
    │
    │ 1:M
    ▼
Order Items
    │
    ├──────────── M:1 ──────────────► Products
    │
    └──────────── M:1 ──────────────► Sellers

Products
    │
    │ M:1
    ▼
Categories

