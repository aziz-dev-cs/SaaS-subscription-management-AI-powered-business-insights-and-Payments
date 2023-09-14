import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import get_db_session
from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.schemas import AnalyticsSummaryResponse, RevenueSnapshotSchema
from app.modules.analytics.service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _get_service(session: AsyncSession = Depends(get_db_session)) -> AnalyticsService:
    return AnalyticsService(repo=AnalyticsRepository(session))


@router.get("/mrr")
async def get_mrr(
    tenant_id: uuid.UUID = Query(...),
    service: AnalyticsService = Depends(_get_service),
):
    return await service.get_mrr_summary(tenant_id)


@router.get("/churn")
async def get_churn(
    tenant_id: uuid.UUID = Query(...),
    service: AnalyticsService = Depends(_get_service),
):
    return await service.get_basic_churn(tenant_id)


@router.get("/snapshots", response_model=list[RevenueSnapshotSchema])
async def list_snapshots(
    tenant_id: uuid.UUID = Query(...),
    days: int = Query(default=30, ge=7, le=365),
    service: AnalyticsService = Depends(_get_service),
):
    today = date.today()
    start = today - timedelta(days=days)
    snapshots = await service._repo.list_snapshots(tenant_id, start, today)
    return snapshots
