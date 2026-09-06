from dataclasses import dataclass
import os
from pathlib import Path
from typing import Mapping

import yaml


@dataclass(frozen=True)
class PipelineConfig:
    project_name: str
    gcp_project_id: str
    gcs_bucket: str
    gcp_region: str
    kaggle_dataset: str
    raw_prefix: str
    staging_directory: Path


def load_pipeline_config(
    config_path: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> PipelineConfig:
    environment = os.environ if environ is None else environ
    repository_root = Path(__file__).resolve().parents[2]
    path = config_path or repository_root / "config" / "config.yaml"

    with path.open(encoding="utf-8") as config_file:
        values = yaml.safe_load(config_file) or {}

    staging_directory = Path(
        environment.get(
            "PIPELINE_STAGING_DIRECTORY",
            values.get("staging_directory", "data/staging"),
        )
    )
    if not staging_directory.is_absolute():
        staging_directory = repository_root / staging_directory

    return PipelineConfig(
        project_name=values["project_name"],
        gcp_project_id=environment.get(
            "GCP_PROJECT_ID", values["gcp_project_id"]
        ),
        gcs_bucket=environment.get("GCS_BUCKET", values["gcs_bucket"]),
        gcp_region=environment.get("GCP_REGION", values["gcp_region"]),
        kaggle_dataset=environment.get(
            "KAGGLE_DATASET", values["kaggle_dataset"]
        ),
        raw_prefix=values.get("raw_prefix", "raw").strip("/"),
        staging_directory=staging_directory,
    )