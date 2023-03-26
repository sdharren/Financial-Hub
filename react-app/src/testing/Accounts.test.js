import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Accounts from '../pages/Accounts';
import AuthContext from '../context/AuthContext';

const mockAuthContextValue = {
  authTokens: {
    access: 'mock-access-token'
  },
  logoutUser: jest.fn()
};

jest.mock('../context/AuthContext', () => ({
  __esModule: true,
  default: jest.fn(() => mockAuthContextValue)
}));

describe('Accounts', () => {
    test('renders Accounts component', async () => {
        const authTokens = { access: 'test_access_token' }; // Set the authentication context value
        const { getByText } = render(
          <AuthContext.Provider value={{ authTokens }}>
            <Accounts />
          </AuthContext.Provider>
        );
      
        const header = getByText(/Accounts/i);
        expect(header).toBeInTheDocument();
  });

//   test('can remove bank', async () => {
//     // Mock fetch request
//     global.fetch = jest.fn().mockResolvedValue({
//       ok: true,
//       json: jest.fn()
//     });

//     render(<Accounts />);

//     // Wait for accounts data to load
//     await waitFor(() => screen.getByText('Accounts'));

//     // Click remove button for first bank in list
//     const removeButton = screen.getAllByText('Remove')[0];
//     removeButton.click();

//     // Check that bank is removed from list
//     await waitFor(() => expect(screen.queryByText('Bank A')).not.toBeInTheDocument());
//   });

//   test('can remove brokerage', async () => {
//     // Mock fetch request
//     global.fetch = jest.fn().mockResolvedValue({
//       ok: true,
//       json: jest.fn()
//     });

//     render(<Accounts />);

//     // Wait for accounts data to load
//     await waitFor(() => screen.getByText('Accounts'));

//     // Click remove button for first brokerage in list
//     const removeButton = screen.getAllByText('Remove')[1];
//     removeButton.click();

//     // Check that brokerage is removed from list
//     await waitFor(() => expect(screen.queryByText('Brokerage A')).not.toBeInTheDocument());
//   });
});
