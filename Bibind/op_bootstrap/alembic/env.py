from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.config.database import SQLALCHEMY_DATABASE_URL
from app.models import Base  # ensure models are imported
import app.models  # noqa: F401

config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
