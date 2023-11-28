/**
 * Billing API layer.
 */

import { apiClient } from '@/shared/lib/apiClient';
import type { PaginatedResponse } from '@/shared/types/api';
import type { Invoice, PaymentMethod, Plan, Subscription } from '../types';

/** GET /billing/plans */
export async function fetchPlans(): Promise<Plan[]> {
  const { data } = await apiClient.get<Plan[]>('/billing/plans');
  return data;
}

/** GET /billing/subscriptions/current */
export async function fetchCurrentSubscription(): Promise<Subscription | null> {
  const { data } = await apiClient.get<Subscription | null>('/billing/subscriptions/current');
  return data;
}

/** POST /billing/subscriptions */
export async function createSubscription(payload: {
  plan_id: string;
  payment_provider: 'stripe' | 'paypal';
  payment_method_token: string;
}): Promise<Subscription> {
  const { data } = await apiClient.post<Subscription>('/billing/subscriptions', payload);
  return data;
}

/** POST /billing/subscriptions/:id/cancel */
export async function cancelSubscription(
  subscriptionId: string,
  cancelImmediately = false
): Promise<Subscription> {
  const { data } = await apiClient.post<Subscription>(
    `/billing/subscriptions/${subscriptionId}/cancel`,
    { cancel_immediately: cancelImmediately }
  );
  return data;
}

/** GET /billing/invoices */
export async function fetchInvoices(
  page = 1,
  pageSize = 20
): Promise<PaginatedResponse<Invoice>> {
  const { data } = await apiClient.get<PaginatedResponse<Invoice>>('/billing/invoices', {
    params: { page, page_size: pageSize },
  });
  return data;
}

/** GET /billing/payment-methods */
export async function fetchPaymentMethods(): Promise<PaymentMethod[]> {
  const { data } = await apiClient.get<PaymentMethod[]>('/billing/payment-methods');
  return data;
}
