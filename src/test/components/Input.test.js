import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import Input from '../../components/input';

describe('Input', () => {
  it('renders an input element with the specified label', () => {
    const labelText = 'Email Address';
    const { getByLabelText } = render(
      <Input
        handleChange={() => {}}
        labelText={labelText}
        labelFor="email"
        id="email"
        name="email"
        type="email"
        placeholder="Enter your email address"
      />
    );

    expect(getByLabelText(labelText)).toBeInTheDocument();
  });

  it('calls handleChange with the entered value', () => {
    const handleChange = jest.fn();
    const { getByLabelText } = render(
      <Input
        handleChange={handleChange}
        labelText="Email Address"
        labelFor="email"
        id="email"
        name="email"
        type="email"
        placeholder="Enter your email address"
      />
    );

    const inputElement = getByLabelText('Email Address');
    const enteredValue = 'test@example.com';
    fireEvent.change(inputElement, { target: { value: enteredValue } });
    expect(handleChange).toHaveBeenCalledWith(expect.objectContaining({
      target: expect.objectContaining({ value: enteredValue })
    }));
  });

  it('renders the input element with the specified placeholder', () => {
    const placeholder = 'Enter your email address';
    const { getByPlaceholderText } = render(
      <Input
        handleChange={() => {}}
        labelText="Email Address"
        labelFor="email"
        id="email"
        name="email"
        type="email"
        placeholder={placeholder}
      />
    );

    expect(getByPlaceholderText(placeholder)).toBeInTheDocument();
  });

  it('renders the input element with the specified custom class', () => {
    const customClass = "rounded-md appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm";
    const { getByLabelText } = render(
      <Input
        handleChange={() => {}}
        labelText="Email Address"
        labelFor="email"
        id="email"
        name="email"
        type="email"
        customClass={customClass}
      />
    );

    expect(getByLabelText('Email Address')).toHaveClass(customClass);
  });
});