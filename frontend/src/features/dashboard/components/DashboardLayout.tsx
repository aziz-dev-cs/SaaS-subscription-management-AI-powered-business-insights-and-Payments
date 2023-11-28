import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '@/shared/components/organisms/Sidebar';
import { TopNav } from '@/shared/components/organisms/TopNav';

/**
 * Main dashboard layout with sidebar and top navigation.
 */
export const DashboardLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="ml-64">
        <TopNav />
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
