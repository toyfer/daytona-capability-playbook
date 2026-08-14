# pdf-extract

**What:** Extract text or tables from an existing PDF.  
**When:** a PDF is in `/workspace` or supplied by the user, and the live host `pdf` skill cannot finish cheaply — missing libraries, a huge file, a layout-hard table, or an explicit fitz/tabula path.  
**Not when:** creating a polished new PDF (host `pdf` skill), the loaded host skill already extracted what was needed, or text is absent (use `ocr-scan`).

## Setup

None in the normal sandbox: `pymupdf`, `pdfplumber`, and `tabula` are usually present. Check `ENV.md` before installing anything.

## Use

```python
import fitz
for i, page in enumerate(fitz.open('/workspace/file.pdf')):
    print(f'--- page {i + 1} ---')
    print(page.get_text())
```

```python
import pdfplumber
with pdfplumber.open('/workspace/file.pdf') as pdf:
    for page in pdf.pages:
        print(page.extract_text())
        for table in page.extract_tables() or []:
            print(table)
```

Use `tabula.read_pdf(..., pages='all')` when a complex table warrants Java-based extraction.

Return only relevant passages or structured results; do not dump a whole document into context.
