from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CrimeX AI API"
    environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = Field(default="sqlite:///./crimex_local.db", validation_alias="DATABASE_URL")

    jwt_secret_key: str = Field(default="dev-jwt-secret", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    catalyst_enabled: bool = Field(default=True, validation_alias="CATALYST_ENABLED")
    catalyst_namespace: str = Field(default="crimex", validation_alias="CATALYST_NAMESPACE")
    catalyst_storage_root: str | None = Field(default=None, validation_alias="CATALYST_STORAGE_ROOT")
    mfa_required: bool = Field(default=False, validation_alias="MFA_REQUIRED")

    # Production environment variables
    secret_key: str = Field(default="dev-secret", validation_alias="SECRET_KEY")
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    cache_url: str | None = Field(default=None, validation_alias="CACHE_URL")
    stratus_bucket: str | None = Field(default=None, validation_alias="STRATUS_BUCKET")
    quickml_model: str | None = Field(default=None, validation_alias="QUICKML_MODEL")
    frontend_url: str | None = Field(default=None, validation_alias="FRONTEND_URL")
    backend_url: str | None = Field(default=None, validation_alias="BACKEND_URL")
    port: int = Field(default=8000, validation_alias="PORT")

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    llm_provider: str = "ollama"
    llm_model: str = "llama3"
    ollama_base_url: str = "http://localhost:11434"
    chatbot_max_sql_rows: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: bool | str) -> bool:
        if isinstance(value, bool):
            return value
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "on", "debug", "development", "dev"}:
            return True
        if normalized in {"false", "0", "no", "off", "release", "production", "prod"}:
            return False
        return False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
