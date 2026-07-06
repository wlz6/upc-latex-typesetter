---
name: upc-latex-typesetter
description: 中国石油大学（华东）课程作业、实训、课程设计、本科毕业设计（论文）LaTeX 排版助手。按文档类型动态生成封面、标题、页眉页脚、目录、正文、参考文献和附录，并用 XeLaTeX 编译验证。
---

# UPC LaTeX Typesetter

## Use This Skill When

Use this skill when the user asks Codex to create, convert, repair, or verify a LaTeX document for **中国石油大学（华东）** coursework, course training, curriculum design, mathematical modeling training, or undergraduate thesis/design formatting.

Typical requests:

- “按学校模板排版”
- “生成可编译的 LaTeX/PDF”
- “数学建模实训/课程设计/毕业设计论文模板”
- “封面、页眉、目录、正文标题动态更换”
- “对照模板 PDF 检查排版”

This skill should produce practical files, not only advice: generate or edit `.tex`, copy required assets, run XeLaTeX when available, and report exact paths and remaining issues.

## Required Inputs

Do not leave `[填入]`, `TODO`, or empty template placeholders in final output. If a required field cannot be inferred from provided files, ask the user before producing the final `.tex`.

Required:

- `doc_type`: one of `math_modeling_training`, `course_design`, `coursework`, `undergraduate_thesis`, or a user-provided equivalent.
- `title`: document title.
- `students`: 1 to 3 `{name, id}` entries for training/course-design covers, or the fields required by the thesis/coursework cover.
- `date`: cover date, e.g. `2026 年 7 月 6 日`.
- `body`: chapter/section content or a source document to convert.
- `logo_path`: school logo image. Use `logo.png` beside the `.tex` unless the user gives another path.

Optional but commonly needed:

- `subtitle`: use an em-dash style prefix in display text, e.g. `——副标题`.
- `major_class`, `advisor`, `college`, `major`, `grade`: required by some coursework/thesis covers.
- `abstract`, `keywords`, `english_title`, `english_abstract`, `english_keywords`.
- `references`, `acknowledgement`, `appendices`.
- `template_pdf`: a requirement PDF. If present, inspect both extracted text and page images before claiming conformance.

## Workflow For Codex

1. Inspect the user's files first: `.tex`, `.pdf`, `.docx`, images, code attachments, and any requirement PDF.
2. If a requirement PDF is provided, render representative pages as images and read extracted text. Check at least cover, Chinese abstract, English abstract if present, TOC, first body page, formulas/figures/tables, references, and appendices.
3. Decide the dynamic style profile from `doc_type`; do not hard-code “数学建模实训” unless that is the actual document type.
4. For the math-modeling requirement PDF, run `scripts/validate_upc_fonts.py` before generating strict output to confirm the required Windows font files exist.
5. Generate or patch the `.tex` using the macro patterns below.
6. Run XeLaTeX twice when a compiler is available. Run a third time if references/TOC are still unresolved.
7. Inspect the log and, when possible, render the resulting PDF pages for visual checks.
8. Verify strict template fonts before reporting success. For the math-modeling requirement PDF, run `scripts/validate_upc_fonts.py --pdf <output.pdf>`; `pdffonts` should show Windows/Office-style fonts such as `SimSun`, `SimHei`, `FangSong`/`FangSong_GB2312`, `KaiTi`/`KaiTi_GB2312`, and `TimesNewRomanPS...`. If the document used fallback fonts, report it as a deviation.
9. Report source path, PDF path, compiler used, and any exact deviations that remain.

## Compiler Detection

Prefer local Linux/WSL `xelatex`. If unavailable, check Windows TeX installations reachable from WSL.

```bash
which xelatex
ls /mnt/c/Program\ Files/MiKTeX/miktex/bin/x64/xelatex.exe
ls /mnt/c/texlive/*/bin/windows/xelatex.exe
ls /mnt/d/Programs/texlive/*/bin/windows/xelatex.exe
cmd.exe /c 'where xelatex' 2>/dev/null
powershell.exe -Command 'Get-Command xelatex -ErrorAction SilentlyContinue | Select-Object Source' 2>/dev/null
```

If only Windows `xelatex.exe` is available from WSL, compile in a Windows-visible directory and copy the PDF back. If no compiler exists, still generate the `.tex` and state that compilation was not run.

## Dynamic Style Profiles

### Mathematical Modeling Training / Course Design

