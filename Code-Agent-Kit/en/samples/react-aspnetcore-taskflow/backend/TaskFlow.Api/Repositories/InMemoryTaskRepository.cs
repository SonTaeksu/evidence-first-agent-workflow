using System.Collections.Concurrent;
using TaskFlow.Api.Domain;

namespace TaskFlow.Api.Repositories;

public sealed class InMemoryTaskRepository : ITaskRepository
{
    private readonly ConcurrentDictionary<Guid, TaskItem> _items = new();

    public InMemoryTaskRepository()
    {
        var now = DateTimeOffset.UtcNow;

        var seedItems = new[]
        {
            TaskItem.Restore(
                Guid.Parse("11111111-1111-1111-1111-111111111111"),
                "Create public workflow sample",
                "Prepare the first stack-neutral sample repository.",
                "Taeksu",
                WorkItemStatus.InProgress,
                now.AddDays(-1),
                now),
            TaskItem.Restore(
                Guid.Parse("22222222-2222-2222-2222-222222222222"),
                "Review deterministic gates",
                "Verify build, API, and UI validation evidence.",
                "Reviewer",
                WorkItemStatus.ReadyForApproval,
                now.AddHours(-8),
                now.AddHours(-2))
        };

        foreach (var item in seedItems)
        {
            _items[item.Id] = item;
        }
    }

    public Task<IReadOnlyList<TaskItem>> GetAllAsync(CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();

        IReadOnlyList<TaskItem> result = _items.Values
            .OrderByDescending(item => item.UpdatedAt)
            .ToArray();

        return Task.FromResult(result);
    }

    public Task<TaskItem?> GetByIdAsync(Guid id, CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();
        _items.TryGetValue(id, out var item);
        return Task.FromResult(item);
    }

    public Task AddAsync(TaskItem item, CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();

        if (!_items.TryAdd(item.Id, item))
        {
            throw new InvalidOperationException($"Task {item.Id} already exists.");
        }

        return Task.CompletedTask;
    }

    public Task<StatusUpdateResult> UpdateStatusAsync(
        Guid id,
        WorkItemStatus nextStatus,
        CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();

        if (!_items.TryGetValue(id, out var item))
        {
            return Task.FromResult(StatusUpdateResult.NotFound());
        }

        lock (item)
        {
            if (!TaskRules.CanTransition(item.Status, nextStatus))
            {
                return Task.FromResult(
                    StatusUpdateResult.InvalidTransition(item.Status, nextStatus));
            }

            item.ChangeStatus(nextStatus);
            return Task.FromResult(StatusUpdateResult.Success(item));
        }
    }
}
