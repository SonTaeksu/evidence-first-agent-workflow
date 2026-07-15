using System.Net;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using TaskFlow.Api.Contracts;
using TaskFlow.Api.Domain;

namespace TaskFlow.Api.Tests;

public sealed class TaskApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public TaskApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetTasks_ReturnsSeedItems()
    {
        var response = await _client.GetAsync("/api/tasks");

        response.EnsureSuccessStatusCode();

        var items = await response.Content.ReadFromJsonAsync<TaskItemResponse[]>();
        Assert.NotNull(items);
        Assert.NotEmpty(items);
    }

    [Fact]
    public async Task CreateTask_WithBlankTitle_ReturnsBadRequest()
    {
        var response = await _client.PostAsJsonAsync(
            "/api/tasks",
            new CreateTaskRequest("   ", "Description", "Tester"));

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task CreateTask_ReturnsCreatedTask()
    {
        var response = await _client.PostAsJsonAsync(
            "/api/tasks",
            new CreateTaskRequest(
                "Add priority field",
                "First public workflow experiment.",
                "Tester"));

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var item = await response.Content.ReadFromJsonAsync<TaskItemResponse>();
        Assert.NotNull(item);
        Assert.Equal(WorkItemStatus.Backlog, item.Status);
    }

    [Fact]
    public async Task InvalidStatusTransition_ReturnsBadRequest()
    {
        var response = await _client.PatchAsJsonAsync(
            "/api/tasks/11111111-1111-1111-1111-111111111111/status",
            new UpdateTaskStatusRequest(WorkItemStatus.Approved));

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}
