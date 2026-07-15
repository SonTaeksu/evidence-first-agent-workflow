import { render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';

const seedTask = {
  id: '11111111-1111-1111-1111-111111111111',
  title: 'Create public workflow sample',
  description: 'Prepare the sample repository.',
  assignee: 'Taeksu',
  status: 'InProgress',
  createdAt: '2026-07-12T00:00:00Z',
  updatedAt: '2026-07-13T00:00:00Z',
};

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify([seedTask]), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('loads and displays tasks', async () => {
    render(<App />);

    expect(
      await screen.findByText('Create public workflow sample'),
    ).toBeInTheDocument();
    expect(screen.getByText('In progress')).toBeInTheDocument();
  });
});
