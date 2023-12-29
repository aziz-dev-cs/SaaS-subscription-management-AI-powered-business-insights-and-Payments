"""Stripe payment provider implementation.

Wraps the Stripe Python SDK behind the PaymentProviderBase interface.
All Stripe-specific logic is contained within this module.
"""

import stripe

from app.config import get_settings
from app.modules.billing.exceptions import PaymentProviderError, WebhookVerificationError
from app.modules.billing.providers.base import (
    PaymentProviderBase,
    ProviderCustomer,
    ProviderPaymentMethod,
    ProviderSubscription,
)

settings = get_settings()


class StripeProvider(PaymentProviderBase):
    """Stripe integration using the official Python SDK."""

    def __init__(self) -> None:
        stripe.api_key = settings.stripe_secret_key

    async def create_customer(self, email: str, name: str, tenant_id: str) -> ProviderCustomer:
        """Create a Stripe customer.

        Args:
            email: Customer's email address.
            name: Customer's display name.
            tenant_id: Internal tenant ID stored as metadata.

        Returns:
            A ProviderCustomer containing the Stripe customer ID.

        Raises:
            PaymentProviderError: If the Stripe API call fails.
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={"tenant_id": tenant_id},
            )
            return ProviderCustomer(external_id=customer.id, email=email)
        except stripe.StripeError as exc:
            raise PaymentProviderError("stripe", str(exc))

    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        payment_method_token: str,
    ) -> ProviderSubscription:
        """Create a Stripe subscription.

        Attaches the payment method to the customer, sets it as default,
        then creates the subscription.

        Args:
            customer_id: Stripe customer ID.
            price_id: Stripe price ID.
            payment_method_token: Payment method ID from Stripe.js.

        Returns:
            A ProviderSubscription with period information.

        Raises:
            PaymentProviderError: If the Stripe API call fails.
        """
        try:
            stripe.PaymentMethod.attach(payment_method_token, customer=customer_id)
            stripe.Customer.modify(
                customer_id,
                invoice_settings={"default_payment_method": payment_method_token},
            )

            sub = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                expand=["latest_invoice.payment_intent"],
            )

            return ProviderSubscription(
                external_id=sub.id,
                customer_id=customer_id,
                status=sub.status,
                current_period_start=sub.current_period_start,
                current_period_end=sub.current_period_end,
            )
        except stripe.StripeError as exc:
            raise PaymentProviderError("stripe", str(exc))

    async def cancel_subscription(
        self, external_sub_id: str, cancel_immediately: bool
    ) -> ProviderSubscription:
        """Cancel a Stripe subscription.

        Args:
            external_sub_id: The Stripe subscription ID.
            cancel_immediately: If True, cancel now. Otherwise at period end.

        Returns:
            The updated ProviderSubscription.

        Raises:
            PaymentProviderError: If the Stripe API call fails.
        """
        try:
            if cancel_immediately:
                sub = stripe.Subscription.cancel(external_sub_id)
            else:
                sub = stripe.Subscription.modify(
                    external_sub_id,
                    cancel_at_period_end=True,
                )

            return ProviderSubscription(
                external_id=sub.id,
                customer_id=sub.customer,
                status=sub.status,
                current_period_start=sub.current_period_start,
                current_period_end=sub.current_period_end,
            )
        except stripe.StripeError as exc:
            raise PaymentProviderError("stripe", str(exc))

    async def get_payment_method(self, payment_method_id: str) -> ProviderPaymentMethod:
        """Retrieve Stripe payment method card details.

        Args:
            payment_method_id: The Stripe payment method ID.

        Returns:
            A ProviderPaymentMethod with card information.

        Raises:
            PaymentProviderError: If the Stripe API call fails.
        """
        try:
            pm = stripe.PaymentMethod.retrieve(payment_method_id)
            card = pm.card
            return ProviderPaymentMethod(
                external_id=pm.id,
                last_four=card.last4,
                brand=card.brand,
                exp_month=card.exp_month,
                exp_year=card.exp_year,
            )
        except stripe.StripeError as exc:
            raise PaymentProviderError("stripe", str(exc))

    def verify_webhook_signature(self, payload: bytes, signature: str) -> dict:
        """Verify a Stripe webhook signature and return the event data.

        Args:
            payload: Raw request body bytes.
            signature: The Stripe-Signature header value.

        Returns:
            The parsed Stripe event as a dictionary.

        Raises:
            WebhookVerificationError: If signature verification fails.
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.stripe_webhook_secret
            )
            return dict(event)
        except (stripe.SignatureVerificationError, ValueError):
            raise WebhookVerificationError("stripe")
