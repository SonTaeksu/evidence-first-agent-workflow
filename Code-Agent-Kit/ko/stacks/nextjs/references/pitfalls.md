# Pitfalls — Next.js

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## The client boundary is transitive

`'use client'` applies to the module and everything it imports. One directive can pull a large subtree into the client bundle, and the only symptom is bundle size.

## Non-serializable props

Passing a callback from a server component to a client component fails at render with a message about serialization, not about the callback.

## Caching defaults are version-specific

Whether `fetch` is cached by default, and how a route is judged static or dynamic, has changed between major versions. An answer from the wrong version's documentation is silently wrong in production only.

## Environment variables in client code

An unprefixed variable read in the browser is `undefined`. Code that treats it as a falsy configuration value takes a wrong branch silently.

## Middleware runtime

Node APIs are not all available in middleware. The failure appears at deploy or at request time, not at build.
