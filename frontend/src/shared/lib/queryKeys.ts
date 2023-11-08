/**
 * Centralized TanStack Query key factory.
 *
 * Using a factory pattern prevents key collisions and makes
 * cache invalidation predictable across features.
 */

export const queryKeys = {
  auth: {
    me: ['auth', 'me'] as const,
  },
  billing: {
    plans: ['billing', 'plans'] as const,
    subscription: ['billing', 'subscription'] as const,
    invoices: (page: number) => ['billing', 'invoices', page] as const,
    paymentMethods: ['billing', 'payment-methods'] as const,
  },
  subscriptions: {
    detail: ['subscriptions', 'detail'] as const,
    usage: ['subscriptions', 'usage'] as const,
  },
  analytics: {
    dashboard: (days: number) => ['analytics', 'dashboard', days] as const,
  },
  insights: {
    list: ['insights', 'list'] as const,
    ask: (question: string) => ['insights', 'ask', question] as const,
  },
} as const;
