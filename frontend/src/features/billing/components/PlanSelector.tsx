import React from 'react';
import clsx from 'clsx';
import { Check } from 'lucide-react';
import { Button } from '@/shared/components/atoms/Button';
import { Badge } from '@/shared/components/atoms/Badge';
import { formatCurrency } from '@/shared/lib/formatters';
import type { Plan } from '../types';

interface PlanSelectorProps {
  /** Available plans. */
  plans: Plan[];
  /** Currently selected plan ID. */
  selectedPlanId: string | null;
  /** Current subscription's plan ID (if any). */
  currentPlanId?: string;
  /** Callback when a plan is selected. */
  onSelect: (planId: string) => void;
}

/**
 * Plan selection grid with pricing and feature comparison.
 */
export const PlanSelector: React.FC<PlanSelectorProps> = ({
  plans,
  selectedPlanId,
  currentPlanId,
  onSelect,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {plans.map((plan) => {
        const isCurrent = plan.id === currentPlanId;
        const isSelected = plan.id === selectedPlanId;
        const features = plan.features as Record<string, unknown> | null;

        return (
          <div
            key={plan.id}
            className={clsx(
              'relative rounded-xl border-2 p-6 transition-all cursor-pointer',
              isSelected ? 'border-blue-600 shadow-lg' : 'border-gray-200 hover:border-gray-300',
              isCurrent && 'ring-2 ring-blue-100'
            )}
            onClick={() => onSelect(plan.id)}
          >
            {isCurrent && (
              <div className="absolute -top-3 left-4">
                <Badge label="Current Plan" variant="blue" />
              </div>
            )}

            <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
            <p className="mt-1 text-sm text-gray-500">{plan.description}</p>

            <div className="mt-4">
              <span className="text-3xl font-bold text-gray-900">
                {formatCurrency(plan.price_cents, plan.currency.toUpperCase())}
              </span>
              <span className="text-sm text-gray-500">/{plan.interval}</span>
            </div>

            <ul className="mt-6 space-y-3">
              {features &&
                Object.entries(features).map(([key, value]) => (
                  <li key={key} className="flex items-center gap-2 text-sm text-gray-700">
                    <Check size={16} className="text-green-500 flex-shrink-0" />
                    <span>
                      {String(value)} {key.replace(/_/g, ' ')}
                    </span>
                  </li>
                ))}
            </ul>

            <Button
              variant={isSelected ? 'primary' : 'secondary'}
              className="w-full mt-6"
              disabled={isCurrent}
            >
              {isCurrent ? 'Current' : isSelected ? 'Selected' : 'Select'}
            </Button>
          </div>
        );
      })}
    </div>
  );
};
