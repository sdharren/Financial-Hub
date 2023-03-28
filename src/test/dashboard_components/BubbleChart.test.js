import React from 'react';
import { render } from '@testing-library/react';
import BubbleChart from '../../dashboard_components/BubbleChart';

describe('BubbleChart component', () => {
    test('renders a bubble chart', () => {
      const { getByText } = render(<BubbleChart />);
      const titleElement = getByText('Bubble Chart for Stocks, Bank Accounts, and Crypto');
      expect(titleElement).toBeInTheDocument();
    });
  });