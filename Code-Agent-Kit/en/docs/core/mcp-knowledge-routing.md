# MCP Knowledge Routing

> Which servers exist, which were actually reached, and which were only named:
> [`mcp-source-verification.md`](mcp-source-verification.md). Every endpoint the
> stack profiles route to is listed there with the result of a real `tools/call`,
> and the untested ones are separated out and labelled. A server nobody has
> connected to reads exactly like an invented one, so the distinction is kept in
> writing rather than in memory.

## Source priority

1. Current project code and generated artifacts
2. Deterministic build, test, and runtime evidence
3. Official documentation retrieved through MCP
4. Official repositories and release notes
5. Model internal knowledge

## Microsoft technologies

Use Microsoft Learn MCP for:

- ASP.NET Core
- C#
- .NET
- dependency injection
- configuration and logging
- authentication and authorization
- Entity Framework Core when added later

Endpoint:

```text
https://learn.microsoft.com/api/mcp
```

## React ecosystem

Use Context7. Pin React core requests to:

```text
/facebook/react
```

Resolve the exact Context7 library ID before using documentation for:

- Vite
- Vitest
- React Testing Library
- Playwright
- React Router if introduced later

## Fallback policy

If MCP is unavailable:

1. inspect local project code and lock files;
2. use an official source only;
3. stop and report `knowledge unavailable` for version-sensitive behavior that cannot be verified;
4. do not silently replace an official-source lookup with model memory.
