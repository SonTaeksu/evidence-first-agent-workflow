using TaskFlow.Api.Domain;

namespace TaskFlow.Api.Repositories;

public interface ITaskRepository
{
    Task<IReadOnlyList<TaskItem>> GetAllAsync(CancellationToken cancellationToken);
    Task<TaskItem?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
    Task AddAsync(TaskItem item, CancellationToken cancellationToken);
    Task<StatusUpdateResult> UpdateStatusAsync(
        Guid id,
        WorkItemStatus nextStatus,
        CancellationToken cancellationToken);
}
