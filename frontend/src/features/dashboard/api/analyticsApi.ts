/**
 * Analytics API layer.
 */

import { apiClient } from '@/shared/lib/apiClient';
import type { AnalyticsDashboard } from '../types';

/** GET /analytics/dashboard */
export async function fetchDashboard(periodDays = 30): Promise<AnalyticsDashboard> {
  const { data } = await apiClient.get<AnalyticsDashboard>('/analytics/dashboard', {
    params: { period_days: periodDays },
  });
  return data;
}
