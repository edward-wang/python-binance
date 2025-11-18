#!/usr/bin/env python3
"""
Pipeline utilities for scanning Binance API Markdown stubs, downloading
official HTML docs, extracting structured parameter data, and rendering
Markdown snippets.

Usage examples:

  python scripts/api_doc_pipeline.py scan --root api_index
  python scripts/api_doc_pipeline.py fetch --input data/doc_pipeline/missing_sections.json
  python scripts/api_doc_pipeline.py parse --manifest data/doc_pipeline/html_manifest.json
  python scripts/api_doc_pipeline.py render --parsed data/doc_pipeline/parsed_sections.json
  python scripts/api_doc_pipeline.py qa --parsed data/doc_pipeline/parsed_sections.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
import ssl

try:
    import requests
except Exception:  # pragma: no cover - dependency/env check
    requests = None  # type: ignore

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover - dependency/env check
    BeautifulSoup = None  # type: ignore


MISSING_FIELDS = ("core_params", "common_values", "returns")
DEFAULT_DATA_DIR = Path("data/doc_pipeline")
PLACEHOLDER_HINTS = (
    "未提供",
    "未说明",
    "暂无",
    "详见官方文档",
    "参见官方",
    "API response",
    "API 响应",
    "源码注释",
)


@dataclass
class SectionBlock:
    file_path: Path
    heading: str
    start_line: int
    content: List[Tuple[int, str]]
    official_url: Optional[str]

    @property
    def block_text(self) -> str:
        lines = [line for _, line in self.content]
        return "\n".join(lines).strip()

    @property
    def section_id(self) -> str:
        raw = f"{self.file_path}::{self.heading}"
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def find_sections(markdown_text: str, file_path: Path) -> Iterable[SectionBlock]:
    lines = markdown_text.splitlines()
    heading = None
    start_line = 0
    buffer: List[Tuple[int, str]] = []

    def flush():
        nonlocal heading, buffer, start_line
        if heading is None:
            return
        block = SectionBlock(
            file_path=file_path,
            heading=heading,
            start_line=start_line,
            content=buffer.copy(),
            official_url=extract_official_url(buffer),
        )
        yield block
        heading = None
        buffer = []

    for idx, line in enumerate(lines, start=1):
        if line.startswith("### "):
            yield from flush()
            heading = line[4:].strip()
            start_line = idx
        else:
            if heading is not None:
                buffer.append((idx, line))
    yield from flush()


def extract_official_url(buffer: Sequence[Tuple[int, str]]) -> Optional[str]:
    pattern = re.compile(r"\[官方文档\]\(([^)]+)\)")
    for _, line in buffer:
        match = pattern.search(line)
        if match:
            return match.group(1)
    return None


def has_filled_section(buffer: Sequence[Tuple[int, str]], marker: str) -> bool:
    marker_line_idx = None
    for idx, (_, line) in enumerate(buffer):
        if line.strip().startswith(marker):
            marker_line_idx = idx
            break
    if marker_line_idx is None:
        return False
    for _, line in buffer[marker_line_idx + 1 :]:
        stripped = line.strip()
        if stripped.startswith("**") and stripped.endswith("**"):
            return False
        if stripped.startswith("-"):
            bullet = stripped.lstrip("-").strip()
            if is_placeholder_line(bullet):
                continue
            return bool(bullet)
        if stripped and not stripped.startswith(">"):
            return False
    return False


def is_placeholder_line(text: str) -> bool:
    normalized = text.replace("（", "(").replace("）", ")")
    for hint in PLACEHOLDER_HINTS:
        if hint in normalized:
            return True
    return False


def run_scan(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    if not root.is_dir():
        raise SystemExit(f"Markdown root not found: {root}")

    missing_sections: List[Dict[str, object]] = []
    for md_file in sorted(root.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for block in find_sections(text, md_file):
            missing: List[str] = []
            if not has_filled_section(block.content, "**核心参数**"):
                missing.append("core_params")
            if not has_filled_section(block.content, "**常用值**"):
                missing.append("common_values")
            if not has_filled_section(block.content, "**返回**"):
                missing.append("returns")
            if missing and block.official_url:
                missing_sections.append(
                    {
                        "id": block.section_id,
                        "file": str(block.file_path),
                        "heading": block.heading,
                        "start_line": block.start_line,
                        "official_url": block.official_url,
                        "missing_fields": missing,
                    }
                )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        json.dump(missing_sections, fh, ensure_ascii=False, indent=2)
    print(f"Detected {len(missing_sections)} incomplete sections. Saved to {output}")


def run_fetch(args: argparse.Namespace) -> None:
    input_path = Path(args.input).resolve()
    cache_dir = Path(args.cache_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    records = json.loads(input_path.read_text(encoding="utf-8"))

    if isinstance(records, dict):
        records = records.get("sections", [])

    manifest = load_manifest(manifest_path)
    cache_dir.mkdir(parents=True, exist_ok=True)
    extra_headers = load_headers_file(getattr(args, "headers_file", None))
    verify_path = getattr(args, "ca_cert", None)
    delay_seconds = max(0.0, getattr(args, "delay", 0.0))
    fetched_count = 0

    for item in records:
        section_id = item["id"]
        url = item.get("official_url")
        manifest_entry = manifest.get(section_id, {})
        if manifest_entry.get("status") == "ok":
            continue
        if not url:
            manifest[section_id] = build_manifest_entry(item, status="no_url", error="Missing official_url")
            continue

        if delay_seconds and fetched_count:
            time.sleep(delay_seconds)
        print(f"Fetching {url} ...")
        try:
            html_text = download_url(url, headers=extra_headers, verify=verify_path)
        except Exception as exc:  # pragma: no cover - network dependent
            manifest[section_id] = build_manifest_entry(item, status="error", error=str(exc))
            continue

        html_name = f"{hashlib.sha1(url.encode('utf-8')).hexdigest()}.html"
        html_path = cache_dir / html_name
        html_path.write_text(html_text, encoding="utf-8")
        fetched_count += 1

        manifest[section_id] = build_manifest_entry(
            item,
            status="ok",
            html_file=str(html_path),
            fetched_at=time.time(),
        )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated manifest at {manifest_path}")


def load_manifest(path: Path) -> Dict[str, Dict[str, object]]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def build_manifest_entry(item: Dict[str, object], **extra: object) -> Dict[str, object]:
    entry = {
        "id": item["id"],
        "file": item["file"],
        "heading": item["heading"],
        "official_url": item.get("official_url"),
    }
    entry.update(extra)
    return entry


def run_parse(args: argparse.Namespace) -> None:
    if BeautifulSoup is None:  # pragma: no cover - dependency check
        raise SystemExit("beautifulsoup4 is required for parse stage. Please install it first.")

    manifest_path = Path(args.manifest).resolve()
    output_path = Path(args.output).resolve()
    manifest = load_manifest(manifest_path)
    parsed_entries: List[Dict[str, object]] = []

    for section_id, entry in manifest.items():
        if entry.get("status") != "ok":
            continue
        html_file = entry.get("html_file")
        if not html_file:
            continue
        html_path = Path(html_file)
        if not html_path.is_file():
            continue

        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        params, responses = extract_tables(soup)
        parsed_entries.append(
            {
                "id": section_id,
                "file": entry.get("file"),
                "heading": entry.get("heading"),
                "official_url": entry.get("official_url"),
                "params": params,
                "responses": responses,
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump({"entries": parsed_entries}, fh, ensure_ascii=False, indent=2)
    print(f"Parsed {len(parsed_entries)} sections → {output_path}")


def extract_tables(soup) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    params: List[Dict[str, str]] = []
    responses: List[Dict[str, str]] = []
    for table in soup.find_all("table"):
        headers = [normalize_text(th.get_text()) for th in table.find_all("th")]
        if not headers:
            continue
        classification = classify_table(headers, table)
        if classification is None:
            continue
        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = [normalize_text(td.get_text(" ")) for td in tr.find_all(["td", "th"])]
            if not cells:
                continue
            row = {}
            for idx, header in enumerate(headers):
                key = normalize_column_name(header)
                value = cells[idx] if idx < len(cells) else ""
                row[key] = value
            rows.append(row)
        if classification == "params":
            params.extend(rows)
        elif classification == "responses":
            responses.extend(rows)
    return params, responses


HEADER_ALIASES = {
    "name": ["parameter", "name", "param", "字段", "field"],
    "type": ["type", "数据类型"],
    "required": ["required", "mandatory", "是否必填"],
    "description": ["description", "desc", "说明", "描述"],
    "example": ["example", "示例", "样例"],
    "min": ["min", "minimum"],
    "max": ["max", "maximum"],
}


def classify_table(headers: Sequence[str], table) -> Optional[str]:
    header_blob = " ".join(headers).lower()
    if any(token in header_blob for token in ("response", "返回", "output")):
        return "responses"
    if any(token in header_blob for token in ("parameter", "param", "参数", "field")):
        return "params"
    previous = table.find_previous(["h2", "h3", "h4"])
    if previous:
        text = previous.get_text(strip=True).lower()
        if "response" in text or "返回" in text:
            return "responses"
        if "parameter" in text or "参数" in text or "request" in text:
            return "params"
    return None


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_column_name(header: str) -> str:
    header_lower = header.lower()
    for normalized, keywords in HEADER_ALIASES.items():
        if any(keyword in header_lower for keyword in keywords):
            return normalized
    return header_lower.replace(" ", "_")


def download_url(url: str, headers: Optional[Dict[str, str]] = None, verify: Optional[str] = None) -> str:
    if requests is not None:
        verify_option = verify if verify is not None else True
        resp = requests.get(url, timeout=15, headers=headers, verify=verify_option)
        resp.raise_for_status()
        return resp.text
    try:
        req = urllib_request.Request(url, headers=headers or {})
        context = ssl.create_default_context()
        if verify:
            context.load_verify_locations(cafile=verify)
        with urllib_request.urlopen(req, timeout=15, context=context) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            data = response.read()
            return data.decode(charset, errors="replace")
    except (HTTPError, URLError) as exc:  # pragma: no cover - network dependent
        raise RuntimeError(str(exc)) from exc


def load_headers_file(path_str: Optional[str]) -> Dict[str, str]:
    if not path_str:
        return {}
    path = Path(path_str)
    if not path.is_file():
        raise SystemExit(f"Headers file not found: {path}")
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {str(k): str(v) for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass
    headers: Dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def run_render(args: argparse.Namespace) -> None:
    parsed_path = Path(args.parsed).resolve()
    output_path = Path(args.output).resolve()
    parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    entries = parsed.get("entries", [])
    rendered: List[Dict[str, object]] = []
    for entry in entries:
        params_md = build_markdown_list(entry.get("params", []), is_param=True)
        responses_md = build_markdown_list(entry.get("responses", []), is_param=False)
        rendered.append(
            {
                "id": entry["id"],
                "file": entry.get("file"),
                "heading": entry.get("heading"),
                "official_url": entry.get("official_url"),
                "markdown": "\n".join(
                    [
                        "**核心参数**:",
                        params_md,
                        "",
                        "**常用值**:",
                        "- 官方未提供固定枚举值",
                        "",
                        "**返回**:",
                        responses_md,
                    ]
                ).strip(),
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump({"entries": rendered}, fh, ensure_ascii=False, indent=2)
    print(f"Rendered {len(rendered)} snippets → {output_path}")


def build_markdown_list(rows: Sequence[Dict[str, str]], is_param: bool) -> str:
    if not rows:
        return "- 官方未说明"
    lines = []
    for row in rows:
        name = row.get("name") or row.get("parameter") or row.get("字段") or "未命名字段"
        desc = row.get("description") or row.get("说明") or row.get("desc") or "官方未说明"
        extras = []
        if row.get("type"):
            extras.append(f"类型 {row['type']}")
        if row.get("required"):
            extras.append(f"必填 {row['required']}")
        if row.get("example"):
            extras.append(f"示例 {row['example']}")
        for field in ("min", "max"):
            if row.get(field):
                extras.append(f"{field.upper()} {row[field]}")
        extra_text = f"（{'；'.join(extras)}）" if extras else ""
        lines.append(f"- `{name}`：{desc}{extra_text}")
    return "\n".join(lines)


def run_qa(args: argparse.Namespace) -> None:
    parsed_path = Path(args.parsed).resolve()
    output_path = Path(args.output).resolve()
    parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    entries = parsed.get("entries", [])
    stats = {
        "total_entries": len(entries),
        "with_params": sum(1 for e in entries if e.get("params")),
        "with_responses": sum(1 for e in entries if e.get("responses")),
        "generated_at": time.time(),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"QA summary → {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="API documentation harvesting pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="scan Markdown files for missing sections")
    scan.add_argument("--root", default="api_index", help="Directory containing Markdown files")
    scan.add_argument(
        "--output",
        default=DEFAULT_DATA_DIR / "missing_sections.json",
        help="Output JSON file for missing sections",
    )
    scan.set_defaults(func=run_scan)

    fetch = sub.add_parser("fetch", help="download official HTML docs")
    fetch.add_argument("--input", default=DEFAULT_DATA_DIR / "missing_sections.json")
    fetch.add_argument("--cache-dir", default=DEFAULT_DATA_DIR / "html_cache")
    fetch.add_argument("--manifest", default=DEFAULT_DATA_DIR / "html_manifest.json")
    fetch.add_argument("--headers-file", help="Path to JSON/txt containing extra HTTP headers")
    fetch.add_argument("--ca-cert", help="Custom CA bundle for HTTPS verification")
    fetch.add_argument("--delay", type=float, default=0.0, help="Delay (seconds) between requests")
    fetch.set_defaults(func=run_fetch)

    parse = sub.add_parser("parse", help="parse cached HTML into structured data")
    parse.add_argument("--manifest", default=DEFAULT_DATA_DIR / "html_manifest.json")
    parse.add_argument("--output", default=DEFAULT_DATA_DIR / "parsed_sections.json")
    parse.set_defaults(func=run_parse)

    render = sub.add_parser("render", help="render Markdown snippets from parsed data")
    render.add_argument("--parsed", default=DEFAULT_DATA_DIR / "parsed_sections.json")
    render.add_argument("--output", default=DEFAULT_DATA_DIR / "rendered_snippets.json")
    render.set_defaults(func=run_render)

    qa = sub.add_parser("qa", help="produce QA summary for parsed data")
    qa.add_argument("--parsed", default=DEFAULT_DATA_DIR / "parsed_sections.json")
    qa.add_argument("--output", default=DEFAULT_DATA_DIR / "qa_report.json")
    qa.set_defaults(func=run_qa)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()

