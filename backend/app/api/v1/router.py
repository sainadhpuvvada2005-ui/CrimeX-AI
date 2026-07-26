from fastapi import APIRouter

from app.api.v1.routes import (
    accused,
    auth,
    cases,
    chatbot,
    dashboard,
    health,
    neo4j,
    prediction,
    reports,
    victim,
    analytics,
    voice,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(cases.router, prefix="/cases", tags=["Case Management"])
api_router.include_router(victim.router, prefix="/victims", tags=["Victim"])
api_router.include_router(accused.router, prefix="/accused", tags=["Accused"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Crime Analytics"])
api_router.include_router(prediction.router, prefix="/prediction", tags=["Prediction"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
api_router.include_router(neo4j.router, prefix="/neo4j", tags=["Neo4j"])

