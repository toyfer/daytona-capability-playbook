# ocr-scan

**What:** OCR a scanned image or PDF page with Tesseract.  
**When:** no usable text layer exists, and `tesseract` is missing or Japanese+English OCR is needed.  
**Not when:** text can already be extracted with pymupdf / pdfplumber, or a loaded host skill already produced usable OCR.

## Setup

Profile: `ocr`. Follow [bootstrap](./bootstrap.md).

Do not trust a host skill that claims tesseract or poppler is preinstalled. Check `command -v tesseract` (and render tools) before assuming OCR will run.

## Use

```bash
tesseract page.png stdout -l jpn+eng
```

## Input quality

- Prefer a real scan or a high-contrast render: roughly **300 DPI** (or a large on-screen bitmap). Tiny default fonts and low-resolution screenshots often yield garbage even when Tesseract is installed correctly.
- For PDF: try the live host `pdf` skill or [pdf-extract](./pdf-extract.md) first. Only OCR when there is no usable text layer; render the needed pages (e.g. pdftoppm / pymupdf) before `tesseract`.
- Japanese + English: `-l jpn+eng` after the `ocr` profile (packages `tesseract-ocr`, `tesseract-ocr-jpn`).
- Do not dump all OCR output into context; keep short excerpts.
