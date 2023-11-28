import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/shared/components/atoms/Button';
import { FormField } from '@/shared/components/molecules/FormField';
import { useAuth } from '../hooks/useAuth';

/**
 * Login form component with email/password fields.
 */
export const LoginForm: React.FC = () => {
  const { login, loginPending, loginError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login({ email, password });
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Sign in to your account</h1>
        <p className="mt-2 text-sm text-gray-600">
          Or{' '}
          <Link to="/register" className="text-blue-600 hover:text-blue-700 font-medium">
            create a new account
          </Link>
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <FormField
          label="Email address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.com"
          required
        />

        <FormField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
        />

        {loginError && (
          <p className="text-sm text-red-600">Invalid email or password. Please try again.</p>
        )}

        <Button type="submit" isLoading={loginPending} className="w-full">
          Sign in
        </Button>
      </form>
    </div>
  );
};
