import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format, parseISO } from 'date-fns';
import type { DailySnapshot } from '../types';

interface RevenueChartProps {
  snapshots: DailySnapshot[];
}

/**
 * Area chart showing MRR trend over time.
 */
export const RevenueChart: React.FC<RevenueChartProps> = ({ snapshots }) => {
  const data = snapshots.map((s) => ({
    date: s.snapshot_date,
    mrr: s.mrr_cents / 100,
    revenue: s.revenue_cents / 100,
  }));

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <h3 className="text-base font-semibold text-gray-900 mb-4">Revenue Trend</h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="mrrGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis
            dataKey="date"
            tickFormatter={(d: string) => format(parseISO(d), 'MMM d')}
            tick={{ fontSize: 12, fill: '#6B7280' }}
          />
          <YAxis
            tickFormatter={(v: number) => `$${v >= 1000 ? `${(v / 1000).toFixed(1)}K` : v}`}
            tick={{ fontSize: 12, fill: '#6B7280' }}
          />
          <Tooltip
            formatter={(value: number) => [`$${value.toFixed(2)}`, 'MRR']}
            labelFormatter={(label: string) => format(parseISO(label), 'MMM d, yyyy')}
          />
          <Area
            type="monotone"
            dataKey="mrr"
            stroke="#3B82F6"
            fill="url(#mrrGradient)"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
