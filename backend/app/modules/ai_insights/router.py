from fastapi import APIRouter

from app.modules.ai_insights.schemas import InsightRequest, InsightResponse
from app.modules.ai_insights.service import AIInsightService

router = APIRouter(prefix="/insights", tags=["AI Insights"])


@router.post("/generate", response_model=InsightResponse)
async def generate_insight(payload: InsightRequest):
    service = AIInsightService()
    return await service.generate_insights(payload)
