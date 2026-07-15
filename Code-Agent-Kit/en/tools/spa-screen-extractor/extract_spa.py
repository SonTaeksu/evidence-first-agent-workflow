# SPDX-License-Identifier: MPL-2.0
"""Evidence-first wrapper around the Code Agent Kit rendered-DOM extractor."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

import extract_screen as engine


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def source_metadata(target: str, mode: str) -> dict[str, Any]:
    source = {
        "mode": mode,
        "target": target,
    }

    path = Path(target)
    if path.exists() and path.is_file():
        source.update(
            {
                "filename": path.name,
                "bytes": path.stat().st_size,
                "source_file_sha256": sha256_file(path),
            }
        )
    return source


def spec_payload(
    spec: dict[str, Any],
    *,
    target: str,
    mode: str,
    rendered_html: str,
    wait_ms: int,
) -> dict[str, Any]:
    return {
        "schema": "evidence-first/rendered-screen-spec/v1",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": source_metadata(target, mode),
        "rendering": {
            "wait_ms": wait_ms,
            "rendered_dom_characters": len(rendered_html),
            "rendered_dom_sha256": sha256_text(rendered_html),
        },
        **spec,
    }


def markdown(spec: dict[str, Any], language: str) -> str:
    grids = spec.get("grids", [])
    forms = spec.get("forms", [])
    buttons = spec.get("buttons", [])
    visual_blocks = spec.get("visual_blocks", [])

    if language == "ko":
        lines = [
            "# 화면 스펙 — 렌더된 DOM 추출",
            "",
            f"- 블록 요약: 그리드 {len(grids)} · 입력영역 {len(forms)} · 버튼 {len(buttons)} · 시각블록 {len(visual_blocks)}",
            "",
        ]
        grid_heading = "## 그리드"
        form_heading = "## 입력·검색 영역"
        button_heading = "## 버튼·탭"
        visual_heading = "## 시각 블록"
        no_header = "⟨헤더 미검출 — 확인 필요⟩"
        footer = (
            "> 이 스펙을 worklog에 고정한 뒤 원본 SPA를 반복해서 "
            "모델 컨텍스트에 넣지 않습니다."
        )
    else:
        lines = [
            "# Screen Specification — Extracted from Rendered DOM",
            "",
            f"- Summary: {len(grids)} grids · {len(forms)} input areas · {len(buttons)} buttons · {len(visual_blocks)} visual blocks",
            "",
        ]
        grid_heading = "## Grids"
        form_heading = "## Input and Search Areas"
        button_heading = "## Buttons and Tabs"
        visual_heading = "## Visual Blocks"
        no_header = "⟨header not detected — review required⟩"
        footer = (
            "> Store this specification in the worklog. Do not repeatedly "
            "send the complete SPA source to the model."
        )

    if grids:
        lines.append(grid_heading)
        for index, grid in enumerate(grids, 1):
            columns = grid.get("columns", [])
            rows = grid.get("sample_rows", grid.get("rows", []))
            estimate = grid.get("row_estimate", grid.get("est", len(rows)))
            lines.extend(
                [
                    "",
                    f"### {index}. `{grid.get('id', 'grid')}` — approximately {estimate} rows",
                    f"- Columns ({len(columns)}): "
                    + (", ".join(columns) if columns else no_header),
                ]
            )
            if rows:
                lines.append("- Sample rows:")
                for row in rows:
                    lines.append(
                        "  - "
                        + json.dumps(row, ensure_ascii=False)
                    )

    if forms:
        lines.extend(["", form_heading])
        for index, form in enumerate(forms, 1):
            lines.append(
                f"- {index}. `{form.get('id', 'form')}`: "
                + ", ".join(form.get("controls", []))
            )

    if buttons:
        lines.extend(["", button_heading, "- " + ", ".join(buttons)])

    if visual_blocks:
        lines.extend(["", visual_heading])
        for index, block in enumerate(visual_blocks, 1):
            state = "EMPTY" if block.get("is_empty") else "filled"
            lines.append(
                f"- {index}. `{block.get('id', 'block')}` "
                f"type={block.get('type')} state={state} "
                f"text={block.get('has_text')} value={block.get('has_value')} "
                f"media={block.get('has_media')}"
            )

    lines.extend(["", footer])
    return "\n".join(lines)


def markdown_pages(payload: dict[str, Any], language: str) -> str:
    pages = payload["pages"]
    title = (
        "# 다중 페이지 화면 스펙"
        if language == "ko"
        else "# Multi-page Screen Specification"
    )
    lines = [title, "", f"- Pages: {len(pages)}", ""]
    for page in pages:
        lines.extend(
            [
                "---",
                "",
                f"## `{page['page']}`",
                "",
                markdown(page, language),
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--from-file")
    mode.add_argument("--browser")
    mode.add_argument("--render")
    mode.add_argument("--crawl")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--browser-bin")
    parser.add_argument("--wait", type=int, default=1500)
    parser.add_argument("--rows", type=int, default=5)
    parser.add_argument("--json")
    parser.add_argument("--out")
    parser.add_argument("--save-dom")
    parser.add_argument("--language", choices=("en", "ko"), default="en")
    args = parser.parse_args()

    try:
        if args.crawl:
            pages = engine.crawl(
                args.crawl,
                args.wait,
                args.depth,
                args.max_pages,
                args.browser_bin,
                args.rows,
            )
            if not pages:
                raise RuntimeError("Crawl produced no pages.")

            payload = {
                "schema": "evidence-first/rendered-screen-spec-crawl/v1",
                "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "source": source_metadata(args.crawl, "crawl"),
                "rendering": {
                    "wait_ms": args.wait,
                    "depth": args.depth,
                    "max_pages": args.max_pages,
                },
                "pages": [
                    {"page": page, **spec}
                    for page, spec in pages
                ],
            }
            output_markdown = markdown_pages(payload, args.language)
        else:
            if args.from_file:
                mode_name = "rendered-dom-file"
                target = args.from_file
                rendered_html = Path(args.from_file).read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            elif args.browser:
                mode_name = "installed-browser"
                target = args.browser
                rendered_html = engine.render_with_browser(
                    args.browser,
                    args.wait,
                    args.browser_bin,
                )
            else:
                mode_name = "playwright-or-browser"
                target = args.render
                rendered_html = engine.render_with_playwright(
                    args.render,
                    args.wait,
                )

            if args.save_dom:
                dom_path = Path(args.save_dom)
                dom_path.parent.mkdir(parents=True, exist_ok=True)
                dom_path.write_text(rendered_html, encoding="utf-8")

            spec = engine.build_spec(rendered_html, args.rows)
            payload = spec_payload(
                spec,
                target=target,
                mode=mode_name,
                rendered_html=rendered_html,
                wait_ms=args.wait,
            )
            output_markdown = markdown(payload, args.language)

        if args.json:
            json_path = Path(args.json)
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        if args.out:
            output_path = Path(args.out)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output_markdown + "\n", encoding="utf-8")
            print(f"Screen specification: {output_path}")
        else:
            print(output_markdown)

        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
