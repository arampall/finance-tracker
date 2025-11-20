import { useState, useEffect } from 'react';
import type { Transaction, TransactionCreate, TransactionUpdate } from '../services/types';

interface TransactionFormProps {
  transaction?: Transaction;
  onSubmit: (data: TransactionCreate | TransactionUpdate) => Promise<void>;
  onCancel: () => void;
}

const TransactionForm = ({ transaction, onSubmit, onCancel }: TransactionFormProps) => {
  const [formData, setFormData] = useState({
    amount: '',
    type: 'expense' as 'income' | 'expense',
    description: '',
    category_id: '',
    transaction_date: new Date().toISOString().split('T')[0],
  });
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (transaction) {
      setFormData({
        amount: transaction.amount.toString(),
        type: transaction.type,
        description: transaction.description || '',
        category_id: transaction.category_id?.toString() || '',
        transaction_date: transaction.transaction_date 
          ? new Date(transaction.transaction_date).toISOString().split('T')[0]
          : new Date().toISOString().split('T')[0],
      });
    }
  }, [transaction]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      // Prepare data
      const submitData: TransactionCreate | TransactionUpdate = {
        amount: parseFloat(formData.amount),
        type: formData.type,
        description: formData.description || undefined,
        category_id: formData.category_id ? parseInt(formData.category_id) : undefined,
        transaction_date: formData.transaction_date 
          ? new Date(formData.transaction_date).toISOString()
          : undefined,
      };

      await onSubmit(submitData);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to save transaction');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            {transaction ? 'Edit Transaction' : 'Add Transaction'}
          </h2>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">
                Type *
              </label>
              <select
                name="type"
                value={formData.type}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="income">Income</option>
                <option value="expense">Expense</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">
                Amount *
              </label>
              <input
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                step="0.01"
                min="0.01"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0.00"
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">
                Date *
              </label>
              <input
                type="date"
                name="transaction_date"
                value={formData.transaction_date}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">
                Category ID (optional)
              </label>
              <input
                type="number"
                name="category_id"
                value={formData.category_id}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Category ID"
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Transaction description"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={submitting}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? 'Saving...' : (transaction ? 'Update' : 'Create')}
              </button>
              <button
                type="button"
                onClick={onCancel}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-lg transition"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TransactionForm;

