"""Loopback-only, allowlisted static test server. Never serves repository data."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
PORT = int(os.getenv("MAP_STAGE1_PORT", "8765"))
if not 1024 <= PORT <= 65535:
    raise ValueError("MAP_STAGE1_PORT must be between 1024 and 65535")
FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/map.mjs": ("map.mjs", "text/javascript; charset=utf-8"),
    "/comparison.mjs": ("comparison.mjs", "text/javascript; charset=utf-8"),
    "/presets.json": ("../../docs/design/MAP_CAMERA_PRESETS.json", "application/json"),
    "/vendor/maplibre-gl.mjs": (
        "node_modules/maplibre-gl/dist/maplibre-gl.mjs",
        "text/javascript",
    ),
    "/vendor/maplibre-gl-worker.mjs": (
        "node_modules/maplibre-gl/dist/maplibre-gl-worker.mjs",
        "text/javascript",
    ),
    "/vendor/maplibre-gl-shared.mjs": (
        "node_modules/maplibre-gl/dist/maplibre-gl-shared.mjs",
        "text/javascript",
    ),
    "/vendor/maplibre-gl.css": (
        "node_modules/maplibre-gl/dist/maplibre-gl.css",
        "text/css",
    ),
    "/vendor/mapbox-gl.js": (
        "node_modules/mapbox-gl/dist/mapbox-gl.js",
        "text/javascript",
    ),
    "/vendor/mapbox-gl.css": ("node_modules/mapbox-gl/dist/mapbox-gl.css", "text/css"),
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass  # No URL, IP or credential logging.

    def do_GET(self):
        # Public browser keys only. Secret account/operator keys never belong here.
        if self.headers.get("Host") not in {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}:
            self.send_error(403)
            return
        path = urlsplit(self.path).path
        if path == "/config.json":
            mapbox_token = os.getenv(
                "MAPBOX_PUBLIC_ACCESS_TOKEN",
                os.getenv("MAP_STAGE1_MAPBOX_PUBLIC_TOKEN", ""),
            )
            # Never transmit a mistakenly configured Mapbox secret token.
            if not mapbox_token.startswith("pk."):
                mapbox_token = ""
            body = json.dumps(
                {
                    "mapboxPublicToken": mapbox_token,
                    "maptilerPublicKey": os.getenv(
                        "MAPTILER_API_KEY",
                        os.getenv("MAP_STAGE1_MAPTILER_PUBLIC_KEY", ""),
                    ),
                }
            ).encode()
            mime = "application/json"
        elif path in FILES:
            relative, mime = FILES[path]
            file = ROOT / relative
            if not file.is_file():
                self.send_error(404, "Run npm ci in tools/map-stage-1 first")
                return
            body = file.read_bytes()
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(
        f"Stage 1B basemap test: http://127.0.0.1:{PORT} (Ctrl+C to stop)", flush=True
    )
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
