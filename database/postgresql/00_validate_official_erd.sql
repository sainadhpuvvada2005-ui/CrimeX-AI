-- CrimeX AI - PostgreSQL official ERD validation
-- Purpose:
--   Validate that the official Karnataka Police FIR tables already exist.
--   This script does not create, alter, drop, or redesign any official table.
--
-- Required official FIR tables:
--   CaseMaster, Victim, Accused, ComplainantDetails, ActSectionAssociation,
--   ArrestSurrender, ChargesheetDetails, CrimeHead, CrimeSubHead, Court,
--   District, State, Unit, Employee, CaseCategory, GravityOffence, Act, Section

BEGIN;

CREATE SCHEMA IF NOT EXISTS crimex_ai;

DO $$
DECLARE
    required_tables text[] := ARRAY[
        'CaseMaster',
        'Victim',
        'Accused',
        'ComplainantDetails',
        'ActSectionAssociation',
        'ArrestSurrender',
        'ChargesheetDetails',
        'CrimeHead',
        'CrimeSubHead',
        'Court',
        'District',
        'State',
        'Unit',
        'Employee',
        'CaseCategory',
        'GravityOffence',
        'Act',
        'Section'
    ];
    table_name text;
    missing_tables text[] := ARRAY[]::text[];
    pk_missing_tables text[] := ARRAY[]::text[];
BEGIN
    FOREACH table_name IN ARRAY required_tables LOOP
        IF to_regclass(format('public.%I', table_name)) IS NULL THEN
            missing_tables := array_append(missing_tables, table_name);
        ELSIF NOT EXISTS (
            SELECT 1
            FROM pg_constraint c
            JOIN pg_class r ON r.oid = c.conrelid
            JOIN pg_namespace n ON n.oid = r.relnamespace
            WHERE n.nspname = 'public'
              AND r.relname = table_name
              AND c.contype = 'p'
        ) THEN
            pk_missing_tables := array_append(pk_missing_tables, table_name);
        END IF;
    END LOOP;

    IF array_length(missing_tables, 1) IS NOT NULL THEN
        RAISE EXCEPTION 'Missing official FIR table(s): %', array_to_string(missing_tables, ', ');
    END IF;

    IF array_length(pk_missing_tables, 1) IS NOT NULL THEN
        RAISE EXCEPTION 'Official FIR table(s) without detected primary key: %', array_to_string(pk_missing_tables, ', ');
    END IF;
END;
$$;

CREATE OR REPLACE VIEW crimex_ai.official_table_constraint_summary AS
SELECT
    n.nspname AS table_schema,
    r.relname AS table_name,
    c.conname AS constraint_name,
    CASE c.contype
        WHEN 'p' THEN 'PRIMARY KEY'
        WHEN 'f' THEN 'FOREIGN KEY'
        WHEN 'u' THEN 'UNIQUE'
        WHEN 'c' THEN 'CHECK'
        ELSE c.contype::text
    END AS constraint_type,
    pg_get_constraintdef(c.oid, true) AS constraint_definition
FROM pg_constraint c
JOIN pg_class r ON r.oid = c.conrelid
JOIN pg_namespace n ON n.oid = r.relnamespace
WHERE n.nspname = 'public'
  AND r.relname = ANY (ARRAY[
        'CaseMaster',
        'Victim',
        'Accused',
        'ComplainantDetails',
        'ActSectionAssociation',
        'ArrestSurrender',
        'ChargesheetDetails',
        'CrimeHead',
        'CrimeSubHead',
        'Court',
        'District',
        'State',
        'Unit',
        'Employee',
        'CaseCategory',
        'GravityOffence',
        'Act',
        'Section'
  ])
ORDER BY r.relname, c.contype, c.conname;

COMMIT;

