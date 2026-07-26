# CrimeX AI PostgreSQL Scripts

These scripts use the official Karnataka Police FIR database as an existing source of truth.

They do not create or modify official FIR tables:

- `CaseMaster`
- `Victim`
- `Accused`
- `ComplainantDetails`
- `ActSectionAssociation`
- `ArrestSurrender`
- `ChargesheetDetails`
- `CrimeHead`
- `CrimeSubHead`
- `Court`
- `District`
- `State`
- `Unit`
- `Employee`
- `CaseCategory`
- `GravityOffence`
- `Act`
- `Section`

## Run Order

1. `00_validate_official_erd.sql`
2. `01_ai_tables.sql`
3. `02_indexes.sql`
4. `03_views.sql`
5. `04_stored_procedures.sql`
6. `05_triggers.sql`
7. `06_performance_optimization.sql`

## Important

The official ERD DDL is not included here because CrimeX AI must not redesign the FIR database.

The only created tables are:

- `crimex_ai."ConversationHistory"`
- `crimex_ai."PredictionLogs"`
- `crimex_ai."AuditLogs"`
- `crimex_ai."UserSessions"`

Official-table views are read-only wrappers that preserve the official table shape. Query-specific joins, foreign key assumptions, and official table indexes should be added only after the actual KSP ERD DDL and DBA-approved query contracts are available.

