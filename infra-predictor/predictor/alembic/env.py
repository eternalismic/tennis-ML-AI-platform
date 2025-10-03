from alembic import context
from sqlalchemy import engine_from_config, pool
import os
config = context.config
db_url = os.getenv("DATABASE_URL","postgresql+psycopg://tennis:tennispass@tennis-data-db-rw.data.svc:5432/tennis")
config.set_main_option("sqlalchemy.url", db_url)
def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"), include_schemas=True, version_table_schema="public")
    with context.begin_transaction(): context.run_migrations()
def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix='', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, include_schemas=True, version_table_schema="public")
        with context.begin_transaction(): context.run_migrations()
if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()
