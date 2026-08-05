# C# Windows Forms Communication and Data Contract

- **Single entry point**: a form reaches everything outside itself through one injected service interface. In the reference skeleton that is `IGreetingService`. A form does not open a connection, call an HTTP client, or read a file directly.
- **Request mapping**: the form passes primitives or a request type it owns. It does not pass control instances or event arguments across the boundary.
- **Response mapping**: the service returns data, never a control or a `Form`. Formatting for display happens in the form.
- **Error contract**: the service raises a typed exception or returns a result value. The form decides what the user sees. A swallowed exception that leaves the UI unchanged is a defect.
- **Authentication propagation**: decided by the `authentication-provider` capability. While it is `unknown`, do not add credential handling.
- **Generated-client ownership**: when a service reference or generated proxy exists, the regeneration command is recorded and the generated file is not hand-edited.

## UI thread boundary

This is the contract that breaks most often, so it is stated as a rule rather than a guideline.

```text
service or background work   ConfigureAwait(false)
→ no control access
→ marshal through Control.Invoke / BeginInvoke
→ form code                  ConfigureAwait(true)
→ control access
```

- Controls are bound to the thread that created them. Only `Invoke`, `BeginInvoke`, `EndInvoke`, and `CreateGraphics` are safe to call from another thread, and `CreateGraphics` only after the handle exists.
- Touching a control from another thread raises `InvalidOperationException` with the message *Cross-thread operation not valid*. It always raises under the debugger and may raise in production, so an untested path is not a safe path.
- `InvokeRequired` returns `false` both when no marshal is needed and when the control's handle does not exist yet. On a background thread, check `IsHandleCreated` as well; otherwise the handle is created on a thread with no message pump and the application becomes unstable.
- Do not disable the check with `CheckForIllegalCrossThreadCalls`. That hides the defect rather than fixing it.

## Contract change

A change to the service interface updates, in the same change: the interface, the implementation, the form call site, the unit tests, and the feature `current.md`. A contract that changes on one side only is an incomplete change, not a partial success.
