import React from 'react';
import { render, screen } from '@testing-library/react';
import About from '../../pages/About';

describe('About', () => {
  it('renders the "About Us" heading', () => {
    render(<About />);
    const heading = screen.getByText('About Us');
    expect(heading).toBeInTheDocument();
  });

  it('renders the "Monitoring Finances" text', () => {
    render(<About />);
    const text = screen.getByText('Your go-to app for monitoring finances');
    expect(text).toBeInTheDocument();
  });

  it('renders the "Link Any of Your Assets" text', () => {
    render(<About />);
    const text = screen.getByText('Just link any of your assets and let us do the magic ✨');
    expect(text).toBeInTheDocument();
  });

  it('renders the "Stocks" heading', () => {
    render(<About />);
    const heading = screen.getByText('Stocks');
    expect(heading).toBeInTheDocument();
  });

  it('renders the "Stocks" image', () => {
    render(<About />);
    const image = screen.getByAltText('Stocks');
    expect(image).toBeInTheDocument();
  });

  it('renders the "Banks" heading', () => {
    render(<About />);
    const heading = screen.getByText('Banks');
    expect(heading).toBeInTheDocument();
  });

  it('renders the "Banks" image', () => {
    render(<About />);
    const image = screen.getByAltText('Banks');
    expect(image).toBeInTheDocument();
  });

  it('renders the "Crypto" heading', () => {
    render(<About />);
    const heading = screen.getByText('Crypto');
    expect(heading).toBeInTheDocument();
  });

  it('renders the "Crypto" image', () => {
    render(<About />);
    const image = screen.getByAltText('Crypto');
    expect(image).toBeInTheDocument();
  });
});