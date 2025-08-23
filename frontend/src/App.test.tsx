import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders basketball video analysis header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Basketball Video Analysis/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders video upload section', () => {
  render(<App />);
  const uploadSection = screen.getByText(/Video Upload/i);
  expect(uploadSection).toBeInTheDocument();
});
