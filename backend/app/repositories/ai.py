import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai import AuditLog, ConversationHistory, PredictionLog, UserSession


class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, user_id: str, role_code: str, unit_code: str | None, district_code: str | None) -> UserSession:
        session = UserSession(
            user_id=user_id,
            role_code=role_code,
            unit_code=unit_code,
            district_code=district_code,
            jurisdiction_scope={},
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get(self, session_id: uuid.UUID) -> UserSession | None:
        return self.db.get(UserSession, session_id)


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def next_sequence(self, session_id: uuid.UUID) -> int:
        rows = self.db.execute(
            select(ConversationHistory.message_sequence)
            .where(ConversationHistory.session_id == session_id)
            .order_by(ConversationHistory.message_sequence.desc())
            .limit(1)
        ).first()
        return int(rows[0]) + 1 if rows else 1

    def create(self, **values: Any) -> ConversationHistory:
        row = ConversationHistory(**values)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_by_session(self, session_id: uuid.UUID, limit: int = 50) -> list[ConversationHistory]:
        return list(
            self.db.execute(
                select(ConversationHistory)
                .where(ConversationHistory.session_id == session_id)
                .order_by(ConversationHistory.message_sequence.asc())
                .limit(limit)
            )
            .scalars()
            .all()
        )


class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **values: Any) -> PredictionLog:
        row = PredictionLog(**values)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **values: Any) -> AuditLog:
        row = AuditLog(**values)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row
