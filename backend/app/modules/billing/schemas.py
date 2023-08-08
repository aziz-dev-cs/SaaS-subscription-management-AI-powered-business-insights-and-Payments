"""Pydantic v2 schemas for the billing module."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.billing.models import (
    BillingInterval,
    InvoiceStatus,
    PaymentProvider,
    SubscriptionStatus,
)


# ── Plan Schemas ─────────────────────────────────────────────────


class PlanResponse(BaseModel):
    """Public representation of a subscription plan."""

    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    price_cents: int
    currency: str
    interval: BillingInterval
    features: dict | None
    is_active: bool
    sort_order: int

    model_config = {"from_attributes": True}


# ── Subscription Schemas ─────────────────────────────────────────


class CreateSubscriptionRequest(BaseModel):
    """Request body for creating a new subscription."""

    plan_id: uuid.UUID
    payment_provider: PaymentProvider
    payment_method_token: str = Field(
        description="One-time token from Stripe.js or PayPal client SDK"
    )


class SubscriptionResponse(BaseModel):
    """Public representation of a subscription."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    plan_id: uuid.UUID
    status: SubscriptionStatus
    payment_provider: PaymentProvider
    current_period_start: datetime | None
    current_period_end: datetime | None
    cancel_at_period_end: bool
    trial_ends_at: datetime | None
    canceled_at: datetime | None
    created_at: datetime
    plan: PlanResponse | None = None

    model_config = {"from_attributes": True}


class CancelSubscriptionRequest(BaseModel):
    """Request body for cancellation — cancel immediately or at period end."""

    cancel_immediately: bool = False


# ── Invoice Schemas ──────────────────────────────────────────────


class InvoiceResponse(BaseModel):
    """Public representation of an invoice."""

    id: uuid.UUID
    subscription_id: uuid.UUID
    amount_cents: int
    currency: str
    status: InvoiceStatus
    paid_at: datetime | None
    period_start: datetime | None
    period_end: datetime | None
    pdf_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Payment Method Schemas ───────────────────────────────────────


class PaymentMethodResponse(BaseModel):
    """Public representation of a stored payment method."""

    id: uuid.UUID
    provider: PaymentProvider
    last_four: str | None
    brand: str | None
    exp_month: int | None
    exp_year: int | None
    is_default: bool

    model_config = {"from_attributes": True}
