/**
 * Custom hook for AI insights data and question mutations.
 */

import { useQuery, useMutation } from '@tanstack/react-query';
import { queryKeys } from '@/shared/lib/queryKeys';
import * as insightsApi from '../api/insightsApi';

export function useInsights() {
  const {
    data: insightsList,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: queryKeys.insights.list,
    queryFn: insightsApi.generateInsights,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });

  const askMutation = useMutation({
    mutationFn: insightsApi.askQuestion,
  });

  return {
    insights: insightsList?.insights ?? [],
    modelUsed: insightsList?.model_used ?? '',
    isLoading,
    regenerate: refetch,
    askQuestion: askMutation.mutate,
    questionAnswer: askMutation.data ?? null,
    isAsking: askMutation.isPending,
  };
}
