# SPDX-License-Identifier: MPL-2.0
"""Self-test rendered-DOM extraction and completeness comparison."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


RENDERED_HTML = """<!doctype html>
<html>
<body>
  <div id="total-users" class="kpi-card">
    <span>Total users</span><strong>2</strong>
  </div>
  <div id="trend-chart" class="chart"><canvas></canvas></div>
  <section id="search-panel">
    <label>Name <input id="name" name="name" /></label>
    <select id="status" name="status"><option>Active</option></select>
    <button>Search</button>
  </section>
  <table id="users-grid">
    <thead><tr><th>Name</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>Alice</td><td>Active</td></tr>
      <tr><td>Bob</td><td>Disabled</td></tr>
    </tbody>
  </table>
  <button>Create</button>
</body>
</html>
"""


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        rendered = folder / "rendered.html"
        reference = folder / "reference.json"
        implementation = folder / "implementation.json"
        report = folder / "report.json"

        rendered.write_text(RENDERED_HTML, encoding="utf-8")

        extraction = run(
            str(ROOT / "extract_spa.py"),
            "--from-file",
            str(rendered),
            "--json",
            str(reference),
            "--out",
            str(folder / "spec.md"),
            "--language",
            "en",
        )
        if extraction.returncode != 0:
            print(extraction.stdout)
            print(extraction.stderr, file=sys.stderr)
            return 1

        payload = json.loads(reference.read_text(encoding="utf-8"))
        assert payload["schema"] == "evidence-first/rendered-screen-spec/v1"
        assert payload["source"]["source_file_sha256"]
        assert len(payload["grids"]) == 1
        assert payload["grids"][0]["columns"] == ["Name", "Status"]
        assert len(payload["grids"][0]["sample_rows"]) == 2
        assert "Search" in payload["buttons"]
        assert "Create" in payload["buttons"]
        assert len(payload["visual_blocks"]) == 2
        assert all(
            not block["is_empty"]
            for block in payload["visual_blocks"]
        )

        implementation.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )
        passing = run(
            str(ROOT / "check_screen_spec.py"),
            "--reference",
            str(reference),
            "--implementation",
            str(implementation),
            "--require-rows",
            "--strict-controls",
            "--strict-visual-blocks",
            "--reject-empty-visual-blocks",
            "--output",
            str(report),
        )
        assert passing.returncode == 0, passing.stderr
        assert json.loads(report.read_text(encoding="utf-8"))["status"] == "PASS"

        broken = json.loads(implementation.read_text(encoding="utf-8"))
        broken["grids"][0]["columns"] = ["Name"]
        implementation.write_text(
            json.dumps(broken),
            encoding="utf-8",
        )
        failing = run(
            str(ROOT / "check_screen_spec.py"),
            "--reference",
            str(reference),
            "--implementation",
            str(implementation),
            "--require-rows",
        )
        assert failing.returncode == 2

        empty_visual = json.loads(reference.read_text(encoding="utf-8"))
        empty_visual["visual_blocks"][0]["is_empty"] = True
        implementation.write_text(
            json.dumps(empty_visual),
            encoding="utf-8",
        )
        visual_failing = run(
            str(ROOT / "check_screen_spec.py"),
            "--reference",
            str(reference),
            "--implementation",
            str(implementation),
            "--strict-visual-blocks",
            "--reject-empty-visual-blocks",
        )
        assert visual_failing.returncode == 2

        print("SPA screen extraction self-test passed.")
        print("Grid mismatch behavior passed with exit code 2.")
        print("Empty visual-block behavior passed with exit code 2.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
