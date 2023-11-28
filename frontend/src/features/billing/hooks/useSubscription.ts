/**
 * Custom hook for subscription data and mutations.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/shared/lib/queryKeys';
import * as billingApi from '../api/billingApi';

export function useSubscription() {
  const queryClient = useQueryClient();

  const { data: subscription, isLoading } = useQuery({
    queryKey: queryKeys.billing.subscription,
    queryFn: billingApi.fetchCurrentSubscription,
  });

  const { data: plans, isLoading: plansLoading } = useQuery({
    queryKey: queryKeys.billing.plans,
    queryFn: billingApi.fetchPlans,
  });

  const createMutation = useMutation({
    mutationFn: billingApi.createSubscription,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.billing.subscription });
    },
  });

  const cancelMutation = useMutation({
    mutationFn: ({ id, immediately }: { id: string; immediately: boolean }) =>
      billingApi.cancelSubscription(id, immediately),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.billing.subscription });
    },
  });

  return {
    subscription: subscription ?? null,
    plans: plans ?? [],
    isLoading: isLoading || plansLoading,
    createSubscription: createMutation.mutate,
    cancelSubscription: cancelMutation.mutate,
    isCreating: createMutation.isPending,
    isCanceling: cancelMutation.isPending,
  };
}
