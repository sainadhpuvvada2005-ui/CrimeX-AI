from app.integrations.catalyst.auth import CatalystAuthService
from app.integrations.catalyst.data_store import CatalystDataStore
from app.integrations.catalyst.nosql import CatalystNoSQL


def test_catalyst_auth_maps_police_roles():
    service = CatalystAuthService()
    claims = service.issue_session("analyst", "dev-password", role="analyst")

    assert claims["role"] == "analyst"
    assert claims["session_id"]
    assert claims["permissions"]


def test_catalyst_nosql_records_and_retrieves_documents():
    store = CatalystNoSQL()
    record_id = store.write("audit_logs", {"action": "login"})
    rows = store.list("audit_logs")

    assert len(rows) >= 1
    assert any(row["id"] == record_id for row in rows)


def test_catalyst_datastore_persists_records():
    datastore = CatalystDataStore(namespace="crimex")
    record_id = datastore.save("sessions", {"user": "admin", "role": "super_admin"})
    saved = datastore.get("sessions", record_id)

    assert saved is not None
    assert saved["user"] == "admin"
