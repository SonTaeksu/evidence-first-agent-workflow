# SPDX-License-Identifier: MPL-2.0
"""Verify that every `.py` check and its `.ps1` twin reach the same verdict.

A machine without Python has the `.ps1` implementations as its only gate. If a
twin disagrees with its Python original, that machine's verdict differs from
everyone else's — and the difference shows up as a false alarm, which is the
one failure mode that teaches an operator to bypass the gate permanently.

**Exit codes alone are not a sufficient comparison.** Two implementations can
both exit 2 for entirely different reasons and look identical. So each case
compares a pair:

    (exit code, set of finding identifiers printed)

Identifiers are `<tool>:<finding-id>`, emitted by the tool itself — see
`docs/core/finding-identifiers.md`.

**Agreement between the twins is not sufficient either.** Two implementations
can be wrong in the same way and still agree, and the harness would report a
clean run. So every case also pins the exit code it expects:

    expect  0 pass · 2 validation failure · 1 tool error

That turns the exit-code convention itself into a machine verdict rather than
a documented intention. A case that agrees but disagrees with `expect` is
reported as a convention violation, separately from a parity mismatch.

Fixtures are owned by this harness, not borrowed from each tool's `self_test`.
A harness that reads a tool's internals breaks every time that tool is
refactored, and then it stops being run.

Requires pwsh or powershell. When neither is present this tool **fails** rather
than passing: an unverified twin recorded as verified is worse than an
unverified twin recorded as unverified.

Exit codes:
  0  every case agrees
  2  at least one disagreement
  1  tool error, including no PowerShell available
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

BOM = "\ufeff"
IDENTIFIER = re.compile(r"\[([a-z0-9][a-z0-9/_-]*:[a-z0-9-]+)\]")


def identifiers(text: str) -> list[str]:
    return sorted(set(IDENTIFIER.findall(text)))


# ---------------------------------------------------------------------------
# Cases. Each entry is:
#   tool   directory name under tools/
#   case   stable id, used in the report
#   desc   what the case establishes
#   files  {relative path: content}  — content starting with BOM keeps it
#   args   argv after the script path; {ROOT} expands to the fixture root
#   expect exit code the convention requires: 0 pass, 2 validation failure,
#          1 tool error. Pinned so "both twins wrong the same way" cannot pass.

# Credential-shaped fixtures are assembled at run time rather than written as
# literals. The public-release sanitization gate cannot tell a test fixture from
# a real leak, and it is right not to try — so the harness does not hand it a
# string to find. Assembling keeps the fixture honest without weakening that gate.
def _secret_fixture(kind: str) -> str:
    if kind == "password":
        return "".join(["pass", "word"]) + ' = "' + "hunter" + "2xyz" + '"\n'
    if kind == "aws":
        return "AK" + "IA" + "IOSFODNN7EXAMPLE" + "\n"
    if kind == "private-key":
        return "-----BEGIN RSA " + "PRIVATE" + " KEY-----\nabc\n"
    raise ValueError(kind)


# A stack fixture built from the readiness validator's own required-document
# list, so the harness and the tool cannot drift apart.
def _stack_fixture(declared="ready", inputs=None, capabilities=None,
                   drop_document=None, extra=None) -> dict:
    from importlib import util as _util
    here = Path(__file__).resolve().parent.parent / "check-stack-readiness"
    spec = _util.spec_from_file_location("_sr_req", here / "check_stack_readiness.py")
    module = _util.module_from_spec(spec)
    spec.loader.exec_module(module)

    documents = [d for d in module.REQUIRED_DEFAULT if d != drop_document]
    files = {f"stack/{d}": "# placeholder\n" for d in documents}
    manifest = {
        "schema": "evidence-first/stack-readiness/v1",
        "stack_key": "fixture",
        "declared_state": declared,
        "required_documents": list(module.REQUIRED_DEFAULT),
        "inputs": inputs if inputs is not None else [
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "evidence": ["global.json"], "notes": ""}],
        "capabilities": capabilities if capabilities is not None else [
            {"key": "shared-api-client", "status": "absent",
             "evidence": ["capability-detection.md"],
             "selected_path": "manual-adapter", "blocks": ["API work"]}],
    }
    # The fixture has to contain what its manifest cites. Evidence is measured
    # now, so a default citing `global.json` without one present would make the
    # baseline fixture itself a forgery -- and every case built on it would fail
    # for a reason that has nothing to do with what the case is testing.
    files["stack/global.json"] = "{}\n"
    files["stack/STACK-READINESS.json"] = json.dumps(manifest, indent=2) + "\n"
    if extra:
        files.update(extra)
    return files


# A fixture that satisfies check-kit-installation, built from the tool's own
# requirement list so the two cannot drift apart. Cases then remove or corrupt
# exactly one thing.
def _kit_fixture(**overrides) -> dict:
    from importlib import util as _util
    here = Path(__file__).resolve().parent.parent / "check-kit-installation"
    spec = _util.spec_from_file_location("_kit_req", here / "check_kit_installation.py")
    module = _util.module_from_spec(spec)
    spec.loader.exec_module(module)

    files = {relative: "# placeholder\n" for relative in module.REQUIRED_FILES}
    for relative in module.REQUIRED_DIRS:
        files.setdefault(f"{relative}/.keep", "")
    files.update(overrides)
    return {k: v for k, v in files.items() if v is not None}


# A tree that satisfies every enforce-agent-gates rule at once, so a case can
# break exactly one thing. Every argument here corresponds to one gate, which is
# what lets a failure name a single cause.
def _gate_fixture(source="frontend/app.ts", worklog=True, sections=(1, 2, 3, 4, 5),
                  expected_entry=True, declares=None, verification="evidence",
                  current=True, history=True, project_map=True,
                  extra=None) -> dict:
    files: dict[str, str] = {}
    if source:
        files[source] = "export const x = 1;\n"
    if current:
        files["docs/features/thing.current.md"] = "# current\n"
    if history:
        files["docs/features/thing.history.md"] = "# history\n"
    if project_map:
        files["docs/project-map.md"] = "# map\n"
    if worklog:
        declared = declares if declares is not None else source
        body = ["# Worklog - fixture\n"]
        titles = {1: "## 1. Analysis", 2: "## 2. Task",
                  3: "## 3. Todo and Micro-Verify", 4: "## 4. Checklist",
                  5: "## 5. Verification"}
        for number in (1, 2, 3, 4, 5):
            if number not in sections:
                continue
            body.append(titles[number])
            if number == 2:
                body.append("### Expected Files\n")
                if expected_entry:
                    body.append(f"- [ ] {declared}")
                else:
                    # Named in prose only. The gate wants a checkbox entry; the
                    # scope gate is satisfied either way, which keeps this case
                    # about the checkbox and nothing else.
                    body.append(f"the file {declared} will change")
            elif number == 5:
                if verification == "evidence":
                    body.append("PASS - `python3 tools/check-last/check_last.py` exit 0")
                elif verification == "bare-claim":
                    body.append("Result: PASS.")
                elif verification == "no-claim":
                    body.append("Not run yet.")
            body.append("")
        files["docs/worklogs/fixture.worklog.md"] = "\n".join(body) + "\n"
    if extra:
        files.update(extra)
    return {k: v for k, v in files.items() if v is not None}


def _inputs_document(status: str = "detected", key: str = "runtime-sdk-versions") -> str:
    """A STACK-INPUTS.md whose table can be joined to the manifest.

    The `Key` column is the join. Without it the drift check cannot compare, which
    is a different outcome from disagreeing and is covered by its own case.
    """
    return (
        "# Stack Inputs\n\n"
        "| Input | Key | Required | Value or Path | Evidence | Status |\n"
        "|---|---|---:|---|---|---|\n"
        f"| Versions in use | `{key}` | yes | 1.0 | global.json | {status} |\n"
    )


def _inputs_document_without_key() -> str:
    """The same table with the `Key` column dropped — a real regression.

    `ko/stacks/react-aspnetcore` shipped exactly this: the column was lost in
    translation, so no row could be joined, so the drift comparison iterated over
    nothing and the stack measured READY with exit 0. The check passed because its
    subject was missing. These cases pin the corrected behaviour in both twins.
    """
    return (
        "# Stack Inputs\n\n"
        "| Input | Required | Value or Path | Evidence | Status |\n"
        "|---|---:|---|---|---|\n"
        "| Versions in use | yes | 1.0 | global.json | detected |\n"
    )


# A well-formed project state tree, built from check-state-model's own section
# and front-matter lists so the harness cannot drift from the requirement it is
# testing. Each argument breaks exactly one rule.
def _state_model_fixture(project_map=True, drop_map_section=None,
                         current=True, front_matter=True, drop_field=None,
                         drop_current_section=None, korean_sections=False,
                         history=True, append_only=True,
                         architecture=True, drop_architecture=None,
                         template=True, drop_template_section=None) -> dict:
    from importlib import util as _util
    here = Path(__file__).resolve().parent.parent / "check-state-model"
    spec = _util.spec_from_file_location("_sm_req", here / "check_state_model.py")
    module = _util.module_from_spec(spec)
    spec.loader.exec_module(module)

    files: dict[str, str] = {}

    if project_map:
        headings = [group[0] for group in module.PROJECT_MAP_SECTIONS
                    if group[0] != drop_map_section]
        files["docs/project-map.md"] = "# Map\n" + "".join(f"{h}\n" for h in headings)

    if current:
        fields = [f for f in module.FRONT_MATTER_FIELDS if f != drop_field]
        block = ""
        if front_matter:
            values = {"feature": "example", "status": "stable"}
            lines = [f"{f}: {values.get(f, 'x')}" for f in fields]
            block = "---\n" + "\n".join(lines) + "\n---\n"
        headings = []
        for group in module.CURRENT_SECTIONS:
            # The Korean alternative must satisfy the same requirement. Picking
            # the last alternative where one exists is what proves the twin
            # honours the alternation and not just the first string.
            chosen = group[-1] if korean_sections else group[0]
            if group[0] == drop_current_section:
                continue
            headings.append(chosen)
        files["docs/features/example.current.md"] = (
            block + "".join(f"{h}\n" for h in headings))

    if history:
        body = "# History\n"
        if append_only:
            body += "\n> Append-only.\n"
        files["docs/features/example.history.md"] = body

    if architecture:
        for area in ("system", "database"):
            for kind in ("current", "history"):
                name = f"{area}.{kind}.md"
                if name == drop_architecture:
                    continue
                body = "# Current\n"
                if kind == "history":
                    body = "# History\n\n> Append-only.\n"
                files[f"docs/architecture/{name}"] = body

    if template:
        headings = [group[0] for group in module.WORKLOG_SECTIONS
                    if group[0] != drop_template_section]
        files["templates/core/worklog.md"] = (
            "```yaml\ncurrent: docs/features/example.current.md\n```\n"
            + "".join(f"{h}\n" for h in headings))

    return files


# check-last is a router, so its fixtures are whole small projects: a state tree,
# optionally a stack, optionally a script, plus the real sub-checks copied in by
# `copy_tools`. Every case here asks "did the right sub-check get invoked", which
# is the only thing a router can get wrong.
_ROUTED = ["check-shell-safety", "check-state-model", "check-stack-readiness"]


def _stacks_fixture(name="demo", **overrides) -> dict:
    inner = _stack_fixture(**overrides)
    return {key.replace("stack/", f"stacks/{name}/", 1): value
            for key, value in inner.items()}


# A seed the kit instructs the reader to copy, placed where check-kit-selfcheck
# looks for it. `manifest_patch` exists for the schema-tampering cases, which
# cannot be expressed through the readiness fixture's own arguments.
def _seed_fixture(prefix="templates/stack-profile", manifest_patch=None,
                  **overrides) -> dict:
    inner = _stack_fixture(**overrides)
    files = {key.replace("stack/", f"{prefix}/", 1): value
             for key, value in inner.items()}
    if manifest_patch:
        key = f"{prefix}/STACK-READINESS.json"
        manifest = json.loads(files[key])
        manifest.update(manifest_patch)
        files[key] = json.dumps(manifest, indent=2) + "\n"
    return files


# The hand-written stack table, with a knob for each way it can stop matching the
# manifests. `label` is prose on purpose: a case proves that changing it does not
# affect the verdict, because the backticked directory is the anchor.
def _stack_table(state="blocked", directory="stacks/demo", label="Demo Stack",
                 extra_row=None) -> dict:
    rows = [
        "| Stack | Directory | Status | Owner inputs still required |",
        "|---|---|---|---|",
        f"| {label} | `{directory}` | planned / {state} | everything |",
    ]
    if extra_row:
        rows.append(f"| Gone | `{extra_row}` | planned / blocked | everything |")
    return {"stacks/README.md": "# Stack Profiles\n\n" + "\n".join(rows) + "\n"}


_UNRESOLVED_INPUT = [
    {"key": "runtime-sdk-versions", "required": True, "source": "user",
     "status": "unknown", "evidence": [], "notes": ""}
]


# Two mirrors that agree, plus one knob per way they can stop agreeing.
def _mirror_fixture(count=None, rule="all-files", drift=False,
                    extra_en=None, extra_ko=None) -> dict:
    shared = {
        "docs/index.md": "# index\n",
        "tools/run.py": "value = 1\n",
    }
    files: dict[str, str] = {}
    for name in ("en", "ko"):
        for relative, content in shared.items():
            files[f"{name}/{relative}"] = content
    if drift:
        files["ko/tools/run.py"] = "value = 2\n"
    if extra_en:
        for relative, content in extra_en.items():
            files[f"en/{relative}"] = content
    if extra_ko:
        for relative, content in extra_ko.items():
            files[f"ko/{relative}"] = content
    if count is not None:
        manifest: dict = {"mirrored_file_count": count}
        if rule is not None:
            manifest["mirrored_file_count_rule"] = rule
        for name in ("en", "ko"):
            files[f"{name}/KIT-MANIFEST.json"] = json.dumps(manifest, indent=2) + "\n"
    return files


# One stylesheet and one check config, with a knob per failure mode.
def _color_fixture(fg="#111111", bg="#ffffff", minimum=None,
                   selector=":root", property_name="color",
                   at_rule=False, comment=False, unbalanced=False) -> dict:
    body = f"  color: {fg};\n  background-color: {bg};\n"
    if comment:
        body = (f"  /* color: #cccccc; */\n  color: {fg};\n"
                f"  background-color: {bg};\n")
    css = ":root {\n" + body + "}\n"
    if at_rule:
        css = "@media (min-width: 40em) {\n  :root {\n" + body + "  }\n}\n"
    if unbalanced:
        css = ":root {\n" + body
    check: dict = {
        "name": "body text",
        "foreground": {"selector": selector, "property": property_name},
        "background": {"selector": ":root", "property": "background-color"},
    }
    if minimum is not None:
        check["minimum"] = minimum
    return {
        "app.css": css,
        "checks.json": json.dumps({"checks": [check]}, indent=2) + "\n",
    }


def _router_fixture(shell=None, stack=None, feature_names=None, **state) -> dict:
    files = _state_model_fixture(**state)
    if shell:
        files.update(shell)
    if stack:
        files.update(stack)
    if feature_names:
        # A feature's current document names its files in backticks; that list is
        # what --feature routes on.
        quoted = " ".join(f"`{name}`" for name in feature_names)
        files["docs/features/example.current.md"] += f"\nSee {quoted}.\n"
    return files


# ---------------------------------------------------------------------------
CASES: list[dict] = [
    # -- check-shell-safety --------------------------------------------------
    {
        "tool": "check-shell-safety", "case": "SS-01", "expect": 0,
        "desc": "clean tree - BOM present, -LiteralPath used, variables quoted",
        "files": {
            "s/ok.ps1": BOM + "Test-Path -LiteralPath $Image\n",
            "s/ok.sh": '#!/usr/bin/env bash\ncd "$ROOT"\n',
        },
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-02", "expect": 2,
        "desc": "ps1 without BOM",
        "files": {"s/a.ps1": "Test-Path -LiteralPath $Image\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-03", "expect": 2,
        "desc": "ps1 path cmdlet without -LiteralPath",
        "files": {"s/a.ps1": BOM + "Test-Path $Image\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-04", "expect": 0,
        "desc": "-LiteralPath after another switch is still recognised",
        "files": {"s/a.ps1": BOM + "Get-Content -Raw -Encoding UTF8 -LiteralPath $File\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-05", "expect": 2,
        "desc": "sh with a BOM loses its shebang",
        "files": {"s/a.sh": BOM + "#!/usr/bin/env bash\necho hi\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-06", "expect": 2,
        "desc": "unquoted shell variable in a path position",
        "files": {"s/a.sh": "#!/usr/bin/env bash\ncd $ROOT\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-07", "expect": 0,
        "desc": "commented-out bad usage is not a finding",
        "files": {"s/a.sh": "#!/usr/bin/env bash\n# cd $ROOT is wrong\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-08", "expect": 0,
        "desc": "extensionless git hook without a BOM is accepted",
        "files": {"hooks/pre-commit": '#!/usr/bin/env sh\npython3 "$GATE" --staged\n'},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-09", "expect": 0,
        "desc": "a quoted literal path is not mistaken for a variable",
        "files": {"s/a.ps1": BOM + 'Test-Path "C:/some path/file.txt"\n'},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-10", "expect": 2,
        "desc": "several findings in one tree",
        "files": {
            "s/a.ps1": "Test-Path $Image\n",
            "s/b.sh": "#!/usr/bin/env bash\ncd $ROOT\n",
        },
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-11", "expect": 0,
        "desc": "a tree with no scripts at all is clean",
        "files": {"README.md": "# nothing\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-12", "expect": 0,
        "desc": "New-Item with a variable path warns - there is no -LiteralPath to demand",
        "files": {"s/a.ps1": BOM + "New-Item -ItemType Directory -Force -Path $Output\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-shell-safety", "case": "SS-13", "expect": 0,
        "desc": "the .NET replacement for New-Item is not flagged at all",
        "files": {"s/a.ps1": BOM + "[void][System.IO.Directory]::CreateDirectory($Output)\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        # argparse exits 2 on a usage error, which this kit publishes as
        # "validation failure" -- so a typo used to be indistinguishable from a
        # finding. tools/_lib/kit_cli.py remaps it to 1. PowerShell's binder
        # already exits 1, so this case is what keeps the two aligned; before the
        # remap they disagreed on every mistyped flag and no case noticed.
        "tool": "check-shell-safety", "case": "SS-14", "expect": 1,
        "desc": "a flag that does not exist is a tool error on both sides, with no finding identifier",
        "files": {"README.md": "# r\n"},
        "args": ["--root", "{ROOT}", "--no-such-flag"],
    },
    # -- check-kit-installation ---------------------------------------------
    {
        "tool": "check-kit-installation", "case": "KI-01", "expect": 0,
        "desc": "a complete mirror passes",
        "files": _kit_fixture(),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-installation", "case": "KI-02", "expect": 2,
        "desc": "a required file is missing",
        "files": _kit_fixture(**{"AGENTS.md": None}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-installation", "case": "KI-03", "expect": 2,
        "desc": "a required directory is missing",
        "files": _kit_fixture(**{"demos/.keep": None, "demos/README.md": None}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-installation", "case": "KI-04", "expect": 2,
        "desc": "a .ko.md language suffix survived the install",
        "files": _kit_fixture(**{"docs/leftover.ko.md": "# ko\n"}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-installation", "case": "KI-05", "expect": 2,
        "desc": "a local Markdown link points at nothing",
        "files": _kit_fixture(**{"README.md": "# r\n\n[gone](docs/not-here.md)\n"}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-installation", "case": "KI-06", "expect": 2,
        "desc": "a link escapes the kit root",
        "files": _kit_fixture(**{"README.md": "# r\n\n[out](../../etc/passwd)\n"}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-installation", "case": "KI-07", "expect": 0,
        "desc": "external links and anchors are not resolved",
        "files": _kit_fixture(**{"README.md": "# r\n\n[a](https://example.invalid) [b](#top)\n"}),
        "args": ["--root", "{ROOT}"],
    },
    # -- check-stack-readiness ----------------------------------------------
    {
        "tool": "check-stack-readiness", "case": "SR-01", "expect": 0,
        "desc": "everything resolved with evidence is ready",
        "files": _stack_fixture(),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-02", "expect": 2,
        "desc": "a required document is missing",
        "files": _stack_fixture(declared="blocked", drop_document="SKILL.md"),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-03", "expect": 2,
        "desc": "a required input is unresolved",
        "files": _stack_fixture(declared="blocked", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "user",
             "status": "unknown", "evidence": [], "notes": ""}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-04", "expect": 2,
        "desc": "a resolved input with no evidence cannot pass as verified",
        "files": _stack_fixture(declared="blocked", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "user",
             "status": "confirmed", "evidence": [], "notes": ""}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-05", "expect": 2,
        "desc": "an unknown capability that blocks something",
        "files": _stack_fixture(declared="blocked", capabilities=[
            {"key": "implementation-path", "status": "unknown", "evidence": [],
             "selected_path": "", "blocks": ["all stack-dependent implementation"]}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-06", "expect": 2,
        "desc": "an unknown capability that blocks nothing is provisional, not ready",
        "files": _stack_fixture(declared="provisional", capabilities=[
            {"key": "optional-thing", "status": "unknown", "evidence": [],
             "selected_path": "", "blocks": []}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-07", "expect": 0,
        "desc": "the same provisional stack passes with --allow-provisional",
        "files": _stack_fixture(declared="provisional", capabilities=[
            {"key": "optional-thing", "status": "unknown", "evidence": [],
             "selected_path": "", "blocks": []}]),
        "args": ["--stack", "{ROOT}/stack", "--allow-provisional"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-08", "expect": 2,
        "desc": "declaring ready on a stack that derives blocked is itself a failure",
        "files": _stack_fixture(declared="ready", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "user",
             "status": "unknown", "evidence": [], "notes": ""}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-09", "expect": 2,
        "desc": "a present capability with no selected_path",
        "files": _stack_fixture(declared="blocked", capabilities=[
            {"key": "shared-api-client", "status": "present",
             "evidence": ["api.ts"], "selected_path": "  ", "blocks": []}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-10", "expect": 2,
        "desc": "an unrecognised status value",
        "files": _stack_fixture(declared="blocked", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "user",
             "status": "probably", "evidence": [], "notes": ""}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        # REGRESSION. Every `status` and `declared_state` in a manifest is a
        # sentence somebody typed, and this tool used only to check that those
        # sentences agreed with each other. An `evidence` list was accepted for
        # being non-empty, never for naming anything that existed — so fourteen
        # placeholder documents plus invented paths reported READY, exit 0.
        "tool": "check-stack-readiness", "case": "SR-12", "expect": 2,
        "desc": "REGRESSION - a manifest whose evidence names nothing that exists is not ready",
        "files": _stack_fixture(declared="ready", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "notes": "",
             "evidence": ["this/does/not/exist.json", "nor/this.md"]}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-13", "expect": 0,
        "desc": "one of several cited paths resolving is enough - a candidate list is not a forgery",
        "files": _stack_fixture(inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "notes": "",
             "evidence": ["STACK.md", "absent-in-this-project/package.json"]}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-14", "expect": 0,
        "desc": "a glob counts when it matches at least one file",
        "files": _stack_fixture(inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "notes": "", "evidence": ["*.md"]}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-15", "expect": 2,
        "desc": "a glob that matches nothing is not evidence",
        "files": _stack_fixture(declared="blocked", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "notes": "", "evidence": ["*.nothing"]}]),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        # `/x` can only mean project-root-relative; that was always the intent of
        # the `/global.json` this kit shipped, and nothing ever resolved it.
        "tool": "check-stack-readiness", "case": "SR-16", "expect": 0,
        "desc": "a leading slash resolves against the project root, found by its marker file",
        "files": dict(_stack_fixture(inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "notes": "", "evidence": ["/global.json"]}]),
            **{"AGENTS.md": "# root marker\n", "global.json": "{}\n"}),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-17", "expect": 0,
        "desc": "--project-root overrides the inferred root for a layout the markers do not describe",
        "files": dict(_stack_fixture(inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "auto",
             "status": "detected", "notes": "", "evidence": ["/elsewhere/versions.json"]}]),
            **{"elsewhere/versions.json": "{}\n"}),
        "args": ["--stack", "{ROOT}/stack", "--project-root", "{ROOT}"],
    },
    {
        # The most likely mistake when unblocking a stack: fill in the table a person
        # reads, forget the manifest the checker reads. It used to keep saying
        # `blocked` without ever saying why.
        "tool": "check-stack-readiness", "case": "SR-18", "expect": 2,
        "desc": "the inputs document and the manifest disagree - a warning, and it moves the state",
        "files": dict(_stack_fixture(), **{
            "stack/STACK-INPUTS.md": _inputs_document(status="unknown")}),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-19", "expect": 0,
        "desc": "the same two files agreeing changes nothing",
        "files": dict(_stack_fixture(), **{
            "stack/STACK-INPUTS.md": _inputs_document(status="detected")}),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        # This case used to pin `expect: 0` on the reasoning that being unable to
        # compare is not the same as disagreeing. That reasoning holds for one key
        # with no row; it does not hold for a filled-in table with no `Key` column
        # at all, and the difference was not academic — `ko/stacks/react-aspnetcore`
        # lost that column in translation and measured READY with exit 0, because
        # the comparison ran over nothing. The pin was protecting the hole, so it is
        # reversed here deliberately rather than quietly.
        "tool": "check-stack-readiness", "case": "SR-20", "expect": 2,
        "desc": "a filled-in document with no key column is reported, not passed",
        "files": dict(_stack_fixture(), **{
            "stack/STACK-INPUTS.md":
                "# Stack Inputs\n\n| Input | Status |\n|---|---|\n| Versions | unknown |\n"}),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        "tool": "check-stack-readiness", "case": "SR-21", "expect": 0,
        "desc": "a key in the document that the manifest does not have is ignored",
        "files": dict(_stack_fixture(), **{
            "stack/STACK-INPUTS.md": _inputs_document(status="unknown", key="not-a-manifest-key")}),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        # A table with no `Key` column cannot be compared to the manifest at all.
        # Reported, and at drift's weight: the warning derives `provisional`, so a
        # stack declaring `ready` on an uncomparable table fails.
        "tool": "check-stack-readiness", "case": "SR-22", "expect": 2,
        "desc": "a document with no Key column is reported, not silently passed",
        "files": dict(_stack_fixture(declared="ready"), **{
            "stack/STACK-INPUTS.md": _inputs_document_without_key()}),
        "args": ["--stack", "{ROOT}/stack"],
    },
    {
        # The other half: it is a warning, not a failure. `--allow-provisional` is
        # what separates the two — it forgives the derived state but not a single
        # entry in `failures`, so exit 0 here proves the finding was recorded as a
        # warning. Pinning both halves stops a later "fix" from quietly promoting
        # it to a failure or demoting it to silence.
        "tool": "check-stack-readiness", "case": "SR-23", "expect": 0,
        "desc": "the same document is a warning, not a failure",
        "files": dict(_stack_fixture(declared="provisional"), **{
            "stack/STACK-INPUTS.md": _inputs_document_without_key()}),
        "args": ["--stack", "{ROOT}/stack", "--allow-provisional"],
    },
    {
        # The same coverage hole in the second tool that had it.
        "tool": "check-stack-readiness", "case": "SR-11", "expect": 0,
        "desc": "--output creates its parent directory",
        "files": _stack_fixture(),
        "args": ["--stack", "{ROOT}/stack", "--output", "{ROOT}/out/nested/report.json"],
    },
    # -- check-build-log -----------------------------------------------------
    {
        "tool": "check-build-log", "case": "BL-01", "expect": 0,
        "desc": "a clean log passes",
        "files": {"build.log": "compiling\nlinking\nBuild succeeded\n"},
        "args": ["{ROOT}/build.log"],
    },
    {
        "tool": "check-build-log", "case": "BL-02", "expect": 2,
        "desc": "a line beginning with error matches the default pattern",
        "files": {"build.log": "compiling\nerror CS0246: type not found\n"},
        "args": ["{ROOT}/build.log"],
    },
    {
        "tool": "check-build-log", "case": "BL-03", "expect": 2,
        "desc": "build failed anywhere in the line",
        "files": {"build.log": "the Build Failed after 3s\n"},
        "args": ["{ROOT}/build.log"],
    },
    {
        "tool": "check-build-log", "case": "BL-04", "expect": 0,
        "desc": "the word error mid-sentence does not match - the pattern is anchored",
        "files": {"build.log": "no error handling needed here\n"},
        "args": ["{ROOT}/build.log"],
    },
    {
        "tool": "check-build-log", "case": "BL-05", "expect": 2,
        "desc": "a required success pattern is absent",
        "files": {
            "build.log": "compiling\n",
            "cfg.json": json.dumps({"required_success_patterns": ["Build succeeded"]}),
        },
        "args": ["{ROOT}/build.log", "--config", "{ROOT}/cfg.json"],
    },
    {
        "tool": "check-build-log", "case": "BL-06", "expect": 0,
        "desc": "an ignore pattern removes the text before judging",
        "files": {
            "build.log": "error: this one is known and ignored\n",
            "cfg.json": json.dumps({"ignore_patterns": ["(?im)^error: this one.*$"]}),
        },
        "args": ["{ROOT}/build.log", "--config", "{ROOT}/cfg.json"],
    },
    {
        "tool": "check-build-log", "case": "BL-07", "expect": 2,
        "desc": "capturing group in a config pattern - Python re and .NET must agree",
        "files": {
            "build.log": "ERR-1 first\nERR-2 second\nERR-3 third\n",
            "cfg.json": json.dumps({"error_patterns": [r"(?m)^ERR-(\d+)"]}),
        },
        "args": ["{ROOT}/build.log", "--config", "{ROOT}/cfg.json"],
    },
    {
        "tool": "check-build-log", "case": "BL-08", "expect": 1,
        "desc": "a missing log file is a tool error, not a validation failure",
        "files": {"placeholder.txt": "x\n"},
        "args": ["{ROOT}/not-here.log"],
    },
    {
        # A coverage hole, found the hard way. No case passed --output, so the
        # directory-creation line inside it was never executed by either twin --
        # and the .ps1 used `New-Item -LiteralPath`, a parameter that does not
        # exist. The .py wrote its report and exited 0; the .ps1 threw and exited
        # 1. It had shipped that way. Any argument a twin accepts needs a case.
        "tool": "check-build-log", "case": "BL-09", "expect": 0,
        "desc": "--output creates its parent directory - the path no case used to exercise",
        "files": {"build.log": "compiling\nBuild succeeded\n"},
        "args": ["{ROOT}/build.log", "--output", "{ROOT}/out/nested/report.json"],
    },
    # -- check-sanitization --------------------------------------------------
    {
        "tool": "check-sanitization", "case": "SA-01", "expect": 0,
        "desc": "a clean tree passes",
        "files": {"src/app.py": "value = 1\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-sanitization", "case": "SA-02", "expect": 2,
        "desc": "a hardcoded password is blocked",
        "files": {"src/app.py": _secret_fixture("password")},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-sanitization", "case": "SA-03", "expect": 2,
        "desc": "a private key block is blocked",
        "files": {"src/id.pem": _secret_fixture("private-key")},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-sanitization", "case": "SA-04", "expect": 2,
        "desc": "an AWS access key id is blocked",
        "files": {"src/cfg.txt": _secret_fixture("aws")},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-sanitization", "case": "SA-05", "expect": 0,
        "desc": "vendor directories are skipped",
        "files": {"node_modules/pkg/index.js": _secret_fixture("password")},
        "args": ["--root", "{ROOT}"],
    },
    # -- check-document-sync -------------------------------------------------
    {
        "tool": "check-document-sync", "case": "DS-01", "expect": 0,
        "desc": "state present and nothing changed since the baseline",
        "git": True, "cwd": True,
        "files": {
            "sample/docs/project-map.md": "# map\n",
            "sample/docs/f.current.md": "# current\n",
            "sample/docs/f.history.md": "# history\n",
        },
        "args": ["--scope", "sample", "--current", "docs/f.current.md",
                 "--history", "docs/f.history.md", "--project-map", "docs/project-map.md"],
    },
    {
        "tool": "check-document-sync", "case": "DS-02", "expect": 2,
        "desc": "code changed but no state file changed with it",
        "git": True, "cwd": True,
        "files": {
            "sample/docs/project-map.md": "# map\n",
            "sample/docs/f.current.md": "# current\n",
            "sample/docs/f.history.md": "# history\n",
        },
        "after_git": {"sample/frontend/app.ts": "export const x = 1;\n"},
        "args": ["--scope", "sample", "--current", "docs/f.current.md",
                 "--history", "docs/f.history.md", "--project-map", "docs/project-map.md"],
    },
    {
        "tool": "check-document-sync", "case": "DS-03", "expect": 2,
        "desc": "the Project Map is missing",
        "git": True, "cwd": True,
        "files": {
            "sample/docs/f.current.md": "# current\n",
            "sample/docs/f.history.md": "# history\n",
        },
        "args": ["--scope", "sample", "--current", "docs/f.current.md",
                 "--history", "docs/f.history.md", "--project-map", "docs/project-map.md"],
    },
    {
        "tool": "check-document-sync", "case": "DS-04", "expect": 2,
        "desc": "the Project Map names a path that does not exist",
        "git": True, "cwd": True,
        "files": {
            "sample/docs/project-map.md": "# map\n\n- entry: `frontend/gone.ts`\n",
            "sample/docs/f.current.md": "# current\n",
            "sample/docs/f.history.md": "# history\n",
        },
        "args": ["--scope", "sample", "--current", "docs/f.current.md",
                 "--history", "docs/f.history.md", "--project-map", "docs/project-map.md"],
    },
    {
        "tool": "check-document-sync", "case": "DS-05", "expect": 2,
        "desc": "a state file is missing",
        "git": True, "cwd": True,
        "files": {
            "sample/docs/project-map.md": "# map\n",
            "sample/docs/f.current.md": "# current\n",
        },
        "args": ["--scope", "sample", "--current", "docs/f.current.md",
                 "--history", "docs/f.history.md", "--project-map", "docs/project-map.md"],
    },
    {
        "tool": "check-document-sync", "case": "DS-06", "expect": 1,
        "desc": "outside a git repository this is a tool error, not a pass",
        "cwd": True,
        "files": {"sample/docs/project-map.md": "# map\n"},
        "args": ["--scope", "sample", "--current", "docs/f.current.md",
                 "--history", "docs/f.history.md", "--project-map", "docs/project-map.md"],
    },
    # -- enforce-agent-gates -------------------------------------------------
    # The commit-layer gate. Its fixtures need files that are *staged and not
    # committed*, which is what the `stage` key produces.
    {
        "tool": "enforce-agent-gates", "case": "EG-01", "expect": 0,
        "desc": "an empty index is not something to govern",
        "git": True, "cwd": True,
        "files": {"README.md": "# r\n"},
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-02", "expect": 2,
        "desc": "project source staged with no worklog and no state update",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(worklog=False, current=False,
                                   history=False, project_map=False),
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-03", "expect": 0,
        "desc": "worklog, state and Project Map all staged with the source",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(),
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-04", "expect": 2,
        "desc": "the worklog is missing one of the five mandatory sections",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(sections=(1, 2, 3, 5)),
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-05", "expect": 2,
        "desc": "Expected Files names the file in prose but has no checkbox entry",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(expected_entry=False),
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-06", "expect": 2,
        "desc": "a credential in a staged config file blocks even with no source change",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"src/settings.json": _secret_fixture("password")},
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-07", "expect": 1,
        "desc": "outside a git repository this gate cannot reach a verdict - tool error, not a block",
        "cwd": True,
        "files": {"README.md": "# r\n"},
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-08", "expect": 2,
        "desc": "Verification claims PASS with no command and no exit code",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(verification="bare-claim"),
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-09", "expect": 2,
        "desc": "--strict-scope blocks a staged source file the worklog never declared",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(source="frontend/widget.ts",
                                   declares="frontend/other.ts"),
        "args": ["--staged", "--strict-scope"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-10", "expect": 0,
        "desc": "the same undeclared file is a warning without --strict-scope",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": _gate_fixture(source="frontend/widget.ts",
                                   declares="frontend/other.ts"),
        "args": ["--staged"],
    },
    {
        "tool": "enforce-agent-gates", "case": "EG-11", "expect": 0,
        "desc": "a .py under tools/ is workflow material, not project source",
        "git": True, "cwd": True, "stage": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"tools/thing/thing.py": "value = 1\n"},
        "args": ["--staged"],
    },
    # -- check-state-model ---------------------------------------------------
    {
        "tool": "check-state-model", "case": "SM-01", "expect": 0,
        "desc": "a well-formed state tree passes",
        "files": _state_model_fixture(),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-02", "expect": 2,
        "desc": "the Project Map is missing",
        "files": _state_model_fixture(project_map=False),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-03", "expect": 2,
        "desc": "the Project Map is missing one required section",
        "files": _state_model_fixture(drop_map_section="## Shared File Reverse Index"),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-04", "expect": 2,
        "desc": "no feature current document exists at all",
        "files": _state_model_fixture(current=False, history=False),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-05", "expect": 2,
        "desc": "a current document with no YAML front matter",
        "files": _state_model_fixture(front_matter=False),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-06", "expect": 2,
        "desc": "one front-matter field is absent",
        "files": _state_model_fixture(drop_field="code-verified"),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-07", "expect": 2,
        "desc": "a current document is missing one required section",
        "files": _state_model_fixture(drop_current_section="## Contracts"),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-08", "expect": 2,
        "desc": "the history document the front matter implies does not exist",
        "files": _state_model_fixture(history=False),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-09", "expect": 2,
        "desc": "history exists but never declares the append-only rule",
        "files": _state_model_fixture(append_only=False),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-10", "expect": 2,
        "desc": "an architecture history document is missing",
        "files": _state_model_fixture(drop_architecture="system.history.md"),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-11", "expect": 0,
        "desc": "the Korean heading alternative satisfies the same requirement",
        "files": _state_model_fixture(korean_sections=True),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-12", "expect": 2,
        "desc": "the worklog template is missing one of the five sections",
        "files": _state_model_fixture(drop_template_section="## 4. Checklist"),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-13", "expect": 1,
        "desc": "a missing worklog template is a tool error, not a finding",
        "files": _state_model_fixture(template=False),
        "args": ["--project-docs", "{ROOT}/docs",
                 "--worklog-template", "{ROOT}/templates/core/worklog.md"],
    },
    {
        "tool": "check-state-model", "case": "SM-14", "expect": 0,
        "desc": "the default relative template path resolves against the working directory",
        "cwd": True,
        "files": _state_model_fixture(),
        "args": ["--project-docs", "docs"],
    },
    # -- check-last ----------------------------------------------------------
    # `cwd` is set so the routed state check resolves its relative worklog
    # template against the fixture, the way it would in a real project.
    {
        "tool": "check-last", "case": "CL-01", "expect": 0,
        "desc": "--all on a clean project runs the applicable checks and passes",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(shell={"src/ok.ps1": BOM + "Test-Path -LiteralPath $Image\n"}),
        "args": ["--root", "{ROOT}", "--all"],
    },
    {
        "tool": "check-last", "case": "CL-02", "expect": 2,
        "desc": "a shell finding reaches the router with the sub-check's own identifier",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(shell={"src/bad.ps1": "Test-Path -LiteralPath $Image\n"}),
        "args": ["--root", "{ROOT}", "--all"],
    },
    {
        "tool": "check-last", "case": "CL-03", "expect": 2,
        "desc": "a state finding reaches the router with the sub-check's own identifier",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(drop_current_section="## Contracts"),
        "args": ["--root", "{ROOT}", "--all"],
    },
    {
        "tool": "check-last", "case": "CL-04", "expect": 0,
        "desc": "no Project Map means this is not a project - the state check is not routed to",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(project_map=False),
        "args": ["--root", "{ROOT}", "--all"],
    },
    {
        "tool": "check-last", "case": "CL-05", "expect": 2,
        "desc": "a stack declaring ready that derives blocked is routed to and fails",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(stack=_stacks_fixture(declared="ready", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "user",
             "status": "unknown", "evidence": [], "notes": ""}])),
        "args": ["--root", "{ROOT}", "--all"],
    },
    {
        "tool": "check-last", "case": "CL-06", "expect": 0,
        "desc": "a stack declaring blocked is deliberately not routed to",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(stack=_stacks_fixture(declared="blocked", inputs=[
            {"key": "runtime-sdk-versions", "required": True, "source": "user",
             "status": "unknown", "evidence": [], "notes": ""}])),
        "args": ["--root", "{ROOT}", "--all"],
    },
    {
        "tool": "check-last", "case": "CL-07", "expect": 0,
        "desc": "--mark resets the baseline and routes to nothing",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(shell={"src/bad.ps1": "Test-Path -LiteralPath $Image\n"}),
        "args": ["--root", "{ROOT}", "--mark"],
    },
    {
        "tool": "check-last", "case": "CL-08", "expect": 1,
        "desc": "--feature naming a document that does not exist is a tool error",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(),
        "args": ["--root", "{ROOT}", "--feature", "absent"],
    },
    {
        "tool": "check-last", "case": "CL-09", "expect": 2,
        "desc": "--feature routes on the paths the current document names, not on the tree",
        "cwd": True, "copy_tools": _ROUTED,
        "files": _router_fixture(
            shell={"src/bad.ps1": "Test-Path -LiteralPath $Image\n"},
            feature_names=["src/bad.ps1"]),
        "args": ["--root", "{ROOT}", "--feature", "example"],
    },
    # -- check-git-scope -----------------------------------------------------
    # `after_git` files are the change set: written after the baseline commit and
    # left unstaged, so `git status --porcelain` reports them.
    {
        "tool": "check-git-scope", "case": "GS-01", "expect": 0,
        "desc": "with nothing declared there is nothing to judge - SKIP, not a failure",
        "git": True,
        "files": {"README.md": "# r\n"},
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-git-scope", "case": "GS-02", "expect": 0,
        "desc": "the one changed file is the one declared",
        "git": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n"},
        "args": ["--root", "{ROOT}", "--expected", "frontend/app.ts"],
    },
    {
        "tool": "check-git-scope", "case": "GS-03", "expect": 2,
        "desc": "a changed file nobody declared or acknowledged",
        "git": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n",
                      "frontend/stray.ts": "export const y = 2;\n"},
        "args": ["--root", "{ROOT}", "--expected", "frontend/app.ts"],
    },
    {
        "tool": "check-git-scope", "case": "GS-04", "expect": 0,
        "desc": "the same stray file passes once it is acknowledged",
        "git": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n",
                      "frontend/stray.ts": "export const y = 2;\n"},
        "args": ["--root", "{ROOT}", "--expected", "frontend/app.ts",
                 "--ack", "frontend/stray.ts"],
    },
    {
        "tool": "check-git-scope", "case": "GS-05", "expect": 0,
        "desc": "a declared file that never changed is a warning by default",
        "git": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n"},
        "args": ["--root", "{ROOT}", "--expected",
                 "frontend/app.ts,frontend/never.ts"],
    },
    {
        "tool": "check-git-scope", "case": "GS-06", "expect": 2,
        "desc": "the same warning blocks under --strict - identifier unchanged, severity is not part of it",
        "git": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n"},
        "args": ["--root", "{ROOT}", "--expected",
                 "frontend/app.ts,frontend/never.ts", "--strict"],
    },
    {
        "tool": "check-git-scope", "case": "GS-07", "expect": 0,
        "desc": "Expected Files is read out of the design document",
        "git": True,
        "files": {
            "README.md": "# r\n",
            "design.md": "# Design\n\n## Expected Files\n\n"
                         "- [ ] `frontend/app.ts`\n\n## Notes\n\nnothing\n",
        },
        "after_git": {"frontend/app.ts": "export const x = 1;\n"},
        "args": ["--root", "{ROOT}", "--design", "{ROOT}/design.md"],
    },
    {
        "tool": "check-git-scope", "case": "GS-08", "expect": 1,
        "desc": "a design with no Expected Files section is a tool error, not a pass",
        "git": True,
        "files": {"README.md": "# r\n", "design.md": "# Design\n\n## Notes\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n"},
        "args": ["--root", "{ROOT}", "--design", "{ROOT}/design.md"],
    },
    {
        "tool": "check-git-scope", "case": "GS-09", "expect": 2,
        "desc": "outside git it falls back to artifact existence, and the artifact is absent",
        "files": {"README.md": "# r\n"},
        "args": ["--root", "{ROOT}", "--expected", "frontend/app.ts"],
    },
    {
        "tool": "check-git-scope", "case": "GS-10", "expect": 0,
        "desc": "outside git an artifact that exists passes, with detection openly skipped",
        "files": {"README.md": "# r\n", "frontend/app.ts": "export const x = 1;\n"},
        "args": ["--root", "{ROOT}", "--expected", "frontend/app.ts"],
    },
    {
        "tool": "check-git-scope", "case": "GS-11", "expect": 0,
        "desc": "--scope prefixes the expected list and ignores changes outside it",
        "git": True,
        "files": {"README.md": "# r\n"},
        "after_git": {"frontend/app.ts": "export const x = 1;\n",
                      "backend/other.cs": "class C {}\n"},
        "args": ["--root", "{ROOT}", "--expected", "app.ts", "--scope", "frontend"],
    },
    {
        "tool": "check-git-scope", "case": "GS-12", "expect": 0,
        "desc": "--expected-file strips checkbox and backtick decoration from each line",
        "git": True,
        "files": {
            "README.md": "# r\n",
            "expected.txt": "- [ ] `frontend/app.ts`\n- [x] `frontend/two.ts`\n",
        },
        "after_git": {"frontend/app.ts": "export const x = 1;\n",
                      "frontend/two.ts": "export const y = 2;\n"},
        "args": ["--root", "{ROOT}", "--expected-file", "{ROOT}/expected.txt"],
    },
    # -- check-kit-selfcheck -------------------------------------------------
    # KS-02 and KS-03 are regression cases, not illustrations. Both tamperings
    # reported CLEAN and exit 0 for three releases, because this check classified
    # the validator's findings by prose prefix and the validator's messages had
    # since gained identifiers. Pinning them here is what stops the gate from
    # dying silently a second time.
    {
        "tool": "check-kit-selfcheck", "case": "KS-01", "expect": 0,
        "desc": "an intact seed has no structural failure",
        "copy_tools": ["check-stack-readiness"],
        "files": _seed_fixture(),
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-02", "expect": 2,
        "desc": "REGRESSION - a required document deleted from a seed must not report CLEAN",
        "copy_tools": ["check-stack-readiness"],
        "files": _seed_fixture(declared="blocked", drop_document="SKILL.md"),
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-03", "expect": 2,
        "desc": "REGRESSION - required_documents as a string instead of an array must not report CLEAN",
        "copy_tools": ["check-stack-readiness"],
        "files": _seed_fixture(declared="blocked",
                               manifest_patch={"required_documents": "STACK.md"}),
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-04", "expect": 2,
        "desc": "a seed declaring a state it cannot reach is a kit defect",
        "copy_tools": ["check-stack-readiness"],
        "files": _seed_fixture(declared="ready", drop_document="SKILL.md"),
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-05", "expect": 0,
        "desc": "a blank seed's unresolved inputs are a deliberate unknown, not a defect",
        "copy_tools": ["check-stack-readiness"],
        "files": _seed_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT),
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-06", "expect": 0,
        "desc": "a seed that is not present is skipped, not failed",
        "copy_tools": ["check-stack-readiness"],
        "files": {"README.md": "# r\n"},
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-07", "expect": 0,
        "desc": "a directory with no readiness manifest is not a stack seed",
        "copy_tools": ["check-stack-readiness"],
        "files": {"templates/stack-profile/STACK.md": "# s\n"},
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-08", "expect": 1,
        "desc": "no validator in the tree is a tool error - a seed cannot be recorded as clean",
        "files": _seed_fixture(),
        "args": ["--root", "{ROOT}", "--seed", "templates/stack-profile"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-09", "expect": 2,
        "desc": "a shipped stack declaring ready that does not validate as ready",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="ready", inputs=_UNRESOLVED_INPUT),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-10", "expect": 0,
        "desc": "a shipped stack declaring blocked is not asserted on",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-11", "expect": 0,
        "desc": "the stack table agrees with the manifest",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT,
                                 extra=_stack_table(state="blocked")),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-12", "expect": 2,
        "desc": "the table still says ready after the manifest was changed to blocked",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT,
                                 extra=_stack_table(state="ready")),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-13", "expect": 2,
        "desc": "a stack with no row in the table",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT,
                                 extra=_stack_table(directory="stacks/other")),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-14", "expect": 2,
        "desc": "a table row for a stack that no longer exists",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT,
                                 extra=_stack_table(state="blocked", extra_row="stacks/removed")),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-kit-selfcheck", "case": "KS-15", "expect": 0,
        "desc": "renaming the prose label cannot break the comparison - the directory is the anchor",
        "copy_tools": ["check-stack-readiness"],
        "files": _stacks_fixture(declared="blocked", inputs=_UNRESOLVED_INPUT,
                                 extra=_stack_table(state="blocked", label="Something Else Entirely")),
        "args": ["--root", "{ROOT}"],
    },
    # -- check-mirror-parity -------------------------------------------------
    {
        "tool": "check-mirror-parity", "case": "MP-01", "expect": 0,
        "desc": "matched mirrors with a matched counted claim",
        "files": _mirror_fixture(),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-02", "expect": 2,
        "desc": "a path present in one mirror and absent from the other",
        "files": _mirror_fixture(extra_en={"docs/only-here.md": "# x\n"}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-03", "expect": 2,
        "desc": "a shared script that is not byte-identical across mirrors",
        "files": _mirror_fixture(drift=True),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-04", "expect": 2,
        "desc": "a counted claim contradicted by measurement",
        "files": _mirror_fixture(count=99, rule="all-files"),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-05", "expect": 0,
        "desc": "a count with no recorded counting rule cannot be checked - warn, not fail",
        "files": _mirror_fixture(count=99, rule=None),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-06", "expect": 0,
        "desc": "a counting rule this tool cannot measure is unverifiable, not wrong",
        "files": _mirror_fixture(count=99, rule="by-moon-phase"),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-07", "expect": 0,
        "desc": "build residue is excluded from measurement and warned about",
        "files": _mirror_fixture(
            extra_en={"tools/__pycache__/run.cpython-312.pyc": "x"}),
        "args": ["--root", "{ROOT}"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-08", "expect": 1,
        "desc": "a named mirror that does not exist is a tool error",
        "files": _mirror_fixture(),
        "args": ["--root", "{ROOT}", "--mirror", "en", "--mirror", "fr"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-09", "expect": 2,
        "desc": "--identical-suffix adds a suffix that must match, and it does not",
        "files": _mirror_fixture(extra_en={"data/x.txt": "a\n"},
                                 extra_ko={"data/x.txt": "b\n"}),
        "args": ["--root", "{ROOT}", "--identical-suffix", "txt"],
    },
    {
        "tool": "check-mirror-parity", "case": "MP-10", "expect": 0,
        "desc": "the same differing file passes when its suffix is not declared shared",
        "files": _mirror_fixture(extra_en={"data/x.txt": "a\n"},
                                 extra_ko={"data/x.txt": "b\n"}),
        "args": ["--root", "{ROOT}"],
    },
    # -- ui-color-gate -------------------------------------------------------
    {
        "tool": "ui-color-gate", "case": "UC-01", "expect": 0,
        "desc": "a pair comfortably above its minimum",
        "files": _color_fixture(fg="#111111", bg="#ffffff", minimum=4.5),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-02", "expect": 2,
        "desc": "a pair below its minimum",
        "files": _color_fixture(fg="#999999", bg="#ffffff", minimum=4.5),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-03", "expect": 0,
        "desc": "exactly on the boundary - #000 on #fff is exactly 21:1, where two implementations of one formula would first diverge",
        "files": _color_fixture(fg="#000000", bg="#ffffff", minimum=21),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-04", "expect": 0,
        "desc": "three-digit hex expands the same way on both sides",
        "files": _color_fixture(fg="#000", bg="#fff", minimum=21),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-05", "expect": 1,
        "desc": "a non-literal colour is refused rather than guessed at",
        "files": _color_fixture(fg="var(--brand)", bg="#ffffff"),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-06", "expect": 1,
        "desc": "a selector the stylesheet does not define",
        "files": _color_fixture(selector=".absent"),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-07", "expect": 1,
        "desc": "a property the selector does not set",
        "files": _color_fixture(property_name="outline-color"),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-08", "expect": 0,
        "desc": "declarations inside an at-rule are found by the recursive walk",
        "files": _color_fixture(at_rule=True, minimum=21,
                                fg="#000000", bg="#ffffff"),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-09", "expect": 0,
        "desc": "a commented-out declaration is stripped before parsing",
        "files": _color_fixture(comment=True, minimum=21,
                                fg="#000000", bg="#ffffff"),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    {
        "tool": "ui-color-gate", "case": "UC-10", "expect": 1,
        "desc": "an unbalanced brace is a tool error, not a silent partial parse",
        "files": _color_fixture(unbalanced=True),
        "args": ["--css", "{ROOT}/app.css", "--config", "{ROOT}/checks.json"],
    },
    # -- run-managed-service -------------------------------------------------
    # No case here starts a process or binds a port. A harness that competes for
    # ports is a harness that gets ignored, and an ignored harness proves nothing.
    # The port-confirmation path (exit 2) is therefore unproven by this harness;
    # the OS-layer evidence lives in the tool's own self-test.
    {
        "tool": "run-managed-service", "case": "RS-01", "expect": 0,
        "desc": "THE INVARIANT - an untracked name is refused, never widened into an image-name sweep",
        "cwd": True,
        "files": {"README.md": "# r\n"},
        "args": ["stop", "--name", "frontend"],
    },
    {
        "tool": "run-managed-service", "case": "RS-02", "expect": 0,
        "desc": "the same refusal when other services are tracked but not this one",
        "cwd": True,
        "files": {".agent-state/services.json": json.dumps(
            {"backend": {"pid": 999999999, "port": 0, "cmd": ["x"], "cwd": "", "started": 1.0}})},
        "args": ["stop", "--name", "frontend"],
    },
    {
        "tool": "run-managed-service", "case": "RS-03", "expect": 1,
        "desc": "start with nothing after -- is a usage error, and starts nothing",
        "cwd": True,
        "files": {"README.md": "# r\n"},
        "args": ["start", "--name", "frontend", "--port", "5173"],
    },
    {
        "tool": "run-managed-service", "case": "RS-04", "expect": 0,
        "desc": "status with no state file reports nothing tracked",
        "cwd": True,
        "files": {"README.md": "# r\n"},
        "args": ["status"],
    },
    {
        "tool": "run-managed-service", "case": "RS-05", "expect": 0,
        "desc": "status for a name that is not tracked says so by identifier",
        "cwd": True,
        "files": {".agent-state/services.json": json.dumps(
            {"backend": {"pid": 999999999, "port": 0, "cmd": ["x"], "cwd": "", "started": 1.0}})},
        "args": ["status", "--name", "frontend"],
    },
    {
        "tool": "run-managed-service", "case": "RS-06", "expect": 0,
        "desc": "a recorded pid that is gone is reported and nothing is signalled - a reused pid must not be collateral",
        "cwd": True,
        "files": {".agent-state/services.json": json.dumps(
            {"frontend": {"pid": 999999999, "port": 0, "cmd": ["x"], "cwd": "", "started": 1.0}})},
        "args": ["stop", "--name", "frontend"],
    },
    {
        "tool": "run-managed-service", "case": "RS-07", "expect": 0,
        "desc": "status reports a tracked entry whose port is not set",
        "cwd": True,
        "files": {".agent-state/services.json": json.dumps(
            {"frontend": {"pid": 999999999, "port": 0, "cmd": ["x"], "cwd": "", "started": 1.0}})},
        "args": ["status"],
    },
    {
        "tool": "run-managed-service", "case": "RS-08", "expect": 0,
        "desc": "stop with no name and an empty state file stops nothing",
        "cwd": True,
        "files": {".agent-state/services.json": "{}\n"},
        "args": ["stop"],
    },
    {
        # THE invariant, second half. PID 1 is alive on every POSIX machine and
        # cannot be ours, so the recorded token cannot match. On Windows PID 1
        # does not exist and both twins take the pid-not-alive path instead --
        # different route, same agreement, and neither route kills anything.
        "tool": "run-managed-service", "case": "RS-10", "expect": 2,
        "desc": "THE INVARIANT - a live pid whose start token does not match is refused, not killed",
        "cwd": True,
        "files": {".agent-state/services.json": json.dumps(
            {"frontend": {"pid": 1, "port": 0, "cmd": ["x"], "cwd": "",
                          "started": 1.0, "start_token": "0"}})},
        "args": ["stop", "--name", "frontend"],
    },
    {
        "tool": "run-managed-service", "case": "RS-11", "expect": 0,
        "desc": "a record from before ownership tokens is accepted with the gap stated, not refused",
        "cwd": True,
        "files": {".agent-state/services.json": json.dumps(
            {"frontend": {"pid": 999999999, "port": 0, "cmd": ["x"], "cwd": "",
                          "started": 1.0}})},
        "args": ["stop", "--name", "frontend"],
    },
    {
        "tool": "run-managed-service", "case": "RS-09", "expect": 1,
        "desc": "an unknown subcommand is a tool error, not a validation failure",
        "cwd": True,
        "files": {"README.md": "# r\n"},
        "args": ["restart", "--name", "frontend"],
    },
]




# ---------------------------------------------------------------------------
# Tools that cannot have a meaningful `.ps1` twin, and why.
#
# Reporting these as "not started" was a defect in this tool: it named work that
# nobody can ever finish, so the `remaining` list stopped meaning "what is left"
# and started meaning "what is left, minus the four you have to remember". The
# reason lives here as a string so the next session does not have to ask.
#
# A twin is required because a machine without Python has the `.ps1` as its only
# gate. That premise fails in two distinct ways:
#
#   - the check is a *meta*-tool, not a gate: it does not block a commit and is
#     not on the hook path, so there is no Python-less machine relying on it;
#   - the check's verdict comes from a Python-only library, so a `.ps1` could
#     only reach the verdict by reimplementing that library — and a check that
#     is wrong is worse than a check that is absent, because one false alarm
#     teaches the operator to pass `--no-verify` forever.
#
# Both get a `.ps1` that says Python is required and exits 1. Exiting 0 would
# record an unverified tree as verified, which is the failure this whole
# exercise exists to prevent.
EXCLUDED: dict[str, str] = {
    "check-script-parity":
        "meta-tool - it runs the .py side to compare against, so on a "
        "Python-less machine there is nothing to compare; not on the gate path",
    "check-agent-config":
        "reads .codex/config.toml with tomllib; no TOML parser exists in "
        "PowerShell 5.1 or 7.x and a hand-rolled one would produce false alarms",
    "reference-image-manifest":
        "pixel measurement needs PIL",
    "spa-screen-extractor":
        "screen capture needs Playwright",
    "collect-validation-evidence":
        "wraps a command and propagates its exit code - it reaches no verdict "
        "of its own, so there is no verdict for a twin to agree with",
}


def report_status(tools: Path) -> int:
    """Answer "how far did the port get" by measuring, not by remembering.

    A handoff document goes stale the moment someone edits the tree. This walks
    the tree instead, so the answer is always current.
    """
    rows = []
    for directory in sorted(p for p in tools.iterdir() if p.is_dir()):
        # `_`-prefixed directories are shared library code, not tools, and have
        # no verdict to twin. Same convention as `stacks/_template`.
        if directory.name.startswith("_"):
            continue
        py = locate_py(directory)
        if py is None:
            continue
        has_ps1 = py.with_suffix(".ps1").is_file()
        has_ids = "[" + directory.name + ":" in py.read_text(
            encoding="utf-8", errors="replace")
        cases = sum(1 for case in CASES if case["tool"] == directory.name)
        if directory.name in EXCLUDED:
            state = "n/a"
        elif has_ps1 and cases:
            state = "twinned"
        elif has_ps1:
            state = "twin, no cases"
        elif has_ids:
            state = "identifiers only"
        else:
            state = "not started"
        rows.append((directory.name, state, cases))

    width = max(len(name) for name, _, _ in rows)
    print("Script parity status")
    for name, state, cases in rows:
        if state == "n/a":
            marker = "n/a "
        elif state == "twinned":
            marker = "OK  "
        else:
            marker = "--  "
        count = f"{cases} case(s)" if cases else "-"
        print(f"  {marker}{name:<{width}}  {state:<17} {count}")
        if state == "n/a":
            print(f"      {'':<{width}}  reason: {EXCLUDED[name]}")

    applicable = [row for row in rows if row[1] != "n/a"]
    done = sum(1 for _, state, _ in applicable if state == "twinned")
    print()
    print(f"  twinned {done} / {len(applicable)} applicable tools "
          f"({len(rows) - len(applicable)} n/a), {len(CASES)} case(s) total")
    remaining = [name for name, state, _ in applicable if state != "twinned"]
    print(f"  remaining: {', '.join(remaining) if remaining else 'none'}")
    return 0


def locate_py(directory: Path) -> Path | None:
    """Find a tool's implementation without assuming it is named after its
    directory.

    Two tools already break that assumption -- `enforce-agent-gates` ships
    `enforce_gates.py` and `collect-validation-evidence` ships `collect.py`.
    While `find_pair` assumed the naming, `enforce-agent-gates` reported "no
    .ps1 twin yet" *after the twin was written*, and the harness exited 0. A
    silent skip in the tool that exists to prevent silent skips is the worst
    possible place for one, so the resolution now lives in one function used by
    both the status report and the comparison.
    """
    stem = directory.name.replace("-", "_")
    candidate = directory / f"{stem}.py"
    if candidate.is_file():
        return candidate
    return next((f for f in sorted(directory.glob("*.py"))
                 if f.name != "self_test.py"), None)


def find_pair(tools: Path, tool: str) -> tuple[Path, Path] | None:
    directory = tools / tool
    py = locate_py(directory)
    if py is None:
        raise OSError(
            f"case defined for '{tool}' but no implementation .py was found "
            f"under {directory} - a case that cannot run must not be skipped"
        )
    ps1 = py.with_suffix(".ps1")
    if ps1.is_file():
        return py, ps1
    return None


def build(root: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="")



def to_powershell_args(argv: list[str]) -> list[str]:
    """Translate `--kebab-case` into `-PascalCase`.

    The canonical harness this generalizes solved the same problem by keeping a
    separate argument list per implementation. Translating instead keeps one
    list per case, so the two sides cannot drift apart by editing only one.
    Values are passed through untouched.

    A repeated `--flag value` is argparse's `action="append"` idiom. PowerShell
    refuses the same parameter twice ("specified more than once") and takes a
    comma-separated list instead, so repeats are collapsed. Without this the twin
    died on argument binding and printed no identifiers at all -- which reads as a
    parity mismatch when the actual fault is in this translation.
    """
    out: list[str] = []
    value_slot: dict[str, int] = {}
    index = 0
    while index < len(argv):
        argument = argv[index]
        if not argument.startswith("--"):
            out.append(argument)
            index += 1
            continue

        name = "-" + "".join(part.capitalize()
                             for part in argument[2:].split("-"))
        takes_value = (index + 1 < len(argv)
                       and not argv[index + 1].startswith("--"))
        if takes_value and name in value_slot:
            out[value_slot[name]] += "," + argv[index + 1]
            index += 2
            continue

        out.append(name)
        if takes_value:
            out.append(argv[index + 1])
            value_slot[name] = len(out) - 1
            index += 2
        else:
            index += 1
    return out



def _init_git(root: Path) -> None:
    """Make the fixture a real repository with one commit on `main`.

    Some checks read git rather than the filesystem, and their two
    implementations can disagree on line endings or path separators in git's
    output. A real repository is the only fixture that exercises that.
    """
    env = {"GIT_AUTHOR_NAME": "parity", "GIT_AUTHOR_EMAIL": "parity@example.invalid",
           "GIT_COMMITTER_NAME": "parity", "GIT_COMMITTER_EMAIL": "parity@example.invalid"}
    import os
    environment = {**os.environ, **env}
    for command in (
        ["git", "init", "-q", "-b", "main"],
        ["git", "add", "-A"],
        ["git", "commit", "-q", "-m", "baseline"],
    ):
        subprocess.run(command, cwd=root, env=environment,
                       capture_output=True, text=True, check=False)


def _materialise(case: dict, tools: Path, temporary: Path) -> Path:
    """Build one throwaway copy of a case's tree."""
    fixture = temporary / "tree"
    fixture.mkdir()
    build(fixture, case["files"])
    # A router resolves its sub-checks under `<root>/tools/`, so exercising its
    # routing means the real sub-checks have to be present. Copying them is not
    # the same thing as reading a tool's internals -- the fixture uses them the
    # way the tool under test does, and a refactor inside one of them cannot
    # break this harness.
    copied = case.get("copy_tools", [])
    if copied:
        # Every tool imports the shared CLI helper, so it travels with them. Left
        # out, a copied sub-check dies on `from kit_cli import ...` and the router
        # above it reports a tool error -- a failure manufactured by the fixture,
        # which is the one kind this harness must never produce.
        shutil.copytree(tools / "_lib", fixture / "tools" / "_lib")
    for name in copied:
        shutil.copytree(tools / name, fixture / "tools" / name)
    if case.get("git"):
        _init_git(fixture)
        if case.get("after_git"):
            build(fixture, case["after_git"])
        # A gate that reads the *staged* diff needs files that are added but not
        # committed. `_init_git` commits everything, which leaves an empty index
        # -- and an empty index makes every such gate pass for the wrong reason.
        if case.get("stage"):
            _git_add(fixture)
    return fixture


