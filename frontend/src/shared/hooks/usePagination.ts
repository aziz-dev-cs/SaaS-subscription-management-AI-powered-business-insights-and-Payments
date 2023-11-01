import { useState, useCallback } from 'react';

interface UsePaginationReturn {
  page: number;
  pageSize: number;
  setPage: (page: number) => void;
  setPageSize: (size: number) => void;
  nextPage: () => void;
  prevPage: () => void;
  canNextPage: (totalPages: number) => boolean;
  canPrevPage: () => boolean;
}

/**
 * Hook for managing pagination state.
 * @param initialPage - Starting page number.
 * @param initialPageSize - Items per page.
 */
export function usePagination(
  initialPage = 1,
  initialPageSize = 20
): UsePaginationReturn {
  const [page, setPage] = useState(initialPage);
  const [pageSize, setPageSize] = useState(initialPageSize);

  const nextPage = useCallback(() => setPage((p) => p + 1), []);
  const prevPage = useCallback(() => setPage((p) => Math.max(1, p - 1)), []);
  const canNextPage = useCallback((totalPages: number) => page < totalPages, [page]);
  const canPrevPage = useCallback(() => page > 1, [page]);

  return { page, pageSize, setPage, setPageSize, nextPage, prevPage, canNextPage, canPrevPage };
}
