import React from 'react';
import { Bell, LogOut } from 'lucide-react';
import { useAuth } from '@/features/auth/hooks/useAuth';

/**
 * Top navigation bar organism with user info and logout.
 */
export const TopNav: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">
          Welcome back{user ? `, ${user.full_name}` : ''}
        </h2>
      </div>

      <div className="flex items-center gap-4">
        <button
          className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Notifications"
        >
          <Bell size={20} />
        </button>

        <div className="h-8 w-px bg-gray-200" />

        <button
          onClick={logout}
          className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </header>
  );
};
