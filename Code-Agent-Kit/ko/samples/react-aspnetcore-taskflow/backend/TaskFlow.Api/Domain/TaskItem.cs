namespace TaskFlow.Api.Domain;

public sealed class TaskItem
{
    private TaskItem(
        Guid id,
        string title,
        string description,
        string assignee,
        WorkItemStatus status,
        DateTimeOffset createdAt,
        DateTimeOffset updatedAt)
    {
        Id = id;
        Title = title;
        Description = description;
        Assignee = assignee;
        Status = status;
        CreatedAt = createdAt;
        UpdatedAt = updatedAt;
    }

    public Guid Id { get; }
    public string Title { get; }
    public string Description { get; }
    public string Assignee { get; }
    public WorkItemStatus Status { get; private set; }
    public DateTimeOffset CreatedAt { get; }
    public DateTimeOffset UpdatedAt { get; private set; }

    public static TaskItem Create(string title, string description, string assignee)
    {
        var now = DateTimeOffset.UtcNow;
        return new TaskItem(
            Guid.NewGuid(),
            title,
            description,
            assignee,
            WorkItemStatus.Backlog,
            now,
            now);
    }

    public static TaskItem Restore(
        Guid id,
        string title,
        string description,
        string assignee,
        WorkItemStatus status,
        DateTimeOffset createdAt,
        DateTimeOffset updatedAt) =>
        new(id, title, description, assignee, status, createdAt, updatedAt);

    public void ChangeStatus(WorkItemStatus status)
    {
        Status = status;
        UpdatedAt = DateTimeOffset.UtcNow;
    }
}
