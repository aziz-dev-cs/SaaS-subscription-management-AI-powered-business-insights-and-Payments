import React from 'react';
import clsx from 'clsx';
import { AlertTriangle, ArrowUpRight, TrendingDown, Zap } from 'lucide-react';
import { Badge } from '@/shared/components/atoms/Badge';
import type { Insight } from '../types';

interface SuggestionCardProps {
  insight: Insight;
}

const categoryIcons: Record<string, React.ReactNode> = {
  revenue: <ArrowUpRight size={18} />,
  churn: <TrendingDown size={18} />,
  growth: <Zap size={18} />,
  optimization: <Zap size={18} />,
  alert: <AlertTriangle size={18} />,
};

const priorityVariant: Record<string, 'green' | 'yellow' | 'red' | 'gray'> = {
  low: 'gray',
  medium: 'yellow',
  high: 'red',
  critical: 'red',
};

/**
 * Card displaying a single AI-generated insight.
 */
export const SuggestionCard: React.FC<SuggestionCardProps> = ({ insight }) => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2 text-gray-500">
          {categoryIcons[insight.category]}
          <span className="text-xs font-medium uppercase tracking-wide">
            {insight.category}
          </span>
        </div>
        <Badge label={insight.priority} variant={priorityVariant[insight.priority]} />
      </div>

      <h4 className="text-sm font-semibold text-gray-900">{insight.title}</h4>
      <p className="mt-1 text-sm text-gray-600 leading-relaxed">{insight.description}</p>

      <div className="mt-3 p-3 bg-gray-50 rounded-lg">
        <p className="text-xs font-medium text-gray-500 mb-1">Suggested Action</p>
        <p className="text-sm text-gray-800">{insight.suggested_action}</p>
      </div>

      <div className="mt-3 flex items-center justify-between">
        <div className="flex items-center gap-1">
          <div
            className="h-1.5 rounded-full bg-blue-500"
            style={{ width: `${insight.confidence_score * 60}px` }}
          />
          <span className="text-xs text-gray-400">
            {(insight.confidence_score * 100).toFixed(0)}% confidence
          </span>
        </div>
      </div>
    </div>
  );
};
