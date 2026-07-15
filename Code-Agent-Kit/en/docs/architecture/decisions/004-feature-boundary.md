# ADR-004: Stack-Owned Feature Boundaries

- Status: accepted

## Decision

The core requires every stack to define a feature boundary and action model. The core does not impose a screen, service, endpoint, or file as the universal feature unit.

## Rejected

Applying one UI framework's screen model to every stack.

## Reason

Enterprise screen frameworks, React applications, APIs, libraries, and batch systems have different ownership and deployment boundaries.
