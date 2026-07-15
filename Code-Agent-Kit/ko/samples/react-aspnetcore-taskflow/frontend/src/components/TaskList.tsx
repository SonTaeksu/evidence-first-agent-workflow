import type { TaskItem, WorkItemStatus } from '../types';

interface TaskListProps {
  items: TaskItem[];
  busyTaskId: string | null;
  onStatusChange: (
    task: TaskItem,
    status: WorkItemStatus,
  ) => Promise<void>;
}

const statusLabels: Record<WorkItemStatus, string> = {
  Backlog: 'Backlog',
  InProgress: 'In progress',
  ReadyForApproval: 'Ready for approval',
  Approved: 'Approved',
  Rejected: 'Rejected',
};

function actionsFor(status: WorkItemStatus): Array<{
  label: string;
  next: WorkItemStatus;
  emphasis?: boolean;
}> {
  switch (status) {
    case 'Backlog':
      return [{ label: 'Start', next: 'InProgress', emphasis: true }];
    case 'InProgress':
      return [
        {
          label: 'Submit for approval',
          next: 'ReadyForApproval',
          emphasis: true,
        },
      ];
    case 'ReadyForApproval':
      return [
        { label: 'Approve', next: 'Approved', emphasis: true },
        { label: 'Reject', next: 'Rejected' },
      ];
    case 'Rejected':
      return [{ label: 'Restart', next: 'InProgress', emphasis: true }];
    case 'Approved':
      return [];
  }
}

export function TaskList({
  items,
  busyTaskId,
  onStatusChange,
}: TaskListProps) {
  if (items.length === 0) {
    return (
      <section className="empty-state" aria-live="polite">
        <h2>No tasks yet</h2>
        <p>Create the first task to begin the workflow experiment.</p>
      </section>
    );
  }

  return (
    <section className="task-list" aria-label="Task list">
      {items.map((task) => {
        const actions = actionsFor(task.status);
        const isBusy = task.id === busyTaskId;

        return (
          <article className="task-card" key={task.id}>
            <div className="task-card-header">
              <div>
                <p className="task-assignee">
                  {task.assignee || 'Unassigned'}
                </p>
                <h3>{task.title}</h3>
              </div>
              <span
                className={`status-badge status-${task.status.toLowerCase()}`}
              >
                {statusLabels[task.status]}
              </span>
            </div>

            <p className="task-description">
              {task.description || 'No description provided.'}
            </p>

            <div className="task-footer">
              <span>
                Updated {new Date(task.updatedAt).toLocaleString()}
              </span>

              <div className="task-actions">
                {actions.map((action) => (
                  <button
                    className={
                      action.emphasis
                        ? 'small-button small-button-primary'
                        : 'small-button'
                    }
                    key={action.next}
                    type="button"
                    disabled={isBusy}
                    onClick={() => onStatusChange(task, action.next)}
                  >
                    {isBusy ? 'Updating…' : action.label}
                  </button>
                ))}
              </div>
            </div>
          </article>
        );
      })}
    </section>
  );
}
