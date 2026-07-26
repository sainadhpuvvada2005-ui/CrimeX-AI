-- CrimeX AI - triggers
-- Triggers are attached only to CrimeX AI-owned tables.
-- No trigger is attached to any official FIR table.

BEGIN;

CREATE SCHEMA IF NOT EXISTS crimex_ai;

CREATE OR REPLACE FUNCTION crimex_ai.set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_usersessions_set_updated_at
    ON crimex_ai."UserSessions";

CREATE TRIGGER trg_usersessions_set_updated_at
BEFORE UPDATE ON crimex_ai."UserSessions"
FOR EACH ROW
EXECUTE FUNCTION crimex_ai.set_updated_at();

DROP TRIGGER IF EXISTS trg_conversationhistory_set_updated_at
    ON crimex_ai."ConversationHistory";

CREATE TRIGGER trg_conversationhistory_set_updated_at
BEFORE UPDATE ON crimex_ai."ConversationHistory"
FOR EACH ROW
EXECUTE FUNCTION crimex_ai.set_updated_at();

DROP TRIGGER IF EXISTS trg_predictionlogs_set_updated_at
    ON crimex_ai."PredictionLogs";

CREATE TRIGGER trg_predictionlogs_set_updated_at
BEFORE UPDATE ON crimex_ai."PredictionLogs"
FOR EACH ROW
EXECUTE FUNCTION crimex_ai.set_updated_at();

COMMIT;

