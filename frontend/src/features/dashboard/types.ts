/** TypeScript interfaces for the dashboard/analytics feature. */

export interface RevenueMetrics {
  mrr_cents: number;
  arr_cents: number;
  mrr_growth_pct: number;
  total_revenue_cents: number;
}

export interface SubscriberMetrics {
  active_subscribers: number;
  new_subscribers: number;
  churned_subscribers: number;
  churn_rate_pct: number;
  net_subscriber_change: number;
}

export interface DailySnapshot {
  snapshot_date: string;
  mrr_cents: number;
  active_subs: number;
  new_subs: number;
  churned_subs: number;
  revenue_cents: number;
}

export interface AnalyticsDashboard {
  revenue: RevenueMetrics;
  subscribers: SubscriberMetrics;
  daily_snapshots: DailySnapshot[];
  period_start: string;
  period_end: string;
}
