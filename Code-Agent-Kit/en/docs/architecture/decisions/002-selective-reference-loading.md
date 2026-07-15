# ADR-002: Selective Reference Loading

- Status: accepted

## Decision

Load references through Project Map and stack SKILL routing. Do not preload the entire knowledge pack.

## Rejected

Always loading all framework documentation.

## Reason

Large context increases cost and lost-in-the-middle risk. Knowledge packs should contain inference-resistant facts and route only task-relevant references.
