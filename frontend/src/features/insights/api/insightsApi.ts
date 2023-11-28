/**
 * AI Insights API layer.
 */

import { apiClient } from '@/shared/lib/apiClient';
import type { InsightQuery, InsightsList } from '../types';

/** GET /insights/generate */
export async function generateInsights(): Promise<InsightsList> {
  const { data } = await apiClient.get<InsightsList>('/insights/generate');
  return data;
}

/** POST /insights/ask */
export async function askQuestion(question: string): Promise<InsightQuery> {
  const { data } = await apiClient.post<InsightQuery>('/insights/ask', { question });
  return data;
}
