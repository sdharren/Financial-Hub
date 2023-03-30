import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter, Link, Route, MemoryRouter } from 'react-router-dom';
import Navbar from '../components/Navbar';
import App from '../App';
import About from '../pages/About';
import Login from '../pages/Login';
import Signup from '../pages/Signup';
import Home from '../pages/Home';
import Dashboard from '../pages/Dashboard';
import LinkAssets from '../pages/LinkAssets';
import Accounts from '../pages/Accounts';
import { AuthProvider } from '../context/AuthContext';
import {customRenderUser, customRenderNoUser} from "./test-utils";


describe('App component', () => {
    it('renders home without crashing', () => {
      render(<Home />);
    });
  
    it('renders about without crashing', () => {
      render(<About />);
    });
  
    it("renders without crashing", () => {
        customRenderNoUser(
            <Login />
        )
    })
  
    it("renders without crashing", () => {
        customRenderNoUser(
            <Signup />
        )
    })

    const user = { name: 'Test User', email: 'test@example.com' };
      const PrivateRouteWrapper = ({ children }) => (
        <AuthProvider value={{ user }}>
          {children}
        </AuthProvider>
      );
  
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