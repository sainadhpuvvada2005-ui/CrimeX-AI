from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_permission
from app.schemas.auth import CurrentUser
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction import PredictionService

router = APIRouter()


@router.post("/crime-risk", response_model=PredictionResponse)
def run_prediction(
    payload: PredictionRequest,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("prediction:run"))],
) -> PredictionResponse:
    return PredictionService(db).run(payload, user)

