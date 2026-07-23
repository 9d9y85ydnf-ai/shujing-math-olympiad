# Shujing Math Olympiad

这是一个用于整理中国高中数学竞赛题解的本地工作项目。GitHub 公开仓库只保存通用的工作规范、题解模板、LaTeX 编译骨架和方法索引；具体题目、原始资料、题解正文及生成的 PDF 均保留在本地。

## 项目规范

- `AGENTS.md`：长期工作规范，包括知识边界、定义域、等号和证明完整性要求。
- `docs/`：竞赛代数审题流程与方法索引。
- `templates/`：新题和章节的统一模板。
- `book/`：可复用的 LaTeX 解析册工程与 Markdown 转换脚本。
- `problems/`、`sources/`：本地题目和资料目录，默认不纳入公开仓库。

## 本地工作流

1. 阅读原始资料的页面图像，确认题目、下标、定义域和小问。
2. 使用 `templates/` 中的模板撰写可誊写的竞赛主解。
3. 检查放缩方向、等号兼容性和边界情形。
4. 使用 `book/build_markdown.py` 将本地题解转换为章节 TeX。
5. 使用 Tectonic 编译 `book/main.tex`，并渲染关键页面检查排版。
6. 只将规范、模板和工程改进提交到 GitHub；具体内容留在本地。

## 公开内容边界

`.gitignore` 会屏蔽本地资料、题解、章节正文、生成文件和 PDF。提交前执行 `git status`、`git diff --check`，确认没有题目内容、个人密钥或临时文件进入提交。

## 目录

```text
AGENTS.md
CHANGELOG.md
docs/
templates/
book/
problems/algebra/README.md
```
