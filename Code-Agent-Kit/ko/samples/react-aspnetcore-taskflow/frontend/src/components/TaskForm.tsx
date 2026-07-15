import { useState, type FormEvent } from 'react';
import type { CreateTaskInput } from '../types';

interface TaskFormProps {
  disabled?: boolean;
  onCreate: (input: CreateTaskInput) => Promise<void>;
}

const initialState: CreateTaskInput = {
  title: '',
  description: '',
  assignee: '',
};

export function TaskForm({
  disabled = false,
  onCreate,
}: TaskFormProps) {
  const [input, setInput] = useState(initialState);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!input.title.trim()) {
      return;
    }

    setSubmitting(true);
    try {
      await onCreate(input);
      setInput(initialState);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-heading">
        <div>
          <p className="eyebrow">New work item</p>
          <h2>Create a task</h2>
        </div>
        <span className="form-hint">Title is required</span>
      </div>

      <label>
        Title
        <input
          name="title"
          maxLength={120}
          value={input.title}
          onChange={(event) =>
            setInput((current) => ({
              ...current,
              title: event.target.value,
            }))
          }
          placeholder="Add deterministic API contract check"
          disabled={disabled || submitting}
          required
        />
      </label>

      <label>
        Description
        <textarea
          name="description"
          maxLength={2000}
          value={input.description}
          onChange={(event) =>
            setInput((current) => ({
              ...current,
              description: event.target.value,
            }))
          }
          placeholder="Describe the expected result and validation evidence."
          disabled={disabled || submitting}
          rows={4}
        />
      </label>

      <label>
        Assignee
        <input
          name="assignee"
          maxLength={80}
          value={input.assignee}
          onChange={(event) =>
            setInput((current) => ({
              ...current,
              assignee: event.target.value,
            }))
          }
          placeholder="Developer or reviewer"
          disabled={disabled || submitting}
        />
      </label>

      <button
        className="primary-button"
        type="submit"
        disabled={disabled || submitting || !input.title.trim()}
      >
        {submitting ? 'Creating…' : 'Create task'}
      </button>
    </form>
  );
}
