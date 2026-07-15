# ADR-001: State Document Granularity

- Status: accepted

## Decision

Use one current, one append-only history, and at most one active worklog per feature. Actions such as create, update, delete, import, and export remain inside the feature state unless the stack defines them as separate deployable boundaries.

## Rejected

One current file per CRUD verb.

## Reason

Verb-level files create synchronization overhead, ambiguous completion, and duplicated state. A feature current document gives the next agent one verified starting map.
