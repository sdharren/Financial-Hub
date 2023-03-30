import React from 'react';
import { render, fireEvent, screen, act } from '@testing-library/react';
import DropDown from '../../pages/DropDown';
import AuthContext from '../../context/AuthContext';
import { useNavigate, MemoryRouter } from 'react-router-dom';
import userEvent from "@testing-library/user-event";

describe('Dropdown', () => {
    beforeEach(() => {
      jest.spyOn(global, 'fetch').mockResolvedValue({
        json: jest.fn().mockResolvedValue([
          { id: 1, name: 'Option 1' },
          { id: 2, name: 'Option 2' },
          { id: 3, name: 'Option 3' },
        ]),
      });
    });
  
    afterEach(() => {
      jest.restoreAllMocks();
    });
  
    it('should display dropdown options', async () => {
        const authTokens = { access: 'access_token'}
      await act(async () => {
        render(<AuthContext.Provider value={{ authTokens }}>
                   <MemoryRouter>
            <DropDown />
                       </MemoryRouter>
                      </AuthContext.Provider>);
      });
  
      const dropdown = screen.getByRole('combobox');
      userEvent.click(dropdown);
  
      const option1 = screen.getByRole('option', { name: 'Option 1' });
      const option2 = screen.getByRole('option', { name: 'Option 2' });
      const option3 = screen.getByRole('option', { name: 'Option 3' });
  
      expect(option1).toBeInTheDocument();
      expect(option2).toBeInTheDocument();
      expect(option3).toBeInTheDocument();
    });
  });
