// import React from 'react';
// import { render, screen, act } from '@testing-library/react';
// import { BrowserRouter } from 'react-router-dom';
// import { MemoryRouter } from 'react-router-dom';
// import Navbar from '../components/Navbar';
// import AuthContext from '../context/AuthContext';

// describe('Navbar', () => {
//   const mockLogout = jest.fn();
//   const mockContextValue = {
//     user: { name: 'test' },
//     logoutUser: mockLogout,
//     authTokens: { access: 'test' },
//   };

//   const mockAuthContext = {
//     user: {
//       id: 1,
//       username: 'testuser',
//       email: 'testuser@test.com',
//     },
//     logoutUser: jest.fn(),
//     authTokens: {
//       access: 'test_access_token',
//       refresh: 'test_refresh_token',
//     },
//   };

//   beforeEach(() => {
//     jest.spyOn(window, 'fetch').mockImplementation(() =>
//       Promise.resolve({
//         json: () => Promise.resolve({ first_name: 'test' }),
//         status: 200,
//       })
//     );
//   });

//   afterEach(() => {
//     window.fetch.mockRestore();
//   });

//   it('renders the default navigation bar when user is not logged in', () => {
//     act(() => {
//         render(
//           <MemoryRouter>
//             <AuthContext.Provider value={{}}>
//               <Navbar />
//             </AuthContext.Provider>
//           </MemoryRouter>
//         );
//     });

//     expect(screen.getByTestId('navbar')).toBeInTheDocument();
//     expect(screen.getByText('About')).toBeInTheDocument();
//     expect(screen.getByText('Sign Up')).toBeInTheDocument();
//     expect(screen.getByText('Login')).toBeInTheDocument();
//     expect(screen.queryByText('Hello, test')).not.toBeInTheDocument();
//     expect(screen.queryByText('Bank accounts')).not.toBeInTheDocument();
//     expect(screen.queryByText('Currencies')).not.toBeInTheDocument();
//     expect(screen.queryByText('Transactions')).not.toBeInTheDocument();
//     expect(screen.queryByText('Bar graph')).not.toBeInTheDocument();
//     expect(screen.queryByText('Logout')).not.toBeInTheDocument();
//   });

//   it('renders the navigation bar with user information when user is logged in', async () => {
//     act(() => {
//     render(
//       <BrowserRouter>
//         <AuthContext.Provider value={mockContextValue}>
//           <Navbar />
//         </AuthContext.Provider>
//       </BrowserRouter>
//     );
//     });


//     expect(screen.getByTestId('navbar')).toBeInTheDocument();
//     expect(screen.queryByText('About')).not.toBeInTheDocument();
//     expect(screen.queryByText('Sign Up')).not.toBeInTheDocument();
//     expect(screen.queryByText('Login')).not.toBeInTheDocument();
//     //expect(screen.getByText('Hello, test')).toBeInTheDocument();
//     expect(screen.getByText('Bank accounts')).toBeInTheDocument();
//     expect(screen.getByText('Currencies')).toBeInTheDocument();
//     expect(screen.getByText('Transactions')).toBeInTheDocument();
//     expect(screen.getByText('Bar graph')).toBeInTheDocument();
//     expect(screen.getByText('Logout')).toBeInTheDocument();
//   });

// //   it('calls logoutUser when "Logout" is clicked', async () => {
// //     act(() => {
// //     const {container} =render(
// //       <BrowserRouter>
// //         <AuthContext.Provider value={mockContextValue}>
// //           <Navbar />
// //         </AuthContext.Provider>
// //       </BrowserRouter>
// //     );
// //     expect(mockLogout).not.toHaveBeenCalled();
// //     expect(container.querySelector('.nav-logout')).toBeInTheDocument();
// //     logoutButton.click();
// //     expect(mockLogout).toHaveBeenCalledTimes(1);
// //   });
// });
