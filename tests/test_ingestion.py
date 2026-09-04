from pathlib import Path

import pytest

from python.extract.kaggle_to_gcs import (
    DATASET_MANIFEST,
    validate_expected_files,
    upload_files,
)
from python.utils.config import PipelineConfig


def create_manifest_files(directory: Path) -> dict:
    files = {}
    for spec in DATASET_MANIFEST:
        file_path = directory / spec.filename
        file_path.write_text(",".join(spec.required_columns) + "\n", encoding="utf-8")
        files[spec] = file_path
    return files


def test_validate_expected_files_finds_all_manifest_files(tmp_path: Path) -> None:
    files = create_manifest_files(tmp_path)

    validated_files = validate_expected_files(tmp_path)

    assert validated_files == files


def test_validate_expected_files_reports_missing_files(tmp_path: Path) -> None:
    create_manifest_files(tmp_path)
    (tmp_path / DATASET_MANIFEST[0].filename).unlink()

    with pytest.raises(ValueError, match="Missing expected file"):
        validate_expected_files(tmp_path)


class FakeBlob:
    def __init__(self, exists: bool) -> None:
        self._exists = exists
        self.uploads = 0

    def exists(self) -> bool:
        return self._exists

    def upload_from_filename(self, filename: str, content_type: str) -> None:
        assert filename
        assert content_type == "text/csv"
        self.uploads += 1


class FakeBucket:
    def __init__(self) -> None:
        self.blobs: dict[str, FakeBlob] = {}

    def blob(self, path: str) -> FakeBlob:
        return self.blobs.setdefault(path, FakeBlob(exists=path.endswith("customers_dataset.csv")))


class FakeStorageClient:
    def __init__(self) -> None:
        self.bucket_instance = FakeBucket()

    def bucket(self, name: str) -> FakeBucket:
        assert name == "test-bucket"
        return self.bucket_instance


def test_upload_files_skips_existing_objects(tmp_path: Path) -> None:
    files = create_manifest_files(tmp_path)
    config = PipelineConfig(
        project_name="test",
        gcp_project_id="test-project",
        gcs_bucket="test-bucket",
        gcp_region="us-central1",
        kaggle_dataset="test/dataset",
        raw_prefix="raw",
        staging_directory=tmp_path,
    )
    client = FakeStorageClient()

    uploaded_paths = upload_files(files, config, storage_client=client, run_id="test-run")

    assert len(uploaded_paths) == len(DATASET_MANIFEST)
    assert client.bucket_instance.blobs[
        "raw/customers/olist_customers_dataset.csv"
    ].uploads == 0
    assert client.bucket_instance.blobs[
        "raw/orders/olist_orders_dataset.csv"
    ].uploads == 1