"""SQLAlchemy ORM models for the billing domain.

Defines Plan, Subscription, PaymentMethod, Invoice, and WebhookEvent
tables with full type annotations and enum constraints.
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class BillingInterval(str, enum.Enum):
    MONTH = "month"
    YEAR = "year"


class PaymentProvider(str, enum.Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"


class SubscriptionStatus(str, enum.Enum):
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    VOID = "void"
    UNCOLLECTIBLE = "uncollectible"


class WebhookEventStatus(str, enum.Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Plan(Base):
    """Subscription plan with pricing and feature definitions."""

    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="usd")
    interval: Mapped[BillingInterval] = mapped_column(
        Enum(BillingInterval, name="billing_interval"), nullable=False
    )
    features: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    stripe_price_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    paypal_plan_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="plan"
    )


class Subscription(Base):
    """Active subscription linking a tenant to a plan."""

    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus, name="subscription_status"), nullable=False
    )
    payment_provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider, name="payment_provider"), nullable=False
    )
    external_sub_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    external_cust_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    current_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False)
    trial_ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    canceled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    plan: Mapped[Plan] = relationship("Plan", back_populates="subscriptions", lazy="joined")
    invoices: Mapped[list["Invoice"]] = relationship("Invoice", back_populates="subscription")


class PaymentMethod(Base):
    """Stored payment method (card, PayPal, etc.) for a tenant."""

    __tablename__ = "payment_methods"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider, name="payment_provider", create_type=False), nullable=False
    )
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    last_four: Mapped[str | None] = mapped_column(String(4), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(50), nullable=True)
    exp_month: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    exp_year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class Invoice(Base):
    """Billing invoice generated for a subscription period."""

    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False, index=True
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    external_inv_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="usd")
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus, name="invoice_status"), nullable=False
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    subscription: Mapped[Subscription] = relationship(
        "Subscription", back_populates="invoices", lazy="joined"
    )


class WebhookEvent(Base):
    """Tracks inbound webhook events for idempotent processing."""

    __tablename__ = "webhook_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider, name="payment_provider", create_type=False), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    external_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[WebhookEventStatus] = mapped_column(
        Enum(WebhookEventStatus, name="webhook_event_status"),
        default=WebhookEventStatus.RECEIVED,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    next_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class DailyRevenueSnapshot(Base):
    """Materialized daily revenue and subscriber metrics per tenant."""

    __tablename__ = "daily_revenue_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )
    snapshot_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    mrr_cents: Mapped[int] = mapped_column(Integer, default=0)
    active_subs: Mapped[int] = mapped_column(Integer, default=0)
    new_subs: Mapped[int] = mapped_column(Integer, default=0)
    churned_subs: Mapped[int] = mapped_column(Integer, default=0)
    revenue_cents: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
