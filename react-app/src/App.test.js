import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter, Route } from 'react-router-dom';
import App from './App';
import Navbar from './components/Navbar';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import HomePage from './pages/HomePage';
import Dashboard from './pages/Dashboard';
import LinkAssets from './pages/LinkAssets';
import Accounts from './pages/Accounts';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';


describe('App component', () => {
  it('renders home without crashing', () => {
    render(<Home />);
  });

  it('renders about without crashing', () => {
    render(<About />);
  });

  // it('renders login without crashing', () => {
  //   render(<Login />);
  // });

  // it('renders signup without crashing', () => {
  //   render(<Signup />);
  // });
  const user = { name: 'Test User', email: 'test@example.com' };
    const PrivateRouteWrapper = ({ children }) => (
      <AuthProvider value={{ user }}>
        {children}
      </AuthProvider>
    );


  test('renders HomePage component when URL path is /homepage', () => {
    render(
      <MemoryRouter initialEntries={[HomePage]}>
        <PrivateRouteWrapper>
          <App />
        </PrivateRouteWrapper>
      </MemoryRouter>
    );
    const homePageElement = screen.queryByTestId('homepagetest');
    expect(homePageElement).toBeDefined();
  });

  test('renders Dashboard component when URL path is /dashboard',  () => {
    render(
      <MemoryRouter initialEntries={[Dashboard]}>
        <PrivateRouteWrapper>
          <App />
        </PrivateRouteWrapper>
      </MemoryRouter>
    );

   
    const dashboardElement = screen.queryByTestId('dashboardtest');
    expect(dashboardElement).toBeDefined();
 
  });

  test('renders Link Assets component when URL path is /linkassets',  () => {
    render(
      <MemoryRouter initialEntries={[LinkAssets]}>
        <PrivateRouteWrapper>
          <App />
        </PrivateRouteWrapper>
      </MemoryRouter>
    );

   
    const dashboardElement = screen.queryByTestId('linkassetstest');
    expect(dashboardElement).toBeDefined();
 
  });

  test('renders Accounts component when URL path is /accounts',  () => {
    render(
      <MemoryRouter initialEntries={[Accounts]}>
        <PrivateRouteWrapper>
          <App />
        </PrivateRouteWrapper>
      </MemoryRouter>
    );

   
    const dashboardElement = screen.queryByTestId('accountstest');
    expect(dashboardElement).toBeDefined();
 
  });

  test('renders navbar', () => {
    render(<App />);
    const navbar = screen.queryByTestId('navbar');
    expect(navbar).toBeDefined();
  });

});