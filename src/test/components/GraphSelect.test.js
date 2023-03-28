import React from 'react';
import GraphSelect from '../../components/GraphSelect';
import { render, fireEvent, queryByText, getByText } from '@testing-library/react';

describe('GraphSelect', () => {
  const options = ['Option 1', 'Option 2', 'Option 3'];
  const selectedOption = 'Option 1';
  const handleSelectionUpdate = jest.fn();

  it('renders a select element with options', () => {
    const { getByRole, getByText } = render(
      <GraphSelect
        options={options}
        selectedOption={selectedOption}
        handleSelectionUpdate={handleSelectionUpdate}
      />
    );
    const selectElement = getByRole('combobox');
    expect(selectElement).toBeInTheDocument();
    expect(selectElement.children.length).toEqual(options.length);
    options.forEach(option => {
      expect(selectElement).toContainElement(getByText(option, { container: selectElement }));
    });
  });

  it('calls handleSelectionUpdate with the selected value', () => {
    const { getByRole } = render(
      <GraphSelect
        options={options}
        selectedOption={selectedOption}
        handleSelectionUpdate={handleSelectionUpdate}
      />
    );
    const selectElement = getByRole('combobox');
    fireEvent.change(selectElement, { target: { value: 'Option 3' } });
    expect(handleSelectionUpdate).toHaveBeenCalledWith('Option 3');
  });
});