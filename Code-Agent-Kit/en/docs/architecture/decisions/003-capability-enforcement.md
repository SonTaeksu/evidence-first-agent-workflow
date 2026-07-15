# ADR-003: Three-Layer Capability Enforcement

- Status: accepted

## Decision

A capability that changes implementation is recorded in Project Map, repeated in Gate Analysis, and enforced by a stack prohibition rule.

## Rejected

A single passive note in documentation.

## Reason

Small models can overlook one instruction. Three independent checkpoints reduce accidental use of an unavailable shared library, generated client, SDK feature, or runtime path.
