import { useCallback, useEffect, useState } from 'react';
import { taskApi } from './api';
import { TaskForm } from './components/TaskForm';
import { TaskList } from './components/TaskList';
import type {
  CreateTaskInput,
  TaskItem,
  WorkItemStatus,
} from './types';
import './styles.css';

export default function App() {
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyTaskId, setBusyTaskId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      setTasks(await taskApi.list());
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : 'Unable to load tasks.',
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadTasks();
  }, [loadTasks]);

  async function handleCreate(input: CreateTaskInput) {
    setError(null);

    try {
      const created = await taskApi.create(input);
      setTasks((current) => [created, ...current]);
    } catch (caught) {
      const message =
        caught instanceof Error
          ? caught.message
          : 'Unable to create the task.';
      setError(message);
      throw caught;
    }
  }

  async function handleStatusChange(
    task: TaskItem,
    status: WorkItemStatus,
  ) {
    setBusyTaskId(task.id);
    setError(null);

    try {
      const updated = await taskApi.updateStatus(task.id, status);
      setTasks((current) =>
        current.map((item) =>
          item.id === updated.id ? updated : item,
        ),
      );
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : 'Unable to update task status.',
      );
    } finally {
      setBusyTaskId(null);
    }
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Evidence-First sample</p>
          <h1>TaskFlow</h1>
          <p className="hero-copy">
            A deliberately small application for testing agent
            handoff, deterministic validation, and Git-synchronized
            project state.
          </p>
        </div>

        <button
          className="secondary-button"
          type="button"
          onClick={() => void loadTasks()}
          disabled={loading}
        >
          {loading ? 'Refreshing…' : 'Refresh'}
        </button>
      </header>

      {error && (
        <div className="error-banner" role="alert">
          <strong>Action failed.</strong>
          <span>{error}</span>
        </div>
      )}

      <section className="content-grid">
        <TaskForm disabled={loading} onCreate={handleCreate} />

        <div className="task-column">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Current state</p>
              <h2>Tasks</h2>
            </div>
            <span>{tasks.length} items</span>
          </div>

          {loading ? (
            <div className="loading-state" aria-live="polite">
              Loading tasks…
            </div>
          ) : (
            <TaskList
              items={tasks}
              busyTaskId={busyTaskId}
              onStatusChange={handleStatusChange}
            />
          )}
        </div>
      </section>
    </main>
  );
}
