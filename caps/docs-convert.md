# docs-convert

**What:** Mechanically convert batches of Markdown to HTML or DOCX with Pandoc.  
**When:** many files need a repeatable conversion.  
**Not when:** creating one polished PDF/DOCX/PPTX (use the host document skill).

## Setup

Profile: `docs-extra`. Follow [bootstrap](./bootstrap.md).

Do not trust a host skill that claims `pandoc` is preinstalled. Check `command -v pandoc` first; install only via this profile if missing.

## Use

```bash
pandoc input.md -o output.html
pandoc input.md -o output.docx
```

Do not use Pandoc PDF by default: a TeX engine is absent. Do not install full TeX Live.
