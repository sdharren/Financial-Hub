import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Header from '../../components/header';

describe('Header', () => {
  test('renders the heading', () => {
    render(<Header heading="Test Heading" />, { wrapper: MemoryRouter });
    const heading = screen.getByText('Test Heading');
    expect(heading).toBeInTheDocument();
  });

  test('renders the paragraph', () => {
    render(<Header paragraph="Test paragraph" />, { wrapper: MemoryRouter });
    const paragraph = screen.getByText('Test paragraph');
    expect(paragraph).toBeInTheDocument();
  });

  test('renders the link with correct text', () => {
    render(<Header linkName="Test link" />, { wrapper: MemoryRouter });
    const link = screen.getByText('Test link');
    expect(link).toBeInTheDocument();
  });

  test('renders the link with correct url', () => {
    render(<Header linkUrl="/test" />, { wrapper: MemoryRouter });
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/test');
  });
});