import React from 'react';
import { Providers } from './providers';
import { AppRoutes } from './routes';

/**
 * Root application component.
 */
export const App: React.FC = () => {
  return (
    <Providers>
      <AppRoutes />
    </Providers>
  );
};
