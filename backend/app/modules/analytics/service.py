import uuid
from datetime import date, timedelta

from app.modules.analytics.repository import AnalyticsRepository


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository) -> None:
        self._repo = repo

    async def get_mrr_summary(self, tenant_id: uuid.UUID) -> dict:
        today = date.today()
        start = today - timedelta(days=30)
        snapshots = await self._repo.list_snapshots(tenant_id, start, today)

        if not snapshots:
            return {"current_mrr_cents": 0, "mrr_growth_pct": 0.0}

        current_mrr = snapshots[-1].mrr_cents
        previous_mrr = snapshots[0].mrr_cents
        growth = ((current_mrr - previous_mrr) / previous_mrr * 100) if previous_mrr else 0.0

        return {"current_mrr_cents": current_mrr, "mrr_growth_pct": round(growth, 2)}

    async def get_basic_churn(self, tenant_id: uuid.UUID) -> dict:
        today = date.today()
        start = today - timedelta(days=30)
        snapshots = await self._repo.list_snapshots(tenant_id, start, today)

        total_churned = sum(s.churned_subs for s in snapshots)
        active = snapshots[-1].active_subs if snapshots else 0
        churn_rate = (total_churned / active * 100) if active else 0.0

        return {"churned_subscribers": total_churned, "churn_rate_pct": round(churn_rate, 2)}
