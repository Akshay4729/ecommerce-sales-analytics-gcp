# E-commerce Sales Analytics Platform on Google Cloud

## Overview

This project demonstrates an end-to-end data engineering and analytics pipeline using Google Cloud Platform (GCP).

The pipeline ingests the Olist Brazilian E-commerce dataset from Kaggle, lands the nine raw CSV files in Google Cloud Storage, loads typed Bronze tables into BigQuery, transforms them into quality-aware Silver models, and publishes Gold tables for Power BI.

## Tech Stack

- Python
- SQL
- Google Cloud Storage
- BigQuery
- Power BI
- Git & GitHub

## Current Implementation

- Completed local profiling in `notebooks/01_data_profiling.ipynb`
- Manifest-driven Kaggle-to-GCS ingestion with dry-run support
- Cloud Run-compatible `/health` and protected `/ingest` service
- Explicit Bronze BigQuery schemas and load-job mapping
- Silver models with data-quality flags
- Gold order, daily sales, and customer KPI models

## Project Status

## Configuration

The default project configuration is in `config/config.yaml`:

- GCP project: `seventh-botany-506408-i1`
- GCS bucket: `akshay-ecommerce-data-lake`
- Region: `us-central1`
- Kaggle dataset: `olistbr/brazilian-ecommerce`

Credentials are supplied through the environment and must not be committed. Start from `.env.example` and provide Kaggle credentials plus an `INGESTION_TOKEN` for the Cloud Run endpoint.

## Local Validation

Use the project virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
python -m compileall -q python
python -m python.extract.kaggle_to_gcs --source-directory data/raw --dry-run
```

The dry run validates all nine expected files and prints their planned `raw/<entity>/` GCS destinations without writing to GCP.

## Cloud Execution Order

1. Run the ingestion service to populate `gs://akshay-ecommerce-data-lake/raw/`.
2. Run `python.load.gcs_to_bigquery` or the equivalent authenticated loader to create Bronze tables.
3. Execute the SQL files in `sql/silver/`.
4. Execute the SQL files in `sql/gold/`.
5. Connect Power BI to the Gold tables and use the KPI definitions in `docs/business_requirements.md`.

Docker is required for local container validation. The container starts with `python -m python.main` and listens on port `8080`.

## Data-Quality Decisions

Source rows are preserved in Silver and flagged rather than silently removed. Gold applies explicit filters such as delivered order status. Revenue is defined as item price plus freight value; payment records are retained separately because an order can have multiple payments.