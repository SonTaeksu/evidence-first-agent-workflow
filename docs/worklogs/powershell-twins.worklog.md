# Worklog — PowerShell twins for the check tools

- Feature: `powershell-twins`
- Status: **complete** — 14 of 14 applicable tools twinned, 5 recorded `n/a`, 154 parity cases, 0 mismatches on both mirrors; every §6 open item closed; 12 stack profiles with 14 verified MCP endpoints; readiness measured rather than declared; stacks unblocked by interview rather than hand-editing
- Resume Point: nothing outstanding. §7 records what closing the open items
  turned up, §8 the stack work and the readiness-forgery defect, §9 the MCP source
  verification and one claim of mine the owner corrected, §10 the stack interview
  and the document/manifest drift check.

> **Read this file for decisions only.** Everything countable is answered by a
> program, not by this document:
>
> ```bash
> python Code-Agent-Kit/en/tools/check-script-parity/check_script_parity.py --root Code-Agent-Kit/en --status
> ```
>
> That prints which tools are twinned, which are `n/a` and why, and the case
> count. It walks the tree, so it cannot go stale the way a hand-written list can.

## 1. Analysis

A machine without Python has the `.ps1` implementations as its only commit
gate. The kit shipped `.py` only, so on such a machine either nothing is
checked or the commit is refused outright.

The canonical private kit requires every check tool to ship as a `.py` + `.ps1`
pair with **identical verdicts and exit codes**, and records that its own `.ps1`
changes went three releases without ever being executed, because the window
that wrote them had no PowerShell.

## 2. Task

Give every check tool a `.ps1` twin whose verdict is proven equal to the Python
original by a harness, not by inspection. Then wire the twins into the commit
hook, because until that is done the twins exist and nothing calls them.

Done means: `check-script-parity` reports `0 mismatched` and `0 convention
violations` on both language mirrors with PowerShell actually present, and a
machine with no Python can both block and pass a commit for the right reasons.

## 3. Decisions taken (a program cannot recover these)

