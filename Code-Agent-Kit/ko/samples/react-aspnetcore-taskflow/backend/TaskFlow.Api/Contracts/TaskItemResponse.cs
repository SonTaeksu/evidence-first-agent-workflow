using TaskFlow.Api.Domain;

namespace TaskFlow.Api.Contracts;

public sealed record TaskItemResponse(
    Guid Id,
    string Title,
    string Description,
    string Assignee,
    WorkItemStatus Status,
    DateTimeOffset CreatedAt,
    DateTimeOffset UpdatedAt)
{
    public static TaskItemResponse From(TaskItem item) => new(
        item.Id,
        item.Title,
        item.Description,
        item.Assignee,
        item.Status,
        item.CreatedAt,
        item.UpdatedAt);
}
