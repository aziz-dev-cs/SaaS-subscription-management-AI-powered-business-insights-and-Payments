"""Factory Boy factories for generating test data.

Provides consistent, randomized test entities for use in unit
and integration tests.
"""

import uuid
from datetime import datetime, timezone

import factory

from app.modules.auth.models import Tenant, User, UserRole
from app.modules.billing.models import (
    BillingInterval,
    InvoiceStatus,
    PaymentProvider,
    Plan,
    Subscription,
    SubscriptionStatus,
)


class TenantFactory(factory.Factory):
    """Factory for creating Tenant test instances."""

    class Meta:
        model = Tenant

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Tenant {n}")
    slug = factory.Sequence(lambda n: f"tenant-{n}")
    settings = factory.LazyFunction(dict)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class UserFactory(factory.Factory):
    """Factory for creating User test instances."""

    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    tenant_id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = "$2b$12$fakehashforspeed"
    full_name = factory.Faker("name")
    role = UserRole.MEMBER
    is_active = True
    email_verified = False
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class PlanFactory(factory.Factory):
    """Factory for creating Plan test instances."""

    class Meta:
        model = Plan

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Plan {n}")
    slug = factory.Sequence(lambda n: f"plan-{n}")
    description = factory.Faker("sentence")
    price_cents = 2999
    currency = "usd"
    interval = BillingInterval.MONTH
    features = factory.LazyFunction(lambda: {"max_seats": 10, "api_calls_limit": 5000})
    is_active = True
    sort_order = factory.Sequence(lambda n: n)


class SubscriptionFactory(factory.Factory):
    """Factory for creating Subscription test instances."""

    class Meta:
        model = Subscription

    id = factory.LazyFunction(uuid.uuid4)
    tenant_id = factory.LazyFunction(uuid.uuid4)
    plan_id = factory.LazyFunction(uuid.uuid4)
    status = SubscriptionStatus.ACTIVE
    payment_provider = PaymentProvider.STRIPE
    external_sub_id = factory.Sequence(lambda n: f"sub_{n}")
    external_cust_id = factory.Sequence(lambda n: f"cus_{n}")
    cancel_at_period_end = False
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
