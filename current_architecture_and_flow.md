# E-commerce Sales Analytics Platform — Current Architecture & Data Flow

## 1. Project Overview

This project is an end-to-end cloud data engineering and analytics platform built on Google Cloud Platform (GCP) using the Olist Brazilian E-commerce dataset.

The project is designed to demonstrate:

- Python-based data ingestion
- Kaggle API integration
- Google Cloud Storage (GCS)
- BigQuery
- SQL-based data transformation and dimensional modeling
- Data quality and validation
- Gold-layer analytics
- Power BI reporting

---

## 2. Current Architecture

```text
                         DEVELOPMENT
                              |
                              v
                           VS Code
                              |
                         Git / GitHub
                              |
                              v
                       Google Cloud Run
                       Python Ingestion
                              |
                       +------+------+
                       |             |
                       | Kaggle API  | GCS API
                       v             v
                    KAGGLE      GCS DATA LAKE
                 Olist Dataset       |
                                     |
                                  RAW LAYER
                                     |
                                     v
                              BigQuery BRONZE
                                     |
                                  SQL / ETL
                                     |
                                     v
                              BigQuery SILVER
                                     |
                              SQL Data Modeling
                                     |
                                     v
                               BigQuery GOLD
                                     |
                              +------+------+
                              |             |
                              v             v
                         SQL Analysis    Power BI
```

---

## 3. Production Data Flow

The actual production-style pipeline is:

```text
Kaggle
  |
  | Kaggle API
  v
Python Ingestion Application
  |
  | Running on Google Cloud Run
  v
Google Cloud Storage (RAW)
  |
  | BigQuery Load
  v
BigQuery BRONZE
  |
  | SQL Transformation
  v
BigQuery SILVER
  |
  | SQL Modeling
  v
BigQuery GOLD
  |
  +--------------------+
  |                    |
  v                    v
SQL Analysis        Power BI
```

The local machine is not part of the production data pipeline.

VS Code is used primarily for development, testing, version control, and maintaining the project code.

---

## 4. Two Separate Workflows

### 4.1 Research / Profiling Workflow — Completed

This workflow was used to understand the dataset before building the production pipeline.

```text
Kaggle
  |
  v
Local CSV Files
  |
  v
Python Profiling Notebook
  |
  +--> Dataset structure
  +--> Data types
  +--> Missing values
  +--> Duplicates
  +--> Primary keys
  +--> Foreign keys
  +--> Relationships
  +--> Data quality rules
  +--> Business-rule violations
  +--> Grain/cardinality analysis
```

The local CSV files were used for offline research and profiling only.

No source records were deleted or modified during profiling.

---

### 4.2 Production Pipeline — Main Project

The production-style pipeline starts from Kaggle and uses Python running in GCP to ingest the source data.

```text
Kaggle
   |
   | API
   v
Cloud Run
   |
   | Python ingestion
   v
GCS RAW
   |
   v
BigQuery BRONZE
   |
   v
BigQuery SILVER
   |
   v
BigQuery GOLD
   |
   +------> SQL Analysis
   |
   +------> Power BI
```

---

# 5. Component Responsibilities

## 5.1 Kaggle — Source

Kaggle is the source of the Olist Brazilian E-commerce dataset.

The dataset contains 9 related CSV files:

```text
customers
orders
order_items
order_payments
order_reviews
products
sellers
categories
geolocation
```

Kaggle is treated as the external source system.

---

## 5.2 Python Ingestion Application

Python acts as the bridge between Kaggle and Google Cloud Storage.

Responsibilities:

1. Authenticate with Kaggle.
2. Identify the required dataset.
3. Download the source dataset programmatically.
4. Extract/identify the expected CSV files.
5. Validate expected files.
6. Upload files to GCS.
7. Log ingestion status.
8. Handle errors.
9. Implement idempotent behavior.
10. Provide a reusable ingestion process.

Planned project location:

```text
python/
└── extract/
    └── kaggle_to_gcs.py
```

---

## 5.3 Cloud Run — Execution Environment

Cloud Run will host the Python ingestion application.

Purpose:

```text
Kaggle API
     |
     v
Python Application
     |
     v
GCS
```

The application will run inside Google Cloud rather than relying on the user's local machine for production ingestion.

This keeps the production pipeline cloud-based.

---

# 6. Google Cloud Storage — Raw Data Lake

GCS is the landing zone for source data.

Bucket:

```text
akshay-ecommerce-data-lake
```

Current raw structure:

