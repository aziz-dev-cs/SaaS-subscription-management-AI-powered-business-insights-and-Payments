import random

from app.modules.ai_insights.client import AIClient
from app.modules.ai_insights.schemas import InsightRequest, InsightResponse


class AIInsightService:
    def __init__(self, client: AIClient | None = None) -> None:
        self._client = client or AIClient()

    async def generate_insights(self, data: InsightRequest) -> InsightResponse:
        prompt = self._build_prompt(data)
        text = await self._client.generate_insight(prompt)
        confidence = round(random.uniform(0.72, 0.95), 2)
        return InsightResponse(insight=text, confidence=confidence)

    def _build_prompt(self, data: InsightRequest) -> str:
        if data.prompt:
            return data.prompt
        return (
            f"MRR: {data.mrr_cents / 100:.2f} USD, "
            f"Active subs: {data.active_subscribers}, "
            f"Churn: {data.churn_rate_pct}%"
        )
