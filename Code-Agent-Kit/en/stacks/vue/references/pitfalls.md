# Pitfalls — Vue.js

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Destructuring loses reactivity

`const { count } = reactive(state)` yields a plain value that never updates. Use `toRefs`, or keep the object. This produces no error — the UI simply stops changing.

## `ref` versus `reactive`

`ref` needs `.value` in script and not in template; `reactive` needs neither and cannot be reassigned. Mixing them is the most common source of a value that renders once and never again.

## `v-for` without a stable key

Index keys cause component state to be reused across different items after a reorder — the symptom is state appearing on the wrong row, not an error.

## Watcher flush timing

`watch` fires before render by default; reading the DOM in it sees the previous frame. `flush: 'post'` or `nextTick` is required.

## Vue 2 array and property caveats

In Vue 2, index assignment and adding a new property are not reactive. In Vue 3 they are. An answer carried across versions is wrong in one of them.