Use this for `doc_type = math_modeling_training` or when the template PDF says “数学建模课程实训/数学建模实训/数学建模课程设计”.

- Cover main course title: `数学建模课程实训` when the requirement PDF uses that exact text. Use `数学建模实训` only if the user/template explicitly says so.
- Front/header title for abstract and TOC: usually `中国石油大学（华东）数学建模实训`.
- Back-matter header for acknowledgement, references, and appendices: use the template wording when provided. The current math-modeling PDF uses `中国石油大学（华东）数学建模课程设计` on 致谢/参考文献/附录 pages.
- Body header: current chapter title, e.g. `第 1 章  引言`.
- Page numbering: cover, Chinese abstract, English abstract, and TOC have no page number. From the first body chapter through appendices, use continuous Arabic page numbers centered in the footer.
- Body length and content requirements belong to the user’s assignment. Do not invent content to meet word count.

### Undergraduate Thesis / Graduation Design

Use this for `undergraduate_thesis`, `毕业设计`, `毕业论文`, or `本科毕业设计(论文)`.

- Front/header title: `中国石油大学（华东）本科毕业设计(论文)` unless the user’s school template says otherwise.
- Cover fields are thesis-specific and may include college, major, class, student, ID, advisor, title, and date. Ask for missing mandatory metadata.
- Keep the same dynamic page style model: preliminary pages unnumbered; body through appendices continuously numbered unless the supplied thesis template requires Roman preliminary numbering.

### Coursework / Other Course Design

Use this for regular course reports or course designs.

- Header title should be built from the actual course/report name, e.g. `中国石油大学（华东）<课程名>课程设计`.
- Cover style may differ from math-modeling training. Follow the supplied template if present.
- Do not reuse math-modeling cover wording unless the assignment is actually math modeling.

## Strict Font Policy

For `数学建模实训模板相关要求说明.pdf`, strict conformance requires the fonts used in that requirement PDF:

- Chinese body text: `SimSun` / 宋体, 小四 unless a section says otherwise.
- Chinese bold headings: `SimHei` / 黑体.
- Header text: `KaiTi_GB2312` in the PDF; in WSL use the Windows `simkai.ttf` file (`KaiTi`) unless a true `KaiTi_GB2312` file is supplied.
- Cover and selected annotations may use `FangSong` / 仿宋; use `simfang.ttf`.
- Western letters, digits, page numbers, formulas, references, and English abstract text: `Times New Roman`.

Do not package Microsoft Windows fonts into this skill or any generated release artifact. They are proprietary system fonts. In WSL strict mode, reference the user's locally installed Windows font files by path:

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

Before compiling in strict mode, check these files exist. If any are missing, ask the user to provide the missing font files or explicitly allow a non-strict fallback. Do not silently substitute Noto, Liberation, or Fandol and then claim template conformance.

Bundled fonts live under `assets/fonts/fandol/` and are GPL + GPL font exception. Use them only when the user explicitly allows a portable/non-strict build or when producing a draft where exact school-template font conformance is not required. When using Fandol, report: `字体使用 Fandol 近似替代，不是严格模板字体`.

## LaTeX Foundation

Use XeLaTeX and `ctexbook` unless an existing project already has a better class. Keep UTF-8.

