# Output Validator Adapter Contract

The core provides generic screen and build-log checks. A stack pack may add validators for framework-specific generated files, bindings, logs, or runtime artifacts.

A stack validator must:

- accept explicit input paths;
- emit machine-readable evidence when practical;
- return `0` for PASS, `2` for validation failure, and `1` for tool error;
- distinguish compile, rendered-output, and runtime failure;
- avoid modifying the artifact being validated;
- include a self-test with one passing and one intentionally failing fixture.

Examples:

- generator log error scan;
- required XML or project node validation;
- data binding existence;
- empty grid or card detection;
- generated-client freshness;
- DTO/data-model synchronization.
