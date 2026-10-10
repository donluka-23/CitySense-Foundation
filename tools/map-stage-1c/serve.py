"""Isolated loopback host. Reuses the Stage 1 SDK without modifying it."""

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent.parent
SDK = REPOSITORY / "tools/map-stage-1/node_modules/maplibre-gl"
FILES = {
    "/": (ROOT / "index.html", "text/html; charset=utf-8"),
    "/navigation.mjs": (ROOT / "navigation.mjs", "text/javascript; charset=utf-8"),
    "/diagnostics.mjs": (ROOT / "diagnostics.mjs", "text/javascript; charset=utf-8"),
    "/presets.json": (
        REPOSITORY / "docs/design/MAP_CAMERA_PRESETS.json",
        "application/json",
    ),
}
for asset in (
    "maplibre-gl.mjs",
    "maplibre-gl-worker.mjs",
    "maplibre-gl-shared.mjs",
    "maplibre-gl.css",
):
    FILES[f"/vendor/{asset}"] = (
        SDK / "dist" / asset,
        "text/css" if asset.endswith(".css") else "text/javascript",
    )


def public_configuration():
    value = os.getenv(
        "MAPTILER_API_KEY", os.getenv("MAP_STAGE1_MAPTILER_PUBLIC_KEY", "")
    )
    value = value.strip()
    secret_prefix = re.match(
        r"^(sk[.-]|ghp_|github_pat_|AKIA|xox[baprs]-|-----)", value
    )
    rejected = bool(value) and (
        bool(secret_prefix) or not re.fullmatch(r"[A-Za-z0-9_-]{10,128}", value)
    )
    return {
        "maptilerPublicKey": "" if rejected else value,
        "keyPresent": bool(value) and not rejected,
        "keyRejected": rejected,
        "expectedSdkVersion": "6.13.0",
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass  # Never log request URLs, configuration values or headers.

    def respond(self, status, body, mime):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "worker-src 'self' blob:; connect-src 'self' https://api.maptiler.com "
            "https://*.maptiler.com; img-src 'self' data: blob: https://api.maptiler.com; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'self'; form-action 'none'",
        )
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        port = self.server.server_address[1]
        if self.headers.get("Host") not in {f"127.0.0.1:{port}", f"localhost:{port}"}:
            self.respond(403, b"Host refused", "text/plain")
            return
        path = urlsplit(self.path).path
        if path == "/config.json":
            self.respond(
                200, json.dumps(public_configuration()).encode(), "application/json"
            )
        elif path in FILES:
            file, mime = FILES[path]
            if not file.is_file():
                self.respond(
                    503,
                    b"Existing Stage 1 SDK or experiment asset unavailable",
                    "text/plain",
                )
                return
            self.respond(200, file.read_bytes(), mime)
        else:
            self.respond(404, b"Path refused", "text/plain")


def main():
    port = int(os.getenv("MAP_STAGE1C_PORT", "8767"))
    if not 1024 <= port <= 65535:
        raise ValueError("MAP_STAGE1C_PORT must be between 1024 and 65535")
    package = SDK / "package.json"
    if not package.is_file() or json.loads(package.read_text())["version"] != "6.13.0":
        raise SystemExit(
            "Existing MapLibre 6.13.0 installation required; no installation attempted"
        )
    config = public_configuration()
    print(f"Stage 1C: http://127.0.0.1:{port}/ (Ctrl+C to stop)", flush=True)
    print(
        f"Public key configured: {config['keyPresent']}; rejected: {config['keyRejected']}",
        flush=True,
    )
    with ThreadingHTTPServer(("127.0.0.1", port), Handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
