"""Explicit URL; migrations never run implicitly on API startup."""

import os

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

url = os.environ.get("CITYSENSE_DATABASE_URL")
if not url:
    raise RuntimeError("CITYSENSE_DATABASE_URL must identify an explicitly selected database")
sqlalchemy_url = url.replace("postgresql://", "postgresql+psycopg://", 1)
if context.is_offline_mode():
    context.configure(url=sqlalchemy_url, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(sqlalchemy_url, poolclass=NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()
