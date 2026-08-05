# SPDX-License-Identifier: MPL-2.0
"""Shared command-line plumbing, so every tool exits the same way for the same
kind of failure.

## Why this exists

This kit's exit-code convention is:

    0  pass
    2  validation failure — the tool looked and found something wrong
    1  tool error — the tool could not reach a verdict at all

`argparse` predates that convention and disagrees with it: `ArgumentParser.error`
calls `sys.exit(2)`. Every tool here therefore exited **2** for a *typo on the
command line*, which under this kit's own convention is indistinguishable from a
real finding. Verified across the tools before changing anything; it is
argparse's default, so it was kit-wide rather than anybody's mistake.

That matters because a runner cannot tell the two apart. The same conflation, in
the other direction, is on record as having blocked correct commits: a check whose
"nothing to check here" and "this is forged" both left as non-zero, with the
runner branching on only one of them.

Remapping here rather than renumbering the convention: `2` for a usage error is
natural for argparse and for POSIX, but this kit already publishes `2` as
"validation failure" in `docs/core/*`, `enforcement-matrix.md`, every tool
docstring and every harness `expect`. Changing the convention costs more than
changing argparse, and a convention that has to be re-explained is a convention
that gets misread.

A side effect worth having: PowerShell exits **1** when parameter binding fails,
so this also brings the `.py` and `.ps1` twins into agreement on a usage error,
which they were not in before.
"""

from __future__ import annotations

import argparse
import sys

# The kit's convention, in one place, for tools that want to name it rather than
# write a bare integer.
EXIT_PASS = 0
EXIT_TOOL_ERROR = 1
EXIT_VALIDATION_FAILURE = 2


class ArgumentParser(argparse.ArgumentParser):
    """`argparse.ArgumentParser` that exits 1, not 2, on a usage error.

    Drop-in: tools import this name instead of `argparse.ArgumentParser` and
    change nothing else.
    """

    def error(self, message: str) -> "None":  # type: ignore[override]
        self.print_usage(sys.stderr)
        # Deliberately **no** `[tool:finding-id]` identifier. Two reasons, and the
        # second one is the binding constraint.
        #
        # A usage error is not a finding about the tree, so putting it in the
        # finding namespace would give `enforcement-matrix.md` a verdict with no
        # rule behind it.
        #
        # And PowerShell rejects an unknown parameter in its own binder, before a
        # line of script runs. There is no hook to make a twin print an
        # identifier there. An identifier on this side only would make the twins
        # disagree on every usage-error case — a divergence invented to decorate
        # an error message.
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        raise SystemExit(EXIT_TOOL_ERROR)


def bootstrap() -> None:
    """No-op kept so importers have something to call if a future version needs
    setup. Present so the import line never has to change again."""
    return None
