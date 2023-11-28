import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Spinner } from '@/shared/components/atoms/Spinner';
import { useAuth } from '../hooks/useAuth';

/**
 * Route guard that redirects unauthenticated users to login.
 */
export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
