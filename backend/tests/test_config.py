import pytest

from app.core.config import Settings


def test_settings_accepts_production_env_aliases(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "prod-secret")
    monkeypatch.setenv("JWT_SECRET", "jwt-secret")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CACHE_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("STRATUS_BUCKET", "reports")
    monkeypatch.setenv("QUICKML_MODEL", "crime-model")
    monkeypatch.setenv("FRONTEND_URL", "https://app.example.com")
    monkeypatch.setenv("BACKEND_URL", "https://api.example.com")
    monkeypatch.setenv("PORT", "9000")

    settings = Settings()

    assert settings.jwt_secret_key == "jwt-secret"
    assert settings.openai_api_key == "sk-test"
    assert settings.cache_url == "redis://localhost:6379/0"
    assert settings.stratus_bucket == "reports"
    assert settings.quickml_model == "crime-model"
    assert settings.frontend_url == "https://app.example.com"
    assert settings.backend_url == "https://api.example.com"
    assert settings.port == 9000
