import uuid

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, INET, JSONB, UUID
from sqlalchemy.orm import mapped_column, relationship

from app.db.session import Base


class UserSession(Base):
    __tablename__ = "UserSessions"
    __table_args__ = {"schema": "crimex_ai"}

    session_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(Text, nullable=False, index=True)
    role_code = mapped_column(Text, nullable=False)
    unit_code = mapped_column(Text)
    district_code = mapped_column(Text)
    jurisdiction_scope = mapped_column(JSONB, nullable=False, default=dict)
    auth_provider = mapped_column(Text)
    login_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    logout_at = mapped_column(DateTime(timezone=True))
    ip_address = mapped_column(INET)
    user_agent = mapped_column(Text)
    is_active = mapped_column(Boolean, nullable=False, default=True)
    metadata_ = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversations = relationship("ConversationHistory", back_populates="session")


class ConversationHistory(Base):
    __tablename__ = "ConversationHistory"
    __table_args__ = (
        CheckConstraint("confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)"),
        CheckConstraint("status IN ('pending', 'completed', 'blocked', 'failed')"),
        {"schema": "crimex_ai"},
    )

    conversation_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crimex_ai.UserSessions.session_id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = mapped_column(Text, nullable=False, index=True)
    message_sequence = mapped_column(Integer, nullable=False)
    user_prompt = mapped_column(Text, nullable=False)
    normalized_prompt = mapped_column(Text)
    assistant_response = mapped_column(Text)
    intent_name = mapped_column(Text)
    tool_name = mapped_column(Text)
    generated_sql = mapped_column(Text)
    official_tables_used = mapped_column(ARRAY(Text), nullable=False, default=list)
    official_record_refs = mapped_column(JSONB, nullable=False, default=list)
    evidence_refs = mapped_column(JSONB, nullable=False, default=list)
    confidence_score = mapped_column(Numeric(5, 4))
    explanation = mapped_column(JSONB, nullable=False, default=dict)
    safety_flags = mapped_column(JSONB, nullable=False, default=dict)
    latency_ms = mapped_column(Integer)
    status = mapped_column(Text, nullable=False, default="completed")
    error_message = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    session = relationship("UserSession", back_populates="conversations")


class PredictionLog(Base):
    __tablename__ = "PredictionLogs"
    __table_args__ = (
        CheckConstraint("confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)"),
        CheckConstraint("status IN ('pending', 'completed', 'failed', 'superseded')"),
        CheckConstraint("risk_level IS NULL OR risk_level IN ('low', 'medium', 'high', 'critical')"),
        {"schema": "crimex_ai"},
    )

    prediction_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crimex_ai.UserSessions.session_id", ondelete="SET NULL"),
    )
    requested_by = mapped_column(Text, nullable=False)
    prediction_type = mapped_column(Text, nullable=False)
    model_name = mapped_column(Text, nullable=False)
    model_version = mapped_column(Text, nullable=False)
    input_filters = mapped_column(JSONB, nullable=False, default=dict)
    feature_snapshot = mapped_column(JSONB, nullable=False, default=dict)
    official_tables_used = mapped_column(ARRAY(Text), nullable=False, default=list)
    official_record_refs = mapped_column(JSONB, nullable=False, default=list)
    prediction_result = mapped_column(JSONB, nullable=False)
    confidence_score = mapped_column(Numeric(5, 4))
    explanation = mapped_column(JSONB, nullable=False, default=dict)
    risk_level = mapped_column(Text)
    status = mapped_column(Text, nullable=False, default="completed")
    error_message = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AuditLog(Base):
    __tablename__ = "AuditLogs"
    __table_args__ = (
        CheckConstraint("decision IN ('allowed', 'denied', 'masked', 'limited', 'failed')"),
        {"schema": "crimex_ai"},
    )

    audit_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    correlation_id = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    session_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crimex_ai.UserSessions.session_id", ondelete="SET NULL"),
    )
    user_id = mapped_column(Text)
    role_code = mapped_column(Text)
    action_name = mapped_column(Text, nullable=False)
    resource_type = mapped_column(Text, nullable=False)
    resource_ref = mapped_column(Text)
    official_tables_used = mapped_column(ARRAY(Text), nullable=False, default=list)
    request_payload = mapped_column(JSONB, nullable=False, default=dict)
    response_summary = mapped_column(JSONB, nullable=False, default=dict)
    decision = mapped_column(Text, nullable=False, default="allowed")
    reason = mapped_column(Text)
    ip_address = mapped_column(INET)
    user_agent = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

