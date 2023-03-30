import { render, screen, fireEvent, act } from '@testing-library/react';
import {AuthProvider} from '../../context/AuthContext';

describe('AuthProvider component', () => {
    test('should render without errors', async () => {
      await act(async () => {
        render(<AuthProvider />);
      });
  
      expect(screen.getByTestId('auth-provider')).toBeInTheDocument();
    });
  
    test('should update token if authTokens is present and call cache_assets function', async () => {
      const mockFetch = jest.fn();
      global.fetch = mockFetch.mockResolvedValueOnce({
        status: 200,
        json: () => Promise.resolve({ access: 'access_token' }),
      });
  
      const mockSetAuthTokens = jest.fn();
      const mockSetUser = jest.fn();
      const mockNavigate = jest.fn();
  
      await act(async () => {
        render(
          <AuthProvider>
            <button onClick={() => mockSetAuthTokens({ access: 'access_token', refresh: 'refresh_token' })} />
          </AuthProvider>
        );
      });
  
      fireEvent.click(screen.getByRole('button'));
  
      expect(mockFetch).toHaveBeenCalledTimes(1);
      expect(mockFetch).toHaveBeenCalledWith('api/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: 'refresh_token' }),
      });
      expect(mockSetAuthTokens).toHaveBeenCalledWith({ access: 'access_token' });
      expect(mockSetUser).toHaveBeenCalled();
      expect(localStorage.getItem('authTokens')).toEqual(JSON.stringify({ access: 'access_token' }));
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  
    test('should call logoutUser function and clear localStorage when authTokens is not present', async () => {
      const mockLogoutUser = jest.fn();
      const mockClearLocalStorage = jest.spyOn(window.localStorage, 'removeItem');
  
      await act(async () => {
        render(
          <AuthProvider>
            <button onClick={() => mockLogoutUser()} />
          </AuthProvider>
        );
      });
  
      fireEvent.click(screen.getByRole('button'));
  
      expect(mockLogoutUser).toHaveBeenCalled();
      expect(mockClearLocalStorage).toHaveBeenCalledWith('authTokens');
      expect(localStorage.getItem('authTokens')).toBeNull();
    });
});