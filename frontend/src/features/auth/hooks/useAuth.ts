/**
 * Custom hook for authentication state and actions.
 *
 * Uses TanStack Query for user fetching and provides login/logout
 * mutations that manage localStorage tokens.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { queryKeys } from '@/shared/lib/queryKeys';
import * as authApi from '../api/authApi';
import type { LoginPayload, RegisterPayload, User } from '../types';

export function useAuth() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { data: user, isLoading } = useQuery<User>({
    queryKey: queryKeys.auth.me,
    queryFn: authApi.fetchCurrentUser,
    retry: false,
    enabled: !!localStorage.getItem('access_token'),
  });

  const loginMutation = useMutation({
    mutationFn: (payload: LoginPayload) => authApi.login(payload),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      queryClient.invalidateQueries({ queryKey: queryKeys.auth.me });
      navigate('/dashboard');
    },
  });

  const registerMutation = useMutation({
    mutationFn: (payload: RegisterPayload) => authApi.register(payload),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      queryClient.invalidateQueries({ queryKey: queryKeys.auth.me });
      navigate('/dashboard');
    },
  });

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    queryClient.clear();
    navigate('/login');
  };

  return {
    user: user ?? null,
    isAuthenticated: !!user,
    isLoading,
    login: loginMutation.mutate,
    loginError: loginMutation.error,
    loginPending: loginMutation.isPending,
    register: registerMutation.mutate,
    registerError: registerMutation.error,
    registerPending: registerMutation.isPending,
    logout,
  };
}
