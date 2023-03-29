
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

  it('should remove bank from the list when remove button is clicked', async () => {

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

  // it('should remove brokerage from the list when remove button is clicked', async () => {
  //   global.fetch = jest.fn();
  //   fetch.mockImplementation((urls) => {
  //     if (urls.includes('linked_brokerage')) {
  //       return Promise.resolve({
  //         ok: true,
  //         json: () => Promise.resolve(['Vanguard', 'Fidelity'])
  //       });

  //     } else if (urls.includes('delete_linked_brokerage')) {
  //       return Promise.resolve({ok : true });
  //     }
      
  //   });

  //   customRenderUser(<Accounts />);

  //   await screen.findByText('Vanguard');

  //   const removeBrokerage = screen.getAllByTestId('remove-brokerage');
  //   const getRemoveButton = removeBrokerage[0];
  //   fireEvent.click(getRemoveButton);

  //   await waitFor(() => {
  //     expect(screen.getByText('Vanguard')).toBeInTheDocument();
  //   });
  // })

});
