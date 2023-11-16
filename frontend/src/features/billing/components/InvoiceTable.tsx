import React from 'react';
import { Badge } from '@/shared/components/atoms/Badge';
import { Button } from '@/shared/components/atoms/Button';
import { DataTable } from '@/shared/components/molecules/DataTable';
import { formatCurrency, formatDate } from '@/shared/lib/formatters';
import type { Invoice } from '../types';

interface InvoiceTableProps {
  invoices: Invoice[];
  page: number;
  totalPages: number;
  onNextPage: () => void;
  onPrevPage: () => void;
}

const statusVariant: Record<string, 'green' | 'yellow' | 'red' | 'gray'> = {
  paid: 'green',
  open: 'yellow',
  draft: 'gray',
  void: 'gray',
  uncollectible: 'red',
};

/**
 * Invoice history table with pagination.
 */
export const InvoiceTable: React.FC<InvoiceTableProps> = ({
  invoices,
  page,
  totalPages,
  onNextPage,
  onPrevPage,
}) => {
  const columns = [
    {
      header: 'Date',
      accessor: (row: Invoice) => formatDate(row.created_at),
    },
    {
      header: 'Amount',
      accessor: (row: Invoice) => formatCurrency(row.amount_cents, row.currency.toUpperCase()),
    },
    {
      header: 'Status',
      accessor: (row: Invoice) => (
        <Badge label={row.status} variant={statusVariant[row.status] ?? 'gray'} />
      ),
    },
    {
      header: 'Period',
      accessor: (row: Invoice) =>
        row.period_start && row.period_end
          ? `${formatDate(row.period_start)} - ${formatDate(row.period_end)}`
          : '-',
    },
    {
      header: '',
      accessor: (row: Invoice) =>
        row.pdf_url ? (
          <a
            href={row.pdf_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            Download
          </a>
        ) : null,
    },
  ];

  return (
    <div className="space-y-4">
      <DataTable
        columns={columns}
        data={invoices}
        keyExtractor={(row) => row.id}
        emptyMessage="No invoices yet"
      />

      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <Button variant="ghost" onClick={onPrevPage} disabled={page <= 1}>
            Previous
          </Button>
          <span className="text-sm text-gray-500">
            Page {page} of {totalPages}
          </span>
          <Button variant="ghost" onClick={onNextPage} disabled={page >= totalPages}>
            Next
          </Button>
        </div>
      )}
    </div>
  );
};
