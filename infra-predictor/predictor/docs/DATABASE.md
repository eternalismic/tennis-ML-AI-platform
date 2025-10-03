# Database (CNPG) schema: raw → curated
- Schemas: `raw` (ingest), `curated` (features/preds).
- Run `alembic upgrade head` with `DATABASE_URL` env set.
- Loader: `src/etl/historical_loader.py` → writes to `raw.matches`.
- GE: `src/quality/run_gx.py` validates `raw.matches`; scheduled in Airflow.
