from datetime import date

from pydantic import BaseModel


class RevenueSnapshotSchema(BaseModel):
    snapshot_date: date
    mrr_cents: int
    active_subs: int
    new_subs: int
    churned_subs: int
    revenue_cents: int

    model_config = {"from_attributes": True}


class AnalyticsSummaryResponse(BaseModel):
    current_mrr_cents: int
    mrr_growth_pct: float
    active_subscribers: int
    churn_rate_pct: float
