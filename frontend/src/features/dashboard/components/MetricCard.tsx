import React from 'react';
import { DollarSign, TrendingUp, Users, UserMinus } from 'lucide-react';
import { StatCard } from '@/shared/components/molecules/StatCard';
import { formatCompactCurrency } from '@/shared/lib/formatters';
import type { AnalyticsDashboard } from '../types';

interface MetricCardsProps {
  dashboard: AnalyticsDashboard;
}

/**
 * Grid of top-level KPI metric cards.
 */
export const MetricCards: React.FC<MetricCardsProps> = ({ dashboard }) => {
  const { revenue, subscribers } = dashboard;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Monthly Recurring Revenue"
        value={formatCompactCurrency(revenue.mrr_cents)}
        change={`${revenue.mrr_growth_pct}%`}
        changePositive={revenue.mrr_growth_pct >= 0}
        icon={<DollarSign size={20} />}
      />
      <StatCard
        title="Annual Recurring Revenue"
        value={formatCompactCurrency(revenue.arr_cents)}
        icon={<TrendingUp size={20} />}
      />
      <StatCard
        title="Active Subscribers"
        value={String(subscribers.active_subscribers)}
        change={`${subscribers.net_subscriber_change} net`}
        changePositive={subscribers.net_subscriber_change >= 0}
        icon={<Users size={20} />}
      />
      <StatCard
        title="Churn Rate"
        value={`${subscribers.churn_rate_pct}%`}
        change={`${subscribers.churned_subscribers} lost`}
        changePositive={false}
        icon={<UserMinus size={20} />}
      />
    </div>
  );
};
