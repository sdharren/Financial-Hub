import React from 'react';
import { render } from '@testing-library/react';
import Home from '../../pages/Home';

describe('Home component', () => {
  it('renders without crashing', () => {
    render(<Home />);
  });

  it('contains the "home_page" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home_page')).toBeInTheDocument();
  });

  it('contains the "home_boxes" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home_boxes')).toBeInTheDocument();
  });

  it('contains the "home_text_holder" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home_text_holder')).toBeInTheDocument();
  });

  it('contains the "home__content__holder" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__content__holder')).toBeInTheDocument();
  });

  it('contains the "home__box" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__box')).toBeInTheDocument();
  });

  it('contains the "home__background_image" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__background__image')).toBeInTheDocument();
  });

  it('contains the "home__content" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__content')).toBeInTheDocument();
  });

  it('contains the "home-text" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home-text')).toBeInTheDocument();
  });

  it('contains the "home__first__image" class', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__first__image')).toBeInTheDocument();
  });

  it('has the correct source for the "home__background__image" element', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__background__image').src).toEqual('http://localhost/home-background.png');
  });

  it('has the correct source for the "home__first__image" elements', () => {
    const { container } = render(<Home />);
    expect(container.querySelectorAll('.home__first__image')[0].src).toEqual('http://localhost/home-cards.png');
    expect(container.querySelectorAll('.home__first__image')[1].src).toEqual('http://localhost/home-comp.png');
  });

  it('has the correct alt text for the "home__background__image" element', () => {
    const { container } = render(<Home />);
    expect(container.querySelector('.home__background__image').alt).toEqual('#');
  });

  it('has the correct alt text for the "home__first__image" elements', () => {
    const { container } = render(<Home />);
    expect(container.querySelectorAll('.home__first__image')[0].alt).toEqual('#');
    expect(container.querySelectorAll('.home__first__image')[1].alt).toEqual('#');
  });
});