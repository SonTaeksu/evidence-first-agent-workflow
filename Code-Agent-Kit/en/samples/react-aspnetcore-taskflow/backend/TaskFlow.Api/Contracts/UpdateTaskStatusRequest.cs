using TaskFlow.Api.Domain;

namespace TaskFlow.Api.Contracts;

public sealed record UpdateTaskStatusRequest(WorkItemStatus Status);