```text
akshay-ecommerce-data-lake/
└── raw/
    ├── categories/
    ├── customers/
    ├── geolocation/
    ├── order_items/
    ├── order_payments/
    ├── order_reviews/
    ├── orders/
    ├── products/
    └── sellers/
```

The raw layer should preserve source data as closely as possible.

### Raw layer principles

- Do not apply business transformations.
- Do not delete source records.
- Preserve source file structure where practical.
- Keep source-to-raw traceability.
- Make ingestion repeatable and idempotent.

---

# 7. BigQuery Medallion Architecture

The project uses three BigQuery layers:

```text
BRONZE
  |
  v
SILVER
  |
  v
GOLD
```

BigQuery datasets already created:

```text
bronze
silver
gold
```

---

## 7.1 Bronze Layer

Bronze contains the source data loaded from GCS into BigQuery.

Example:

```text
bronze.customers
bronze.orders
bronze.order_items
bronze.order_payments
bronze.order_reviews
bronze.products
bronze.sellers
bronze.categories
bronze.geolocation
```

Purpose:

- Cloud warehouse copy of raw source data
- Preserve source-level information
- Provide a stable starting point for transformations
- Enable SQL-based validation

Bronze should involve minimal transformation.

---

## 7.2 Silver Layer

Silver contains cleaned, standardized, and validated data.

This is where the findings from the profiling phase will be addressed.

Examples:

```text
Timestamp standardization
Missing-value handling
Data-type standardization
Business-rule validation
Category reference-data handling
Order lifecycle validation
Invalid numeric value handling
Geolocation grain handling
```

The goal is to produce reliable analytical data while preserving important business meaning.

---

## 7.3 Gold Layer

Gold contains business-ready analytical models.

Potential models include:

```text
gold.daily_sales
gold.customer_metrics
gold.product_performance
gold.seller_performance
gold.order_metrics
```

The exact Gold model will be finalized after the Silver layer is designed.

Gold is intended for:

- Business analysis
- SQL analytics
- KPI reporting
- Power BI dashboards

---

# 8. Key Data Modeling Principles

The profiling phase established that the datasets have different grains.

Important relationships:

```text
customers.customer_id
        |
        v
orders.customer_id


orders.order_id
        |
        +------> order_items.order_id
        |
        +------> order_payments.order_id
        |
        +------> order_reviews.order_id


products.product_id
        |
        v
order_items.product_id


sellers.seller_id
        |
        v
order_items.seller_id


categories.product_category_name
        |
        v
products.product_category_name
```

Important cardinalities:

```text
Customers 1 : M Orders

Orders 1 : M Order Items

Orders 1 : M Payments

Orders 1 : M Reviews

Products 1 : M Order Items

Sellers 1 : M Order Items

Categories 1 : M Products
```

---

# 9. Important Profiling Decisions Affecting the Pipeline

The profiling phase identified several issues that will influence the Silver and Gold layers.

## Customer Identity

Two identifiers exist:

```text
customer_id
customer_unique_id
```

`customer_id` identifies the customer record associated with an order.

`customer_unique_id` represents the underlying real customer.

For real-customer-level analysis, `customer_unique_id` should be used.

---

## Payments

One order can have multiple payment records.

Therefore:

```text
orders 1 : M payments
```

`order_id` alone is not a unique key in the payments table.

The combination:

```text
order_id + payment_sequential
```

is used to identify individual payment records.

---

## Reviews

Reviews also have a one-to-many relationship with orders in the source data.

Therefore, review data must be handled at its appropriate grain rather than blindly joining it to order-level data.

---

## Geolocation

The geolocation dataset is not one row per ZIP prefix.

```text
ZIP prefix
    |
    +--> Geographic observation 1
    +--> Geographic observation 2
    +--> Geographic observation 3
    +--> ...
```

A direct join using only:

```text
geolocation_zip_code_prefix
```

can multiply rows.

Therefore, a ZIP-level lookup or aggregation strategy must be defined before using geolocation in analytical models.

---

## Product Categories

Two product category values were found in the products data but were not present in the category lookup.

These reference-data mismatches will be handled during transformation rather than silently dropping the affected products.

---

# 10. Data Quality Strategy

The pipeline will follow this principle:

```text
Profile
   |
   v
Identify issue
   |
   v
Understand business meaning
   |
   v
Define transformation rule
   |
   v
Apply in Silver
   |
   v
Validate result
```

We will not automatically delete anomalous records simply because they violate a rule.

