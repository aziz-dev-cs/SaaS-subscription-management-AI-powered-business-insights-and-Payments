import React, { useState } from 'react';
import { Button } from '@/shared/components/atoms/Button';
import { FormField } from '@/shared/components/molecules/FormField';

interface PaymentMethodFormProps {
  /** Callback with the payment method token (simulated). */
  onSubmit: (token: string, provider: 'stripe' | 'paypal') => void;
  /** Loading state. */
  isLoading: boolean;
}

/**
 * Payment method form (simplified — in production this would be
 * Stripe Elements or PayPal Buttons).
 */
export const PaymentMethodForm: React.FC<PaymentMethodFormProps> = ({
  onSubmit,
  isLoading,
}) => {
  const [provider, setProvider] = useState<'stripe' | 'paypal'>('stripe');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In production: collect token from Stripe.js / PayPal SDK
    const simulatedToken = `pm_simulated_${Date.now()}`;
    onSubmit(simulatedToken, provider);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => setProvider('stripe')}
          className={`flex-1 p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
            provider === 'stripe'
              ? 'border-blue-600 bg-blue-50 text-blue-700'
              : 'border-gray-200 text-gray-600 hover:border-gray-300'
          }`}
        >
          Stripe (Card)
        </button>
        <button
          type="button"
          onClick={() => setProvider('paypal')}
          className={`flex-1 p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
            provider === 'paypal'
              ? 'border-blue-600 bg-blue-50 text-blue-700'
              : 'border-gray-200 text-gray-600 hover:border-gray-300'
          }`}
        >
          PayPal
        </button>
      </div>

      {provider === 'stripe' && (
        <>
          <FormField label="Card number" placeholder="4242 4242 4242 4242" />
          <div className="grid grid-cols-2 gap-3">
            <FormField label="Expiry" placeholder="MM/YY" />
            <FormField label="CVC" placeholder="123" />
          </div>
        </>
      )}

      {provider === 'paypal' && (
        <div className="py-8 text-center text-sm text-gray-500 border rounded-lg">
          You will be redirected to PayPal to complete payment.
        </div>
      )}

      <Button type="submit" isLoading={isLoading} className="w-full">
        Subscribe Now
      </Button>
    </form>
  );
};
