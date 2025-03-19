from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Import your database URL from your project
try:
    from database import DATABASE_URL
    config.set_main_option('sqlalchemy.url', DATABASE_URL)
except ImportError:
    # Fall back to the URL in alembic.ini if import fails
    pass

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your models
# Adjust the import path to match your project structure
try:
    from src.models import Base
except ImportError:
    try:
        from models import Base
    except ImportError:
        raise Exception(
            "Could not import Base from models. "
            "Make sure your models are properly defined with a Base object."
        )

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
