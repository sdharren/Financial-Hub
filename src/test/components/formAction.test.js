import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import FormAction from '../../components/formAction';

describe('FormAction', () => {
  test('renders a button with text and onSubmit function', () => {
    const handleSubmit = jest.fn();
    const { getByText } = render(
      <FormAction handleSubmit={handleSubmit} text="Submit" />
    );
    const submitButton = getByText(/submit/i);
    expect(submitButton).toBeInTheDocument();
   
  });

  test('renders a button with type and action props', () => {
    const handleSubmit = jest.fn();
    const { getByRole } = render(
      <FormAction handleSubmit={handleSubmit} type="Button" action="submit" text="Submit" />
    );
    const submitButton = getByRole('button');
    expect(submitButton).toHaveAttribute('type', 'submit');
  });

  test('renders an empty div when type prop is not "Button"', () => {
    const { container } = render(<FormAction type="div" />);
    expect(container.firstChild).toMatchInlineSnapshot(`
    <div>
      <div />
    </div>
  `);
  });
});