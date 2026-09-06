# E-commerce Sales Analytics Platform on Google Cloud

## Overview

This project demonstrates an end-to-end data engineering and analytics pipeline using Google Cloud Platform (GCP).

The pipeline ingests raw e-commerce data, performs data validation and transformation using Python, stores data in Google Cloud Storage, loads it into BigQuery, and creates analytics-ready tables for reporting through Power BI.

## Tech Stack

- Python
- SQL
- Google Cloud Storage
- BigQuery
- Power BI
- Git & GitHub

## Project Status

🚧 In Progress

## Run the ingestion script

From the repository root in Cloud Shell, run the script as a module so the
repository root is available for the `python.utils` import:

```bash
source .venv/bin/activate
python -m python.extract.kaggle_to_gcs --help
```

To validate the files and show which GCS objects would be uploaded without
making changes:

```bash
python -m python.extract.kaggle_to_gcs --dry-run
```

Running `python/extract/kaggle_to_gcs.py` directly changes Python's import path
to `python/extract`, which causes `ModuleNotFoundError: No module named
'python'`.