```latex
% !TEX program = xelatex
\documentclass[12pt,a4paper,openany,fontset=none,AutoFakeBold=true,AutoFakeSlant=true]{ctexbook}

\usepackage[top=2.5cm,bottom=2.5cm,left=3.0cm,right=3.0cm]{geometry}
\setlength{\headheight}{13pt}
\usepackage{setspace}
\onehalfspacing
\setlength{\parindent}{2em}

\usepackage{fontspec}
\usepackage{unicode-math}
\newcommand{\upcwinfontdir}{/mnt/c/Windows/Fonts/}
\setmainfont{times.ttf}[
  Path=\upcwinfontdir,
  BoldFont=timesbd.ttf,
  ItalicFont=timesi.ttf,
  BoldItalicFont=timesbi.ttf
]
\setsansfont{times.ttf}[
  Path=\upcwinfontdir,
  BoldFont=timesbd.ttf,
  ItalicFont=timesi.ttf,
  BoldItalicFont=timesbi.ttf
]
\setmonofont{times.ttf}[Path=\upcwinfontdir]
\setCJKmainfont{simsun.ttc}[
  Path=\upcwinfontdir,
  BoldFont=simhei.ttf,
  ItalicFont=simkai.ttf,
  AutoFakeBold=true
]
\setCJKsansfont{simhei.ttf}[Path=\upcwinfontdir]
\setCJKmonofont{simfang.ttf}[Path=\upcwinfontdir]
\setCJKfamilyfont{zhsong}{simsun.ttc}[Path=\upcwinfontdir]
\setCJKfamilyfont{zhhei}{simhei.ttf}[Path=\upcwinfontdir]
\setCJKfamilyfont{zhkai}{simkai.ttf}[Path=\upcwinfontdir]
\setCJKfamilyfont{zhfs}{simfang.ttf}[Path=\upcwinfontdir]
\providecommand{\songti}{\CJKfamily{zhsong}}
\providecommand{\heiti}{\CJKfamily{zhhei}}
\providecommand{\kaishu}{\CJKfamily{zhkai}}
\providecommand{\fangsong}{\CJKfamily{zhfs}}
\setmathfont{TeX Gyre Termes Math}

\usepackage{amsmath,amsthm,booktabs,array,caption,fancyhdr,graphicx,enumitem}
\usepackage{tocloft}
\usepackage{chngcntr}

\newcommand{\upcfrontheader}{中国石油大学（华东）数学建模实训}
\newcommand{\upcbackheader}{中国石油大学（华东）数学建模课程设计}
\newcommand{\upcbodyheader}{\leftmark}
```

Load additional packages only when needed, for example `listings` for source code, `longtable` for multi-page tables, `float` for strict placement, or `hyperref` if the user wants clickable PDF links.

## Titles, TOC, And Counters

The math-modeling requirement PDF specifies:

- Chapter title: centered, 小二黑体. Display as `第 1 章  引言`, with spacing between number and title.
- Section title: 四号黑体, left aligned, number followed by one space.
- Subsection title: 小四黑体, left aligned.
- TOC title: `目\quad 录`, 三号黑体 centered, 1.5 line spacing, paragraph before/after about 0.5 line.
- TOC entries exclude 摘要 and ABSTRACT, but include body chapters, 致谢, 参考文献, and 附录. Include at most three title levels.
- Figure/table/equation counters reset by chapter. Use visible labels like `(3-1)`, `图3-1`, `表4-1`.
- Appendix figures/tables/equations should use appendix labels such as `图A1`, `表B2`, `(B3)` when appendices are present.

Recommended configuration:

```latex
\ctexset{
  chapter = {
    name = {第,章},
    number = \arabic{chapter},
    format = \zihao{-2}\heiti\centering,
    nameformat = {},
    titleformat = {},
    aftername = \quad,
    beforeskip = 0.5\baselineskip,
    afterskip = \baselineskip,
    pagestyle = upcbody
  },
  section = {
    format = \zihao{4}\heiti\raggedright,
    aftername = \quad,
    beforeskip = 0.5\baselineskip,
    afterskip = 0.5\baselineskip
  },
  subsection = {
    format = \zihao{-4}\heiti\raggedright,
    aftername = \quad,
    beforeskip = 0.5\baselineskip,
    afterskip = 0.5\baselineskip
  }
}

\renewcommand{\contentsname}{目\quad 录}
\setcounter{tocdepth}{2}
\counterwithin{figure}{chapter}
\counterwithin{table}{chapter}
\numberwithin{equation}{chapter}
\renewcommand{\theequation}{\arabic{chapter}-\arabic{equation}}
\renewcommand{\thefigure}{\arabic{chapter}-\arabic{figure}}
\renewcommand{\thetable}{\arabic{chapter}-\arabic{table}}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
```

## Page Styles

Use separate page styles for preliminary pages, body pages, and back matter. This is required because many UPC templates change headers by section type.

```latex
\fancypagestyle{upcprelim}{%
  \fancyhf{}
  \fancyhead[C]{\zihao{5}\kaishu \upcfrontheader}
  \renewcommand{\headrulewidth}{0.4pt}
}

\fancypagestyle{upcbody}{%
  \fancyhf{}
  \fancyhead[C]{\zihao{5}\kaishu \leftmark}
  \fancyfoot[C]{\zihao{5}\rmfamily \thepage}
  \renewcommand{\headrulewidth}{0.4pt}
}

\fancypagestyle{upcback}{%
  \fancyhf{}
  \fancyhead[C]{\zihao{5}\kaishu \upcbackheader}
  \fancyfoot[C]{\zihao{5}\rmfamily \thepage}
  \renewcommand{\headrulewidth}{0.4pt}
}

\fancypagestyle{plain}{%
  \fancyhf{}
  \fancyhead[C]{\zihao{5}\kaishu \leftmark}
  \fancyfoot[C]{\zihao{5}\rmfamily \thepage}
  \renewcommand{\headrulewidth}{0.4pt}
}
```

