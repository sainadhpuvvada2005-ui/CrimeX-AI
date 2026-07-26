from sqlalchemy.orm import Session

from app.repositories.ai import PredictionRepository
from app.schemas.auth import CurrentUser
from app.schemas.prediction import PredictionRequest, PredictionResponse


class PredictionService:
    def __init__(self, db: Session):
        self.db = db

    def run(self, payload: PredictionRequest, user: CurrentUser) -> PredictionResponse:
        result = {
            "risk_level": "medium",
            "summary": "Baseline placeholder prediction. Connect approved trained model before production decisions.",
            "filters": payload.filters,
        }
        explanation = {
            "method": "baseline",
            "limitations": "No trained model artifact is configured yet.",
            "official_tables_used": ["CaseMaster"],
        }
        row = PredictionRepository(self.db).create(
            requested_by=user.user_id,
            prediction_type=payload.prediction_type,
            model_name="baseline-risk-model",
            model_version="0.1.0",
            input_filters=payload.filters,
            official_tables_used=["CaseMaster"],
            prediction_result=result,
            confidence_score=0.5,
            explanation=explanation,
            risk_level="medium",
        )
        return PredictionResponse(
            prediction_id=str(row.prediction_id),
            prediction_type=payload.prediction_type,
            result=result,
            confidence_score=0.5,
            explanation=explanation,
        )

