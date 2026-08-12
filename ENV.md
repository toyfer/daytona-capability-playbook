# 環境インベントリ

> 実測: 2026-08-12（product-compare セッション後の pipeline smoke）。環境が変わった時だけ更新する。

| 項目 | 値 |
|---|---|
| OS / arch | Debian 12 (bookworm), x86_64 |
| user | 多くの場合 `root`（`sudo` 不要） |
| workspace | `/workspace`、同一チャットセッション内のみ永続 |
| disk | overlay 約 10G |
| network | 一般 HTTPS 可 |
| runtimes | Python 3.12 + pip + uv、Node 18 + npm/npx、Java 17、gcc/make |

## Initial CLI

`bash` `curl` `git` `python3` `pip3` `uv` `node` `npm` `npx` `perl` `java` `tar` `gzip` `xz` `openssl` `iconv` `sqlite3` GNU coreutils

## Initial Python

`pymupdf` (`fitz`) `pdfplumber` `pdfminer` `pypdfium2` `tabula` `bs4` `lxml` `httpx` `requests` `pandas` `numpy` `scipy` `sklearn` `matplotlib` `seaborn` `plotly` `yfinance` `duckdb`

## Usually absent (need bootstrap profile)

`jq` `rg` `fd` `nkf` `pandoc` `pdftotext` / poppler `qpdf` `tesseract` `ffmpeg` `convert` (ImageMagick v6; `magick` often absent)

## Notes (re-measured 2026-08-12)

- `sqlite3` CLI and Python `duckdb` are **present** without bootstrap; profile `data` is often a no-op but still safe.
- After profile `media`, ImageMagick is typically **v6**: command is `convert`. `magick` (v7) is often **absent**.
- After profile `ocr`, Tesseract languages include at least `eng` and `jpn`.
- Static installs land in `/workspace/.tools/bin` (`jq`, `rg`, `fd`); apt packages use system PATH.
- Use `command -v` (or a Python import check) before installing. Install only through [caps/bootstrap.md](./caps/bootstrap.md).
