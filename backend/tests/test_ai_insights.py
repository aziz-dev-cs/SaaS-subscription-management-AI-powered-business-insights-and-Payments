import pytest

from app.modules.ai_insights.schemas import InsightRequest, InsightResponse
from app.modules.ai_insights.service import AIInsightService


@pytest.fixture
def insight_service():
    return AIInsightService()


@pytest.mark.asyncio
async def test_generate_insight(insight_service):
    payload = InsightRequest(
        prompt="Summarize MRR trend",
        mrr_cents=150_00,
        active_subscribers=25,
        churn_rate_pct=4.2,
    )
    result = await insight_service.generate_insights(payload)
    assert isinstance(result, InsightResponse)
    assert len(result.insight) > 0
    assert 0.0 <= result.confidence <= 1.0
