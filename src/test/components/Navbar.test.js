import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';
import Navbar from '../../components/Navbar';

describe('Navbar', () => {
  const authTokens = { access: 'fakeToken' };
  const logoutUser = jest.fn();
  const user = {
    name: 'testuser',
    email: 'testuser@test.com',
    id: 1,
  };

  beforeEach(() => {
    jest.spyOn(window, 'fetch');
    window.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ first_name: 'test' }),
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders navbar contents', async () => {
    render(
      <MemoryRouter>
        <AuthContext.Provider value={{ user, authTokens, logoutUser }}>
          <Navbar />
        </AuthContext.Provider>
      </MemoryRouter>
    );

    expect(screen.getByTestId('navbar')).toBeInTheDocument();
    expect(screen.getByText('Financial Hub')).toBeInTheDocument();
    expect(screen.getByText('Bank accounts')).toBeInTheDocument();
    expect(screen.getByText('Currencies')).toBeInTheDocument();
    expect(screen.getByText('Transactions')).toBeInTheDocument();
    expect(screen.getByText('Bar graph')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  test('renders default form when user is not logged in', async () => {
    render(
      <MemoryRouter>
        <AuthContext.Provider value={{ user: null }}>
          <Navbar />
        </AuthContext.Provider>
      </MemoryRouter>
    );

    expect(screen.getByTestId('navbar')).toBeInTheDocument();
    expect(screen.getByText('Financial Hub')).toBeInTheDocument();
    expect(screen.getByText('About')).toBeInTheDocument();
    expect(screen.getByText('Sign Up')).toBeInTheDocument();
    expect(screen.getByText('Login')).toBeInTheDocument();
  });

//   test('displays user first name when logged in', async () => {
//     render(
//       <MemoryRouter>
//         <AuthContext.Provider value={{ user, authTokens, logoutUser }}>
//           <Navbar />
//         </AuthContext.Provider>
//       </MemoryRouter>
//     );

//     expect(screen.getByText('test')).toBeInTheDocument();
//   });

  test('calls logoutUser function when "Logout" is clicked', async () => {
    render(
      <MemoryRouter>
        <AuthContext.Provider value={{ user, authTokens, logoutUser }}>
          <Navbar />
        </AuthContext.Provider>
      </MemoryRouter>
    );

    userEvent.click(screen.getByText('Logout'));
    expect(logoutUser).toHaveBeenCalled();
  });
});