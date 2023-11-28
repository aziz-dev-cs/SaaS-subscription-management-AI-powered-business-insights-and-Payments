import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/shared/components/atoms/Button';
import { FormField } from '@/shared/components/molecules/FormField';
import { useAuth } from '../hooks/useAuth';

/**
 * Registration form with tenant creation.
 */
export const RegisterForm: React.FC = () => {
  const { register, registerPending, registerError } = useAuth();
  const [form, setForm] = useState({
    email: '',
    password: '',
    full_name: '',
    tenant_name: '',
  });

  const update = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    register(form);
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Create your account</h1>
        <p className="mt-2 text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-blue-600 hover:text-blue-700 font-medium">
            Sign in
          </Link>
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <FormField
          label="Full name"
          value={form.full_name}
          onChange={update('full_name')}
          placeholder="Jane Doe"
          required
        />

        <FormField
          label="Company name"
          value={form.tenant_name}
          onChange={update('tenant_name')}
          placeholder="Acme Corp"
          required
        />

        <FormField
          label="Email address"
          type="email"
          value={form.email}
          onChange={update('email')}
          placeholder="jane@acme.com"
          required
        />

        <FormField
          label="Password"
          type="password"
          value={form.password}
          onChange={update('password')}
          placeholder="Min 8 chars, 1 uppercase, 1 digit"
          required
          minLength={8}
        />

        {registerError && (
          <p className="text-sm text-red-600">Registration failed. Please check your details.</p>
        )}

        <Button type="submit" isLoading={registerPending} className="w-full">
          Create account
        </Button>
      </form>
    </div>
  );
};
