from pathlib import Path
import logging

from google.cloud import storage


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ID = "seventh-botany-506408-i1"
BUCKET_NAME = "akshay-ecommerce-data-lake"

LOCAL_FILE = Path("data/raw/olist_customers_dataset.csv")
GCS_PATH = "raw/customers/olist_customers_dataset.csv"


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Upload function
# --------------------------------------------------

def upload_to_gcs(
    project_id: str,
    bucket_name: str,
    local_file: Path,
    gcs_path: str
) -> None:

    # 1. Check local file
    if not local_file.exists():
        raise FileNotFoundError(
            f"Local file not found: {local_file}"
        )

    logger.info(f"Local file found: {local_file}")

    # 2. Create GCS client
    client = storage.Client(project=project_id)

    # 3. Get bucket
    bucket = client.bucket(bucket_name)

    # 4. Get destination object
    blob = bucket.blob(gcs_path)

    # 5. Check whether object already exists
    if blob.exists():

        logger.info(
            f"File already exists in GCS: gs://{bucket_name}/{gcs_path}"
        )

        return

    # 6. Upload file
    blob.upload_from_filename(
        local_file,
        content_type="text/csv"
    )

    logger.info(
        f"Upload successful: gs://{bucket_name}/{gcs_path}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    upload_to_gcs(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
        local_file=LOCAL_FILE,
        gcs_path=GCS_PATH
    )