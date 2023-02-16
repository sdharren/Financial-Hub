import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom'; 
import Navbar from './Navbar';

describe('Navbar', () => {
  test('renders the site title', () => {
    render(
      <MemoryRouter> 
        <Navbar />
      </MemoryRouter>
    );
    const siteTitle = screen.getByRole('link', { name: /financial hub/i });
    expect(siteTitle).toBeInTheDocument();
  });

  test('renders the correct number of nav links', () => {
    render(
      <MemoryRouter> 
        <Navbar />
      </MemoryRouter>
    );
    const navLinks = screen.getAllByRole('link');
    expect(navLinks).toHaveLength(4);
  });

  test('renders the about nav link', () => {
    render(
      <MemoryRouter> 
        <Navbar />
      </MemoryRouter>
    );
    const aboutLink = screen.getByRole('link', { name: /about/i });
    expect(aboutLink).toBeInTheDocument();
  });

  test('renders the sign up nav link', () => {
    render(
      <MemoryRouter> 
        <Navbar />
      </MemoryRouter>
    );
    const signUpLink = screen.getByRole('link', { name: /sign up/i });
    expect(signUpLink).toBeInTheDocument();
  });

  test('renders the log in nav link', () => {
    render(
      <MemoryRouter> 
        <Navbar />
      </MemoryRouter>
    );
    const logInLink = screen.getByRole('link', { name: /log in/i });
    expect(logInLink).toBeInTheDocument();
  });
});