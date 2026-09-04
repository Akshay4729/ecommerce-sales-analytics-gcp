import json
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from python.main import create_handler
from python.utils.config import PipelineConfig


def test_health_and_authorized_ingestion(monkeypatch) -> None:
    config = PipelineConfig(
        project_name="test",
        gcp_project_id="test-project",
        gcs_bucket="test-bucket",
        gcp_region="us-central1",
        kaggle_dataset="test/dataset",
        raw_prefix="raw",
        staging_directory=Path("data/staging"),
    )
    monkeypatch.setenv("INGESTION_TOKEN", "test-token")
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        create_handler(config, lambda _: ["raw/orders/orders.csv"]),
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(f"{base_url}/health") as response:
            assert response.status == 200
            assert json.loads(response.read()) == {"status": "ok"}

        with urlopen(Request(f"{base_url}/ingest", method="POST")) as response:
            assert response.status == 401
    except HTTPError as error:
        assert error.code == 401
    else:
        raise AssertionError("Unauthorized ingestion request was accepted")

    request = Request(
        f"{base_url}/ingest",
        headers={"Authorization": "Bearer test-token"},
        method="POST",
    )
    with urlopen(request) as response:
        assert response.status == 200
        assert json.loads(response.read()) == {
            "status": "completed",
            "objects": ["raw/orders/orders.csv"],
        }

    server.shutdown()
    thread.join()
    server.server_close()