Rules:

- Cover: `\pagestyle{empty}` and no page number.
- Abstract/English abstract/TOC: `\pagestyle{upcprelim}` and no page number.
- First body page: `\clearpage\pagenumbering{arabic}\setcounter{page}{1}\pagestyle{upcbody}`.
- Back matter: switch to `\pagestyle{upcback}` but do **not** reset page numbers.
- Do not state that 致谢/参考文献/附录 are unnumbered for the math-modeling template. They are part of the continuous Arabic numbering after the body begins.

## Math-Modeling Cover

For the PDF “数学建模实训模板相关要求说明.pdf”, use this cover pattern.

```latex
\begin{document}
\pagestyle{empty}

\begin{center}
\vspace*{0.5cm}
\includegraphics[width=6.5cm]{logo.png}

\vspace{1.8cm}
{\zihao{-0}\heiti\bfseries 数学建模课程实训\par}

\vspace{1.8cm}
\begin{minipage}{0.82\textwidth}
{\zihao{-2}\heiti\bfseries
\noindent 题\quad 目：\parbox[t]{0.62\textwidth}{\centering TITLE}\par}
\vspace{0.25cm}
{\zihao{-2}\heiti\bfseries\hfill SUBTITLE\par}
\end{minipage}

\vspace{2.2cm}
{\fangsong\zihao{3}
\begin{tabular}{@{}r@{\quad}p{9.5cm}@{}}
姓\quad 名： & \centering\arraybackslash\underline{\makebox[9.5cm]{NAME1}} \\
学\quad 号： & \centering\arraybackslash\underline{\makebox[9.5cm]{ID1}} \\
姓\quad 名： & \centering\arraybackslash\underline{\makebox[9.5cm]{NAME2}} \\
学\quad 号： & \centering\arraybackslash\underline{\makebox[9.5cm]{ID2}} \\
姓\quad 名： & \centering\arraybackslash\underline{\makebox[9.5cm]{NAME3}} \\
学\quad 号： & \centering\arraybackslash\underline{\makebox[9.5cm]{ID3}}
\end{tabular}
\par}

\vfill
{\fangsong\zihao{3} DATE\par}
\end{center}
```

If fewer than 3 students are provided, omit the unused name/ID row pairs. If the title is long, wrap it so that continuation lines align under the first title character rather than under “题目：”. The subtitle, when present, starts with `——` and is placed on its own right-aligned line.

## Abstracts And Keywords

Chinese abstract:

- Optional document title above abstract: 小二黑体 centered; include it only if the template/user wants the title repeated on the abstract page.
- Abstract heading: `摘\quad 要`, 三号黑体 centered.
- Body: 小四宋体, 1.5 line spacing, first-line indent 2 characters, justified.
- Chinese abstract should normally fit within one page for the math-modeling template.
- Keywords line: first-line indent 2 characters, `关键词：` bold, 3 to 5 keywords separated by `；`, no final punctuation.

English abstract:

- English title: Times New Roman, 小二, bold, centered.
- Heading: `Abstract`, Times New Roman, 三号, bold, centered.
- Body: Times New Roman, 小四, first-line indent 2 characters, 1.5 line spacing.
- `Keywords：` bold, terms separated by semicolons, no final punctuation, content should correspond to Chinese keywords.
- Usually no more than 250 English words.

## Figures, Tables, Equations, Theorems

- Cite every figure and table in the text before or near its placement.
- Figure caption goes below the figure, centered, 五号宋体.
- Table caption goes above the table, centered, 五号宋体.
- Use three-line tables with `booktabs` by default.
- Table parameters must include quantities and units where applicable. Do not use “同前” or “同左”; repeat the content.
- For tables continuing on later pages, repeat the header and mark the continuation, e.g. `续表4-1`.
- Number only formulas that are referenced. Numbered formulas are centered with right-aligned numbers like `(3-1)`.
- Explain variables below formulas.
- Definitions/theorems/proofs should use bold labels and the document body font.

Recommended snippets:

