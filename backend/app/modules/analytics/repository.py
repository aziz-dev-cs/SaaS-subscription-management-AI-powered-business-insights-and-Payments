import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import DailyRevenueSnapshot


class AnalyticsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_snapshot_by_date(self, tenant_id: uuid.UUID, target_date: date) -> DailyRevenueSnapshot | None:
        stmt = select(DailyRevenueSnapshot).where(
            DailyRevenueSnapshot.tenant_id == tenant_id,
            DailyRevenueSnapshot.snapshot_date == target_date,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_snapshots(self, tenant_id: uuid.UUID, start: date, end: date) -> list[DailyRevenueSnapshot]:
        stmt = (
            select(DailyRevenueSnapshot)
            .where(
                DailyRevenueSnapshot.tenant_id == tenant_id,
                DailyRevenueSnapshot.snapshot_date >= start,
                DailyRevenueSnapshot.snapshot_date <= end,
            )
            .order_by(DailyRevenueSnapshot.snapshot_date.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
