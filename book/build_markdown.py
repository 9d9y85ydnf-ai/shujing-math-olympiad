from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROBLEM_DIR = ROOT / "problems" / "algebra"
GENERATED = Path(__file__).resolve().parent / "generated"


def inline(text: str) -> str:
    parts = re.split(r"(\\\(.*?\\\)|\\\[.*?\\\])", text)
    out = []
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
    out = []
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
            out.append(r"\section*{" + inline(line[2:]) + "}")
        elif line.startswith("## "):
            out.append(r"\subsection*{" + inline(line[3:]) + "}")
        elif line.startswith("### "):
            out.append(r"\subsubsection*{" + inline(line[4:]) + "}")
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
    GENERATED.mkdir(parents=True, exist_ok=True)
    files = sorted(PROBLEM_DIR.glob("高联二试-GG1-第1讲-均值不等式-第*.md"))
    files.sort(key=lambda p: int(re.search(r"第(\d+)题", p.name).group(1)))
    if len(files) != 16:
        raise SystemExit(f"expected 16 lecture-1 files, found {len(files)}")
    target = GENERATED / "gg1-01.tex"
    target.write_text("\n".join(convert(p.read_text(encoding="utf-8")) for p in files), encoding="utf-8")
    print(f"generated {target} from {len(files)} Markdown files")


if __name__ == "__main__":
    main()
