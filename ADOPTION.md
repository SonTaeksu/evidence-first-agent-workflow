# Adoption Report Guide

**English** | [한국어](ADOPTION.ko.md)

Please open an Adoption Report or Failure Report with:

- project type;
- stack — and whether you used a shipped one or filled in your own;
- workflow components used;
- task size and type;
- validation-loop count;
- human correction after generation — **what you had to step in and fix, and whether it was the workflow's fault or the stack's**;
- session-handoff result;
- unexpected regressions;
- total elapsed time and estimated model cost;
- changes made to AGENTS.md or the templates.

## Model and machine

This matters more than it sounds. The whole premise is that the procedure carries the judgement, so the model does not have to be large — and that premise needs evidence from machines other than the maintainer's.

- model name and size, and whether it ran locally or through an API;
- coding-agent tool (Codex, Claude Code, Cline, Roo Code, Pi Agent, other);
- **for a local model**: GPU and VRAM, system RAM, quantization;
- context window, and whether you hit it;
- observed generation speed, and whether it degraded as the context grew;
- how far it got — read the kit's documents, followed the five headings, produced a passing commit, or completed a feature.

Approximate numbers are fine. Say they are approximate.

## Please report failures

An unsuccessful experiment is as valuable as a successful one, and usually more so. Specifically worth reporting:

- a check that blocked something that was actually correct — a false alarm is the most damaging defect this project can have;
- a point where you gave up and used `git commit --no-verify`, and what pushed you there;
- a document that told you to do something that did not work;
- a model that could not follow the five headings at all.