/**
 * Formatting utilities for currency, dates, and percentages.
 */

/**
 * Format cents as a dollar string (e.g., 2999 → "$29.99").
 * @param cents - Amount in cents.
 * @param currency - ISO 4217 currency code.
 */
export function formatCurrency(cents: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(cents / 100);
}

/**
 * Format a date string or Date object for display.
 * @param date - The date to format.
 * @param style - 'short' for compact, 'long' for verbose.
 */
export function formatDate(
  date: string | Date,
  style: 'short' | 'long' = 'short'
): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: style === 'long' ? 'long' : 'short',
    day: 'numeric',
  });
}

/**
 * Format a decimal as a percentage string (e.g., 0.156 → "15.6%").
 * @param value - The decimal value.
 * @param decimals - Number of decimal places.
 */
export function formatPercent(value: number, decimals = 1): string {
  return `${(value * 100).toFixed(decimals)}%`;
}

/**
 * Compact number formatting (e.g., 1234567 → "$12.3K").
 * @param cents - Amount in cents.
 */
export function formatCompactCurrency(cents: number): string {
  const dollars = cents / 100;
  if (dollars >= 1_000_000) return `$${(dollars / 1_000_000).toFixed(1)}M`;
  if (dollars >= 1_000) return `$${(dollars / 1_000).toFixed(1)}K`;
  return `$${dollars.toFixed(0)}`;
}
