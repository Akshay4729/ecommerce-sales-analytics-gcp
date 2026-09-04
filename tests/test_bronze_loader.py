from pathlib import Path

from python.load.gcs_to_bigquery import (
    BRONZE_TABLES,
    build_load_job_config,
    load_all_bronze_tables,
)
from python.utils.config import PipelineConfig


class FakeJob:
    def __init__(self) -> None:
        self.completed = False

    def result(self) -> None:
        self.completed = True


class FakeBigQueryClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, object]] = []

    def load_table_from_uri(self, uri: str, table_id: str, job_config: object) -> FakeJob:
        self.calls.append((uri, table_id, job_config))
        return FakeJob()


def test_bronze_manifest_has_all_source_tables() -> None:
    assert len(BRONZE_TABLES) == 9
    assert {spec.dataset.entity for spec in BRONZE_TABLES} == {
        "customers",
        "geolocation",
        "order_items",
        "order_payments",
        "order_reviews",
        "orders",
        "products",
        "sellers",
        "categories",
    }


def test_load_all_bronze_tables_maps_gcs_to_bq(tmp_path: Path) -> None:
    config = PipelineConfig(
        project_name="test",
        gcp_project_id="test-project",
        gcs_bucket="test-bucket",
        gcp_region="us-central1",
        kaggle_dataset="test/dataset",
        raw_prefix="raw",
        staging_directory=tmp_path,
    )
    client = FakeBigQueryClient()

    loaded_tables = load_all_bronze_tables(config, client=client)

    assert loaded_tables[0] == "test-project.bronze.customers"
    assert len(client.calls) == 9
    assert client.calls[0][0] == (
        "gs://test-bucket/raw/customers/olist_customers_dataset.csv"
    )
    assert client.calls[0][1] == "test-project.bronze.customers"


def test_load_config_uses_explicit_schema() -> None:
    job_config = build_load_job_config(BRONZE_TABLES[5])

    assert job_config.autodetect is False
    assert job_config.skip_leading_rows == 1
    assert [field.name for field in job_config.schema] == [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]