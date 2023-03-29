import React from 'react';
import { useState, useEffect } from 'react';
import { act } from 'react-dom/test-utils';
import { render, screen } from '@testing-library/react';
import useApiResult from '../../custom_hooks/useApiResult';

describe('useApiResult', () => {
  const mockRequest = ['https://example.com', { headers: { 'Content-Type': 'application/json' } }];
  const mockData = { name: 'John Doe' };
  const mockError = 'Error occurred';

  beforeEach(() => {
    jest.spyOn(global, 'fetch').mockImplementation((url) => {
      if (url === mockRequest[0]) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        });
      } else {
        return Promise.resolve({
          ok: false,
          statusText: mockError,
        });
      }
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should fetch data successfully and return data', async () => {
    const TestComponent = () => {
      const [data, error] = useApiResult({ request: mockRequest, endpoint: 'user' });
      return (
        <div>
          <span data-testid="data">{JSON.stringify(data)}</span>
          <span data-testid="error">{error}</span>
        </div>
      );
    };

    await act(async () => {
      render(<TestComponent />);
    });

    const dataEl = screen.getByTestId("data");
    const errorEl = screen.getByTestId("error");

    expect(dataEl.textContent).toEqual(JSON.stringify(mockData));
    expect(errorEl.textContent).toEqual('');
  });

  it('should return an error if fetch fails', async () => {
    const TestComponent = () => {
      const [data, error] = useApiResult({ request: ['https://notfound.com'], endpoint: 'user' });
      return (
        <div>
          <span data-testid="data">{JSON.stringify(data)}</span>
          <span data-testid="error">{error}</span>
        </div>
      );
    };

    await act(async () => {
      render(<TestComponent />);
    });

    const dataEl = screen.getByTestId("data");
    const errorEl = screen.getByTestId("error");

    expect(dataEl.textContent).toEqual("null");
    expect(errorEl.textContent).toEqual(mockError);
  });
});