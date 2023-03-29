import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../../pages/Home';

describe('Home component', () => {
  it('renders without crashing', () => {
    render(<Home />);
  });

  it('contains the "welcome-box" class', () => {
    render(<Home />);
    const welcomeBox = screen.getByText(/Welcome/i)
    expect(welcomeBox).toBeInTheDocument();
  });

  it("test welcome-box image", () => {
    render(<Home />)
    const welcomeImg = screen.getByRole('img', {name : "welcome-box-image"})
    expect(welcomeImg['src']).toEqual("http://localhost/home-cards.png")
  })

  it('contains the "aggregate-box" class', () => {
    render(<Home />);
    const aggregateBox = screen.getByText(/Our aggregate/i)
    expect(aggregateBox).toBeInTheDocument();
  });

  it("test welcome-box image", () => {
    render(<Home />)
    const aggregateImg = screen.getByRole('img', {name : "aggregate-box-image"})
    expect(aggregateImg['src']).toEqual("http://localhost/home-comp.png")
  })
  
});