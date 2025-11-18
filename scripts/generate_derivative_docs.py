#!/usr/bin/env python3
from __future__ import annotations

import ast
import inspect
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
CLIENT_PATH = ROOT / "binance" / "client.py"
ASYNC_PATH = ROOT / "binance" / "async_client.py"

CATEGORY_FILES = {
    "portfolio": ROOT / "api_index" / "derivative-portfolio-margin.md",
    "um": ROOT / "api_index" / "derivative-um-futures.md",
    "cm": ROOT / "api_index" / "derivative-cm-futures.md",
    "margin": ROOT / "api_index" / "margin-trading.md",
}

SUMMARY_PREFIX = "说明："
DOC_HOST = "https://developers.binance.com"

@dataclass
class FunctionInfo:
    name: str
    start_line: int
    end_line: int
    source: str
    docstring: Optional[str]


@dataclass
class ParamDetails:
    desc: str = ""
    type_hint: str = ""
    required: Optional[bool] = None


def load_class_functions(file_path: Path, class_name: str) -> Dict[str, FunctionInfo]:
    text = file_path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    lines = text.splitlines()
    functions: Dict[str, FunctionInfo] = {}

    class ClassVisitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            if node.name != class_name:
                return
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    start = item.lineno
                    end = getattr(item, "end_lineno", item.lineno)
                    snippet = "\n".join(lines[start - 1 : end])
                    doc = ast.get_docstring(item)
                    functions[item.name] = FunctionInfo(
                        name=item.name,
                        start_line=start,
                        end_line=end,
                        source=snippet,
                        docstring=doc,
                    )

    ClassVisitor().visit(tree)
    return functions


def determine_category(name: str, source: str) -> Optional[str]:
    if name.startswith("papi_"):
        return "portfolio"
    if name.startswith("futures_coin_"):
        return "cm"
    if name.startswith("futures_"):
        return "um"
    if name.startswith("margin_") or "_margin_" in name or "_request_margin_api" in source:
        return "margin"
    return None


def format_signature(source: str) -> str:
    first_line = source.strip().splitlines()[0]
    header = first_line.strip()
    if header.endswith(":"):
        header = header[:-1]
    header = header.replace("def ", "").strip()
    if "(" not in header:
        return header
    name, rest = header.split("(", 1)
    params = rest.rsplit(")", 1)[0]
    items = [item.strip() for item in params.split(",") if item.strip()]
    if items and items[0] == "self":
        items = items[1:]
    signature = f"{name}({', '.join(items)})" if items else f"{name}()"
    return signature


def parse_docstring(docstring: Optional[str]) -> Dict:
    if not docstring:
        return {
            "summary": "",
            "link": "",
            "params": [],
            "returns": "",
            "notes": [],
        }

    cleaned = inspect.cleandoc(docstring)
    lines = cleaned.splitlines()

    summary = ""
    link = ""
    params_order: List[str] = []
    params: Dict[str, ParamDetails] = {}
    returns_lines: List[str] = []
    capture_returns = False

    param_pattern = re.compile(r"^:param\s+([^:]+):\s*(.*)$")
    type_pattern = re.compile(r"^:type\s+([^:]+):\s*(.*)$")

    for raw_line in lines:
        line = raw_line.strip()
        if not summary and line and not line.startswith(":"):
            summary = line
        if not link and DOC_HOST in line:
            link = line

        param_match = param_pattern.match(line)
        if param_match:
            name = param_match.group(1).strip()
            desc = param_match.group(2).strip()
            if name not in params:
                params[name] = ParamDetails()
                params_order.append(name)
            if desc:
                existing = params[name].desc.strip()
                params[name].desc = (existing + " " + desc).strip() if existing else desc
                lowered = desc.lower()
                if "required" in lowered:
                    params[name].required = True
                elif "optional" in lowered:
                    params[name].required = False
            capture_returns = False
            continue

        type_match = type_pattern.match(line)
        if type_match:
            name = type_match.group(1).strip()
            desc = type_match.group(2).strip()
            if name not in params:
                params[name] = ParamDetails()
                params_order.append(name)
            params[name].type_hint = desc
            capture_returns = False
            continue

        if line.startswith(":returns:"):
            returns_lines.append(line.split(":", 2)[-1].strip())
            capture_returns = True
            continue

        if capture_returns:
            if line.startswith(":"):
                capture_returns = False
            else:
                returns_lines.append(line)

    ordered_params = [
        {
            "name": name,
            "desc": params[name].desc,
            "type": params[name].type_hint,
            "required": params[name].required,
        }
        for name in params_order
    ]

    returns_text = " ".join([part for part in returns_lines if part]).strip()

    return {
        "summary": summary,
        "link": link,
        "params": ordered_params,
        "returns": returns_text,
        "notes": [],
    }


