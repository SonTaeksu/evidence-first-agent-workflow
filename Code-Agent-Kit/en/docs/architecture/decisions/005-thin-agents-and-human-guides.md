# ADR-005: Thin AGENTS and Human-Guide Separation

- Status: accepted

## Decision

Keep root `AGENTS.md` concise and normative. Put detailed procedures in routed documents. Keep long onboarding guides under `docs/human/` and outside normal agent indexing.

## Rejected

Duplicating all operational details in every agent adapter and loading developer tutorials in routine agent context.

## Reason

Duplicated rules drift. Long guides consume context and can conflict with the actual source of truth.
