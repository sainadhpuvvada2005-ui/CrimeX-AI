-- CrimeX AI - indexes
-- Indexes are created only on CrimeX AI-owned tables.
-- No index is created on official FIR tables in this script, because that would
-- change official database objects without the ERD governance process.

BEGIN;

CREATE INDEX IF NOT EXISTS idx_usersessions_user_active
    ON crimex_ai."UserSessions" (user_id, is_active, last_seen_at DESC);

CREATE INDEX IF NOT EXISTS idx_usersessions_role_unit
    ON crimex_ai."UserSessions" (role_code, unit_code, district_code);

CREATE INDEX IF NOT EXISTS idx_usersessions_metadata_gin
    ON crimex_ai."UserSessions" USING gin (metadata);

CREATE INDEX IF NOT EXISTS idx_conversationhistory_session_sequence
    ON crimex_ai."ConversationHistory" (session_id, message_sequence);

CREATE INDEX IF NOT EXISTS idx_conversationhistory_user_created
    ON crimex_ai."ConversationHistory" (user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversationhistory_intent_created
    ON crimex_ai."ConversationHistory" (intent_name, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversationhistory_tables_gin
    ON crimex_ai."ConversationHistory" USING gin (official_tables_used);

CREATE INDEX IF NOT EXISTS idx_conversationhistory_refs_gin
    ON crimex_ai."ConversationHistory" USING gin (official_record_refs);

CREATE INDEX IF NOT EXISTS idx_predictionlogs_requested_created
    ON crimex_ai."PredictionLogs" (requested_by, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_predictionlogs_model
    ON crimex_ai."PredictionLogs" (model_name, model_version, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_predictionlogs_type_risk
    ON crimex_ai."PredictionLogs" (prediction_type, risk_level, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_predictionlogs_input_filters_gin
    ON crimex_ai."PredictionLogs" USING gin (input_filters);

CREATE INDEX IF NOT EXISTS idx_predictionlogs_result_gin
    ON crimex_ai."PredictionLogs" USING gin (prediction_result);

CREATE INDEX IF NOT EXISTS idx_auditlogs_correlation
    ON crimex_ai."AuditLogs" (correlation_id);

CREATE INDEX IF NOT EXISTS idx_auditlogs_user_created
    ON crimex_ai."AuditLogs" (user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_auditlogs_action_created
    ON crimex_ai."AuditLogs" (action_name, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_auditlogs_resource
    ON crimex_ai."AuditLogs" (resource_type, resource_ref);

CREATE INDEX IF NOT EXISTS idx_auditlogs_decision_created
    ON crimex_ai."AuditLogs" (decision, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_auditlogs_tables_gin
    ON crimex_ai."AuditLogs" USING gin (official_tables_used);

COMMIT;

