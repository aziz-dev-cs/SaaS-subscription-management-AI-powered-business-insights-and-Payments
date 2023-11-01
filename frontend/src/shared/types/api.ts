/** Shared API response types used across all features. */

export interface ApiError {
  error: {
    code: number;
    message: string;
    request_id: string | null;
    details?: unknown[];
  };
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}
