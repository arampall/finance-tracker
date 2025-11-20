import type { TransactionType } from '../services/types';

interface TransactionFiltersProps {
  filters: {
    transaction_type: string;
    start_date: string;
    end_date: string;
    category_id: string;
  };
  setFilters: (filters: {
    transaction_type: string;
    start_date: string;
    end_date: string;
    category_id: string;
  }) => void;
}

const TransactionFilters = ({ filters, setFilters }: TransactionFiltersProps) => {
  const handleFilterChange = (name: string, value: string) => {
    setFilters({
      ...filters,
      [name]: value
    });
  };

  const clearFilters = () => {
    setFilters({
      transaction_type: '',
      start_date: '',
      end_date: '',
      category_id: '',
    });
  };

  const hasActiveFilters = filters.transaction_type || filters.start_date || filters.end_date || filters.category_id;

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Type
          </label>
          <select
            value={filters.transaction_type}
            onChange={(e) => handleFilterChange('transaction_type', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Start Date
          </label>
          <input
            type="date"
            value={filters.start_date}
            onChange={(e) => handleFilterChange('start_date', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            End Date
          </label>
          <input
            type="date"
            value={filters.end_date}
            onChange={(e) => handleFilterChange('end_date', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex items-end">
          <button
            onClick={clearFilters}
            disabled={!hasActiveFilters}
            className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransactionFilters;

