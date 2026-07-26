-- CrimeX AI - AI-owned tables only
-- This file creates only:
--   ConversationHistory
--   PredictionLogs
--   AuditLogs
--   UserSessions
--
-- No official FIR table is created or modified.

BEGIN;

CREATE SCHEMA IF NOT EXISTS crimex_ai;

CREATE TABLE IF NOT EXISTS crimex_ai."UserSessions" (
    session_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id text NOT NULL,
    role_code text NOT NULL,
    unit_code text,
    district_code text,
    jurisdiction_scope jsonb NOT NULL DEFAULT '{}'::jsonb,
    auth_provider text,
    login_at timestamptz NOT NULL DEFAULT now(),
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    logout_at timestamptz,
    ip_address inet,
    user_agent text,
    is_active boolean NOT NULL DEFAULT true,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT usersessions_logout_after_login_chk
        CHECK (logout_at IS NULL OR logout_at >= login_at)
);

CREATE TABLE IF NOT EXISTS crimex_ai."ConversationHistory" (
    conversation_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id uuid NOT NULL REFERENCES crimex_ai."UserSessions"(session_id) ON DELETE CASCADE,
    user_id text NOT NULL,
    message_sequence bigint NOT NULL,
    user_prompt text NOT NULL,
    normalized_prompt text,
    assistant_response text,
    intent_name text,
    tool_name text,
    generated_sql text,
    official_tables_used text[] NOT NULL DEFAULT ARRAY[]::text[],
    official_record_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    confidence_score numeric(5,4),
    explanation jsonb NOT NULL DEFAULT '{}'::jsonb,
    safety_flags jsonb NOT NULL DEFAULT '{}'::jsonb,
    latency_ms integer,
    status text NOT NULL DEFAULT 'completed',
    error_message text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT conversationhistory_message_sequence_uk
        UNIQUE (session_id, message_sequence),
    CONSTRAINT conversationhistory_confidence_chk
        CHECK (confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)),
    CONSTRAINT conversationhistory_status_chk
        CHECK (status IN ('pending', 'completed', 'blocked', 'failed'))
);

CREATE TABLE IF NOT EXISTS crimex_ai."PredictionLogs" (
    prediction_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id uuid REFERENCES crimex_ai."UserSessions"(session_id) ON DELETE SET NULL,
    requested_by text NOT NULL,
    prediction_type text NOT NULL,
    model_name text NOT NULL,
    model_version text NOT NULL,
    input_filters jsonb NOT NULL DEFAULT '{}'::jsonb,
    feature_snapshot jsonb NOT NULL DEFAULT '{}'::jsonb,
    official_tables_used text[] NOT NULL DEFAULT ARRAY[]::text[],
    official_record_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    prediction_result jsonb NOT NULL,
    confidence_score numeric(5,4),
    explanation jsonb NOT NULL DEFAULT '{}'::jsonb,
    risk_level text,
    status text NOT NULL DEFAULT 'completed',
    error_message text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT predictionlogs_confidence_chk
        CHECK (confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)),
    CONSTRAINT predictionlogs_status_chk
        CHECK (status IN ('pending', 'completed', 'failed', 'superseded')),
    CONSTRAINT predictionlogs_risk_level_chk
        CHECK (risk_level IS NULL OR risk_level IN ('low', 'medium', 'high', 'critical'))
);

CREATE TABLE IF NOT EXISTS crimex_ai."AuditLogs" (
    audit_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    correlation_id uuid NOT NULL DEFAULT gen_random_uuid(),
    session_id uuid REFERENCES crimex_ai."UserSessions"(session_id) ON DELETE SET NULL,
    user_id text,
    role_code text,
    action_name text NOT NULL,
    resource_type text NOT NULL,
    resource_ref text,
    official_tables_used text[] NOT NULL DEFAULT ARRAY[]::text[],
    request_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    response_summary jsonb NOT NULL DEFAULT '{}'::jsonb,
    decision text NOT NULL DEFAULT 'allowed',
    reason text,
    ip_address inet,
    user_agent text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT auditlogs_decision_chk
        CHECK (decision IN ('allowed', 'denied', 'masked', 'limited', 'failed'))
);

COMMIT;

