/**
 * Auth API layer using TanStack Query patterns.
 */

import { apiClient } from '@/shared/lib/apiClient';
import type { TokenResponse } from '@/shared/types/api';
import type { LoginPayload, RegisterPayload, User } from '../types';

/** POST /auth/register */
export async function register(payload: RegisterPayload): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>('/auth/register', payload);
  return data;
}

/** POST /auth/login */
export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>('/auth/login', payload);
  return data;
}

/** POST /auth/refresh */
export async function refreshToken(refreshToken: string): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>('/auth/refresh', {
    refresh_token: refreshToken,
  });
  return data;
}

/** GET /auth/me */
export async function fetchCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>('/auth/me');
  return data;
}
