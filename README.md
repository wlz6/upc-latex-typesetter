# UPC LaTeX Typesetter

`upc-latex-typesetter` 是一个 Codex skill，用于生成、修复、编译和检查中国石油大学（华东）课程作业、数学建模实训、课程设计、本科毕业设计（论文）等 LaTeX 文档。

当前版本重点适配数学建模实训 / 课程设计模板，固化了严格字体策略、封面、摘要、目录、正文页眉页码、参考文献和附录等排版规则。

## 功能

- 根据文档类型生成可编译的 `.tex` 文件，而不是只给排版建议。
- 默认使用 XeLaTeX 和 `ctexbook`。
- 支持动态封面、中文摘要、英文摘要、目录、正文、致谢、参考文献和附录。
- 对数学建模模板提供严格字体文件检查和编译后 PDF 字体检查。
- 内置 Fandol 字体作为可合法分发的非严格 fallback。

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── logo.png
├── scripts/
│   └── validate_upc_fonts.py
└── assets/
    └── fonts/
        └── fandol/
```

- `SKILL.md`：Codex skill 主说明，包含完整工作流和 LaTeX 排版规则。
- `scripts/validate_upc_fonts.py`：严格字体环境和 PDF 嵌入字体校验脚本。
- `assets/fonts/fandol/`：Fandol 中文字体，仅用于非严格 fallback，许可证为 GPL + GPL font exception。
- `logo.png`：默认校徽资源；用户提供其他 logo 时可替换。

## 严格字体策略

数学建模模板的严格匹配依赖本机 Windows / Office 风格字体。本仓库不会打包 Microsoft Windows 字体。

在 WSL 中，严格模式默认检查以下文件：

```text
/mnt/c/Windows/Fonts/simsun.ttc
/mnt/c/Windows/Fonts/simhei.ttf
/mnt/c/Windows/Fonts/simkai.ttf
/mnt/c/Windows/Fonts/simfang.ttf
/mnt/c/Windows/Fonts/times.ttf
/mnt/c/Windows/Fonts/timesbd.ttf
/mnt/c/Windows/Fonts/timesi.ttf
/mnt/c/Windows/Fonts/timesbi.ttf
```

如果缺少这些字体，只能使用 Fandol 进行草稿或非严格构建，并需要明确报告：

```text
字体使用 Fandol 近似替代，不是严格模板字体
```

## 环境要求

推荐环境：

- `xelatex`
- `latexmk`
- `texlive-xetex`
- `texlive-latex-extra`
- `texlive-lang-chinese`
- `pdfinfo`
- `pdffonts`
- `pdftoppm`

该 skill 优先面向 WSL / Linux 使用；如果 WSL 能访问 Windows 侧 TeX 发行版，也可以调用 Windows 版 XeLaTeX。

## 校验

检查严格字体文件是否存在：

```bash
scripts/validate_upc_fonts.py
```

检查已编译 PDF 是否嵌入严格模板字体：

```bash
scripts/validate_upc_fonts.py --pdf /path/to/output.pdf
```

成功输出：

```text
Strict UPC font check passed.
```

## 在 Codex 中使用

将本仓库安装或放置为 Codex skill 后，可以这样请求：

```text
按中国石油大学（华东）数学建模实训模板生成 LaTeX 并编译 PDF
```

通常需要提供：

- 文档类型，例如数学建模实训、课程设计、课程作业、本科毕业设计；
- 标题和可选副标题；
- 学生姓名、学号；
- 日期；
- 正文、摘要、关键词、参考文献和附录内容；
- `logo.png` 或用户指定的校徽图片。

生成严格数学建模模板时，应在生成前运行 `validate_upc_fonts.py`，并在 PDF 编译后再次运行 `validate_upc_fonts.py --pdf <output.pdf>`。

## 发布说明

当前发布版本：`v0.1`。

发布包：`upc-latex-typesetter-0.1.tar.gz`。

主要变化：

- 使用显式 Windows 字体路径，不再依赖 `fontset=windows`。
- 新增基于 `pdffonts` 的 PDF 字体校验。
- 不在仓库或发布包中包含专有 Windows 字体。
- 仅将 Fandol 字体作为合法的非严格 fallback 打包。

## 后续计划

- 增加模板生成脚本，统一输出严格字体 preamble 和版式骨架。
- 增加视觉回归检查，覆盖封面、摘要、目录、正文首页、参考文献和附录页面。
- 随着规则增长，将 `SKILL.md` 中的长规则拆分为独立 reference 文件。
