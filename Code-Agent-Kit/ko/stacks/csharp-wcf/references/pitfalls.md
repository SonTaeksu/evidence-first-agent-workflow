# Pitfalls — WCF (.NET Framework 4.7.2+)

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Binding configuration resolved by name

An endpoint's `bindingConfiguration` is matched by name. A typo does not error — the default binding for that binding type is used instead, silently changing timeouts, message size and security.

## Regeneration overwrites hand edits

Edits to a generated proxy survive until the next regeneration and then vanish. Put adaptation in a hand-written wrapper, never in generated code.

## Undeclared faults lose their detail

Callers see `FaultException` with no typed detail, so the failure cannot be handled specifically. Declare `[FaultContract]` for every fault a caller is expected to branch on.

## MaxReceivedMessageSize default

The default is small. A payload that grows past it fails at the transport with a message that does not name the size as the cause.

## Serializer choice

`DataContractSerializer` and `XmlSerializer` produce different wire formats for the same type. Which one applies depends on attributes; do not assume.
