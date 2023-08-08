"""Billing module domain exceptions."""


class BillingError(Exception):
    """Base exception for billing domain errors."""

    def __init__(self, message: str = "Billing error") -> None:
        self.message = message
        super().__init__(self.message)


class PlanNotFoundError(BillingError):
    def __init__(self, plan_id: str) -> None:
        super().__init__(f"Plan not found: {plan_id}")


class SubscriptionNotFoundError(BillingError):
    def __init__(self, subscription_id: str) -> None:
        super().__init__(f"Subscription not found: {subscription_id}")


class ActiveSubscriptionExistsError(BillingError):
    def __init__(self) -> None:
        super().__init__("Tenant already has an active subscription")


class PaymentProviderError(BillingError):
    """Raised when a payment provider API call fails."""

    def __init__(self, provider: str, detail: str) -> None:
        super().__init__(f"{provider} error: {detail}")


class WebhookVerificationError(BillingError):
    """Raised when webhook signature verification fails."""

    def __init__(self, provider: str) -> None:
        super().__init__(f"Invalid webhook signature from {provider}")
