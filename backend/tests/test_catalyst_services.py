from app.integrations.catalyst.cron import CatalystCron
from app.integrations.catalyst.quickml import CatalystQuickML
from app.integrations.catalyst.smartbrowz import CatalystSmartBrowz
from app.integrations.catalyst.zia import CatalystZia


def test_quickml_retrieves_documents():
    service = CatalystQuickML()
    docs = service.retrieve("case summary")
    assert docs
    assert any(doc["source"] == "official_erd" for doc in docs)


def test_zia_helpers_prepare_content():
    service = CatalystZia()
    assert service.ocr("evidence.png", {"language": "en"})["result"] == "ocr-ready"
    assert service.speech_to_text("voice.wav")["result"] == "transcript-ready"


def test_cron_and_reports_helpers_expose_jobs():
    cron = CatalystCron()
    report = CatalystSmartBrowz().generate_report("daily", {"user": "admin"})

    assert "daily_sync" in cron.list_jobs()
    assert report["status"] == "generated"
