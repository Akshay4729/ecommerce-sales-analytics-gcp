from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

from google.cloud import bigquery

from python.utils.config import PipelineConfig, load_pipeline_config


logger = logging.getLogger(__name__)


def load_sql_file(sql_file: Path) -> str:
    """Read a SQL file and return its contents."""
    logger.info("Reading SQL file: %s", sql_file)

    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    return sql_file.read_text(encoding="utf-8")


def execute_sql(
    client: bigquery.Client,
    sql: str,
    sql_file: Path,
) -> None:
    """Execute a SQL transformation in BigQuery."""

    logger.info("Executing: %s", sql_file)

    query_job = client.query(sql)
    query_job.result()

    logger.info("Completed: %s", sql_file)


def run_silver_transformations(
    config: PipelineConfig,
    sql_directory: Path,
) -> list[str]:
    """Execute all Silver SQL transformations."""

    client = bigquery.Client(project=config.gcp_project_id)

    sql_files = sorted(sql_directory.glob("*.sql"))

    if not sql_files:
        raise FileNotFoundError(
            f"No SQL files found in directory: {sql_directory}"
        )

    completed_files: list[str] = []

    logger.info(
        "Found %d Silver SQL files in %s",
        len(sql_files),
        sql_directory,
    )

    for sql_file in sql_files:
        sql = load_sql_file(sql_file)

        if not sql.strip():
            logger.warning("Skipping empty SQL file: %s", sql_file)
            continue

        execute_sql(
            client=client,
            sql=sql,
            sql_file=sql_file,
        )

        completed_files.append(sql_file.name)

    return completed_files


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run all Silver-layer BigQuery transformations."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to pipeline configuration file.",
    )

    parser.add_argument(
        "--sql-dir",
        type=Path,
        default=Path("sql/silver"),
        help="Directory containing Silver SQL files.",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    config = load_pipeline_config(args.config)

    completed_files = run_silver_transformations(
        config=config,
        sql_directory=args.sql_dir,
    )

    logger.info(
        "Silver transformation completed successfully. "
        "Executed %d SQL files: %s",
        len(completed_files),
        completed_files,
    )


if __name__ == "__main__":
    main()