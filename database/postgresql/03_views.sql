-- CrimeX AI - governed views
-- These views expose official FIR tables without creating or modifying them.
-- They preserve the official column structure at view creation time.

BEGIN;

CREATE SCHEMA IF NOT EXISTS crimex_ai;

CREATE OR REPLACE VIEW crimex_ai.v_official_case_master AS
SELECT * FROM public."CaseMaster";

CREATE OR REPLACE VIEW crimex_ai.v_official_victim AS
SELECT * FROM public."Victim";

CREATE OR REPLACE VIEW crimex_ai.v_official_accused AS
SELECT * FROM public."Accused";

CREATE OR REPLACE VIEW crimex_ai.v_official_complainant_details AS
SELECT * FROM public."ComplainantDetails";

CREATE OR REPLACE VIEW crimex_ai.v_official_act_section_association AS
SELECT * FROM public."ActSectionAssociation";

CREATE OR REPLACE VIEW crimex_ai.v_official_arrest_surrender AS
SELECT * FROM public."ArrestSurrender";

CREATE OR REPLACE VIEW crimex_ai.v_official_chargesheet_details AS
SELECT * FROM public."ChargesheetDetails";

CREATE OR REPLACE VIEW crimex_ai.v_official_crime_head AS
SELECT * FROM public."CrimeHead";

CREATE OR REPLACE VIEW crimex_ai.v_official_crime_sub_head AS
SELECT * FROM public."CrimeSubHead";

CREATE OR REPLACE VIEW crimex_ai.v_official_court AS
SELECT * FROM public."Court";

CREATE OR REPLACE VIEW crimex_ai.v_official_district AS
SELECT * FROM public."District";

CREATE OR REPLACE VIEW crimex_ai.v_official_state AS
SELECT * FROM public."State";

CREATE OR REPLACE VIEW crimex_ai.v_official_unit AS
SELECT * FROM public."Unit";

CREATE OR REPLACE VIEW crimex_ai.v_official_employee AS
SELECT * FROM public."Employee";

CREATE OR REPLACE VIEW crimex_ai.v_official_case_category AS
SELECT * FROM public."CaseCategory";

CREATE OR REPLACE VIEW crimex_ai.v_official_gravity_offence AS
SELECT * FROM public."GravityOffence";

CREATE OR REPLACE VIEW crimex_ai.v_official_act AS
SELECT * FROM public."Act";

CREATE OR REPLACE VIEW crimex_ai.v_official_section AS
SELECT * FROM public."Section";

CREATE OR REPLACE VIEW crimex_ai.v_ai_activity_summary AS
SELECT
    date_trunc('day', created_at)::date AS activity_date,
    user_id,
    count(*) AS conversation_count,
    count(*) FILTER (WHERE status = 'completed') AS completed_count,
    count(*) FILTER (WHERE status = 'blocked') AS blocked_count,
    count(*) FILTER (WHERE status = 'failed') AS failed_count,
    avg(latency_ms) AS avg_latency_ms
FROM crimex_ai."ConversationHistory"
GROUP BY date_trunc('day', created_at)::date, user_id;

CREATE OR REPLACE VIEW crimex_ai.v_prediction_summary AS
SELECT
    date_trunc('day', created_at)::date AS prediction_date,
    prediction_type,
    model_name,
    model_version,
    risk_level,
    count(*) AS prediction_count,
    avg(confidence_score) AS avg_confidence_score
FROM crimex_ai."PredictionLogs"
GROUP BY
    date_trunc('day', created_at)::date,
    prediction_type,
    model_name,
    model_version,
    risk_level;

CREATE OR REPLACE VIEW crimex_ai.v_audit_decision_summary AS
SELECT
    date_trunc('day', created_at)::date AS audit_date,
    action_name,
    resource_type,
    decision,
    count(*) AS event_count
FROM crimex_ai."AuditLogs"
GROUP BY
    date_trunc('day', created_at)::date,
    action_name,
    resource_type,
    decision;

COMMIT;

