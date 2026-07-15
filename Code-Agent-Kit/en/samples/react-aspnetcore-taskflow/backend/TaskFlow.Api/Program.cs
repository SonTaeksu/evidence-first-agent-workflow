using System.Text.Json.Serialization;
using TaskFlow.Api.Contracts;
using TaskFlow.Api.Domain;
using TaskFlow.Api.Repositories;

var builder = WebApplication.CreateBuilder(args);

builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter());
});

builder.Services.AddSingleton<ITaskRepository, InMemoryTaskRepository>();

var frontendOrigins = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
{
    "http://localhost:5173",
    "http://127.0.0.1:5173"
};

var configuredFrontendOrigin = builder.Configuration["FrontendOrigin"];
if (!string.IsNullOrWhiteSpace(configuredFrontendOrigin))
{
    frontendOrigins.Add(configuredFrontendOrigin);
}

builder.Services.AddCors(options =>
{
    options.AddPolicy("frontend", policy =>
    {
        policy
            .WithOrigins(frontendOrigins.ToArray())
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseCors("frontend");

app.MapGet("/health", () => Results.Ok(new
{
    status = "ok",
    service = "taskflow-api",
    utc = DateTimeOffset.UtcNow
}));

var tasks = app.MapGroup("/api/tasks");

tasks.MapGet("/", async (ITaskRepository repository, CancellationToken cancellationToken) =>
{
    var items = await repository.GetAllAsync(cancellationToken);
    return Results.Ok(items.Select(TaskItemResponse.From));
});

tasks.MapGet("/{id:guid}", async Task<IResult> (
    Guid id,
    ITaskRepository repository,
    CancellationToken cancellationToken) =>
{
    var item = await repository.GetByIdAsync(id, cancellationToken);
    return item is null
        ? Results.NotFound()
        : Results.Ok(TaskItemResponse.From(item));
});

tasks.MapPost("/", async Task<IResult> (
    CreateTaskRequest request,
    ITaskRepository repository,
    CancellationToken cancellationToken) =>
{
    var errors = RequestValidation.Validate(request);
    if (errors.Count > 0)
    {
        return Results.ValidationProblem(errors);
    }

    var item = TaskItem.Create(
        request.Title.Trim(),
        request.Description?.Trim() ?? string.Empty,
        request.Assignee?.Trim() ?? string.Empty);

    await repository.AddAsync(item, cancellationToken);

    return Results.Created($"/api/tasks/{item.Id}", TaskItemResponse.From(item));
});

tasks.MapPatch("/{id:guid}/status", async Task<IResult> (
    Guid id,
    UpdateTaskStatusRequest request,
    ITaskRepository repository,
    CancellationToken cancellationToken) =>
{
    var result = await repository.UpdateStatusAsync(id, request.Status, cancellationToken);

    return result.Kind switch
    {
        StatusUpdateKind.NotFound => Results.NotFound(),
        StatusUpdateKind.InvalidTransition => Results.BadRequest(new ProblemDetailsResponse(
            "Invalid status transition",
            result.Error ?? "The requested transition is not allowed.")),
        StatusUpdateKind.Success when result.Item is not null =>
            Results.Ok(TaskItemResponse.From(result.Item)),
        _ => Results.Problem("Unexpected status update result.")
    };
});

app.Run();

public partial class Program { }
