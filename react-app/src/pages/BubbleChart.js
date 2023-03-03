import React from 'react';
import { BubbleChart } from 'react-bubble-chart';

const data = [
  { label: 'AAPL', value: 10, color: '#FFC107' },
  { label: 'GOOGL', value: 20, color: '#FF9800' },
  { label: 'BRK.A', value: 15, color: '#FF5722' },
  { label: 'ETH', value: 8, color: '#F44336' },
  { label: 'BTC', value: 18, color: '#F44336' },
  { label: 'USD', value: 80, color: '#F44336' },
  { label: 'GBP', value: 120, color: '#F44336' },
  { label: 'YEN', value: 20, color: '#F44336' },
];

const BubbleChartExample = () => {
  return (
    <BubbleChart
      graph={{
        zoom: 1,
        offsetX: -0.05,
        offsetY: -0.01,
      }}
      width={500}
      height={500}
      showLegend={false}
      valueFont={{
        family: 'Arial',
        size: 12,
        color: '#fff',
        weight: 'bold',
      }}
      labelFont={{
        family: 'Arial',
        size: 16,
        color: '#fff',
        weight: 'bold',
      }}
      data={data}
    />
  );
};

export default BubbleChartExample;
