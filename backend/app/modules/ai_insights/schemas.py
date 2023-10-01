from pydantic import BaseModel


class InsightRequest(BaseModel):
    prompt: str | None = None
    mrr_cents: int = 0
    active_subscribers: int = 0
    churn_rate_pct: float = 0.0


class InsightResponse(BaseModel):
    insight: str
    confidence: float = 0.85
