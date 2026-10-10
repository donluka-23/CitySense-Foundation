"""No provider requests, dependencies, database or repository configuration changes."""

import importlib.util
import json
import os
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "stage1c_host", Path(__file__).parents[1] / "serve.py"
)
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)


class ConfigurationTests(unittest.TestCase):
    def test_no_credentials_is_an_explicit_block(self):
        with patch.dict(os.environ, {}, clear=True):
            config = host.public_configuration()
        self.assertFalse(config["keyPresent"])
        self.assertEqual(config["maptilerPublicKey"], "")

    def test_explicit_empty_primary_overrides_legacy_key(self):
        with patch.dict(
            os.environ,
            {
                "MAPTILER_API_KEY": "",
                "MAP_STAGE1_MAPTILER_PUBLIC_KEY": "test-public-key-12345",
            },
            clear=True,
        ):
            self.assertFalse(host.public_configuration()["keyPresent"])

    def test_known_secret_sentinels_are_never_transmitted(self):
        for value in [
            "sk.test-secret-sentinel",
            "sk-proj-test-sentinel",
            "ghp_test_secret_sentinel",
            "xoxb-test-secret-sentinel",
            "bad\nheader",
        ]:
            with (
                self.subTest(value=value),
                patch.dict(os.environ, {"MAPTILER_API_KEY": value}, clear=True),
            ):
                config = host.public_configuration()
                self.assertTrue(config["keyRejected"])
                self.assertEqual(config["maptilerPublicKey"], "")

    def test_authorized_browser_key_source_only(self):
        with patch.dict(
            os.environ,
            {"MAP_STAGE1_MAPTILER_PUBLIC_KEY": "test-public-key-12345"},
            clear=True,
        ):
            self.assertEqual(
                host.public_configuration()["maptilerPublicKey"],
                "test-public-key-12345",
            )


class HostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = host.ThreadingHTTPServer(("127.0.0.1", 0), host.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, path, method="GET", hostname=None):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
        connection.request(
            method, path, headers={"Host": hostname or f"127.0.0.1:{self.port}"}
        )
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_all_exact_allowlisted_assets_are_available_without_store(self):
        for path in host.FILES:
            with self.subTest(path=path):
                status, headers, body = self.request(path)
                self.assertEqual(status, 200)
                self.assertEqual(body, host.FILES[path][0].read_bytes())
                self.assertEqual(headers["Cache-Control"], "no-store")
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
                self.assertIn(
                    "frame-ancestors 'self'", headers["Content-Security-Policy"]
                )

    def test_repository_paths_and_encoded_traversal_are_refused(self):
        for path in [
            "/.env",
            "/../.env",
            "/%2e%2e/.env",
            "/services/api",
            "/tests/test_server.py",
            "/vendor/../package.json",
            "/presets.json/extra",
        ]:
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 404)

    def test_untrusted_host_is_refused(self):
        self.assertEqual(
            self.request("/config.json", hostname="external.invalid")[0], 403
        )

    def test_config_has_no_root_env_or_backend_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            status, _, body = self.request("/config.json")
        self.assertEqual(status, 200)
        config = json.loads(body)
        self.assertEqual(
            set(config),
            {"maptilerPublicKey", "keyPresent", "keyRejected", "expectedSdkVersion"},
        )
        self.assertFalse(config["keyPresent"])

    def test_head_is_supported_without_sending_body(self):
        status, headers, body = self.request("/", method="HEAD")
        self.assertEqual(status, 200)
        self.assertGreater(int(headers["Content-Length"]), 0)
        self.assertEqual(body, b"")


if __name__ == "__main__":
    unittest.main()
