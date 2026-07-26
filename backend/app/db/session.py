from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _build_engine():
    engine_options: dict[str, object] = {"pool_pre_ping": True}
    database_url = settings.database_url

    if database_url.startswith("postgresql"):
        try:
            engine_options.update({"pool_size": 10, "max_overflow": 20})
            return create_engine(database_url, **engine_options)
        except ModuleNotFoundError:
            database_url = "sqlite:///./crimex_local.db"

    if database_url.startswith("sqlite"):
        engine_options = {"connect_args": {"check_same_thread": False}}

    return create_engine(database_url, **engine_options)


engine = _build_engine()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
