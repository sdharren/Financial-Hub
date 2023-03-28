
// import React from 'react';
// import { render, screen } from '@testing-library/react';
// import userEvent from '@testing-library/user-event';
// import Accounts from '../pages/Accounts';
// import App from '../App';
// import AuthProvider from '../context/AuthContext';
// import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"
// import { MemoryRouter } from 'react-router-dom';

// describe('Accounts component', () => {
//   const user = { name: 'Test User', email: 'test@example.com' };
//   const PrivateRouteWrapper = ({ children }) => (
//     <AuthProvider value={{ user }}>
//       {() => children}
//     </AuthProvider>
//   );
//   test('renders the component', () => {
//     render(
//     <MemoryRouter>
//       <AuthProvider value = {{user}}>
//         <Accounts />
//       </AuthProvider>
//     </MemoryRouter>);
//     expect(screen.getByTestId('accountstest')).toBeInTheDocument();
//   });

//   test('renders the heading', () => {
//     render(
//       <MemoryRouter>
//         <PrivateRouteWrapper>
//           <Accounts />
//         </PrivateRouteWrapper>
//       </MemoryRouter>);
//     expect(screen.getByText('Accounts')).toBeInTheDocument();
//   });

//   test('renders the table', () => {
//     render(
//       <MemoryRouter>
//         <PrivateRouteWrapper>
//           <Accounts />
//         </PrivateRouteWrapper>
//       </MemoryRouter>);
//     expect(screen.getByRole('table')).toBeInTheDocument();
//   });

//   test('renders bank accounts', () => {
//     const banks = ['Bank A', 'Bank B', 'Bank C'];
//     jest.spyOn(global, 'fetch').mockResolvedValueOnce({
//       json: async () => banks,
//     });
//     render(
//       <MemoryRouter>
//         <PrivateRouteWrapper>
//           <Accounts />
//         </PrivateRouteWrapper>
//       </MemoryRouter>);
//     expect(screen.getAllByText(/Bank/)).toHaveLength(3);
//   });

//   test('renders brokerage accounts', () => {
//     const brokerages = ['Brokerage A', 'Brokerage B'];
//     jest.spyOn(global, 'fetch').mockResolvedValueOnce({
//       json: async () => [],
//     }).mockResolvedValueOnce({
//       json: async () => brokerages,
//     });
//     render(
//       <MemoryRouter>
//         <PrivateRouteWrapper>
//           <Accounts />
//         </PrivateRouteWrapper>
//       </MemoryRouter>);
//     expect(screen.getAllByText(/Brokerage/)).toHaveLength(2);
//   });

//   test('clicking remove button calls handleRemoveBank function', () => {
//     const banks = ['Bank A', 'Bank B', 'Bank C'];
//     const mockRemoveBank = jest.fn();
//     jest.spyOn(global, 'fetch').mockResolvedValueOnce({
//       json: async () => banks,
//     });
//     render(
//       <MemoryRouter>
//         <PrivateRouteWrapper>
//           <Accounts handleRemoveBrokerage={mockRemoveBank} />
//         </PrivateRouteWrapper>
//       </MemoryRouter>);
//     userEvent.click(screen.getByText('Remove', { exact: false }));
//     expect(mockRemoveBank).toHaveBeenCalledTimes(1);
//   });

//   test('clicking remove button calls handleRemoveBrokerage function', () => {
//     const brokerages = ['Brokerage A', 'Brokerage B'];
//     const mockRemoveBrokerage = jest.fn();
//     jest.spyOn(global, 'fetch').mockResolvedValueOnce({
//       json: async () => [],
//     }).mockResolvedValueOnce({
//       json: async () => brokerages,
//     });

//     render(
//       <MemoryRouter>
//         <PrivateRouteWrapper>
//           <Accounts handleRemoveBrokerage={mockRemoveBrokerage} />
//         </PrivateRouteWrapper>
//       </MemoryRouter>);
//     userEvent.click(screen.getByText('Remove', { exact: false }));
//     expect(mockRemoveBrokerage).toHaveBeenCalledTimes(1);
//   });
// });
