namespace TaskFlow.Api.Domain;

public enum WorkItemStatus
{
    Backlog,
    InProgress,
    ReadyForApproval,
    Approved,
    Rejected
}
