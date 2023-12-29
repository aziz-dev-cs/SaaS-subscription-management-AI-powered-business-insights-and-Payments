from app.modules.billing.providers.base import (
    PaymentProviderBase,
    ProviderCustomer,
    ProviderSubscription,
)


class PayPalProvider(PaymentProviderBase):
    async def create_customer(self, email: str, name: str, tenant_id: str) -> ProviderCustomer:
        # TODO: call PayPal API
        return ProviderCustomer(external_id=f"pp_cust_{tenant_id}", email=email)

    async def create_subscription(self, customer_id: str, price_id: str, payment_method_token: str) -> ProviderSubscription:
        # TODO: call PayPal subscriptions API
        return ProviderSubscription(external_id="pp_sub_placeholder", customer_id=customer_id, status="active", current_period_start=0, current_period_end=0)

    async def cancel_subscription(self, external_sub_id: str, cancel_immediately: bool) -> ProviderSubscription:
        # TODO: call PayPal cancel API
        return ProviderSubscription(external_id=external_sub_id, customer_id="", status="canceled", current_period_start=0, current_period_end=0)

    async def get_payment_method(self, payment_method_id: str):
        pass

    def verify_webhook_signature(self, payload: bytes, signature: str) -> dict:
        pass