def build_summary_text(summary: str) -> str:
    if not summary:
        return "说明：参考源码注释"
    return f"{SUMMARY_PREFIX}{summary.strip()}"


def format_param_entry(param: Dict[str, Any]) -> str:
    pieces: List[str] = [str(param.get("name", ""))]
    type_hint = param.get("type")
    if isinstance(type_hint, str) and type_hint:
        pieces.append(f"({type_hint})")
    desc = param.get("desc")
    if isinstance(desc, str) and desc:
        pieces.append(f": {desc}")
    return " ".join(pieces)


def build_entry(func: FunctionInfo, doc: Dict, async_info: Optional[FunctionInfo]) -> str:
    signature = format_signature(func.source)
    summary_line = build_summary_text(doc.get("summary", ""))
    link = doc.get("link") or "-"

    client_ref = f"同步 binance/client.py:{func.start_line}-{func.end_line}"
    if async_info:
        async_ref = f"异步 binance/async_client.py:{async_info.start_line}-{async_info.end_line}"
    else:
        async_ref = "异步 暂无对应实现"

    header = f"### {signature}\n{summary_line} | [源码]({client_ref}, {async_ref}) | [官方文档]({link})\n"

    params = doc.get("params", [])
    required = [format_param_entry(p) for p in params if p.get("required") is True]
    optional = [format_param_entry(p) for p in params if p.get("required") is False]
    unknown = [format_param_entry(p) for p in params if p.get("required") is None]

    core_lines = ["**核心参数**:"]
    if required:
        core_lines.append("- ✅ **必需**: " + ", ".join(required))
    if optional:
        core_lines.append("- ☑️ **可选**: " + ", ".join(optional))
    if unknown:
        core_lines.append("- ℹ️ **未标注**: " + ", ".join(unknown))
    if len(core_lines) == 1:
        core_lines.append("- （源码未提供参数说明）")

    common_lines = ["**常用值**:", "- 源码注释未提供固定枚举值"]

    returns_text = doc.get("returns") or "API response"
    returns_lines = ["**返回**:", f"- {returns_text}；详见官方文档"]

    sections = [header, "\n".join(core_lines), "\n".join(common_lines), "\n".join(returns_lines)]
    return "\n\n".join(section.strip() for section in sections if section).strip()


def update_markdown_file(path: Path, entries: List[str]) -> None:
    if not entries:
        return
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = text.splitlines()
    cutoff = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith("### "):
            cutoff = idx
            break
    preserved = "\n".join(lines[:cutoff]).rstrip()
    combined = "\n\n".join(entries).strip()
    new_text_parts = [preserved.strip(), combined]
    new_text = "\n\n".join(part for part in new_text_parts if part) + "\n"
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    client_funcs = load_class_functions(CLIENT_PATH, "Client")
    async_funcs = load_class_functions(ASYNC_PATH, "AsyncClient")

    categorized: Dict[str, List[tuple[int, str]]] = {key: [] for key in CATEGORY_FILES}

    for func in client_funcs.values():
        if func.name.startswith("_"):
            continue
        category = determine_category(func.name, func.source)
        if not category:
            continue
        doc_info = parse_docstring(func.docstring)
        entry = build_entry(func, doc_info, async_funcs.get(func.name))
        categorized[category].append((func.start_line, entry))

    for category, items in categorized.items():
        sorted_entries = [entry for _, entry in sorted(items, key=lambda item: item[0])]
        update_markdown_file(CATEGORY_FILES[category], sorted_entries)
        print(f"Updated {CATEGORY_FILES[category]} with {len(sorted_entries)} entries.")


if __name__ == "__main__":
    main()
