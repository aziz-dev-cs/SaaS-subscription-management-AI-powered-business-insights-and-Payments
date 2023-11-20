/**
 * Custom hook for analytics dashboard data.
 */

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { queryKeys } from '@/shared/lib/queryKeys';
import * as analyticsApi from '../api/analyticsApi';

export function useAnalytics() {
  const [periodDays, setPeriodDays] = useState(30);

  const { data, isLoading, error } = useQuery({
    queryKey: queryKeys.analytics.dashboard(periodDays),
    queryFn: () => analyticsApi.fetchDashboard(periodDays),
  });

  return {
    dashboard: data ?? null,
    isLoading,
    error,
    periodDays,
    setPeriodDays,
  };
}
