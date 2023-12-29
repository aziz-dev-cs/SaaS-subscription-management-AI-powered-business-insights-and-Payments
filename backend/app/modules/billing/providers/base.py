"""Abstract base class for payment providers.

Defines the contract that all payment provider implementations (Stripe,
PayPal, etc.) must satisfy. Uses the Strategy pattern so the billing
service can switch providers without changing its own logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCustomer:
    """Represents a customer record in the external payment system."""

    external_id: str
    email: str


@dataclass(frozen=True)
class ProviderSubscription:
    """Represents a subscription record in the external payment system."""

    external_id: str
    customer_id: str
    status: str
    current_period_start: int  # Unix timestamp
    current_period_end: int  # Unix timestamp


@dataclass(frozen=True)
class ProviderPaymentMethod:
    """Represents a payment method in the external payment system."""

    external_id: str
    last_four: str
    brand: str
    exp_month: int
    exp_year: int


class PaymentProviderBase(ABC):
    """Contract for all payment provider integrations."""

    @abstractmethod
    async def create_customer(self, email: str, name: str, tenant_id: str) -> ProviderCustomer:
        """Create a customer in the external payment system.

        Args:
            email: Customer's email address.
            name: Customer's full name.
            tenant_id: Internal tenant identifier for metadata.

        Returns:
            A ProviderCustomer with the external ID.
        """
        ...

    @abstractmethod
    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        payment_method_token: str,
    ) -> ProviderSubscription:
        """Create a subscription for a customer.

        Args:
            customer_id: The external customer ID.
            price_id: The provider-specific price/plan ID.
            payment_method_token: A one-time token from the client SDK.

        Returns:
            A ProviderSubscription with the external subscription ID.
        """
        ...

    @abstractmethod
    async def cancel_subscription(
        self, external_sub_id: str, cancel_immediately: bool
    ) -> ProviderSubscription:
        """Cancel an existing subscription.

        Args:
            external_sub_id: The external subscription ID.
            cancel_immediately: If True, cancel now. If False, cancel at period end.

        Returns:
            The updated ProviderSubscription.
        """
        ...

    @abstractmethod
    async def get_payment_method(self, payment_method_id: str) -> ProviderPaymentMethod:
        """Retrieve payment method details.

        Args:
            payment_method_id: The external payment method ID.

        Returns:
            A ProviderPaymentMethod with card details.
        """
        ...

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str) -> dict:
        """Verify and parse a webhook event payload.

        Args:
            payload: The raw request body bytes.
            signature: The provider's signature header value.

        Returns:
            The parsed event data dictionary.

        Raises:
            WebhookVerificationError: If the signature is invalid.
        """
        ...
