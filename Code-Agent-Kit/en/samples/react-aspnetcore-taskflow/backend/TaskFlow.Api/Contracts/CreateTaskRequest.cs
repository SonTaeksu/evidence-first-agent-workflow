namespace TaskFlow.Api.Contracts;

public sealed record CreateTaskRequest(
    string Title,
    string? Description,
    string? Assignee);
