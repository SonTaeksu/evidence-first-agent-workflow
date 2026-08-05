# Pitfalls — Elixir

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Assigns accumulating in socket state

Anything assigned to a LiveView socket is retained per connected user. A large assign is a memory leak that only appears under concurrency, never in development.

## Compile-time versus runtime configuration

Reading an environment variable in `config/config.exs` captures the build machine's value into the release. It works in development and ships the wrong value.

## Ecto preloads and N+1

Accessing an unloaded association raises rather than lazy-loading, which is the safe behaviour — but preloading inside a loop produces one query per row with no error.

## Changeset validation is not a database constraint

A changeset check does not prevent a concurrent insert from violating uniqueness. A matching database constraint is required, and its error has to be handled.

## Unbounded mailboxes

A process that receives faster than it handles grows its mailbox until the node dies. The symptom is memory, not an error.
