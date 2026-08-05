# Pitfalls — Go

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Loop variable capture before 1.22

A goroutine closing over the loop variable sees the final value under a `go` directive below 1.22, and a per-iteration copy from 1.22 on. The same source has two behaviours; the directive decides which.

## Nil interface versus nil pointer

Returning a nil `*T` as an `error` makes `err != nil` true. The check looks correct and always passes.

## Slice aliasing on append

`append` may reuse the backing array, so two slices can share storage and mutate each other. No error, just a value changing from somewhere else.

## Context cancellation not propagated

A call that ignores the context keeps running after the caller gave up. The symptom is load, not failure.

## Error wrapping

`fmt.Errorf` without `%w` breaks `errors.Is` and `errors.As`. The chain silently ends there.
