# Pitfalls — Rust

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Runtime mismatch

A library written for one runtime, used under another, compiles and then panics at first IO with a message about a missing reactor. It is a dependency-selection error, not a code error.

## Feature unification surprises

A workspace build enables the union of features. Behaviour differs between building the member alone and building the workspace, which makes it look intermittent.

## Blocking inside async

A synchronous call in an async task stalls the executor thread. Throughput collapses with no error.

## Error model chosen inconsistently

Mixing a typed error crate with a dynamic one across a boundary loses the type information the caller needed to branch on.

## MSRV is not the installed toolchain

Code that compiles locally can fail on the minimum supported version. The declared MSRV is the contract; the local compiler is not.