| Decision | Choice | Why |
|---|---|---|
| Finding identifier scheme | **tool-namespaced** — `<tool-directory>:<finding-id>` | The canonical uses a central `AC-<AREA>-<NNN>` registry. That assumes a closed set; this kit has pluggable stacks, so a stack shipping its own validator would produce a "ghost id" against the core matrix, and two stacks could collide. The tool directory name is already unique, so it is a namespace for free — no central allocation, no 15th required document in the stack contract. |
| Identifier registry | **not adopted** | Rejected `AC-` numbering along with it. Numbers are opaque and stable; tool-scoped names are self-describing and therefore tempting to rename. `docs/core/finding-identifiers.md` forbids renaming to compensate. |
| Case density | **all tools, canonical density** | Not just the gate-critical ones. |
| Fixture ownership | **the harness owns them** | Not borrowed from each tool's `self_test`. A harness that reads a tool's internals breaks whenever that tool is refactored, and then it stops being run. Where a fixture must match a tool's own requirement list, the harness imports that list rather than duplicating it. A *router*'s fixture instead copies the real sub-checks in (`copy_tools`), because routing cannot be exercised without them; that is using them as the tool under test does, not reading their internals. |
| Exit code convention | **`0` pass, `2` validation failure, `1` tool error** — one tool corrected | An earlier pass believed four tools violated this and found on inspection that none did. That pass did not cover `enforce-agent-gates`, which was still unported. It returned **2** for "not inside a git repository". Corrected to **1**: that is not a verdict, it is the absence of one, and `check-document-sync` already exited 1 on the identical condition. Two values for one condition inside one repository is itself the defect. Every caller branches on `!= 0` only (surveyed again), and the CI sample has no `continue-on-error` and no per-code branching, so the change is invisible in behaviour. Both ends are now pinned by the harness — `EG-07 expect 1` and `DS-06 expect 1` — so changing one without the other fails. |
| Argument style across twins | **auto-translated** in the harness | `--kebab-case` becomes `-PascalCase`, and a repeated `--flag value` (argparse's `append`) collapses to `-Flag a,b`, because PowerShell refuses the same parameter twice. The canonical harness kept a separate argument list per implementation; translating keeps one list per case, so the two sides cannot drift by editing only one. |
| Fixture isolation | **one tree per implementation** | Both sides used to share one fixture. That silently breaks any check that *writes* to the tree it inspects: `check-last` stamps a baseline marker, so whichever ran second saw a freshly-marked tree and legitimately reached a different verdict. A disagreement invented by the harness, not found by it. |
| Tools that get no twin | **5, each with a recorded reason** | Not a list to remember — `EXCLUDED` in the harness holds the reason as a string, `--status` prints it as `n/a — <reason>`, and they are excluded from `remaining`. `check-script-parity` (meta-tool: it runs the `.py` side to compare against, so on a Python-less machine there is nothing to compare, and it blocks no commit); `check-agent-config` (TOML, see below); `reference-image-manifest` (PIL); `spa-screen-extractor` (Playwright); `collect-validation-evidence` (wraps a command and propagates its exit code — it reaches no verdict of its own, so there is no verdict for a twin to agree with). Each gets a `.ps1` that states Python is required and exits **1**, never 0: a stub that exited 0 would record an unchecked tree as checked. |
| `check-agent-config` | **stub, no partial twin** | `.codex/config.toml` is TOML, and neither PowerShell 5.1 nor 7 has a parser. A hand-rolled one must handle multi-line strings, inline tables, arrays of tables and dates; any of those wrong is a false alarm, and one false alarm buys `--no-verify` forever. A partial twin — read `.mcp.json`, skip the TOML — was considered and rejected: it would mean a machine with Python catches a TOML defect while a machine without it passes the same tree, which is exactly what twins exist to prevent. **Checked whether the TOML is our choice: it is not.** Codex reads `~/.codex/config.toml` and project-scoped `.codex/config.toml`, profile layers are `$CODEX_HOME/<name>.config.toml`, and `agents.<name>.config_file` is documented as "Path to a TOML config layer". JSON appears only for `hooks.json` and `model_catalog_json`, neither of which is the `mcp_servers` configuration this tool validates. So there is no format change to trade for a twin. |
| `check-kit-selfcheck` coupling | **subprocess + identifier parsing on both sides** | It imported the readiness validator as a Python module and classified the returned failure strings by prose prefix. Two things were wrong. The prose matching died silently (see §5). And the module import was a choice that bought a dependency on an internal signature while leaving the CLI layer — the one every agent, hook and CI job runs — exercised by nothing, and it could not be mirrored by a `.ps1` at all. Both twins now invoke the validator and read identifiers off its output, so this check re-verifies the identifier contract every time it runs. |
| `run-managed-service` | **twinned, with no case that starts a process** | It is not a check and reaches no verdict about the tree, but a PowerShell-only agent without it has no safe way to stop a dev server, and the unsafe way (`Get-Process node \| Stop-Process`) kills the MCP servers the agent itself depends on. The harness proves the paths that need no process or port: the untracked-name refusal, the dead-PID refusal, the usage error, state parsing. Full process cases were rejected — a harness that competes for ports becomes flaky, and a flaky harness is an ignored one. The port-confirmation path (exit 2) is not reachable without a listener, so it is proven in the tool's own `self_test` instead — see §6.5. |
| PID *ownership* verification | **implemented, on the kernel's own start time** | First recorded as deliberately undone, then done on the owner's instruction: preventing a reused-PID kill ranks with preventing a bulk kill, because it is the same failure at a smaller scale. `start` asks the OS for the child's start time and records it; `stop` compares before signalling. The token is the kernel's, never a timestamp this tool took — a local one would drift and force a tolerance window, and a tolerance window is a hole. Sources are per-platform but equivalent: `/proc/<pid>/stat` field 22 on POSIX, `StartTime.Ticks` on Windows. Both twins read the *same* source per platform on purpose; `Get-Process` on Linux returns a .NET-computed wall clock that would never match the raw ticks the `.py` side reads. |
| Usage errors | **remapped to exit 1, kit-wide** | `tools/_lib/kit_cli.py` holds one `ArgumentParser` subclass; all 23 tools use it. argparse exits 2, which this kit publishes as "validation failure", so a typo on the command line was indistinguishable from a finding. Remapping rather than renumbering the convention: `2` suits argparse, but the convention is already published in `docs/core/*`, the enforcement matrix, every docstring and every harness `expect`. No identifier is emitted, and that is forced rather than chosen — PowerShell rejects an unknown parameter in its own binder before any script runs, so a twin cannot print one, and an identifier on one side only would make them disagree on every mistyped flag. |
| Unknown parameters in twins | **`[CmdletBinding()]` everywhere** | A plain PowerShell script collects arguments it does not recognise into `$args` and ignores them, so a mistyped `-AllowProvisonal` would have run with the switch off and reported success. Eight twins were plain scripts. |
| The stack table | **compared, not generated** | Generation is the better shape in the abstract, and a generator was rejected anyway: it introduces its own wiring problem — who runs it, and when — and an ungenerated table is exactly as stale as an unchecked one. `check-kit-selfcheck` is already on the CI path, so a comparison takes effect immediately. Only derived columns are compared, anchored on a backticked `stacks/<name>` cell rather than on the prose label, so renaming a label can neither break the check nor silently disable it. |
| Identifier prefix | **promoted to a documented contract** | `docs/core/finding-identifiers.md` now states that `[<tool>:<finding-id>]` is a stable interface, that machine consumers match the identifier and never the prose, and that changing the format is not finished until a consumer survey is complete. The survey commands are in the document. |
| CI sample self-tests | **enumerated, not listed** | The sample named five `self_test.py` files individually; four others existed and were never run. A hand-written list goes stale the moment somebody adds a tool, and the cost is a gate that looks enforced and is not. Now a `set -e` glob, plus the parity harness. |
| Commit hook | **choose an interpreter, then run once** | The old hook was `python3 "$GATE" --staged 2>/dev/null \|\| python "$GATE" --staged \|\| exit 1`. When python3 was present and the gate legitimately blocked, `\|\|` read that as "python3 did not work" and retried — and `2>/dev/null` had already discarded the findings. On a machine with python3 but no `python`, the operator saw `python: not found` and a refused commit with no stated reason. Conflating "the interpreter is missing" with "the gate found something" is how a gate earns a reputation for lying. |

## 4. Checklist

- Call sites surveyed before the exit-code change: **every caller branches on
  `!= 0` or `== 0`**, none distinguishes 1 from 2. The CI sample has no
  `continue-on-error` and no per-code branching. The hook is `|| exit 1`.
- Consumers that match another tool's output as **prose** — surveyed across the
  whole tree, not guessed at. Exactly one existed (`check-kit-selfcheck`) and it
  was dead. `importlib` use to reach another tool: also exactly one, the same
  place. Other `startswith` uses are on paths, URLs and the BOM;
  `check-document-sync` and `check-git-scope` parse **git's** stdout, not a
  check's; `check-last` forwards a sub-check's output without matching on it. No
  shell or CI consumer greps check output.
- `self_test` assertions that matched on prose were moved to the identifier.
  Only one existed (`check-stack-readiness`).
- Public-release scan after each batch: no sandbox paths, no canonical kit
  material, sanitization clean.
- `KIT-MANIFEST.json` `mirrored_file_count` updated 343 → 358 on both mirrors,
  because `check-mirror-parity` caught the claim contradicting the measurement
  after these files were added.

## 5. Verification

Run with PowerShell on `PATH`:

```bash
python Code-Agent-Kit/en/tools/check-script-parity/check_script_parity.py --root Code-Agent-Kit/en
python Code-Agent-Kit/ko/tools/check-script-parity/check_script_parity.py --root Code-Agent-Kit/ko
```

Last recorded result: **144 agree, 0 mismatched, 0 convention violations** on
each mirror, `exit 0`. `pwsh 7.4.6`, Python 3.10 for the harness itself.

Also green on both mirrors: all **10** `self_test.py` (`run-managed-service` is
new), `check-shell-safety`, `check-kit-selfcheck`, `check-kit-installation`,
`check-state-model` against the sample, and the same checks again through their
`.ps1` twins. Cross-mirror: `check-mirror-parity` CLEAN from **both** twins (360
paths, 96 shared scripts compared) and `check-sanitization` CLEAN over the whole
repository. `--status` reports `remaining: none` on both mirrors.

Guards that were themselves tested rather than assumed:

- with no PowerShell on `PATH` the harness exits **1**, not 0;
- deliberately pinning a wrong `expect` produces a `CONV` finding and exit **2**,
  proving that twins agreeing on a wrong answer cannot pass;
- renaming one identifier inside a twin produces `FAIL` on the affected case —
  run against `enforce_gates.ps1` to confirm the twin was really being exercised
  and not trivially agreeing;
- the commit hook was tested on a repository with **no Python on `PATH` at all**:
  it blocks a non-compliant commit with the full identifier list, passes a
  compliant one, and with neither Python nor PowerShell present it refuses the
  commit rather than passing it. Re-run after `tools/_lib` was introduced, since
  the hook now depends on it being copied too;
- the `check-shell-safety` rule table was checked by *breaking* it: putting
  `New-Item` back into the `-LiteralPath` list makes `self_test.py` fail with
  `NO-LITERALPATH New-Item`, so the guard is proven to fire rather than assumed to;
- the usage-error remap was checked on five tools and on the unknown-subcommand
  path, all exit 1;
- `run-managed-service` was run end to end against a real kernel on both twins:
  a child is started, tracked, stopped, and confirmed gone.

### Defects the harness caught

Every one of these would have mis-judged on a Python-less machine.

1. **PowerShell variable names are case-insensitive.** A local named `$manifest`
   *was* the `[string]$Manifest` parameter, so the parsed JSON object was coerced
   to a string, every property lookup found nothing, and **every stack reported
   READY**. The gate was completely inert.
2. **The same defect, twice more.** In `check_css_contrast.ps1` a local `$config`
   was the `[string]$Config` parameter, and the tool reported a missing `checks`
   key on a perfectly valid config. In `check_mirror_parity.ps1` a local
   `$manifest` overwrote the script-level `$Manifest` holding the filename, so
   only the *first* mirror's claim was ever checked — and comparing identifier
   *sets* hid it, because the set was identical while the count was wrong. This
   mistake is easy to make repeatedly; the comment at each site says so.
3. **A `.ps1` that did not parse at all.** In `check_git_scope.ps1` the `$(` of
   `"...$([\s\S]*?)..."` opened a subexpression inside a double-quoted string.
   The whole gate was a syntax error. The harness reported 12 of 12 cases failing
   on the first run.
4. **A PowerShell function returns its whole pipeline.** `Write-Output` inside
   `Stop-One`, which also returns an exit code, made the message *part of the
   return value*: the caller got `@("...", 0)`, the text never reached the
   console, and the identifier vanished. The one invariant `run-managed-service`
   exists to hold — an untracked name is refused, not widened into an image-name
   sweep — was unobservable from outside.
5. **Argument style differs between the twins.** `--allow-provisional` is not a
   PowerShell parameter, and a repeated `--mirror` cannot bind twice; both made
   the twin error out instead of running.
6. **`New-Item` has no `-LiteralPath`.** Acting on a `check-shell-safety`
   finding broke four twins at once; the parity run caught it immediately. See
   §6.

### The defect that was not in a twin

`check-kit-selfcheck`'s seed assertion was **completely inert**, and had been for
three releases. It classified the readiness validator's failures by prose prefix
(`"Missing or empty required document:"`); the validator's messages had since
gained `[check-stack-readiness:<id>]` identifiers, so no prefix could ever match
again. Measured, not inferred:

- delete a declared required document from a seed → `CLEAN`, exit **0**;
- replace `required_documents` with a string instead of an array → `CLEAN`, exit
  **0**;
- the readiness validator itself caught both, exit 2.

Its own `self_test` caught this too — restoring the prose classifier makes it
print `FAIL: incomplete seed expected exit 2, got 0`. **Nothing ran the
self-test.** The CI sample named five self-tests and this was not one of the
five, and the repository has no workflow of its own at all (§6).

Both tamperings are now harness cases (`KS-02`, `KS-03`) with the word
REGRESSION in their descriptions, so the gate cannot die silently a second time.

## 6. Open items — all closed

Recorded as found, then closed on the owner's decisions. Kept in full because the
*reasons* are the durable part.

1. **`check-shell-safety` demanded a parameter that does not exist.** `New-Item`
   was in its `-LiteralPath` cmdlet list; `New-Item` has only `-Path`. All twelve
   other cmdlets in that list do have it. The finding was therefore
   *unsatisfiable*: obeying it broke the script.

   Closed three ways, per the owner: `New-Item` removed from the list; a
   `new-item-path` **warning** added that names the fix that exists
   (`[System.IO.Directory]::CreateDirectory`); and — the root repair — the rule
   table is now **verified against the installed PowerShell** by `self_test.py`,
   in both directions. Putting `New-Item` back makes the self-test print
   `FAIL: rule table disagrees with PowerShell — NO-LITERALPATH New-Item`.
   Reviewing that table could never have caught it; nobody remembers which of
   thirteen cmdlets has which parameter.

   The blast radius was larger than first reported: **six** shipped files had
   obeyed the impossible rule and thrown at runtime, including
   `scripts/pre-commit-validate.ps1`, an entry point, and the `--output` path of
   `check-build-log` and `check-stack-readiness`. See §7.

2. **Every argparse tool exited 2 on a usage error** — indistinguishable from a
   validation failure under this kit's own convention. Closed with
   `tools/_lib/kit_cli.py`, a shared `ArgumentParser` whose `error()` exits 1,
   adopted by all 23 tools. Remapping rather than renumbering the convention:
   `2` is natural for argparse, but this kit already publishes `2` as "validation
   failure" in `docs/core/*`, the enforcement matrix, every tool docstring and
   every harness `expect`.

   No identifier is emitted for a usage error, and that is a constraint rather
   than a preference: PowerShell rejects an unknown parameter in its own binder,
   before a line of script runs, so there is no hook to print one. An identifier
   on the Python side alone would make the twins disagree on every mistyped flag.

3. **This repository had no CI workflow.** `.github/` held only issue and PR
   templates; the only workflow was the *sample* inside the kit, which protects
   whoever installs the kit and not this repository. That is the confirmed root
   cause of the three-release silence. Closed with `.github/workflows/ci.yml`:
   every `self_test.py` by glob on both mirrors, the parity harness, a
   `remaining: none` coverage assertion, the cross-mirror checks, sanitization,
   and the enforcement gate on the diff. Python pinned to **3.11**, the floor,
   not to latest — passing on 3.13 says nothing about the oldest interpreter in
   use.

4. **PID ownership** — implemented. `start` records the kernel's own start time
   for the child (`/proc/<pid>/stat` field 22 on POSIX, `StartTime.Ticks` on
   Windows), and `stop` compares it before signalling anything. A reused PID gets
   a refusal and exit 2, and the record is **kept**: dropping it would make the
   next run report "not tracked" and look clean.

   The token is the kernel's, never a timestamp this tool took. A local timestamp
   would drift from the kernel's and force a tolerance window, and a tolerance
   window is a hole. Records written before tokens existed are accepted with
   `ownership-unverified` stated rather than refused, so an upgrade mid-session
   is not a lockout — an explicit gap instead of a silent one.

5. **`run-managed-service`'s exit 2 path** — proven, in a new `self_test.py` that
   also covers the full start → stop → gone cycle on both twins. The port case is
   *constructed*, not provoked: the test holds the port itself and records a PID
   that is already gone, so `stop` has nothing to kill and the port cannot come
   free. That isolates the port assertion from the killing.

6. **`check-agent-config` on Python < 3.11** — the `ModuleNotFoundError`
   traceback is gone. The import is guarded and the check exits 1 with the
   requirement stated, so "this machine cannot run the check" is distinguishable
   from "this configuration is wrong". Floor confirmed at **3.11** by the owner
   and documented in `QUICKSTART.md`; `tomllib` is standard there, so no
   third-party parser is vendored.

7. **The stack table** (`stacks/README.md`) was hand-written with nothing checking
   it. Closed by comparison, not generation, on the owner's reasoning: an
   unwired generator is itself another "check nobody runs", while
   `check-kit-selfcheck` is already on the CI path so a comparison takes effect
   immediately. A `Directory` column holding a backticked `stacks/<name>` was
   added as the anchor, and only the derived columns are compared — directory
   existence and `declared_state`. Prose is left alone, and a case proves that
   renaming the label cannot affect the verdict.

## 7. What closing those items turned up

Each of these was found by running something, not by reading it.

1. **Obeying the impossible `New-Item` rule had already shipped broken, in six
   files.** `scripts/pre-commit-validate.ps1`, `scripts/create-spa-screen-spec.ps1`,
   `scripts/create-reference-image-manifest.ps1`,
   `samples/.../scripts/validate.ps1`, and the `--output` path of
   `check_build_log.ps1` and `check_stack_readiness.ps1`. All threw
   `A parameter cannot be found that matches parameter name 'LiteralPath'`.

   The last two mattered most and reveal a harness gap, not just a rule bug: **no
   case passed `--output`**, so that branch had never executed on either side. The
   `.py` wrote its report and exited 0; the `.ps1` threw and exited 1. `BL-09` and
   `SR-11` now cover it. *Any argument a twin accepts needs a case.*

2. **A PowerShell script without `[CmdletBinding()]` silently swallows unknown
   arguments.** They land in `$args` and are ignored, so a mistyped
   `-AllowProvisonal` would have run the check with the switch off and reported
   success. Eight twins were plain scripts. All are now advanced, and `SS-14`
   pins the alignment — it failed on the first run, which is how this was found.

3. **`check-mirror-parity` failed on a state the kit's own instructions produce.**
   Running `scripts/pre-commit-validate` writes
   `samples/.../docs/evidence/generated/*`, which `.gitignore` already declares as
   generated, and the mirror check called them orphan paths. Same shape as the
   `New-Item` rule: a gate must not fail a tree its own instructions create. The
   generated-evidence path is now residue.

4. **The shared library has to travel with any copied tool.** Three fixtures copy
   tools into a temporary tree, and all three broke on `from kit_cli import ...`
   until `tools/_lib` was copied alongside — reporting a tool error the fixture
   had manufactured. `tools/_lib/kit_cli.py` is now in `check-kit-installation`'s
   required files, so a partial install is reported once, at the right layer,
   instead of as a traceback from whichever tool ran first.

5. **A test fixture can accuse the tool of its own bug.** The exit-2 port test
   failed at first: a bound socket that never *accepts* fills its backlog after a
   few probes, the next probe times out, and the tool correctly concluded "free".
   The listener now accepts in a background thread. Recorded because the first
   reading was "the tool is broken", and it was not.

6. **`--` does not survive `pwsh -File`, and neither does `-c`.** PowerShell's
   binder consumes the separator and then matches `-c` against `-Command`/`-Cwd`.
   Declaring `[string[]]` does not help either: comma splitting is done by
   PowerShell's *command-line parser*, and arguments arriving from an external
   argv — which is how a hook or CI invokes anything — pass through literally. So
   `run_service.ps1` takes one comma-separated string and splits it itself. The
   two twins are invoked differently here by necessity; both spellings are
   documented.

## 8. Stack profiles, and readiness becoming measured

Ten stack profiles were added: WPF, WCF and ASMX on .NET Framework; Vue, Next.js
and Node.js; Go, Go + HTMX, Rust and Elixir. Sixteen documents each, generated
from one data module so a hundred and eighty files cannot drift, with every
stack-specific sentence authored rather than templated.

### The question that changed the design

Asked what needed providing to make a stack `ready`, the honest answer turned out
to be *almost nothing* — and that was the finding. `declared_state` was a hand-typed
claim, each input's `status` was a hand-typed claim, and the validator checked only
that the claims agreed with each other. An `evidence` list was accepted for being
**non-empty**. Measured:

```
evidence: ["this/file/does/not/exist.json"]   ->   Stack readiness: READY, exit 0
```

Fourteen placeholder documents and invented paths validated as ready. The owner's
question — "can readiness not be judged by measuring the evidence when the kit is
actually used?" — is the correct answer to that, and it also removes the choice of
what to declare for the new stacks: the tool measures, and whatever it reports is
the state.

`check-stack-readiness` now resolves every cited path against the tree:

- stack-relative first, then project-root-relative, because a profile legitimately
  cites its own documents *and* files in the project it governs;
- a leading `/` means project-root-relative and nothing else — the only reading
  `/global.json` ever had;
- globs count when they match at least one file;
- the project root is found by marker file, with `--project-root` to override it.

**At least one** reference must resolve, not all. A profile may list several
candidate manifests, and a project with only some of them is not unevidenced.
Nothing resolving is the forgery.

### What measurement found immediately

`react-aspnetcore` was shipping `ready` with its `runtime-sdk-versions` evidence
pointing at `/global.json`, `frontend/package.json` and `backend/*.csproj` — **none
of which exist anywhere in this repository**, and no `global.json` exists in the
sample either. It read as "the versions were detected" and nothing had been. The
paths now name the real sample files, and it measures `ready` for a reason.

`csharp-winforms` passed unchanged: its evidence pointed at its own skeleton all
along, which is why it was the only stack whose `ready` meant anything.

### Evidence is a path, not a description

This tool's own self-test cited `"search: no client"` as evidence. A sentence
cannot be checked by anything, which puts it back among the things somebody typed.
Proving a capability *absent* is the case that seems to need prose and does not:
the search belongs in `capability-detection.md`, and that document is the evidence.
The shipped stacks already did it that way.

### The ten stacks, and why all ten are `blocked`

Not a shortfall — the measured state. Each needs versions, chosen libraries, a
validation profile and a confidentiality decision, and each `STACK-INPUTS.md` is
those questions rather than a guess at the answers. Inventing them would
manufacture exactly the claim the readiness check now tests for.

WPF additionally ships a skeleton, and the skeleton's own README says plainly that
**it has not been compiled** — no MSBuild and no .NET Framework targeting pack
existed where it was written. The files exist and are internally consistent; that
is the whole claim.

The one line in it that earns its place is in `App.xaml.cs`: raising
`PresentationTraceSources.DataBindingSource` to Warning. A failed WPF binding
throws nothing, logs nothing at the default level, and renders an empty control.
Without that line "the binding works" is unfalsifiable.

### MCP configuration

Every stack ships `mcp-profile.json.example` with both servers and
`mcp/source-routing.md` saying which is authoritative for what. Only two servers
are named anywhere in this kit — `microsoft-learn` and `context7` — because only
two are known to exist for this purpose. The connector registry was searched; it
has no others for developer documentation. A configuration entry for a server
nobody has connected to is indistinguishable from an invented one.

Both are included per stack rather than only the authoritative one: a .NET project
still consumes NuGet packages and a Node project still touches Microsoft-documented
tooling. Which server answers which question is a routing decision, not a matter of
leaving one out of the file.

### Three more instances of one pattern

The kit's own gates flagging states the kit's own instructions produce.

1. **The harness fixture became a forgery** the moment evidence was measured: its
   default cited `global.json` without creating one, so every case built on it
   failed for a reason unrelated to what the case tested. The fixture now contains
   what it cites — as do `check-stack-readiness`'s and two others' self-tests.
2. **`check-shell-safety` flagged the glob branch** of the new evidence resolver.
   Here the rule was *right*: rather than suppress it, the wildcard is split off
   and passed as `-Filter` so the base path is still matched with `-LiteralPath`.
   A project under a directory called `project [old]` is exactly the case the rule
   guards, and `-Path` would have made this tool fail on it while looking correct.
3. **`check-mirror-parity` flagged generated evidence** written by
   `scripts/pre-commit-validate` — paths `.gitignore` already declares as
   generated. Now residue.

### A mirror repaired rather than papered over

Fifty-five files under `Code-Agent-Kit/ko/stacks/{rust,elixir,go-htmx}/<same-name>/`
were nested duplicates: `rm -rf` failed silently against the mount's permissions
and `cp -r` then nested the source inside the target. Three ways not to fix it were
available and all three were wrong — create the same directories in `en` so the
paths match; add the paths to the residue list; lower the counted claim to 594.
Each silences `check-mirror-parity` while leaving the defect, which is the failure
mode this repository exists to prevent.

`KIT-MANIFEST.json` was set to 539 — the correct tree — while the garbage was still
present, so the gate went on reporting until the tree actually matched. Recording
594 would have made the garbage official.

Deleted once permission was granted for that folder, after showing that all 55
extra files lay inside the four target paths and none outside. Four residue files
(`__pycache__`, generated evidence) were cleaned in the same pass rather than left
to the residue exclusion. `check-mirror-parity` now reports CLEAN from both twins:
539 paths each side, 100 shared scripts byte-identical.

## 9. MCP sources, verified rather than listed

The stack profiles previously named two servers — `microsoft-learn` and
`context7` — because those were the only two anyone had connected to. The owner
then ran `@modelcontextprotocol/inspector` against a candidate list: connect,
`tools/list`, and a real `tools/call`. **16 checks, 15 PASS, 1 PARTIAL, 0
unreachable, 0 requiring authentication.** That is the layer this window could not
reach, and it is what turned a list of URLs into evidence.

Recorded in `docs/core/mcp-source-verification.md` and referenced from
`mcp-knowledge-routing.md` and the enforcement matrix, because an unreferenced
document is the same failure as an unrun check.

### What each stack now routes to

Fourteen verified endpoints across ten stacks, each with the **tool names the
server actually exposed** — not the ones its documentation claims. That precision
earns its keep: the routing rules name specific tools, so a rename is a finding
rather than a detail, and the re-verification command is in the document.

`microsoft-learn` for the three .NET stacks, GitMCP on the official documentation
repository for each of the rest, plus DeepWiki for `go-htmx` structure with the
standing caveat that its answers are model-generated and never the final citation.

### Not enabled by default, and that is the design

The root adapter configuration still carries only `microsoft-learn` and
`context7`. Per-stack servers live in each stack's `mcp-profile.json.example`.
Copying that file is the act by which an operator accepts that these queries leave
the machine — which matters because this kit is used on closed networks, and a
call to a public endpoint transmits the query, the arguments the agent assembled,
and whatever context it attached. The owner's own guidance says register only what
a project uses; this makes that the default rather than the advice.

### Findings from checking rather than reading

1. **GitMCP's landing page is not evidence of anything.** `gitmcp.io/{owner}/{repo}`
   serves a confident page — naming the repository, offering client snippets — for
   repositories that **do not exist**. Measured against
   `thisorgdoesnotexist99/norepohere99`. The page is generated from the URL path,
   so a browser check establishes nothing. Verify the repository on `github.com`
   (real returns a page, missing returns nothing) and the server with the
   Inspector.

2. **Transport is Streamable HTTP because SSE failed.** The first run used SSE and
   every GitMCP endpoint answered `405`. Recorded so nobody re-derives it from the
   client examples that still show SSE.

3. **A claim of mine that was wrong, kept rather than deleted.** `dotnet/docs` and
   `vuejs/docs` both yield GitMCP tools named `search_docs_documentation`, and I
   wrote that as a collision prohibiting registering the two together. The owner
   pushed back: the entry points differ. Correct — most clients qualify a tool by
   its server (Claude Code presents `mcp__<server>__<tool>`), so the identifiers do
   not collide. What survives is weaker and still real: a model choosing between
   them sees identical base names differing only by which repository they search,
   and whether each tool's *description* names its repository was not captured.
   Downgraded from prohibition to caution, with the correction left visible in the
   document — a retraction that is quietly edited out teaches nothing.

4. **One candidate rejected on inspection.** `snyk-labs/mcp-server-nodejs-api-docs`
   is named in the source guide as a Node.js option. 9 stars, 36 commits, no
   releases, and **42 open pull requests against 0 open issues** — dependency bots
   accumulating on a repository nobody merges. Recorded as *not recommended* rather
   than silently omitted, so the next person does not re-evaluate it from scratch.

5. **The one PARTIAL is optional, not primary.** `mcp.vue-mcp.org` connected and
   listed five tools; `vue_docs_search` returned `isError:true` on a real call. Two
   further reasons not to depend on it: FSL-1.1-ALv2 is not an OSI-approved
   licence, and it is one maintainer behind a single hosted endpoint. `vuejs/docs`
   GitMCP, which passed, is the default.

6. **The kit's own link check caught the wiring.** The first generated routing
   documents linked `../../docs/core/...` from `stacks/<name>/mcp/`, one level
   short. `check-kit-installation` reported ten dangling links before anything was
   committed.

### What is still not established

Answer correctness — a `PASS` is a call that returned, not one that was right.
Availability over time: fourteen third-party endpoints are fourteen things that can
disappear. And the default branch a GitMCP endpoint searches is not any project's
installed version, which is the specific confusion these profiles exist to prevent.

## 10. Unblocking a stack without hand-editing two files

The owner asked whether the blocked stacks could be filled in, and said hand-editing
looked inconvenient. It was worse than inconvenient. `STACK-INPUTS.md` is the table a
person fills in and `STACK-READINESS.json` is what the checker reads, and **nothing
compared them**. Fill in the table, forget the manifest, and the stack stayed
`blocked` while never saying why. Update the manifest, leave the table stale, and the
document lied about the project. No tool existed to help; the instruction was
literally "fill the files in that folder".

### Two decisions, both the owner's

**An agent interview, not a CLI wizard.** `prompts/8-fill-stack.md` — the agent reads
the project's manifests and lock files to detect what it can, asks only what it
cannot read, writes both files together, then runs the checker and reports its
verdict rather than stating one. The rules are the substance: detect before asking,
never fill a row from memory, ask three or four questions at a time, and treat a
row nobody can answer as `unknown` rather than a gap to close. A blocked stack is a
correct state.

**The drift check blocks, and the user is told.** First proposed as a note that could
not move the derived state. The owner overruled that: leave it able to block, and
notify. So it is a warning, a warning derives `provisional`, and a stack declaring
`ready` with disagreeing files fails on the declared-state mismatch. That is the
intended outcome rather than a side effect, and the finding message carries the fix
because the person reading it is mid-task and will not go looking for an explanation.

### The join had to be built before the comparison could exist

The tables were prose-keyed — `| .NET SDK | ... | detected |` against a manifest key
of `runtime-sdk-versions`. Nothing to join on. A `Key` column now carries the
manifest key in backticks, the same anchoring technique already used for the stacks
table, for the same reason: joining on prose breaks the moment somebody improves a
sentence.

A document with **no** key column is not compared at all. Being unable to compare is
not the same as disagreeing, and reporting it as a disagreement would fail every
stack whose document predates the check. `SR-20` pins that.

The two `ready` stacks got the column by hand, because they are the ones making a
`ready` claim and were the only ones the check would otherwise have skipped. Adding
it surfaced a documentation gap in `react-aspnetcore`: its manifest resolved
`authoritative-sources` while its table had no row for it at all. Added.

### Verified by breaking it

Flipping one status in `react-aspnetcore`'s table — the exact "filled the table,
forgot the manifest" mistake — produces:

```text
WARN: [check-stack-readiness:inputs-document-drift] feature-model: STACK-INPUTS.md
      says 'unknown' but STACK-READINESS.json says 'confirmed'. Both must agree ...
FAIL: [check-stack-readiness:declared-state-mismatch] declared 'ready' but derived 'provisional'
Stack readiness: BLOCKED
```

Both twins, identically. Restoring it returns `READY`. Four harness cases: drift
blocks, agreement changes nothing, no key column is not compared, and a document key
the manifest does not have is ignored.

### A number in prose that had already rotted

The README said the twins were compared on "150 cases". Adding four made it 154 while
the sentence still said 150 — a counted claim in prose with nothing checking it, which
is the same shape as the `mirrored_file_count` defect, minus the mechanism that
catches that one. The beginner-facing sentence now makes the claim without a number
("case by case, and fails if any single case disagrees") so it cannot rot, and
`OVERVIEW.md` keeps the figure alongside the command that prints the current one.
