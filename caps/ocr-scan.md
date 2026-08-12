# ocr-scan

**What:** OCR a scanned image or PDF page with Tesseract.  
**When:** no usable text layer exists.  
**Not when:** text can already be extracted with pymupdf / pdfplumber.

## Setup

Profile: `ocr`. Follow [bootstrap](./bootstrap.md).

## Use

```bash
tesseract page.png stdout -l jpn+eng
```

For PDF pages, render pages first when needed. Do not dump all OCR output into context.
