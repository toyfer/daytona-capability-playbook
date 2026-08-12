# pdf-extract

**What:** 既存 PDF からテキスト・表を抜く。  
**When:** アップロードまたは `/workspace` 上の PDF を読むとき。  
**Not when:** 体裁の良い新規 PDF を作る → host `pdf` スキル。スキャン画像のみ → `ocr-scan`。

## Setup

**不要。** スナップショットに pymupdf / pdfplumber / tabula が入っている想定（無ければ ENV を確認し pip）。

## Use

```python
import fitz  # pymupdf
doc = fitz.open("/workspace/file.pdf")
for i, page in enumerate(doc):
    print(f"--- page {i+1} ---")
    print(page.get_text())
```

```python
import pdfplumber
with pdfplumber.open("/workspace/file.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
        for table in page.extract_tables() or []:
            print(table)
```

表が複雑なとき（Java 利用可）:

```python
import tabula
dfs = tabula.read_pdf("/workspace/file.pdf", pages="all")
```

## Hard no

- 全文を回答にダンプしない。該当箇所だけ
- テキスト層があるのに先に tesseract しない
- poppler を「とりあえず」入れない（既備で足りることが多い）
