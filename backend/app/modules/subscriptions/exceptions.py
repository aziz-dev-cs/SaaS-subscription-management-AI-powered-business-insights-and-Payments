"""Subscriptions module domain exceptions."""


class SubscriptionError(Exception):
    """Base exception for subscription domain errors."""

    def __init__(self, message: str = "Subscription error") -> None:
        self.message = message
        super().__init__(self.message)


class NoActiveSubscriptionError(SubscriptionError):
    def __init__(self) -> None:
        super().__init__("No active subscription found for this tenant")


class PlanChangeNotAllowedError(SubscriptionError):
    def __init__(self, reason: str) -> None:
        super().__init__(f"Plan change not allowed: {reason}")


class UsageLimitExceededError(SubscriptionError):
    def __init__(self, resource: str) -> None:
        super().__init__(f"Usage limit exceeded for {resource}")
