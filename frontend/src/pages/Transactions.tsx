import { useState, useEffect } from 'react';
import { transactionService } from '../services/transactions';
import type { Transaction, TransactionCreate, TransactionUpdate, TransactionFilters } from '../services/types';
import TransactionForm from '../components/TransactionForm';
import TransactionList from '../components/TransactionList';
import TransactionFiltersComponent from '../components/TransactionFilters';

const Transactions = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);
  const [filters, setFilters] = useState({
    transaction_type: '',
    start_date: '',
    end_date: '',
    category_id: '',
  });

  // Fetch transactions
  const fetchTransactions = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Build filter object (only include non-empty values)
      const activeFilters: TransactionFilters = {};
      if (filters.transaction_type) {
        activeFilters.transaction_type = filters.transaction_type as 'income' | 'expense';
      }
      if (filters.start_date) {
        activeFilters.start_date = filters.start_date;
      }
      if (filters.end_date) {
        activeFilters.end_date = filters.end_date;
      }
      if (filters.category_id) {
        activeFilters.category_id = parseInt(filters.category_id);
      }
      
      const data = await transactionService.getAll(activeFilters);
      setTransactions(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch transactions');
      console.error('Error fetching transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [filters]);

  // Handle create
  const handleCreate = async (transactionData: TransactionCreate) => {
    try {
      await transactionService.create(transactionData);
      setShowForm(false);
      fetchTransactions();
    } catch (err) {
      throw err; // Let form handle error display
    }
  };

  // Handle update
  const handleUpdate = async (id: number, transactionData: TransactionUpdate) => {
    try {
      await transactionService.update(id, transactionData);
      setEditingTransaction(null);
      setShowForm(false);
      fetchTransactions();
    } catch (err) {
      throw err; // Let form handle error display
    }
  };

  // Handle delete
  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this transaction?')) {
      return;
    }

    try {
      await transactionService.delete(id);
      fetchTransactions();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete transaction');
    }
  };

  // Handle edit
  const handleEdit = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setShowForm(true);
  };

  // Handle form close
  const handleFormClose = () => {
    setShowForm(false);
    setEditingTransaction(null);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Transactions</h1>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition"
        >
          + Add Transaction
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
          <button
            onClick={() => setError(null)}
            className="float-right text-red-700 hover:text-red-900"
          >
            ×
          </button>
        </div>
      )}

      <TransactionFiltersComponent filters={filters} setFilters={setFilters} />

      {showForm && (
        <TransactionForm
          transaction={editingTransaction || undefined}
          onSubmit={editingTransaction ? 
            (data) => handleUpdate(editingTransaction.id, data as TransactionUpdate) : 
            (data) => handleCreate(data as TransactionCreate)
          }
          onCancel={handleFormClose}
        />
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Loading transactions...</p>
        </div>
      ) : (
        <TransactionList
          transactions={transactions}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
};

export default Transactions;

