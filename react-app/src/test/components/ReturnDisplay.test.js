import React from 'react';
import { render } from '@testing-library/react';
import ReturnDisplay from '../../components/ReturnDisplay';

describe('ReturnDisplay component', () => {
  test('should render nothing when there are no returns', () => {
    const { container } = render(<ReturnDisplay returns={{}} />);
    expect(container.firstChild).toBeNull();
  });

  test('should render returns for 30d, 5d, and 1d when they exist', () => {
    const returns = { '30': 1.23, '5': -0.45, '1': 0.67 };
    const { getByText } = render(<ReturnDisplay returns={returns} />);
    expect(getByText('30d: 1.23%')).toBeInTheDocument();
    expect(getByText('5d: -0.45%')).toBeInTheDocument();
    expect(getByText('1d: 0.67%')).toBeInTheDocument();
  });

  test('should render positive returns in green and negative returns in red', () => {
    const returns = { '30': 1.23, '5': -0.45, '1': 0.67 };
    const { getByText } = render(<ReturnDisplay returns={returns} />);
    expect(getByText('30d: 1.23%')).toHaveClass('investment-return-positive');
    expect(getByText('5d: -0.45%')).toHaveClass('investment-return-negative');
    expect(getByText('1d: 0.67%')).toHaveClass('investment-return-positive');
  });

  test('should not render returns for 30d and 5d when they do not exist', () => {
    const returns = { '1': 0.67 };
    const { queryByText } = render(<ReturnDisplay returns={returns} />);
    expect(queryByText('30d:')).toBeNull();
    expect(queryByText('5d:')).toBeNull();
  });

  test('should not render returns for 5d and 1d when they do not exist', () => {
    const returns = { '30': 1.23 };
    const { queryByText } = render(<ReturnDisplay returns={returns} />);
    expect(queryByText('5d:')).toBeNull();
    expect(queryByText('1d:')).toBeNull();
  });

});