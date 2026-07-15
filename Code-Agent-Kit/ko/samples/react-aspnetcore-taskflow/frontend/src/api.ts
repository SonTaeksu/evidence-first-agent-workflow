import type {
  CreateTaskInput,
  TaskItem,
  WorkItemStatus,
} from './types';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:5098';

async function parseError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as {
      title?: string;
      detail?: string;
      errors?: Record<string, string[]>;
    };

    if (body.errors) {
      return Object.values(body.errors).flat().join(' ');
    }

    return body.detail ?? body.title ?? `Request failed: ${response.status}`;
  } catch {
    return `Request failed: ${response.status}`;
  }
}

async function request<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as T;
}

export const taskApi = {
  list: () => request<TaskItem[]>('/api/tasks'),

  create: (input: CreateTaskInput) =>
    request<TaskItem>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(input),
    }),

  updateStatus: (id: string, status: WorkItemStatus) =>
    request<TaskItem>(`/api/tasks/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    }),
};
