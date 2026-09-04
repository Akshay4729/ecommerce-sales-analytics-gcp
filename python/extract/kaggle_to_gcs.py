from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import import_module
import logging
from pathlib import Path
from typing import Callable, Iterable

from google.cloud import storage

from python.utils.config import PipelineConfig, load_pipeline_config


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DatasetSpec:
    entity: str
    filename: str
    required_columns: tuple[str, ...]


DATASET_MANIFEST = (
    DatasetSpec("customers", "olist_customers_dataset.csv", ("customer_id",)),
    DatasetSpec("geolocation", "olist_geolocation_dataset.csv", ("geolocation_zip_code_prefix",)),
    DatasetSpec("order_items", "olist_order_items_dataset.csv", ("order_id", "order_item_id")),
    DatasetSpec("order_payments", "olist_order_payments_dataset.csv", ("order_id", "payment_sequential")),
    DatasetSpec("order_reviews", "olist_order_reviews_dataset.csv", ("review_id", "order_id")),
    DatasetSpec("orders", "olist_orders_dataset.csv", ("order_id", "customer_id")),
    DatasetSpec("products", "olist_products_dataset.csv", ("product_id",)),
    DatasetSpec("sellers", "olist_sellers_dataset.csv", ("seller_id",)),
    DatasetSpec("categories", "product_category_name_translation.csv", ("product_category_name",)),
)


def validate_expected_files(
    source_directory: Path,
    manifest: Iterable[DatasetSpec] = DATASET_MANIFEST,
) -> dict[DatasetSpec, Path]:
    files: dict[DatasetSpec, Path] = {}
    errors: list[str] = []

    for spec in manifest:
        matches = list(source_directory.rglob(spec.filename))
        if not matches:
            errors.append(f"Missing expected file: {spec.filename}")
            continue
        if len(matches) > 1:
            errors.append(f"Multiple files found for {spec.filename}: {matches}")
            continue

        file_path = matches[0]
        with file_path.open(newline="", encoding="utf-8-sig") as source_file:
            columns = set(next(csv.reader(source_file), []))
        missing_columns = set(spec.required_columns) - columns
        if missing_columns:
            errors.append(
                f"{spec.filename} is missing columns: {sorted(missing_columns)}"
            )
            continue
        files[spec] = file_path

    if errors:
        raise ValueError("Dataset validation failed: " + "; ".join(errors))
    return files


def download_dataset(
    dataset_slug: str,
    staging_directory: Path,
    downloader: Callable[..., str] | None = None,
) -> Path:
    staging_directory.mkdir(parents=True, exist_ok=True)
    if downloader is None:
        kagglehub = import_module("kagglehub")
        downloader = kagglehub.dataset_download

    downloaded_path = Path(
        downloader(dataset_slug, output_dir=str(staging_directory))
    )
    if not downloaded_path.exists():
        raise FileNotFoundError(
            f"Kaggle download path does not exist: {downloaded_path}"
        )
    return downloaded_path


def upload_files(
    files: dict[DatasetSpec, Path],
    config: PipelineConfig,
    storage_client: storage.Client | None = None,
    dry_run: bool = False,
    run_id: str | None = None,
) -> list[str]:
    client = None if dry_run else (
        storage_client or storage.Client(project=config.gcp_project_id)
    )
    bucket = None if client is None else client.bucket(config.gcs_bucket)
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    uploaded_paths: list[str] = []

    for spec, local_file in files.items():
        object_path = f"{config.raw_prefix}/{spec.entity}/{spec.filename}"
        uploaded_paths.append(object_path)
        if dry_run:
            logger.info("[%s] Would upload %s to gs://%s/%s", run_id, local_file, config.gcs_bucket, object_path)
            continue

        blob = bucket.blob(object_path)
        if blob.exists():
            logger.info("[%s] Object already exists: gs://%s/%s", run_id, config.gcs_bucket, object_path)
            continue
        blob.upload_from_filename(str(local_file), content_type="text/csv")
        logger.info("[%s] Uploaded gs://%s/%s", run_id, config.gcs_bucket, object_path)

    return uploaded_paths


def run_ingestion(
    config: PipelineConfig,
    source_directory: Path | None = None,
    storage_client: storage.Client | None = None,
    downloader: Callable[..., str] | None = None,
    dry_run: bool = False,
) -> list[str]:
    source = source_directory or download_dataset(
        config.kaggle_dataset,
        config.staging_directory,
        downloader=downloader,
    )
    files = validate_expected_files(source)
    return upload_files(
        files,
        config,
        storage_client=storage_client,
        dry_run=dry_run,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Olist data into GCS.")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--source-directory", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    config = load_pipeline_config(args.config)
    run_ingestion(
        config,
        source_directory=args.source_directory,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()