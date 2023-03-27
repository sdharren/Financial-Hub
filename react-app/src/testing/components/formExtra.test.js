import React from 'react';
import { shallow } from 'enzyme';
import FormExtra from '../../components/formExtra';

describe('FormExtra', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallow(<FormExtra />);
  });

  it('renders a checkbox', () => {
    expect(wrapper.find('input[type="checkbox"]').exists()).toBe(true);
  });

  it('renders a label for the checkbox', () => {
    expect(wrapper.find('label[htmlFor="remember-me"]').text()).toBe('Remember me');
  });

  it('renders a forgot password link', () => {
    expect(wrapper.find('a[href="#"]').text()).toBe('Forgot your password?');
  });
});