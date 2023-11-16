/**
 * Custom hook for paginated invoice data.
 */

import { useQuery } from '@tanstack/react-query';
import { queryKeys } from '@/shared/lib/queryKeys';
import { usePagination } from '@/shared/hooks/usePagination';
import * as billingApi from '../api/billingApi';

export function useInvoices() {
  const pagination = usePagination();

  const { data, isLoading } = useQuery({
    queryKey: queryKeys.billing.invoices(pagination.page),
    queryFn: () => billingApi.fetchInvoices(pagination.page, pagination.pageSize),
  });

  return {
    invoices: data?.items ?? [],
    total: data?.total ?? 0,
    totalPages: data?.total_pages ?? 1,
    isLoading,
    ...pagination,
  };
}
