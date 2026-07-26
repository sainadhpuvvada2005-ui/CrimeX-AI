-- CrimeX AI - stored procedures and functions
-- These functions write only to CrimeX AI-owned tables.

BEGIN;

CREATE SCHEMA IF NOT EXISTS crimex_ai;

CREATE OR REPLACE FUNCTION crimex_ai.start_user_session(
    p_user_id text,
    p_role_code text,
    p_unit_code text DEFAULT NULL,
    p_district_code text DEFAULT NULL,
    p_jurisdiction_scope jsonb DEFAULT '{}'::jsonb,
    p_auth_provider text DEFAULT NULL,
    p_ip_address inet DEFAULT NULL,
    p_user_agent text DEFAULT NULL,
    p_metadata jsonb DEFAULT '{}'::jsonb
)
RETURNS uuid
LANGUAGE plpgsql
AS $$
DECLARE
    v_session_id uuid;
BEGIN
    INSERT INTO crimex_ai."UserSessions" (
        user_id,
        role_code,
        unit_code,
        district_code,
        jurisdiction_scope,
        auth_provider,
        ip_address,
        user_agent,
        metadata
    )
    VALUES (
        p_user_id,
        p_role_code,
        p_unit_code,
        p_district_code,
        COALESCE(p_jurisdiction_scope, '{}'::jsonb),
        p_auth_provider,
        p_ip_address,
        p_user_agent,
        COALESCE(p_metadata, '{}'::jsonb)
    )
    RETURNING session_id INTO v_session_id;

    RETURN v_session_id;
END;
$$;

CREATE OR REPLACE FUNCTION crimex_ai.end_user_session(
    p_session_id uuid
)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE crimex_ai."UserSessions"
    SET
        logout_at = now(),
        last_seen_at = now(),
        is_active = false,
        updated_at = now()
    WHERE session_id = p_session_id;
END;
$$;

CREATE OR REPLACE FUNCTION crimex_ai.log_conversation(
    p_session_id uuid,
    p_user_id text,
    p_message_sequence bigint,
    p_user_prompt text,
    p_normalized_prompt text DEFAULT NULL,
    p_assistant_response text DEFAULT NULL,
    p_intent_name text DEFAULT NULL,
    p_tool_name text DEFAULT NULL,
    p_generated_sql text DEFAULT NULL,
    p_official_tables_used text[] DEFAULT ARRAY[]::text[],
    p_official_record_refs jsonb DEFAULT '[]'::jsonb,
    p_evidence_refs jsonb DEFAULT '[]'::jsonb,
    p_confidence_score numeric DEFAULT NULL,
    p_explanation jsonb DEFAULT '{}'::jsonb,
    p_safety_flags jsonb DEFAULT '{}'::jsonb,
    p_latency_ms integer DEFAULT NULL,
    p_status text DEFAULT 'completed',
    p_error_message text DEFAULT NULL
)
RETURNS uuid
LANGUAGE plpgsql
AS $$
DECLARE
    v_conversation_id uuid;
BEGIN
    INSERT INTO crimex_ai."ConversationHistory" (
        session_id,
        user_id,
        message_sequence,
        user_prompt,
        normalized_prompt,
        assistant_response,
        intent_name,
        tool_name,
        generated_sql,
        official_tables_used,
        official_record_refs,
        evidence_refs,
        confidence_score,
        explanation,
        safety_flags,
        latency_ms,
        status,
        error_message
    )
    VALUES (
        p_session_id,
        p_user_id,
        p_message_sequence,
        p_user_prompt,
        p_normalized_prompt,
        p_assistant_response,
        p_intent_name,
        p_tool_name,
        p_generated_sql,
        COALESCE(p_official_tables_used, ARRAY[]::text[]),
        COALESCE(p_official_record_refs, '[]'::jsonb),
        COALESCE(p_evidence_refs, '[]'::jsonb),
        p_confidence_score,
        COALESCE(p_explanation, '{}'::jsonb),
        COALESCE(p_safety_flags, '{}'::jsonb),
        p_latency_ms,
        COALESCE(p_status, 'completed'),
        p_error_message
    )
    RETURNING conversation_id INTO v_conversation_id;

    UPDATE crimex_ai."UserSessions"
    SET last_seen_at = now(), updated_at = now()
    WHERE session_id = p_session_id;

    RETURN v_conversation_id;
