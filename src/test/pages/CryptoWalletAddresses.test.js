import { render, fireEvent, screen, act } from '@testing-library/react';
import React from 'react';
import CryptoWalletAddresses from '../../pages/CryptoWalletAddresses';
import AuthContext from '../../context/AuthContext';
import { customRenderUser } from '../test-utils';
import { useNavigate, MemoryRouter } from 'react-router-dom';

describe('CryptoWalletAddresses', () => {
  test('should render input field for address', () => {
    customRenderUser(<CryptoWalletAddresses />)
    const inputElement = screen.getByLabelText('Address 1:');
    expect(inputElement).toBeInTheDocument();
  });

  test('should add a new input field for address when add button is clicked', () => {
    customRenderUser(<CryptoWalletAddresses />);
    const addButton = screen.getByText('Add Address');
    fireEvent.click(addButton);
    const inputElement = screen.getByLabelText('Address 2:');
    expect(inputElement).toBeInTheDocument();
  });

  test('should remove an input field for address when remove button is clicked', () => {
    customRenderUser(<CryptoWalletAddresses />);
    const addButton = screen.getByText('Add Address');
    fireEvent.click(addButton);
    const removeButtons = screen.getAllByText('Remove');
    fireEvent.click(removeButtons[1]);
    const inputElement = screen.queryByLabelText('Address 2:');
    expect(inputElement).not.toBeInTheDocument();
  });

  test('should submit addresses to the server', async () => {
    const authTokens = { access: 'access_token'}
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({}),
      })
    );
    await act(async () => {
        render(
          <AuthContext.Provider value={{ authTokens }}>
            <MemoryRouter>
              <CryptoWalletAddresses />
            </MemoryRouter>
          </AuthContext.Provider>
        );
      });
   
    const addButton = screen.getByText('Add Address');
    fireEvent.click(addButton);
    const inputElement2 = screen.getByLabelText('Address 2:');
    fireEvent.change(inputElement2, { target: { value: '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2' } });
    const submitButton = screen.getByText('Submit');
    fireEvent.click(submitButton);
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('api/link_crypto_wallet/?param=1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authTokens.access}`,
      },
    });
  });
});