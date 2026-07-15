# Portable Code Agent Kit Layout

`Code-Agent-Kit/en/` and `Code-Agent-Kit/ko/` are independently copyable distributions with identical relative paths.

Included in each mirror:

- operational root files and hidden agent adapters;
- `docs/core`, `docs/architecture/decisions`, `docs/getting-started`, `docs/agents`, and `docs/human`;
- prompts, templates, stacks, tools, scripts, demos, reference assets, agent configs, sample, and licenses.

Excluded from the portable kit:

- historical design-review and evaluation reports;
- repository release notes, changelog, update manifests, and citation metadata;
- generated validation evidence;
- active `.github/workflows` files.

An inactive CI sample is placed under `templates/ci/github/`.

The mirrors are validated for exact path parity, absence of `.ko.md`, and links that remain inside the selected language root.
