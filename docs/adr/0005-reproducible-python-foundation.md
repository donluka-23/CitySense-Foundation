# ADR-0005: Locked Python 3.12 foundation and explicit quality gates

Date: 2026-10-09. Status: implemented; human release review pending.

## Problem and constraints

The starter used open dependency ranges and installed whatever happened to be available.
Reproducing a failure, comparing experiment outputs, and reviewing dependency risk require
the same runtime and transitive versions. The workspace is Windows; CI targets Linux.

## Decision

Use Python 3.12.13, uv 0.12.24, exact direct pins and `services/api/uv.lock` with
artifact hashes. `uv sync --locked` rejects metadata/lock drift; `tool.uv.required-version`
also rejects a different installer version. Pin the setuptools build backend.
Ruff, strict mypy, pytest, Bandit and pip-audit are explicit local and CI gates.
Audit the complete exported dependency set, including development tools. Pin Actions
to commit hashes and the PostGIS service to its registry digest. Retain check logs and
JUnit results. Dependabot proposes updates; accepted updates require rerunning checks.

## Alternatives and tradeoffs

Pip with an unhashed requirements list was rejected because it leaves transitive drift.
Poetry would satisfy locking but adds no needed capability here. Python version ranges
across several minors increase the verification matrix before there is a portability need.
Exact pins require maintenance: old pins are not automatically safe. The scan exposed
pytest 8.4.2 and uv 0.8.22 advisories; both were upgraded rather than suppressed.

## Evidence and limits

See [Sprint report](../SPRINT_1_REPORT.md) for actual checks and clean-install evidence.
An advisory scan is time-specific and cannot establish absence of undisclosed vulnerabilities.
Hosted CI and its Docker image have not been executed from this Git-less workspace.
The lock does not pin the host OS; packaging is reproducible, deployment is not yet certified.

Reference: [uv locking semantics](https://docs.astral.sh/uv/concepts/projects/sync/).
Revisit Python support when another deployment platform or supported Python minor is needed.
