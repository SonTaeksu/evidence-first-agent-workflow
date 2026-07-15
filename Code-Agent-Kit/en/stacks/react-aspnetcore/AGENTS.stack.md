# React and ASP.NET Core Agent Rules

This file extends root `AGENTS.md`.

- Run stack-readiness validation before adopting this profile in another project.
- Reuse the detected frontend API module; do not create a second client.
- Preserve Minimal API unless Project Map records a different confirmed backend style.
- Keep frontend and backend contracts synchronized.
- Do not introduce database, authentication, generated clients, state libraries, or design systems while their capability is unknown.
- Verify version-sensitive .NET behavior through Microsoft Learn and React behavior through official-source routing.
- Run artifact, rendered-output, runtime, and color/accessibility gates separately.