Examples include:

- Timestamp inconsistencies
- Missing delivery timestamps
- Invalid payment installments
- Non-positive product weights
- Category lookup mismatches
- Geolocation duplicates

Each issue will be handled according to its business meaning.

---

# 11. Current GCP Resources

GCP Project:

```text
seventh-botany-506408-i1
```

GCS Bucket:

```text
akshay-ecommerce-data-lake
```

BigQuery datasets:

```text
bronze
silver
gold
```

GCS region:

```text
us-central1
```

---

# 12. Development Workflow

Development will follow:

```text
VS Code
   |
   | Code
   v
Git
   |
   v
GitHub
   |
   v
Cloud environment
   |
   v
GCP services
```

VS Code is the primary development environment.

Cloud Shell / Cloud Editor can be used for authenticated cloud-side testing and deployment tasks.

The production ingestion workload is intended to run on Cloud Run.

---

# 13. Current Project Status

Completed:

```text
[✓] GCP project created
[✓] GCS bucket created
[✓] BigQuery bronze dataset created
[✓] BigQuery silver dataset created
[✓] BigQuery gold dataset created
[✓] Kaggle dataset downloaded locally
[✓] Data profiling completed
[✓] GCS raw folder structure created
[✓] Source CSVs manually uploaded to GCS
[✓] GCS verified through Cloud Shell
```

Current task:

```text
[ ] Configure Kaggle API authentication
[ ] Build kaggle_to_gcs.py
[ ] Test Kaggle → Python
[ ] Test Python → GCS
[ ] Add validation
[ ] Add idempotency
[ ] Add logging
[ ] Test all 9 datasets
[ ] Containerize ingestion application
[ ] Deploy ingestion application to Cloud Run
```

After ingestion:

```text
[ ] GCS → BigQuery Bronze
[ ] Bronze validation
[ ] Bronze → Silver SQL transformations
[ ] Silver validation
[ ] Silver → Gold analytical models
[ ] Gold SQL analysis
[ ] Power BI dashboard
[ ] End-to-end testing
[ ] Documentation
```

---

# 14. Target End-to-End Architecture

The final target architecture is:

```text
                         ┌─────────────────┐
                         │     KAGGLE      │
                         │  Olist Dataset  │
                         └────────┬────────┘
                                  │
                             Kaggle API
                                  │
                                  v
                         ┌─────────────────┐
                         │   CLOUD RUN     │
                         │ Python Ingestion│
                         └────────┬────────┘
                                  │
                            GCS API
                                  │
                                  v
                  ┌────────────────────────────┐
                  │            GCS             │
                  │       RAW DATA LAKE        │
                  │                            │
                  │ raw/                      │
                  │ ├── customers/            │
                  │ ├── orders/               │
                  │ ├── order_items/          │
                  │ ├── order_payments/       │
                  │ ├── order_reviews/        │
                  │ ├── products/             │
                  │ ├── sellers/              │
                  │ ├── categories/           │
                  │ └── geolocation/          │
                  └────────────┬───────────────┘
                               │
                          BigQuery Load
                               │
                               v
                  ┌────────────────────────────┐
                  │     BIGQUERY BRONZE        │
                  │       Source Tables        │
                  └────────────┬───────────────┘
                               │
                            SQL ETL
                               │
                               v
                  ┌────────────────────────────┐
                  │     BIGQUERY SILVER        │
                  │ Cleaned / Standardized     │
                  │ Validated Data             │
                  └────────────┬───────────────┘
                               │
                       SQL Data Modeling
                               │
                               v
                  ┌────────────────────────────┐
                  │      BIGQUERY GOLD         │
                  │ Business-ready Analytics   │
                  └────────────┬───────────────┘
                               │
                       ┌───────┴───────┐
                       │               │
                       v               v
                 SQL Analysis      Power BI
```

---

# 15. Design Goal

The final project should demonstrate an end-to-end cloud data pipeline rather than a collection of manually executed SQL queries.

The key engineering story is:

```text
External Data Source
        ↓
API-based Python Ingestion
        ↓
Cloud Data Lake
        ↓
Cloud Data Warehouse
        ↓
SQL Transformation
        ↓
Analytical Data Models
        ↓
Business Intelligence
```

This architecture demonstrates practical skills in:

- Python
- SQL
- BigQuery
- Google Cloud Storage
- Cloud Run
- API integration
- Data quality
- Data modeling
- ETL/ELT
- Analytics
- Power BI
