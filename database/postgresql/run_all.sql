-- CrimeX AI - psql deployment entrypoint
-- Run from repository root with:
--   psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/postgresql/run_all.sql

\i database/postgresql/00_validate_official_erd.sql
\i database/postgresql/01_ai_tables.sql
\i database/postgresql/02_indexes.sql
\i database/postgresql/03_views.sql
\i database/postgresql/04_stored_procedures.sql
\i database/postgresql/05_triggers.sql
\i database/postgresql/06_performance_optimization.sql

