"""Run local quality gates and retain exact, redacted outcomes; never hide skipped DB tests."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


def redact(text: str) -> str:
    return re.sub(r"postgresql(?:\+psycopg)?://[^\s'\"]+", "[REDACTED_DATABASE_URL]", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-db", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    api = Path(__file__).resolve().parents[1]
    root = api.parents[1]
    output = args.output or root / "artifacts" / "checks"
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    task_temp = root / ".local" / "tmp"
    task_temp.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TMP"], env["TEMP"] = str(task_temp), str(task_temp)
    if args.require_db:
        env["CITYSENSE_REQUIRE_DB"] = "1"
    py = sys.executable
    commands = [
        ("lock", [py, "-m", "uv", "lock", "--check"]),
        (
            "format",
            [py, "-m", "ruff", "format", "--check", "src", "tests", "migrations", "scripts"],
        ),
        ("lint", [py, "-m", "ruff", "check", "src", "tests", "migrations", "scripts"]),
        ("types", [py, "-m", "mypy"]),
        ("contracts", [py, "scripts/export_contracts.py", "--check"]),
        ("tests", [py, "-m", "pytest", "-q", f"--junitxml={output / 'pytest.xml'}"]),
        ("security", [py, "-m", "bandit", "-r", "src", "-q"]),
        (
            "requirements",
            [
                py,
                "-m",
                "uv",
                "export",
                "--locked",
                "--all-groups",
                "--no-emit-project",
                "--format",
                "requirements-txt",
                "--output-file",
                str(output / "requirements.txt"),
            ],
        ),
        (
            "dependencies",
            [
                py,
                "-m",
                "pip_audit",
                "-r",
                str(output / "requirements.txt"),
                "--disable-pip",
                "--require-hashes",
                "--format",
                "json",
                "--output",
                str(output / "dependency-audit.json"),
            ],
        ),
        ("ci_structure", [py, "scripts/validate_ci.py"]),
    ]
    actionlint = shutil.which("actionlint")
    local_actionlint = root / ".local" / "actionlint" / "actionlint.exe"
    if not actionlint and local_actionlint.is_file():
        actionlint = str(local_actionlint)
    if actionlint:
        commands.append(
            (
                "workflow_syntax",
                [actionlint, "-shellcheck=", str(root / ".github/workflows/ci.yml")],
            )
        )
    results = []
    for name, command in commands:
        began = time.monotonic()
        try:
            completed = subprocess.run(
                command, cwd=api, env=env, text=True, capture_output=True, timeout=180, check=False
            )  # nosec B603 - fixed local tool argv
            code = completed.returncode
            log = redact(completed.stdout + completed.stderr)
            status = "passed" if code == 0 else "failed"
        except (OSError, subprocess.TimeoutExpired) as error:
            code, status, log = None, "unavailable", redact(str(error))
        (output / f"{name}.log").write_text(log, encoding="utf-8")
        result = {
            "gate": name,
            "status": status,
            "exit_code": code,
            "elapsed_seconds": round(time.monotonic() - began, 3),
        }
        results.append(result)
        print(f"{name}: {status} (exit {code})", flush=True)
    if not actionlint:
        results.append(
            {
                "gate": "workflow_syntax",
                "status": "unavailable",
                "reason": "Install pinned actionlint; structural validation is narrower",
            }
        )
    report = {
        "at": datetime.now(UTC).isoformat(),
        "python": sys.version.split()[0],
        "require_db": args.require_db,
        "results": results,
    }
    (output / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    sys.exit(0 if all(r["status"] == "passed" for r in results) else 1)


if __name__ == "__main__":
    main()
