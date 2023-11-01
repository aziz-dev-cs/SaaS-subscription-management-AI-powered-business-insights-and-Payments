import React from 'react';
import clsx from 'clsx';

interface StatCardProps {
  /** The metric title. */
  title: string;
  /** The formatted metric value. */
  value: string;
  /** Optional change indicator (e.g., "+12.5%"). */
  change?: string;
  /** Whether the change is positive. */
  changePositive?: boolean;
  /** Optional icon component. */
  icon?: React.ReactNode;
}

/**
 * Dashboard stat card molecule for displaying KPIs.
 */
export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  change,
  changePositive,
  icon,
}) => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-gray-500">{title}</p>
        {icon && <div className="text-gray-400">{icon}</div>}
      </div>
      <p className="mt-2 text-3xl font-bold text-gray-900">{value}</p>
      {change && (
        <p
          className={clsx(
            'mt-1 text-sm font-medium',
            changePositive ? 'text-green-600' : 'text-red-600'
          )}
        >
          {changePositive ? '+' : ''}{change}
        </p>
      )}
    </div>
  );
};
