import { useEffect, useState } from 'react';

/**
 * Debounce a value by the specified delay.
 * @param value - The value to debounce.
 * @param delay - Debounce delay in milliseconds.
 */
export function useDebounce<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
