import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database import Base


class DailyRevenueSnapshot(Base):
    __tablename__ = "daily_revenue_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    mrr_cents: Mapped[int] = mapped_column(Integer, default=0)
    active_subs: Mapped[int] = mapped_column(Integer, default=0)
    new_subs: Mapped[int] = mapped_column(Integer, default=0)
    churned_subs: Mapped[int] = mapped_column(Integer, default=0)
    revenue_cents: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
