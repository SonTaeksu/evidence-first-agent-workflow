# SPDX-License-Identifier: MPL-2.0
"""Self-test for the designer-tree extractor and the specification check.

Half the fixtures assert that something is removed; the other half assert that
something is kept. The keep cases matter more: a comment stripper that eats a
string literal breaks correct code, which is the failure mode that kills a gate.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "extract_designer_tree.py"
CHECK = HERE / "check_designer_spec.py"
SKELETON = HERE.parent / "skeletons" / "MinimalApp" / "MainForm.Designer.cs"

sys.path.insert(0, str(HERE))
from extract_designer_tree import extract, strip_comments  # noqa: E402

FIXTURE = '''
namespace Fixture
{
    partial class SampleForm
    {
        private void InitializeComponent()
        {
            this.panelMain = new System.Windows.Forms.Panel();
            this.btnSave = new System.Windows.Forms.Button();
            this.grpEmpty = new System.Windows.Forms.GroupBox();
            // this.btnGhost = new System.Windows.Forms.Button();
            /* this.btnAlsoGhost = new System.Windows.Forms.Button(); */
            this.panelMain.Controls.Add(this.btnSave);
            this.Controls.Add(this.panelMain);
            this.Controls.Add(this.grpEmpty);
            this.btnSave.Text = "Save";
            this.btnSave.Tag = "https://example.invalid/a//b";
            this.ClientSize = new System.Drawing.Size(300, 200);
            this.Name = "SampleForm";
        }

        private System.Windows.Forms.Panel panelMain;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.GroupBox grpEmpty;
        private System.Windows.Forms.Button btnGhost;
        private System.Windows.Forms.Button btnAlsoGhost;
    }
}
'''


def run(command: list[str]) -> int:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode


def check(label: str, condition: bool, failures: list[str]) -> None:
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    tree = extract(FIXTURE, "fixture")
    names = {control["name"] for control in tree["controls"]}
    by_name = {control["name"]: control for control in tree["controls"]}

    check("form name is read", tree["form"] == "SampleForm", failures)
    check("real control is found", "btnSave" in names, failures)
    check("line-commented control is removed", "btnGhost" not in names, failures)
    check(
        "block-commented control is removed",
        "btnAlsoGhost" not in names,
        failures,
    )
    check(
        "double slash inside a string literal is kept",
        "//b" in strip_comments(FIXTURE),
        failures,
    )
    check(
        "comment removal preserves length and line count",
        len(strip_comments(FIXTURE)) == len(FIXTURE)
        and strip_comments(FIXTURE).count("\n") == FIXTURE.count("\n"),
        failures,
    )
    check(
        "nesting is recorded",
        by_name["btnSave"]["parent"] == "panelMain",
        failures,
    )
    check(
        "root parent is the form",
        by_name["panelMain"]["parent"] == "SampleForm",
        failures,
    )
    check(
        "empty container is detectable",
        by_name["grpEmpty"]["is_container"]
        and by_name["grpEmpty"]["child_count"] == 0,
        failures,
    )
    check(
        "form property assignment is not a control",
        "ClientSize" not in names,
        failures,
    )

    with tempfile.TemporaryDirectory() as temporary:
        work = Path(temporary)
        designer = work / "SampleForm.Designer.cs"
        designer.write_text(FIXTURE, encoding="utf-8")
        tree_path = work / "tree.json"

        code = run(
            [
                sys.executable,
                str(EXTRACT),
                "--designer",
                str(designer),
                "--output",
                str(tree_path),
            ]
        )
        check("extractor exits 0 on a valid designer file", code == 0, failures)

        good = work / "good.json"
        good.write_text(
            json.dumps(
                {
                    "form": "SampleForm",
                    "required_controls": [
                        {"name": "btnSave", "type": "Button", "parent": "panelMain"}
                    ],
                }
            ),
            encoding="utf-8",
        )
        code = run(
            [sys.executable, str(CHECK), "--tree", str(tree_path), "--spec", str(good)]
        )
        check("satisfied specification exits 0", code == 0, failures)

        bad = work / "bad.json"
        bad.write_text(
            json.dumps(
                {
                    "form": "SampleForm",
                    "required_controls": [{"name": "btnMissing", "type": "Button"}],
                }
            ),
            encoding="utf-8",
        )
        code = run(
            [sys.executable, str(CHECK), "--tree", str(tree_path), "--spec", str(bad)]
        )
        check("missing required control exits 2", code == 2, failures)

        if SKELETON.is_file():
            real = extract(SKELETON.read_text(encoding="utf-8-sig"), "skeleton")
            real_names = {control["name"] for control in real["controls"]}
            check(
                "shipped skeleton parses to its five controls",
                real["form"] == "MainForm"
                and real_names
                == {"panelInput", "lblName", "txtName", "btnGreet", "lblStatus"},
                failures,
            )

    print(f"self-test failures: {len(failures)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
