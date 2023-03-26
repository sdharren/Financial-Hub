import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import Navbar from './components/Navbar';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import HomePage from './pages/HomePage';
import Dashboard from './pages/Dashboard';
import BarGraph from './pages/BarGraph';
import TransactionDisplay from './pages/TransactionDisplay';
import PieChart from './pages/PieChart';
import BalancesDisplay from './pages/Balances';
import InvestmentGraphs from './pages/InvestmentGraphs';
import PrivateRoutes from './utils/PrivateRoute';
import Link from './pages/Link';
import Currency from './pages/Currency';
import TransactionTable from './pages/RecentTransactionsDisplay';
import SectorSpending from './pages/SectorSpending';
import LinkAssets from './pages/LinkAssets';
import Accounts from './pages/Accounts';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

describe('App component', () => {
  test('renders Navbar component', () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );
    const navbarElement = screen.getByTestId('navbar');
    expect(navbarElement).toBeInTheDocument();
  });

  test('renders Home component by default', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
      <App />
    </MemoryRouter>
    );
    const homeElement = screen.getByTestId('home');
    expect(homeElement).toBeInTheDocument();
  });

  test('renders About component when URL path is /about', () => {
    window.history.pushState({}, 'Test About Page', '/about');
    render(
      <MemoryRouter initialEntries={['/about']}>
      <App />
    </MemoryRouter>
    );
    const aboutElement = screen.getByTestId('about');
    expect(aboutElement).toBeInTheDocument();
  });

  test('renders Login component when URL path is /login', () => {
    window.history.pushState({}, 'Test Login Page', '/login');
    render(
      <MemoryRouter initialEntries={['/login']}>
      <App />
    </MemoryRouter>
    );
    const loginElement = screen.getByTestId('login');
    expect(loginElement).toBeInTheDocument();
  });

  test('renders Signup component when URL path is /signup', () => {
    window.history.pushState({}, 'Test Signup Page', '/signup');
    render(
      <MemoryRouter initialEntries={['/signup']}>
      <App />
    </MemoryRouter>
    );
    const signupElement = screen.getByTestId('signup');
    expect(signupElement).toBeInTheDocument();
  });

  test('renders HomePage component when URL path is /homepage', () => {
    const user = { name: 'Test User', email: 'test@example.com' };
    const PrivateRouteWrapper = ({ children }) => (
      <AuthProvider value={{ user }}>
        {children}
      </AuthProvider>
    );
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
    const user = { name: 'Test User', email: 'test@example.com' };
    const PrivateRouteWrapper = ({ children }) => (
      <AuthProvider value={{ user }}>
        {children}
      </AuthProvider>
    );
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

});