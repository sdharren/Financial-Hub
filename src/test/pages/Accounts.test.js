
import React from 'react';
import { render, screen,fireEvent, waitFor, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Accounts from '../../pages/Accounts';
import { act } from "react-dom/test-utils";

import {customRenderUser} from "../test-utils";


describe('Accounts component', () => {


    test('renders the component', () => {
    customRenderUser(
        <Accounts />
    );
    expect(screen.getByTestId('accountstest')).toBeInTheDocument();
  });


  test('renders the table', () => {
    customRenderUser(
        <Accounts />
    );
    expect(screen.getByRole('table')).toBeInTheDocument();
  });

  test('renders bank accounts', async () => {
    const banks = ['Bank A', 'Bank B', 'Bank C'];
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      json: async () => banks,
    });
    customRenderUser(<Accounts />);
    expect(await screen.findAllByRole('cell', { name: /^Bank/ })).toHaveLength(3);
  });

  test('renders brokerage accounts', async () => {
    const brokerage = ['Brokerage 1', 'Brokerage 2'];
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      json: async () => brokerage,
    });
    customRenderUser(<Accounts />);
    expect(await screen.findAllByRole('cell', { name: /^Brokerage/ })).toHaveLength(2);
  });

  test('renders crypto accounts', async () => {
    const cryptos = ['Crypto A', 'Crypto B'];
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      json: async () => cryptos,
    });
    customRenderUser(<Accounts />);
    expect(await screen.findAllByRole('cell', { name: /^Crypto/ })).toHaveLength(2);
  });


  test('should remove bank from the list when remove button is clicked', async () => {

    global.fetch = jest.fn();
    fetch.mockImplementation((url) => {
      if (url.includes('get_linked_banks')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(['Chase Bank', 'Bank of America'])
        });
      } else if (url.includes('delete_linked_banks')) {
        return Promise.resolve({ ok: true });
      }
    });
  
    customRenderUser(<Accounts />);
  
  
    await screen.findByText('Chase Bank');
  
  
    const removeButtons = screen.getAllByTestId('remove-bank');
    const firstRemoveButton = removeButtons[0];
    fireEvent.click(firstRemoveButton);
  
   
    await waitFor(() => {
      expect(screen.queryByText('Chase Bank')).not.toBeInTheDocument();
    });
  });

  test('should remove brokerage from the list when remove button is clicked', async () => {
    global.fetch = jest.fn();
    fetch.mockImplementation((url) => {
  
      if (url.includes('get_linked_banks')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(['Bank A', 'Bank B'])
        });
      } else if (url.includes('delete_linked_brokerage')) {
        return Promise.resolve({ ok: true });
      } else if (url.includes('linked_brokerage')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(['Brokerage A', 'Brokerage B'])
        });
      }
    });
  
    customRenderUser(<Accounts />);
  
    await screen.findByText('Brokerage A');
  
    const removeButtons = screen.getAllByTestId('remove-brokerage');
    const firstRemoveButton = removeButtons[0];
    fireEvent.click(firstRemoveButton);
  
    await waitFor(() => {
      expect(screen.queryByText('Brokerage A')).not.toBeInTheDocument();
    });
  });

  test('should remove crypto from the list when remove button is clicked', async () => {
    global.fetch = jest.fn();
    fetch.mockImplementation((url) => {
  
      if (url.includes('get_linked_banks')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(['Bank A', 'Bank B'])
        });
      } else if (url.includes('linked_brokerage') ) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(['Brokerage A', 'Brokerage B'])
        });
      } 
      else if (url.includes('delete_linked_crypto')) {
        return Promise.resolve({ ok: true });
      } else if (url.includes('linked_crypto')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(['Crypto A', 'Crypto B'])
        });
      }
    });
  
    customRenderUser(<Accounts />);
  
    await screen.findByText(/Crypto A/i);
  
    const removeButtons = screen.getAllByTestId('remove-crypto');
    const firstRemoveButton = removeButtons[0];
    fireEvent.click(firstRemoveButton);
  
    await waitFor(() => {
      expect(screen.queryByText('Crypto A')).not.toBeInTheDocument();
    });
  });


});