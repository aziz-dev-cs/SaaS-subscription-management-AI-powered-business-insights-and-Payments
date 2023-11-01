import React from 'react';
import { NavLink } from 'react-router-dom';
import clsx from 'clsx';
import { BarChart3, CreditCard, Home, Lightbulb, Settings, Users } from 'lucide-react';

interface NavItem {
  label: string;
  to: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', to: '/dashboard', icon: <Home size={20} /> },
  { label: 'Billing', to: '/billing', icon: <CreditCard size={20} /> },
  { label: 'Analytics', to: '/analytics', icon: <BarChart3 size={20} /> },
  { label: 'Insights', to: '/insights', icon: <Lightbulb size={20} /> },
  { label: 'Settings', to: '/settings', icon: <Settings size={20} /> },
];

/**
 * Application sidebar navigation organism.
 */
export const Sidebar: React.FC = () => {
  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-gray-900 text-white flex flex-col">
      {/* Brand */}
      <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-800">
        <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center text-sm font-bold">
          S
        </div>
        <span className="text-lg font-semibold">SaaS Dashboard</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              )
            }
          >
            {item.icon}
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-6 py-4 border-t border-gray-800">
        <p className="text-xs text-gray-500">v1.0.0</p>
      </div>
    </aside>
  );
};
