export type WorkItemStatus =
  | 'Backlog'
  | 'InProgress'
  | 'ReadyForApproval'
  | 'Approved'
  | 'Rejected';

export interface TaskItem {
  id: string;
  title: string;
  description: string;
  assignee: string;
  status: WorkItemStatus;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTaskInput {
  title: string;
  description: string;
  assignee: string;
}
