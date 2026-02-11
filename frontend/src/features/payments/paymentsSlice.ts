import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export interface Transaction {
  id: number;
  user: number;
  transaction_type: 'deposit' | 'payout' | 'payment';
  amount: number;
  status: 'pending' | 'completed' | 'failed';
  description: string;
  task?: number;
  created_at: string;
  processed_at?: string;
}

interface PaymentsState {
  transactions: Transaction[];
  balance: number;
  loading: boolean;
  error: string | null;
}

const initialState: PaymentsState = {
  transactions: [],
  balance: 0,
  loading: false,
  error: null,
};

export const fetchTransactions = createAsyncThunk(
  'payments/fetchTransactions',
  async () => {
    const response = await axios.get('/api/transactions/');
    return response.data;
  }
);

export const createDeposit = createAsyncThunk(
  'payments/createDeposit',
  async (amount: number) => {
    const response = await axios.post('/api/transactions/', {
      transaction_type: 'deposit',
      amount,
    });
    return response.data;
  }
);

export const requestPayout = createAsyncThunk(
  'payments/requestPayout',
  async (amount: number) => {
    const response = await axios.post('/api/transactions/', {
      transaction_type: 'payout',
      amount,
    });
    return response.data;
  }
);

const paymentsSlice = createSlice({
  name: 'payments',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTransactions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchTransactions.fulfilled, (state, action) => {
        state.loading = false;
        state.transactions = action.payload;
      })
      .addCase(fetchTransactions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Ошибка загрузки';
      });
  },
});

export default paymentsSlice.reducer;
