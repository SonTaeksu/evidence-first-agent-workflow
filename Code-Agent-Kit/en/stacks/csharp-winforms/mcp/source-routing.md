# Source Routing

## Official sources

- Windows Forms, C#, .NET Framework, MSBuild, and configuration schema: Microsoft Learn.
- .NET Framework release notes for version-sensitive behaviour changes.
- The installed SDK, targeting pack, and reference assemblies on the build machine.

## MCP servers

- Microsoft Learn MCP for anything under `System.Windows.Forms`, `System.Drawing`, `System.Configuration`, MSBuild properties, and framework version behaviour.
- Do not route Windows Forms questions to a general package-documentation server. Windows Forms is not a package.

## Priority

1. Current project code, project file, and generated designer files.
2. Deterministic build, test, and designer-tree evidence.
3. Microsoft Learn through MCP.
4. Official release notes and the .NET repositories.
5. Model memory.

## Version-sensitive lookups

Always look up rather than recall:

- which framework version introduced an API or a configuration key;
- the exact spelling of a configuration key or a manifest identifier;
- whether a property belongs to the .NET SDK or the .NET Desktop SDK;
- default values that changed between framework versions.

## Fallback

When the target framework in the project disagrees with the version a source describes, **stop and report the mismatch**. Do not implement against the version the documentation happened to show. Record the unresolved item as `⟨verification required: what and how⟩`.
