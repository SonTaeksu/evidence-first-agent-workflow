# Pitfalls — ASMX Web Service 2.0 (.NET Framework 4+)

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## XmlSerializer silently drops members

A member without a public setter, or a type without a parameterless constructor, is omitted from the wire format without any error. The field arrives as its default and looks like valid data.

## Interfaces and generics do not serialize

An `interface`-typed or open-generic member cannot be expressed in the schema. This surfaces as a runtime serialization exception on first call, not at build.

## Nullable value types

Without the `Specified` pattern, `0` and 'not supplied' are the same message. Any logic that branches on absence is wrong.

## Proxy regeneration

A regenerated proxy overwrites edits, exactly as with WCF. Adapt in a wrapper.

## Legacy status is a constraint, not a value judgement

New APIs and framework features are not added to ASMX. Do not carry a pattern over from newer stacks and assume it is supported; look it up.
