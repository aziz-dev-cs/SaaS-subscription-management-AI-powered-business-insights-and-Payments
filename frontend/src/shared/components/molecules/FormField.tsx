import React from 'react';
import { Input } from '../atoms/Input';

interface FormFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Label text displayed above the input. */
  label: string;
  /** Error message for validation display. */
  error?: string;
}

/**
 * Labeled form field molecule combining a label with an Input atom.
 */
export const FormField = React.forwardRef<HTMLInputElement, FormFieldProps>(
  ({ label, error, id, ...props }, ref) => {
    const fieldId = id || label.toLowerCase().replace(/\s+/g, '-');

    return (
      <div className="space-y-1">
        <label htmlFor={fieldId} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
        <Input ref={ref} id={fieldId} error={error} {...props} />
      </div>
    );
  }
);

FormField.displayName = 'FormField';