def _git_add(root: Path) -> None:
    """Stage the working tree without committing it."""
    subprocess.run(["git", "add", "-A"], cwd=root,
                   capture_output=True, text=True, check=False)


def run(command: list[str], cwd: Path | None = None) -> tuple[int, str]:
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def main() -> int:
    parser = ArgumentParser(
        description="Compare .py and .ps1 twins on identical input."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--tool", action="append", default=[],
                        help="restrict to these tool directories; repeatable")
    parser.add_argument("--output", type=Path, help="write a JSON report here")
    parser.add_argument("--status", action="store_true",
                        help="report how far the port got, and stop")
    args = parser.parse_args()

    try:
        root = args.root.resolve()
        tools = root / "tools"
        if not tools.is_dir():
            raise OSError(f"no tools directory under {root}")

        if args.status:
            return report_status(tools)

        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            print(
                "ERROR: no pwsh or powershell on PATH. This check cannot pass "
                "without one — an unverified twin recorded as verified is "
                "worse than one recorded as unverified.",
                file=sys.stderr,
            )
            return 1

        selected = [c for c in CASES if not args.tool or c["tool"] in args.tool]
        print(f"Script parity: {shell}")
        print(f"  root: {root}")

        agree = 0
        mismatches: list[dict] = []
        violations: list[dict] = []
        skipped: list[str] = []
        current = ""

        for case in selected:
            pair = find_pair(tools, case["tool"])
            if pair is None:
                if case["tool"] not in skipped:
                    skipped.append(case["tool"])
                continue
            py, ps1 = pair

            if case["tool"] != current:
                current = case["tool"]
                print(f"\n  -- {current} --")

            # Each implementation gets its own tree. A shared fixture silently
            # breaks any check that *writes* to the tree it inspects: check-last
            # stamps a baseline marker, so the second run to execute would see a
            # freshly-marked tree and legitimately reach a different verdict.
            # That is a disagreement invented by the harness, not found by it.
            with tempfile.TemporaryDirectory() as temporary:
                fixture = _materialise(case, tools, Path(temporary))
                argv = [a.replace("{ROOT}", str(fixture)) for a in case["args"]]
                workdir = fixture if case.get("cwd") else None
                py_code, py_out = run([sys.executable, str(py), *argv], workdir)

            with tempfile.TemporaryDirectory() as temporary:
                fixture = _materialise(case, tools, Path(temporary))
                argv = [a.replace("{ROOT}", str(fixture)) for a in case["args"]]
                workdir = fixture if case.get("cwd") else None
                ps_code, ps_out = run(
                    [shell, "-NoProfile", "-NonInteractive", "-File", str(ps1),
                     *to_powershell_args(argv)], workdir
                )

            left = (py_code, identifiers(py_out))
            right = (ps_code, identifiers(ps_out))

            if left == right:
                agree += 1
                shown = ", ".join(left[1]) if left[1] else "-"
                wanted = case.get("expect")
                if wanted is not None and left[0] != wanted:
                    violations.append({"case": case["case"], "tool": case["tool"],
                                       "expect": wanted, "got": left[0]})
                    print(f"  CONV  {case['case']}  exit {left[0]} but the convention "
                          f"requires {wanted}  {case['desc']}")
                    print(f"          both twins agree and both are wrong — "
                          f"agreement alone would have hidden this")
                else:
                    print(f"  OK    {case['case']}  exit {left[0]}  {shown}  {case['desc']}")
            else:
                mismatches.append({"case": case["case"], "tool": case["tool"],
                                   "py": {"exit": left[0], "ids": left[1]},
                                   "ps1": {"exit": right[0], "ids": right[1]}})
                print(f"  FAIL  {case['case']}  {case['desc']}")
                print(f"          .py  exit {left[0]}  {left[1]}")
                print(f"          .ps1 exit {right[0]}  {right[1]}")
                tail = ps_out.strip().splitlines()[-3:]
                for line in tail:
                    print(f"          ps1: {line[:150]}")

        print()
        if skipped:
            print(f"  no .ps1 twin yet: {', '.join(sorted(skipped))}")

        total = agree + len(mismatches)
        print("=" * 60)
        print(f"  verdict parity   : {agree} agree - {len(mismatches)} mismatched "
              f"({total} case(s))")
        print(f"  exit convention  : {len(violations)} violation(s)")
        print("=" * 60)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps({"schema": "evidence-first/script-parity/v1",
                            "shell": shell, "agree": agree,
                            "mismatches": mismatches,
                            "convention_violations": violations,
                            "no_twin": sorted(skipped)},
                           ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        return 2 if (mismatches or violations) else 0
    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