END;
$$;

CREATE OR REPLACE FUNCTION crimex_ai.log_prediction(
    p_session_id uuid,
    p_requested_by text,
    p_prediction_type text,
    p_model_name text,
    p_model_version text,
    p_prediction_result jsonb,
    p_input_filters jsonb DEFAULT '{}'::jsonb,
    p_feature_snapshot jsonb DEFAULT '{}'::jsonb,
    p_official_tables_used text[] DEFAULT ARRAY[]::text[],
    p_official_record_refs jsonb DEFAULT '[]'::jsonb,
    p_confidence_score numeric DEFAULT NULL,
    p_explanation jsonb DEFAULT '{}'::jsonb,
    p_risk_level text DEFAULT NULL,
    p_status text DEFAULT 'completed',
    p_error_message text DEFAULT NULL
)
RETURNS uuid
LANGUAGE plpgsql
AS $$
DECLARE
    v_prediction_id uuid;
BEGIN
    INSERT INTO crimex_ai."PredictionLogs" (
        session_id,
        requested_by,
        prediction_type,
        model_name,
        model_version,
        input_filters,
        feature_snapshot,
        official_tables_used,
        official_record_refs,
        prediction_result,
        confidence_score,
        explanation,
        risk_level,
        status,
        error_message
    )
    VALUES (
        p_session_id,
        p_requested_by,
        p_prediction_type,
        p_model_name,
        p_model_version,
        COALESCE(p_input_filters, '{}'::jsonb),
        COALESCE(p_feature_snapshot, '{}'::jsonb),
        COALESCE(p_official_tables_used, ARRAY[]::text[]),
        COALESCE(p_official_record_refs, '[]'::jsonb),
        p_prediction_result,
        p_confidence_score,
        COALESCE(p_explanation, '{}'::jsonb),
        p_risk_level,
        COALESCE(p_status, 'completed'),
        p_error_message
    )
    RETURNING prediction_id INTO v_prediction_id;

    RETURN v_prediction_id;
END;
$$;

CREATE OR REPLACE FUNCTION crimex_ai.log_audit_event(
    p_correlation_id uuid,
    p_session_id uuid,
    p_user_id text,
    p_role_code text,
    p_action_name text,
    p_resource_type text,
    p_resource_ref text DEFAULT NULL,
    p_official_tables_used text[] DEFAULT ARRAY[]::text[],
    p_request_payload jsonb DEFAULT '{}'::jsonb,
    p_response_summary jsonb DEFAULT '{}'::jsonb,
    p_decision text DEFAULT 'allowed',
    p_reason text DEFAULT NULL,
    p_ip_address inet DEFAULT NULL,
    p_user_agent text DEFAULT NULL
)
RETURNS uuid
LANGUAGE plpgsql
AS $$
DECLARE
    v_audit_id uuid;
BEGIN
    INSERT INTO crimex_ai."AuditLogs" (
        correlation_id,
        session_id,
        user_id,
        role_code,
        action_name,
        resource_type,
        resource_ref,
        official_tables_used,
        request_payload,
        response_summary,
        decision,
        reason,
        ip_address,
        user_agent
    )
    VALUES (
        COALESCE(p_correlation_id, gen_random_uuid()),
        p_session_id,
        p_user_id,
        p_role_code,
        p_action_name,
        p_resource_type,
        p_resource_ref,
        COALESCE(p_official_tables_used, ARRAY[]::text[]),
        COALESCE(p_request_payload, '{}'::jsonb),
        COALESCE(p_response_summary, '{}'::jsonb),
        COALESCE(p_decision, 'allowed'),
        p_reason,
        p_ip_address,
        p_user_agent
    )
    RETURNING audit_id INTO v_audit_id;

    RETURN v_audit_id;
END;
$$;

COMMIT;

