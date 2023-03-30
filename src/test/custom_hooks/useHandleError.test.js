
import { render, screen, waitFor, act } from '@testing-library/react';
import { useNavigate, MemoryRouter } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';
import useHandleError from '../../custom_hooks/useHandleError';

const TestComponent = ({ error }) => {
    useHandleError(error);
    return null;
  };
  
  

describe('useHandleError', () => {


  beforeEach(() => {
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should do nothing for null error', () => {
    const authTokens = { access: 'access_token' };
    const logoutUser = jest.fn();
    const value = {
      authTokens,
      logoutUser,
    };

    const { container } = render(
      <AuthContext.Provider value={value}>
        <MemoryRouter>
          <TestComponent error={null} />
        </MemoryRouter>
      </AuthContext.Provider>
    );

    expect(container.firstChild).toBeNull();
  });
  

  it('should call alert function when error is Internal Server Error', () => {
    const authTokens = { access: 'access_token' };
    const navigate = jest.fn();
    const logoutUser = jest.fn();
    const mockAlert = jest.spyOn(window, 'alert').mockImplementation(() => {});
    jest.spyOn(global, 'fetch').mockResolvedValue({
      status: 500,
      json: () => ({ error: 'Internal Server Error' })
    });
    const value = {
      authTokens,
      logoutUser,
    };
    render(
      <AuthContext.Provider value={{authTokens, navigate}}>
        <MemoryRouter>
          <TestComponent error="Internal Server Error" />
        </MemoryRouter>
      </AuthContext.Provider>
    );
    expect(mockAlert).toHaveBeenCalledWith('Something went wrong. Please try again later.');
  });


  it('should call console.log function when error is not Internal Server Error', () => {

    const authTokens = { access: 'access_token' };
    const navigate = jest.fn();
    const logoutUser = jest.fn();
    const mockConsole = jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(global, 'fetch').mockResolvedValue({
      status: 500,
      json: () => ({ error: 'Error not null' })
    });
    const value = {
      authTokens,
      logoutUser,
    };
    render(
      <AuthContext.Provider value={{authTokens, navigate}}>
        <MemoryRouter>
          <TestComponent error="Error not null" />
        </MemoryRouter>
      </AuthContext.Provider>
    );
    expect(mockConsole).toHaveBeenCalledWith("Error not null");
  });


  it('should call redirectToLink if error is Investments not linked', async () => {
    const error = { error: 'Investments not linked.' };
    const authTokens = { access: 'access_token' };
    const ATestComponent = () => {
      useHandleError(error);
      return <div>Test</div>;
    };
  
    const fetchSpy = jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      status: 200,
      json: () => ({ link_token: 'test-link-token' }),
    });
  
    await act(async () => {
      render(
        <AuthContext.Provider value={{ authTokens }}>
          <MemoryRouter>
            <ATestComponent />
          </MemoryRouter>
        </AuthContext.Provider>
      );
    });
  
    expect(fetchSpy).toHaveBeenCalledWith('api/link_token/?product=investments', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authTokens.access}`,
      },
    });

  });

});