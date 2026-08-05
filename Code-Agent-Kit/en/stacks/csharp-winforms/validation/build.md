# Build validation

## Required

The build route depends on the `project-format` capability. Confirm it before running anything.

```bash
# SDK-style, TargetFramework net472
msbuild {PROJECT}.csproj /t:Restore,Build /p:Configuration=Release
# or, with the .NET SDK and the 4.7.2 targeting pack installed
dotnet build {PROJECT}.csproj -c Release

# Legacy .csproj, TargetFrameworkVersion v4.7.2
msbuild {PROJECT}.csproj /t:Build /p:Configuration=Release
```

Restore differs by package management:

| Package management | Restore |
|---|---|
| `PackageReference` | `msbuild /t:Restore` or `dotnet restore` |
| `packages.config` | `nuget restore {SOLUTION}.sln` |

## Evidence

- the exact command and its exit code;
- the error and warning counts from the log tail;
- the target framework the log reports, compared against the project file;
- for a warnings-as-errors project, the confirmation that no warning was suppressed to make the build pass.

## What a passing build does not prove

It does not prove the form contains anything, that it opens, or that it scales. Record the rendered-output layer separately — see [`ui.md`](ui.md).

A build made to pass by suppressing a warning, lowering the target framework, or removing `TreatWarningsAsErrors` is a scope change, not a fix. Report it as such.
