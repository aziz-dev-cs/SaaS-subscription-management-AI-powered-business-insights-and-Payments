import React from 'react';

interface Column<T> {
  /** Column header text. */
  header: string;
  /** Key of the data object or custom render function. */
  accessor: keyof T | ((row: T) => React.ReactNode);
}

interface DataTableProps<T> {
  /** Column definitions. */
  columns: Column<T>[];
  /** Row data. */
  data: T[];
  /** Unique key extractor for each row. */
  keyExtractor: (row: T) => string;
  /** Show when no data is available. */
  emptyMessage?: string;
}

/**
 * Generic data table molecule for displaying tabular data.
 */
export function DataTable<T>({
  columns,
  data,
  keyExtractor,
  emptyMessage = 'No data available',
}: DataTableProps<T>): React.ReactElement {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th
                key={String(col.header)}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-6 py-8 text-center text-sm text-gray-500">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row) => (
              <tr key={keyExtractor(row)} className="hover:bg-gray-50">
                {columns.map((col) => (
                  <td key={String(col.header)} className="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                    {typeof col.accessor === 'function'
                      ? col.accessor(row)
                      : String(row[col.accessor] ?? '')}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
