from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

from python.extract.kaggle_to_gcs import DATASET_MANIFEST
from python.utils.config import PipelineConfig, load_pipeline_config


logger = logging.getLogger(__name__)


def build_load_job_config() -> Any:
    from google.cloud import bigquery

    return bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        encoding="UTF-8",
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )


def load_table_from_gcs(
    client: Any,
    config: PipelineConfig,
    entity: str,
    filename: str,
) -> str:
    table_id = f"{config.gcp_project_id}.{config.bronze_dataset}.{entity}"
    source_uri = (
        f"gs://{config.gcs_bucket}/{config.raw_prefix}/"
        f"{entity}/{filename}"
    )
    job = client.load_table_from_uri(
        source_uri,
        table_id,
        job_config=build_load_job_config(),
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

    loaded_tables = []

    for spec in DATASET_MANIFEST:
        loaded_table = load_table_from_gcs(
            client,
            config,
            spec.entity,
            spec.filename,
        )
        loaded_tables.append(loaded_table)

    return loaded_tables


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
