"""
build_final.py — 数模论文第二阶段构建脚本
角色：合并 PDF、打包参考资料、计算 MD5

用法：python utils/build_final.py
需在项目根目录下执行，且 text/frozen/Main.md 与 Appendix.md 已通过 Typora 导出为 PDF。
"""

import os
import io
import sys
import zipfile
import hashlib
from datetime import datetime
from pathlib import Path

try:
    from PyPDF2 import PdfMerger
    from reportlab.pdfgen import canvas
    from pdfrw import PdfReader, PdfWriter, PageMerge
except ImportError as e:
    print(f"缺少依赖: {e}")
    print("请安装: pip install PyPDF2 reportlab pdfrw")
    sys.exit(1)

# ── 路径配置 ──────────────────────────────────────────
ROOT = Path.cwd()
TEXT_FROZEN = ROOT / "text" / "frozen"
CIT_DIR = ROOT / "cit"
CODE_DIR = ROOT / "code"
QUES_DIR = ROOT / "ques"

OUTPUT_DIR = ROOT / "frozen" / datetime.now().strftime("%Y%m%d_%H%M")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAPER_NAME = "我的论文"
ZIP_NAME = "我的参考资料"


# ── 辅助函数 ──────────────────────────────────────────
def md5(filepath: Path) -> str:
    """计算文件 MD5 值"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def merge_pdfs(pdf_paths: list[Path], output: Path) -> None:
    merger = PdfMerger()
    for p in pdf_paths:
        if p.exists():
            merger.append(str(p))
            print(f"  + 添加 {p.name}")
        else:
            print(f"  ⚠ 未找到 {p}，跳过")
    merger.write(str(output))
    merger.close()
    print(f"✅ 已合并 PDF: {output}")


def create_reference_zip(output_path: Path) -> None:
    """创建参考资料压缩包"""
    exclude_dirs = {"__pycache__", "deprecated", "raw"}
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in CODE_DIR.rglob("*"):
            if f.is_file() and not any(ex in f.parts for ex in exclude_dirs):
                zf.write(f, f.relative_to(ROOT))

        # 添加原始题目
        for f in QUES_DIR.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(ROOT))

        # 添加引用资料
        for f in CIT_DIR.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(ROOT))

    print(f"✅ 参考资料已打包: {output_path}")


# ── 主流程 ────────────────────────────────────────────
def main():
    print("=" * 50)
    print("第二阶段构建开始（最终输出）")
    print("=" * 50)

    # 1. 确定要合并的 PDF
    main_pdf = TEXT_FROZEN / "Main.pdf"
    appendix_pdf = TEXT_FROZEN / "Appendix.pdf"
    prefix_pdf = TEXT_FROZEN / "Prefix.pdf"

    pdfs_to_merge = []
    if prefix_pdf.exists():
        pdfs_to_merge.append(prefix_pdf)
        print("📄 检测到 Prefix.pdf，添加在最前")
    if main_pdf.exists():
        pdfs_to_merge.append(main_pdf)
    else:
        print("⚠ Main.pdf 不存在！请先在 Typora 中导出。")
        return
    if appendix_pdf.exists():
        pdfs_to_merge.append(appendix_pdf)

    # 2. 合并 PDF
    output_pdf = OUTPUT_DIR / f"{PAPER_NAME}.pdf"
    merge_pdfs(pdfs_to_merge, output_pdf)

    # 3. 打包参考资料
    output_zip = OUTPUT_DIR / f"{ZIP_NAME}.zip"
    create_reference_zip(output_zip)

    # 4. 计算 MD5
    md5_lines = []
    for f in [output_pdf, output_zip]:
        if f.exists():
            h = md5(f)
            md5_lines.append(f"{f.name}：{h}")
            print(f"🔐 {f.name}：{h}")

    md5_path = OUTPUT_DIR / "md5.txt"
    md5_path.write_text("\n".join(md5_lines), encoding="utf-8")
    print(f"✅ MD5 已写入: {md5_path}")

    print("=" * 50)
    print(f"🎯 最终输出目录: {OUTPUT_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
