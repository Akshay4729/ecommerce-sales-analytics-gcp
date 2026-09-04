from __future__ import annotations

import argparse
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Any

from python.extract.kaggle_to_gcs import DATASET_MANIFEST, DatasetSpec
from python.utils.config import PipelineConfig, load_pipeline_config


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BronzeTableSpec:
    dataset: DatasetSpec
    columns: tuple[tuple[str, str, str], ...]


BRONZE_TABLES = (
    BronzeTableSpec(DATASET_MANIFEST[0], (
        ("customer_id", "STRING", "REQUIRED"),
        ("customer_unique_id", "STRING", "REQUIRED"),
        ("customer_zip_code_prefix", "INT64", "NULLABLE"),
        ("customer_city", "STRING", "NULLABLE"),
        ("customer_state", "STRING", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[1], (
        ("geolocation_zip_code_prefix", "INT64", "NULLABLE"),
        ("geolocation_lat", "FLOAT64", "NULLABLE"),
        ("geolocation_lng", "FLOAT64", "NULLABLE"),
        ("geolocation_city", "STRING", "NULLABLE"),
        ("geolocation_state", "STRING", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[2], (
        ("order_id", "STRING", "REQUIRED"),
        ("order_item_id", "INT64", "REQUIRED"),
        ("product_id", "STRING", "NULLABLE"),
        ("seller_id", "STRING", "NULLABLE"),
        ("shipping_limit_date", "TIMESTAMP", "NULLABLE"),
        ("price", "NUMERIC", "NULLABLE"),
        ("freight_value", "NUMERIC", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[3], (
        ("order_id", "STRING", "REQUIRED"),
        ("payment_sequential", "INT64", "REQUIRED"),
        ("payment_type", "STRING", "NULLABLE"),
        ("payment_installments", "INT64", "NULLABLE"),
        ("payment_value", "NUMERIC", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[4], (
        ("review_id", "STRING", "NULLABLE"),
        ("order_id", "STRING", "REQUIRED"),
        ("review_score", "INT64", "NULLABLE"),
        ("review_comment_title", "STRING", "NULLABLE"),
        ("review_comment_message", "STRING", "NULLABLE"),
        ("review_creation_date", "TIMESTAMP", "NULLABLE"),
        ("review_answer_timestamp", "TIMESTAMP", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[5], (
        ("order_id", "STRING", "REQUIRED"),
        ("customer_id", "STRING", "REQUIRED"),
        ("order_status", "STRING", "NULLABLE"),
        ("order_purchase_timestamp", "TIMESTAMP", "NULLABLE"),
        ("order_approved_at", "TIMESTAMP", "NULLABLE"),
        ("order_delivered_carrier_date", "TIMESTAMP", "NULLABLE"),
        ("order_delivered_customer_date", "TIMESTAMP", "NULLABLE"),
        ("order_estimated_delivery_date", "TIMESTAMP", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[6], (
        ("product_id", "STRING", "REQUIRED"),
        ("product_category_name", "STRING", "NULLABLE"),
        ("product_name_lenght", "INT64", "NULLABLE"),
        ("product_description_lenght", "INT64", "NULLABLE"),
        ("product_photos_qty", "INT64", "NULLABLE"),
        ("product_weight_g", "FLOAT64", "NULLABLE"),
        ("product_length_cm", "FLOAT64", "NULLABLE"),
        ("product_height_cm", "FLOAT64", "NULLABLE"),
        ("product_width_cm", "FLOAT64", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[7], (
        ("seller_id", "STRING", "REQUIRED"),
        ("seller_zip_code_prefix", "INT64", "NULLABLE"),
        ("seller_city", "STRING", "NULLABLE"),
        ("seller_state", "STRING", "NULLABLE"),
    )),
    BronzeTableSpec(DATASET_MANIFEST[8], (
        ("product_category_name", "STRING", "NULLABLE"),
        ("product_category_name_english", "STRING", "NULLABLE"),
    )),
)


def build_bigquery_schema(table_spec: BronzeTableSpec) -> list[Any]:
    from google.cloud import bigquery

    return [
        bigquery.SchemaField(name, field_type, mode=mode)
        for name, field_type, mode in table_spec.columns
    ]


def build_load_job_config(table_spec: BronzeTableSpec) -> Any:
    from google.cloud import bigquery

    return bigquery.LoadJobConfig(
        schema=build_bigquery_schema(table_spec),
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=False,
        ignore_unknown_values=False,
    )


def load_table_from_gcs(
    client: Any,
    config: PipelineConfig,
    table_spec: BronzeTableSpec,
) -> str:
    table_name = table_spec.dataset.entity
    table_id = f"{config.gcp_project_id}.bronze.{table_name}"
    source_uri = (
        f"gs://{config.gcs_bucket}/{config.raw_prefix}/"
        f"{table_name}/{table_spec.dataset.filename}"
    )
    job = client.load_table_from_uri(
        source_uri,
        table_id,
        job_config=build_load_job_config(table_spec),
    )
    job.result()
    logger.info("Loaded %s into %s", source_uri, table_id)
    return table_id


def load_all_bronze_tables(
    config: PipelineConfig,
    client: Any | None = None,
) -> list[str]:
    if client is None:
        from google.cloud import bigquery

        client = bigquery.Client(project=config.gcp_project_id)
    return [
        load_table_from_gcs(client, config, table_spec)
        for table_spec in BRONZE_TABLES
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load GCS raw CSV files into BigQuery Bronze tables."
    )
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    config = load_pipeline_config(args.config)
    loaded_tables = load_all_bronze_tables(config)
    logger.info("Loaded %d Bronze tables: %s", len(loaded_tables), loaded_tables)


if __name__ == "__main__":
    main()