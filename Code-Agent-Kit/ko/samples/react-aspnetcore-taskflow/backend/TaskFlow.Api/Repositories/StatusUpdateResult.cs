using TaskFlow.Api.Domain;

namespace TaskFlow.Api.Repositories;

public enum StatusUpdateKind
{
    Success,
    NotFound,
    InvalidTransition
}

public sealed record StatusUpdateResult(
    StatusUpdateKind Kind,
    TaskItem? Item = null,
    string? Error = null)
{
    public static StatusUpdateResult Success(TaskItem item) =>
        new(StatusUpdateKind.Success, item);

    public static StatusUpdateResult NotFound() =>
        new(StatusUpdateKind.NotFound);

    public static StatusUpdateResult InvalidTransition(
        WorkItemStatus current,
        WorkItemStatus next) =>
        new(
            StatusUpdateKind.InvalidTransition,
            Error: $"Cannot move from {current} to {next}.");
}
