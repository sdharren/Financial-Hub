// import React from 'react';
// import { render, screen } from '@testing-library/react';
// import RecentTransactions from '../pages/RecentTransactionsDisplay';
// import AuthContext from '../context/AuthContext';

// describe('RecentTransactions', () => {
//   const mockTransactions = [
//     {
//       date: new Date('2023-03-01'),
//       merchant: 'Merchant A',
//       category: ['Category 1', 'Category 2'],
//       amount: 100.00,
//     },
//     {
//       date: new Date('2023-03-05'),
//       merchant: 'Merchant B',
//       category: ['Category 2'],
//       amount: 50.00,
//     },
//   ];

//   const mockAuthContext = {
//     authTokens: { access: 'mock-access-token' },
//     logoutUser: jest.fn(),
//   };

//   beforeEach(() => {
//     jest.spyOn(window, 'fetch');
//     window.fetch.mockResolvedValue({
//       json: () => Promise.resolve({ 'Royal Bank of Scotland - Current Accounts': mockTransactions }),
//       status: 200,
//     });
//   });

//   afterEach(() => {
//     window.fetch.mockRestore();
//   });

//   it('should fetch and render recent transactions', async () => {
//     render(<RecentTransactions />, { wrapper: ({ children }) => <AuthContext.Provider value={mockAuthContext}>{children}</AuthContext.Provider> });
//     expect(window.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/api/recent_transactions/?param=Royal Bank of Scotland - Current Accounts', {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         'Authorization': 'Bearer mock-access-token',
//       },
//     });

//     const tableRows = await screen.findAllByRole('row');
//     expect(tableRows).toHaveLength(mockTransactions.length + 1); // +1 for table header
//     expect(screen.getByText(mockTransactions[0].merchant)).toBeInTheDocument();
//     expect(screen.getByText(mockTransactions[1].merchant)).toBeInTheDocument();
//   });

//   it('should log an error if the fetch request fails', async () => {
//     const mockedConsoleError = jest.fn();
//     window.fetch.mockResolvedValueOnce({
//       json: () => Promise.resolve(),
//       status: 500,
//       statusText: 'Internal Server Error',
//     });
  
//     render(
//       <RecentTransactions />,
//       {
//         wrapper: ({ children }) => (
//           <AuthContext.Provider value={mockAuthContext}>
//             {children}
//           </AuthContext.Provider>
//         ),
//         console: {
//           error: mockedConsoleError,
//         },
//       }
//     );
//     expect(window.fetch).toHaveBeenCalledWith(
//       'http://127.0.0.1:8000/api/recent_transactions/?param=Royal Bank of Scotland - Current Accounts',
//       {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': 'Bearer mock-access-token',
//         },
//       }
//     );
  
//     expect(mockedConsoleError).toHaveBeenCalledWith(
//       'Failed to fetch recent transactions: 500 Internal Server Error'
//     );
//   });
// });