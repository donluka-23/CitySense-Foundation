# Primary technology/reference sources reviewed October 2026

- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/latest/
- PostGIS spatial indexes: https://postgis.net/documentation/faq/spatial-indexes/
- OpenTelemetry Python: https://opentelemetry.io/docs/languages/python/
- Ruff official guide: https://docs.astral.sh/ruff/installation/
- Open-Meteo commercial usage limitations: https://open-meteo.com/en/terms
- OpenStreetMap ODbL: https://www.openstreetmap.org/copyright

**Not yet cleared:** any commercial license for live provider usage, geocoding redistribution, on-site collection consent, and exact production provider SLA. **Do not ship commercial live feeds until cleared.**

## Sprint 1 references actually consulted (2026-10-09)

Sprint 2 provider/competitor references and findings are in
[data governance](DATA_GOVERNANCE_AND_LICENSING.md), [competitive analysis](COMPETITIVE_TECHNICAL_ANALYSIS.md),
[MCP design](MCP_INTERFACE_DESIGN.md) and [research review](RESEARCH_VALIDATION_READINESS.md).

- uv locking and exact sync: https://docs.astral.sh/uv/concepts/projects/sync/
- Alembic migrations: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- PostGIS geography meter-distance behavior: https://postgis.net/docs/ST_DWithin.html
- Pydantic aware datetime/contracts: https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/
- PostgreSQL isolated cluster initialization: https://www.postgresql.org/docs/16/app-initdb.html
- Official Windows PostGIS bundle directory: https://download.osgeo.org/postgis/windows/pg16/
- PostGIS Docker support/tags: https://github.com/postgis/docker-postgis
- GitHub workflow syntax: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- uv entry-point security advisory: https://github.com/astral-sh/uv/security/advisories/GHSA-4gg8-gxpx-9rph

Package availability and vulnerabilities were checked through the package index and pip-audit;
the final audited set is retained in `docs/evidence/dependency-audit.json`. The original
provider license statements remain starting assumptions requiring source-specific current
legal review; this session did not enable or clear any provider or claim signed rights.
