import api from './api';
import type { Transaction, TransactionCreate, TransactionUpdate, TransactionFilters } from './types';

export const transactionService = {
  // Get all transactions with optional filters
  getAll: async (filters: TransactionFilters = {}): Promise<Transaction[]> => {
    const params = new URLSearchParams();
    
    if (filters.skip !== undefined) params.append('skip', filters.skip.toString());
    if (filters.limit !== undefined) params.append('limit', filters.limit.toString());
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.transaction_type) params.append('transaction_type', filters.transaction_type);
    if (filters.category_id !== undefined) params.append('category_id', filters.category_id.toString());

    const queryString = params.toString();
    const url = queryString ? `/api/transactions?${queryString}` : '/api/transactions';
    const response = await api.get<Transaction[]>(url);
    return response.data;
  },

  // Get single transaction
  getById: async (id: number): Promise<Transaction> => {
    const response = await api.get<Transaction>(`/api/transactions/${id}`);
    return response.data;
  },

  // Create transaction
  create: async (transactionData: TransactionCreate): Promise<Transaction> => {
    const response = await api.post<Transaction>('/api/transactions', transactionData);
    return response.data;
  },

  // Update transaction
  update: async (id: number, transactionData: TransactionUpdate): Promise<Transaction> => {
    const response = await api.put<Transaction>(`/api/transactions/${id}`, transactionData);
    return response.data;
  },

  // Delete transaction
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/transactions/${id}`);
  },
};

