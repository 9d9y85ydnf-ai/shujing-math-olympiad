"""将本地 Markdown 题解目录转换为一个 TeX 章节文件。

这是公开的通用工程脚本，不包含任何具体题目或答案。具体输入目录和输出文件
通过命令行参数提供，默认目录位于项目的本地题解区。
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def inline(text: str) -> str:
    parts = re.split(r"(\\\(.*?\\\)|\\\[.*?\\\])", text)
    out: list[str] = []
    for part in parts:
        if part.startswith(r"\(") or part.startswith(r"\["):
            out.append(part)
            continue
        part = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", part)
        part = part.replace("&", r"\&").replace("%", r"\%")
        part = part.replace("#", r"\#").replace("_", r"\_")
        out.append(part)
    return "".join(out)


def convert(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_quote = False
    in_list = False
    in_math = False

    for raw in lines:
        line = raw.rstrip()
        if line.strip() == r"\[":
            in_math = True
            out.append(r"\[")
        elif in_math:
            out.append(line)
            if line.strip() == r"\]":
                in_math = False
        elif line.startswith("# "):
            out.append(r"\section*{" + inline(line[2:]) + r"}")
        elif line.startswith("## "):
            out.append(r"\subsection*{" + inline(line[3:]) + r"}")
        elif line.startswith("### "):
            out.append(r"\subsubsection*{" + inline(line[4:]) + r"}")
        elif line.startswith("> "):
            if not in_quote:
                out.append(r"\begin{quote}")
                in_quote = True
            out.append(inline(line[2:]) + r"\\")
        elif line == ">":
            if in_quote:
                out.append(r"\\")
        elif line.startswith("- "):
            if not in_list:
                out.append(r"\begin{itemize}")
                in_list = True
            out.append(r"\item " + inline(line[2:]))
        elif not line:
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            if in_list:
                out.append(r"\end{itemize}")
                in_list = False
            out.append("")
        else:
            out.append(inline(line))

    if in_quote:
        out.append(r"\end{quote}")
    if in_list:
        out.append(r"\end{itemize}")
    return "\n".join(out) + "\n"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=root / "problems" / "algebra")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "generated" / "chapter.tex",
    )
    args = parser.parse_args()

    files = sorted(args.input_dir.glob("*.md"))
    if not files:
        raise SystemExit(f"no Markdown files found in {args.input_dir}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(convert(path.read_text(encoding="utf-8")) for path in files),
        encoding="utf-8",
    )
    print(f"generated {args.output} from {len(files)} Markdown files")


if __name__ == "__main__":
    main()
