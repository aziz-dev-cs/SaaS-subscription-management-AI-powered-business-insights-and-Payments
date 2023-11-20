import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { format, parseISO } from 'date-fns';
import type { DailySnapshot } from '../types';

interface ChurnIndicatorProps {
  snapshots: DailySnapshot[];
}

/**
 * Bar chart showing new vs. churned subscribers over time.
 */
export const ChurnIndicator: React.FC<ChurnIndicatorProps> = ({ snapshots }) => {
  const data = snapshots.map((s) => ({
    date: s.snapshot_date,
    new: s.new_subs,
    churned: -s.churned_subs,
  }));

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <h3 className="text-base font-semibold text-gray-900 mb-4">
        Subscriber Growth vs. Churn
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis
            dataKey="date"
            tickFormatter={(d: string) => format(parseISO(d), 'MMM d')}
            tick={{ fontSize: 12, fill: '#6B7280' }}
          />
          <YAxis tick={{ fontSize: 12, fill: '#6B7280' }} />
          <Tooltip
            labelFormatter={(label: string) => format(parseISO(label), 'MMM d, yyyy')}
          />
          <Legend />
          <Bar dataKey="new" name="New" fill="#10B981" radius={[4, 4, 0, 0]} />
          <Bar dataKey="churned" name="Churned" fill="#EF4444" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
