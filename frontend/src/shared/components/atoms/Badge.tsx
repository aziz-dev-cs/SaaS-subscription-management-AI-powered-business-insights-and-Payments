import React from 'react';
import clsx from 'clsx';

interface BadgeProps {
  /** The text content of the badge. */
  label: string;
  /** Color variant. */
  variant?: 'green' | 'yellow' | 'red' | 'blue' | 'gray';
}

const variantStyles = {
  green: 'bg-green-100 text-green-800',
  yellow: 'bg-yellow-100 text-yellow-800',
  red: 'bg-red-100 text-red-800',
  blue: 'bg-blue-100 text-blue-800',
  gray: 'bg-gray-100 text-gray-800',
};

/**
 * Status badge atom for displaying labels with color coding.
 */
export const Badge: React.FC<BadgeProps> = ({ label, variant = 'gray' }) => {
  return (
    <span
      className={clsx(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
        variantStyles[variant]
      )}
    >
      {label}
    </span>
  );
};
