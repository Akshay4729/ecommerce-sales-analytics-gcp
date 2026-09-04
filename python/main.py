from __future__ import annotations

from hmac import compare_digest
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from python.extract.kaggle_to_gcs import run_ingestion
from python.utils.config import PipelineConfig, load_pipeline_config


logger = logging.getLogger(__name__)


def create_handler(
	config: PipelineConfig,
	ingestion_function: Callable[[PipelineConfig], list[str]] = run_ingestion,
) -> type[BaseHTTPRequestHandler]:
	class PipelineRequestHandler(BaseHTTPRequestHandler):
		def _send_json(self, status_code: int, payload: dict[str, object]) -> None:
			response = json.dumps(payload).encode("utf-8")
			self.send_response(status_code)
			self.send_header("Content-Type", "application/json")
			self.send_header("Content-Length", str(len(response)))
			self.end_headers()
			self.wfile.write(response)

		def do_GET(self) -> None:
			if self.path == "/health":
				self._send_json(200, {"status": "ok"})
				return
			self._send_json(404, {"error": "not_found"})

		def do_POST(self) -> None:
			if self.path != "/ingest":
				self._send_json(404, {"error": "not_found"})
				return

			expected_token = os.environ.get("INGESTION_TOKEN")
			authorization = self.headers.get("Authorization", "")
			supplied_token = authorization.removeprefix("Bearer ").strip()
			if not expected_token or not compare_digest(supplied_token, expected_token):
				self._send_json(401, {"error": "unauthorized"})
				return

			try:
				uploaded_paths = ingestion_function(config)
			except Exception:
				logger.exception("Ingestion request failed")
				self._send_json(500, {"error": "ingestion_failed"})
				return
			self._send_json(200, {"status": "completed", "objects": uploaded_paths})

		def log_message(self, format: str, *args: object) -> None:
			logger.info("%s - %s", self.address_string(), format % args)

	return PipelineRequestHandler


def main() -> None:
	logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
	config = load_pipeline_config()
	port = int(os.environ.get("PORT", "8080"))
	server = ThreadingHTTPServer(("0.0.0.0", port), create_handler(config))
	logger.info("Pipeline service listening on port %s", port)
	server.serve_forever()


if __name__ == "__main__":
	main()
