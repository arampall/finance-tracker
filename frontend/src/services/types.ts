// Transaction types matching backend schemas

export type TransactionType = 'income' | 'expense';

export interface Category {
  id: number;
  name: string;
  description?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: number;
  user_id: number;
  amount: number;
  type: TransactionType;
  transaction_date: string;
  description?: string;
  category_id?: number;
  category?: Category;
  created_at: string;
  updated_at: string;
}

export interface TransactionCreate {
  amount: number;
  type: TransactionType;
  transaction_date?: string;
  description?: string;
  category_id?: number;
}

export interface TransactionUpdate {
  amount?: number;
  type?: TransactionType;
  transaction_date?: string;
  description?: string;
  category_id?: number;
}

export interface TransactionFilters {
  skip?: number;
  limit?: number;
  start_date?: string;
  end_date?: string;
  transaction_type?: TransactionType;
  category_id?: number;
}

