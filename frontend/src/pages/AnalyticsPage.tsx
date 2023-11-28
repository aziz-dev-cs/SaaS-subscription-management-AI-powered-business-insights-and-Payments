import React from 'react';
import { Spinner } from '@/shared/components/atoms/Spinner';
import { MetricCards } from '@/features/dashboard/components/MetricCard';
import { RevenueChart } from '@/features/dashboard/components/RevenueChart';
import { ChurnIndicator } from '@/features/dashboard/components/ChurnIndicator';
import { useAnalytics } from '@/features/dashboard/hooks/useAnalytics';

/**
 * Detailed analytics page with expanded charts and metrics.
 */
const AnalyticsPage: React.FC = () => {
  const { dashboard, isLoading, periodDays, setPeriodDays } = useAnalytics();

  if (isLoading || !dashboard) {
    return <Spinner size="lg" className="py-24" />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <select
          value={periodDays}
          onChange={(e) => setPeriodDays(Number(e.target.value))}
          className="text-sm border border-gray-300 rounded-lg px-3 py-2"
        >
          <option value={7}>Last 7 days</option>
          <option value={30}>Last 30 days</option>
          <option value={90}>Last 90 days</option>
          <option value={365}>Last year</option>
        </select>
      </div>

      <MetricCards dashboard={dashboard} />
      <RevenueChart snapshots={dashboard.daily_snapshots} />
      <ChurnIndicator snapshots={dashboard.daily_snapshots} />
    </div>
  );
};

export default AnalyticsPage;
