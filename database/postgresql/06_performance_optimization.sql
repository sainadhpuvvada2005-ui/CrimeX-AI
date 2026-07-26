-- CrimeX AI - performance optimization
-- This script optimizes only CrimeX AI-owned tables.
-- Official FIR table optimization must be handled through the official ERD and
-- database governance process.

BEGIN;

ALTER TABLE crimex_ai."AuditLogs"
    SET (
        autovacuum_vacuum_scale_factor = 0.05,
        autovacuum_analyze_scale_factor = 0.02
    );

ALTER TABLE crimex_ai."ConversationHistory"
    SET (
        autovacuum_vacuum_scale_factor = 0.05,
        autovacuum_analyze_scale_factor = 0.02
    );

ALTER TABLE crimex_ai."PredictionLogs"
    SET (
        autovacuum_vacuum_scale_factor = 0.05,
        autovacuum_analyze_scale_factor = 0.02
    );

ALTER TABLE crimex_ai."UserSessions"
    SET (
        autovacuum_vacuum_scale_factor = 0.10,
        autovacuum_analyze_scale_factor = 0.05
    );

ANALYZE crimex_ai."UserSessions";
ANALYZE crimex_ai."ConversationHistory";
ANALYZE crimex_ai."PredictionLogs";
ANALYZE crimex_ai."AuditLogs";

COMMIT;

-- Official FIR table index recommendations must be generated only after the
-- exact ERD, PK columns, FK columns, query patterns, and KSP DBA approval are
-- available. Do not add indexes to official tables from CrimeX deployment
-- scripts without that approval.

