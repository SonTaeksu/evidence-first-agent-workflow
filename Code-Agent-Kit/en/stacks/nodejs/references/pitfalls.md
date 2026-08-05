# Pitfalls — Node.js

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Module system mismatch

A dependency that is ESM-only cannot be `require`d, and the error names the file rather than the cause. Establish the module system before anything else.

## Interop defaults

`import x from 'cjs-package'` gives the `module.exports` object, which may not have the named export expected. Named imports from CommonJS are resolved statically and can fail at load.

## `exports` masks real files

A path that exists on disk still fails to import once `exports` is declared and does not list it.

## Async errors escaping a handler

An `async` callback passed where a synchronous one is expected rejects into nothing; the request hangs or the process exits depending on version.

## Version drift between install and runtime

`engines` is advisory unless enforced. Record the actual `node --version` from the machine that ran the validation, not the range in the manifest.
