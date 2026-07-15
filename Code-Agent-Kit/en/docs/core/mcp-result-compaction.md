# MCP and Retrieval Result Compaction

MCP reduces search effort but does not remove context limits.

After retrieval:

1. extract only the fact needed for the task;
2. record source, version, and verification method;
3. place the compact fact in the worklog or stack provenance;
4. keep a link or identifier when permitted;
5. do not copy the full retrieval result into current state;
6. do not re-inject the full result in later sessions.

Current state records verified decisions, not retrieval transcripts.
