# Pitfalls — Go + HTMX

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Swap target mismatch is silent

A wrong `hx-target` selector, or a fragment whose root element id differs, produces no console error and no server error. The page simply does not update. Assert on the rendered fragment, not on the 200.

## Returning a full page to a fragment request

The whole document gets swapped into a `div`. It often looks nearly right, which is worse than a failure.

## Response codes HTMX treats specially

Some status codes suppress the swap entirely. A handler that signals an error with a code and also returns markup may have the markup discarded.

## CSRF on hx-post

An HTMX request is a normal request and needs the same token as a form post. Omitting it fails at the middleware, which reports nothing to the user.

## HTMX version pinned client-side

Attribute behaviour differs between HTMX major versions, and the version lives in a script tag rather than in `go.mod`. Read it from the asset.
