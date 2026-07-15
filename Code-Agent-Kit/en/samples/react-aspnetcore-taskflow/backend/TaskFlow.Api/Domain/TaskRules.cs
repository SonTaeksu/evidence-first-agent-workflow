namespace TaskFlow.Api.Domain;

public static class TaskRules
{
    public static bool CanTransition(WorkItemStatus current, WorkItemStatus next)
    {
        if (current == next)
        {
            return true;
        }

        return current switch
        {
            WorkItemStatus.Backlog => next == WorkItemStatus.InProgress,
            WorkItemStatus.InProgress => next == WorkItemStatus.ReadyForApproval,
            WorkItemStatus.ReadyForApproval =>
                next is WorkItemStatus.Approved or WorkItemStatus.Rejected,
            WorkItemStatus.Rejected => next == WorkItemStatus.InProgress,
            WorkItemStatus.Approved => false,
            _ => false
        };
    }
}
