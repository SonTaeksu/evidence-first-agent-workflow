namespace TaskFlow.Api.Contracts;

public static class RequestValidation
{
    public static Dictionary<string, string[]> Validate(CreateTaskRequest request)
    {
        var errors = new Dictionary<string, string[]>(StringComparer.OrdinalIgnoreCase);

        if (string.IsNullOrWhiteSpace(request.Title))
        {
            errors["title"] = ["Title is required."];
        }
        else if (request.Title.Trim().Length > 120)
        {
            errors["title"] = ["Title must be 120 characters or fewer."];
        }

        if ((request.Description?.Length ?? 0) > 2_000)
        {
            errors["description"] = ["Description must be 2,000 characters or fewer."];
        }

        if ((request.Assignee?.Length ?? 0) > 80)
        {
            errors["assignee"] = ["Assignee must be 80 characters or fewer."];
        }

        return errors;
    }
}
