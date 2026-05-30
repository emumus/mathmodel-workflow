"""
build.py — 数模论文第一阶段构建脚本
角色：合并章节、生成附录、产出 text/frozen/ 下的可审阅 Markdown

用法：python utils/build.py（或 python scripts/build.py，取决于实际位置）
需在项目根目录下执行。
"""

import re
import os
import json
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────
ROOT = Path.cwd()
if ROOT.name == "utils":
    ROOT = ROOT.parent
TEXT_PAPER = ROOT / "text" / "paper"
TEXT_APPENDIX = ROOT / "text" / "appendix"
TEXT_FROZEN = ROOT / "text" / "frozen"
CODE_DIR = ROOT / "code"

CACHE_DIR = ROOT / "utils" / "cache"
DESC_CACHE = CACHE_DIR / "desc.json"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
if not DESC_CACHE.exists():
    DESC_CACHE.write_text("{}", encoding="utf-8")
desc = json.loads(DESC_CACHE.read_text(encoding="utf-8"))


TEXT_FROZEN.mkdir(parents=True, exist_ok=True)


# ── 辅助函数 ──────────────────────────────────────────


def natural_sort_key(path: Path) -> list:
    """按数字前缀自然排序，如 2_xxx.md < 10_xxx.md"""
    stem = path.stem
    parts = re.split(r"(\d+)", stem)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def collect_chapters() -> list[Path]:
    """收集 text/paper/ 下所有以数字前缀开头的 .md 章节文件"""

    pattern = re.compile(r"^[\d.]+_.*\.md$")
    files = sorted(
        (f for f in TEXT_PAPER.iterdir() if pattern.match(f.name)),
        key=natural_sort_key,
    )
    if not files:
        print("未在 text/paper/ 下找到任何章节文件（以数字前缀命名）。")
    return files


EXTYPE = {
    ".py": "Python代码",
    ".pdf": "PDF文件",
    ".md": "Markdown文件",
    ".txt": "文本文件",
    ".xlsx": "表格",
    ".xls": "表格",
    ".csv": "表格",
    ".npy": "NumPy数组文件",
    ".json": "JSON文件",
    ".html": "HTML文件",
    ".png": "图片",
    ".jpg": "图片",
    ".jpeg": "图片",
    ".gif": "图片",
}


def _get_desc(filename: str) -> str:
    crtdesc = desc.get(filename)
    if not crtdesc:
        crtdesc = "..."
        desc[filename] = crtdesc
        DESC_CACHE.write_text(
            json.dumps(desc, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return crtdesc


def _build_file_table() -> list[str]:
    table = [
        "| 文件 | 类型 | 描述 |",
        "| --- | --- | --- |",
    ]
    for qdir in sorted(CODE_DIR.glob("*/")):
        qname = qdir.name
        if qname.startswith("_") or qname in ["raw", "deprecated", "__pycache__"]:
            continue
        for f in sorted(qdir.glob("*")):
            file_name = f.name
            ext_label = EXTYPE.get(f.suffix, "其他")
            table.append(f"| {file_name} | {ext_label} | {_get_desc(file_name)} |")
    return table


def _collect_code_sections() -> list[tuple[str, str]]:
    sections = []
    for qdir in sorted(CODE_DIR.glob("*/")):
        qname = qdir.name
        if qname.startswith("_") or qname in ["raw", "deprecated", "__pycache__"]:
            continue
        for py_file in sorted(qdir.glob("*.py")):
            if "img" in py_file.name:
                continue
            rel_path = str(py_file.relative_to(ROOT / "code"))
            code_block = (
                "```python\n" + py_file.read_text(encoding="utf-8").strip() + "\n```"
            )
            sections.append((rel_path, code_block))
    return sections


def _next_label(letter: int) -> tuple[str, int]:
    return chr(letter), letter + 1


def collect_appendix() -> str:
    """生成完整附录：支撑文件列表 + 额外附录 + 核心代码"""
    lines = ["# 附录\n"]
    letter = ord("A")

    label, letter = _next_label(letter)
    lines.append(f"## 附录{label} 支撑文件列表\n")
    lines.extend(_build_file_table())
    lines.append("")

    pattern = re.compile(r"^\d.*\.md$")
    extra_files = sorted(
        (f for f in TEXT_APPENDIX.iterdir() if pattern.match(f.name)),
        key=natural_sort_key,
    )
    for f in extra_files:
        label, letter = _next_label(letter)
        lines.append(f"## 附录{label} {f.stem}\n")
        lines.append(f.read_text(encoding="utf-8"))
        lines.append("")

    for rel_path, code_block in _collect_code_sections():
        label, letter = _next_label(letter)
        lines.append(f"## 附录{label} {rel_path}\n")
        lines.append(code_block)
        lines.append("")

    return "\n".join(lines)


FIG_PATTERN = re.compile(r"!\[(.*?)\]\((.+?)\)")
REF_FIG_PATTERN = re.compile(r"::ref\{fig:(.+?)\}")
REF_TBL_PATTERN = re.compile(r"::ref\{tbl:(.+?)\}")
H2_PATTERN = re.compile(r"^## ", re.MULTILINE)


def merge_chapters(chapters: list[Path]) -> str:
    """合并章节文件"""
    parts = []
    section = -1

    for ch in chapters:
        content = ch.read_text(encoding="utf-8")
        h2_list = H2_PATTERN.findall(content)
        if len(h2_list) > 1:
            raise ValueError(
                f"章节文件 {ch.name} 包含 {len(h2_list)} 个二级标题，"
                f"请拆分为独立文件"
            )

        section += 1

        fig_map = {}
        fig_order = 0
        for m in FIG_PATTERN.finditer(content):
            fname = Path(m.group(2)).name
            if fname not in fig_map:
                fig_order += 1
                fig_map[fname] = (fig_order, m.group(1), m.group(2))

        tbl_map = {}
        tbl_order = 0

        def _replace_fig(m: re.Match) -> str:
            fname = Path(m.group(1)).name
            if fname in fig_map:
                return f"图{section}-{fig_map[fname][0]}"
            return m.group(0)

        def _replace_tbl(m: re.Match) -> str:
            fname = Path(m.group(1)).name
            if fname in tbl_map:
                return f"表{section}-{tbl_map[fname][0]}"
            return m.group(0)

        content = REF_FIG_PATTERN.sub(_replace_fig, content)
        content = REF_TBL_PATTERN.sub(_replace_tbl, content)
        parts.append(content)

    return "\n\n".join(parts)


# ── 主流程 ────────────────────────────────────────────
def main():
    print("=" * 50)
    print(f"第一阶段构建开始: {ROOT}")
    print("=" * 50)

    # 1. 合并章节主论文
    chapters = collect_chapters()
    if chapters:
        main_md = merge_chapters(chapters)
        (TEXT_FROZEN / "Main.md").write_text(main_md, encoding="utf-8")
        print(f"Main.md 已生成（ {len(chapters)} 个章节）")
    else:
        print("⚠ 跳过 Main.md 生成")

    # 2. 生成附录
    appendix_content = collect_appendix()
    if appendix_content.strip():
        (TEXT_FROZEN / "Appendix.md").write_text(appendix_content, encoding="utf-8")
        print("✅ Appendix.md 已生成")
    else:
        print("⚠ 跳过 Appendix.md 生成（无附录内容）")

    print("=" * 50)
    print("第一阶段构建完成")
    print(f"输出目录：{TEXT_FROZEN}")
    print("=" * 50)


if __name__ == "__main__":
    main()
