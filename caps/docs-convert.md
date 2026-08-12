# docs-convert

**What:** pandoc 等で md の一括変換（html/docx など）。  
**When:** 多数ファイルの機械的変換。  
**Not when:** 体裁の良い 1 本の PDF/docx/pptx → host の `pdf` / `docx` / `pptx` スキル。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh docs-extra
source /workspace/.tools/env
```

## Use

```bash
pandoc input.md -o output.html
pandoc input.md -o output.docx
```

## Hard no

- pandoc で PDF（pdflatex 不在で落ちやすい）。PDF は host `pdf`
- フル TeX Live を入れない（ディスク破壊的）
