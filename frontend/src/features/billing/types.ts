/** TypeScript interfaces for the billing feature. */

export interface Plan {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  price_cents: number;
  currency: string;
  interval: 'month' | 'year';
  features: Record<string, unknown> | null;
  is_active: boolean;
  sort_order: number;
}

export interface Subscription {
  id: string;
  tenant_id: string;
  plan_id: string;
  status: 'trialing' | 'active' | 'past_due' | 'canceled' | 'unpaid';
  payment_provider: 'stripe' | 'paypal';
  current_period_start: string | null;
  current_period_end: string | null;
  cancel_at_period_end: boolean;
  trial_ends_at: string | null;
  canceled_at: string | null;
  created_at: string;
  plan: Plan | null;
}

export interface Invoice {
  id: string;
  subscription_id: string;
  amount_cents: number;
  currency: string;
  status: 'draft' | 'open' | 'paid' | 'void' | 'uncollectible';
  paid_at: string | null;
  period_start: string | null;
  period_end: string | null;
  pdf_url: string | null;
  created_at: string;
}

export interface PaymentMethod {
  id: string;
  provider: 'stripe' | 'paypal';
  last_four: string | null;
  brand: string | null;
  exp_month: number | null;
  exp_year: number | null;
  is_default: boolean;
}
