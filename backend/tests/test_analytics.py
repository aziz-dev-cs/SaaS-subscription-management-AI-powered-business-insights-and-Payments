from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.analytics.service import AnalyticsService


@pytest.fixture
def analytics_service():
    repo = AsyncMock()
    repo.list_snapshots.return_value = [
        MagicMock(mrr_cents=100_00, active_subs=10, churned_subs=1, snapshot_date="2025-12-01"),
        MagicMock(mrr_cents=120_00, active_subs=12, churned_subs=0, snapshot_date="2025-12-31"),
    ]
    repo.get_snapshot_by_date.return_value = MagicMock(
        mrr_cents=120_00, active_subs=12, churned_subs=0,
    )
    return AnalyticsService(repo=repo)


@pytest.mark.asyncio
async def test_mrr_summary(analytics_service):
    summary = await analytics_service.get_mrr_summary("tenant_a")
    assert summary is not None


@pytest.mark.asyncio
async def test_snapshot_fetch(analytics_service):
    snapshots = await analytics_service.repo.list_snapshots("tenant_a")
    assert len(snapshots) == 2
    assert snapshots[1].mrr_cents == 120_00
