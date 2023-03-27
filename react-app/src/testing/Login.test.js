import React from 'react';
import { fireEvent } from '@testing-library/react';
import { render } from '@testing-library/react';
import AuthContext from '../context/AuthContext';
import Login from '../pages/Login';

describe('Login component', () => {
  it('should update input values when typing', () => {
    const loginUser = jest.fn();
    const user = { name: 'Test User', email: 'test@example.com' };
    const PrivateRouteWrapper = ({ children }) => (
      <AuthContext value={{ user }}>
        {children}
      </AuthContext>
    );
    render(
      <PrivateRouteWrapper>
        <Login />
      </PrivateRouteWrapper>
    );

    const emailInput = getByLabelText('Email');
    const passwordInput = getByLabelText('Password');

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });

    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('testpassword');
  });
});