```latex
\DeclareCaptionFont{upcsong}{\zihao{5}\songti}
\captionsetup{font=upcsong,labelsep=space,skip=5pt}
\captionsetup[figure]{justification=centering}
\captionsetup[table]{position=above,justification=centering}

\theoremstyle{definition}
\newtheorem{upcdefinition}{定义}[chapter]
\newtheorem{upctheorem}{定理}[chapter]
\newtheorem{upclemma}{引理}[chapter]
\renewenvironment{proof}[1][证明]{\par\zihao{-4}\songti\indent\textbf{#1}\quad}{\par}
```

## Back Matter

The math-modeling template orders the back matter as:

1. `致\quad 谢`
2. `参考文献`
3. `附\quad 录`

Use the user’s requested order only if they explicitly require a different one. Add all back-matter headings to the TOC. Keep Arabic page numbering continuous from the body.

Reference rules from the template:

- Every reference should be cited in the body.
- Sort references by first citation order.
- Labels use bracketed numbers, e.g. `[1]`.
- Content is 小四宋体; letters/digits use Times New Roman; 1.5 line spacing.
- Use English punctuation inside reference entries and place one space after punctuation where appropriate.
- Include at least 10 references and at least 2 foreign-language references when the assignment requires that. Do not invent sources; ask the user or say the source list is incomplete.

Appendix rules:

- Appendix title page uses `附\quad 录`, centered.
- Appendix sections use `附录A ...`, `附录B ...`.
- Appendix figures/tables/equations use appendix-specific labels, e.g. `图A1`, `表B2`, `(B3)`.

## Document Assembly Order

For math-modeling training/course design:

```latex
\begin{document}
% cover: empty style

% Chinese abstract: upcprelim, no page number
% English abstract if present: upcprelim, no page number
% TOC: upcprelim, no page number

\clearpage
\pagenumbering{arabic}
\setcounter{page}{1}
\pagestyle{upcbody}
% body chapters

\clearpage
\pagestyle{upcback}
\chapter*{致\quad 谢}
\addcontentsline{toc}{chapter}{致\quad 谢}
% acknowledgement

\clearpage
\pagestyle{upcback}
\chapter*{参考文献}
\addcontentsline{toc}{chapter}{参考文献}
% references

\clearpage
\pagestyle{upcback}
\chapter*{附\quad 录}
\addcontentsline{toc}{chapter}{附\quad 录}
\appendix
% appendix sections
\end{document}
```

## Verification Checklist

Before reporting success, check:

- Cover has no page number and uses the correct dynamic course/report title.
- Logo exists and renders.
- Math-modeling cover title is 小初黑体 bold centered; “题目：” block is 小二黑体; subtitle is its own right-aligned line.
- Student name/ID rows match the number of students and do not leave blank rows.
- Abstract/TOC have the correct fixed header and no page number.
- TOC heading is `目\quad 录`; TOC excludes abstracts and includes body, acknowledgement, references, and appendix.
- Body starts at page 1; page footer is centered Times New Roman 五号.
- Body header is current chapter title, not a stale fixed course title.
- Back matter switches to the required fixed back header and keeps continuous Arabic page numbers.
- Chapter/section/subsection font sizes and alignment match the selected template.
- Formula, figure, and table numbering follow chapter numbering; appendix numbering changes when appendices begin.
- Figure/table captions are in the right location and use 五号宋体.
- Tables use three-line style unless data requires a justified exception.
- References are cited in the body and ordered by first citation.
- There are no raw placeholders, unresolved references, missing images, LaTeX errors, or obvious overfull title/header text.
- `scripts/validate_upc_fonts.py --pdf <output.pdf>` passes for strict math-modeling template output. If it fails, do not claim strict font conformance.

## Failure Handling

- Missing required metadata: ask only for the missing fields.
- Missing logo: ask for it or proceed only if the user explicitly allows no-logo output; report the deviation.
- Missing compiler: generate `.tex`, skip compilation, and give the exact command the user can run.
- Compilation failure: show the first meaningful error and fix source issues before returning.
- Requirement conflict: follow the supplied template PDF over the generic rules in this skill, and state the conflict briefly.

## Response Format

Final responses should be concise and file-oriented:

```text
已更新并编译：
- 源码：/abs/path/report.tex
- PDF：/abs/path/report.pdf
- 编译器：xelatex

检查结果：
- 封面、摘要、目录、正文页眉页码符合当前模板
- 参考文献还缺 2 篇外文来源，需要用户补充
```
