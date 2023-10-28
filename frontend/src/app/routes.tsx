import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from '@/features/auth/components/ProtectedRoute';
import { DashboardLayout } from '@/features/dashboard/components/DashboardLayout';
import { LoginForm } from '@/features/auth/components/LoginForm';
import { RegisterForm } from '@/features/auth/components/RegisterForm';

// Lazy-loaded page components
const DashboardPage = React.lazy(() => import('../pages/DashboardPage'));
const BillingPage = React.lazy(() => import('../pages/BillingPage'));
const AnalyticsPage = React.lazy(() => import('../pages/AnalyticsPage'));
const InsightsPage = React.lazy(() => import('../pages/InsightsPage'));

/**
 * Application route configuration.
 */
export const AppRoutes: React.FC = () => {
  return (
    <React.Suspense
      fallback={
        <div className="h-screen flex items-center justify-center">
          <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
        </div>
      }
    >
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
              <LoginForm />
            </div>
          }
        />
        <Route
          path="/register"
          element={
            <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
              <RegisterForm />
            </div>
          }
        />

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/billing" element={<BillingPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/insights" element={<InsightsPage />} />
            <Route path="/settings" element={<div className="text-gray-500">Settings — Coming soon</div>} />
          </Route>
        </Route>

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </React.Suspense>
  );
};
