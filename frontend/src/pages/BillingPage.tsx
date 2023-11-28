import React, { useState } from 'react';
import { Spinner } from '@/shared/components/atoms/Spinner';
import { Badge } from '@/shared/components/atoms/Badge';
import { PlanSelector } from '@/features/billing/components/PlanSelector';
import { PaymentMethodForm } from '@/features/billing/components/PaymentMethodForm';
import { InvoiceTable } from '@/features/billing/components/InvoiceTable';
import { useSubscription } from '@/features/billing/hooks/useSubscription';
import { useInvoices } from '@/features/billing/hooks/useInvoices';
import { formatCurrency, formatDate } from '@/shared/lib/formatters';

const statusVariant: Record<string, 'green' | 'yellow' | 'red' | 'gray'> = {
  active: 'green',
  trialing: 'blue',
  past_due: 'yellow',
  canceled: 'red',
  unpaid: 'red',
};

/**
 * Billing page with subscription management and invoice history.
 */
const BillingPage: React.FC = () => {
  const {
    subscription,
    plans,
    isLoading,
    createSubscription,
    isCreating,
  } = useSubscription();
  const invoiceData = useInvoices();
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(null);

  if (isLoading) {
    return <Spinner size="lg" className="py-24" />;
  }

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Billing</h1>

      {/* Current subscription card */}
      {subscription && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                {subscription.plan?.name ?? 'Current Plan'}
              </h3>
              <p className="text-sm text-gray-500 mt-1">
                {subscription.plan
                  ? `${formatCurrency(subscription.plan.price_cents)}/${subscription.plan.interval}`
                  : ''}
              </p>
            </div>
            <Badge
              label={subscription.status}
              variant={statusVariant[subscription.status] ?? 'gray'}
            />
          </div>
          {subscription.current_period_end && (
            <p className="text-sm text-gray-500 mt-3">
              Current period ends {formatDate(subscription.current_period_end, 'long')}
            </p>
          )}
        </div>
      )}

      {/* Plan selection */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          {subscription ? 'Change Plan' : 'Choose a Plan'}
        </h2>
        <PlanSelector
          plans={plans}
          selectedPlanId={selectedPlanId}
          currentPlanId={subscription?.plan_id}
          onSelect={setSelectedPlanId}
        />
      </div>

      {/* Payment form — shown when a new plan is selected */}
      {selectedPlanId && selectedPlanId !== subscription?.plan_id && (
        <div className="max-w-md">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Payment Details</h2>
          <PaymentMethodForm
            isLoading={isCreating}
            onSubmit={(token, provider) =>
              createSubscription({
                plan_id: selectedPlanId,
                payment_provider: provider,
                payment_method_token: token,
              })
            }
          />
        </div>
      )}

      {/* Invoice history */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Invoice History</h2>
        <InvoiceTable
          invoices={invoiceData.invoices}
          page={invoiceData.page}
          totalPages={invoiceData.totalPages}
          onNextPage={invoiceData.nextPage}
          onPrevPage={invoiceData.prevPage}
        />
      </div>
    </div>
  );
};

export default BillingPage;
