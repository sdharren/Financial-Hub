import React from 'react';
import FormExtra from '../../components/formExtra';
import { render, screen } from '@testing-library/react';

describe('FormExtra', () => {
    test('renders the "Remember me" checkbox and "Forgot your password?" link', () => {
        render(<FormExtra />);
    
       
        const rememberMeCheckbox = screen.getByRole('checkbox', { name: /remember me/i });
        expect(rememberMeCheckbox).toBeInTheDocument();
        

        const forgotPasswordLink = screen.getByRole('link', { name: /forgot your password/i });
        expect(forgotPasswordLink).toBeInTheDocument();
      });
});