# 環境インベントリ

> 実測: 2026-08-12。環境が変わった時だけ更新する。

| 項目 | 値 |
|---|---|
| OS / arch | Debian 12 (bookworm), x86_64 |
| user | 多くの場合 `root`（`sudo` 不要） |
| workspace | `/workspace`、同一チャットセッション内のみ永続 |
| disk | overlay 約 10G |
| network | 一般 HTTPS 可 |
| runtimes | Python 3.12 + pip + uv、Node 18 + npm/npx、Java 17、gcc/make |

## Initial CLI

`bash` `curl` `git` `python3` `pip3` `uv` `node` `npm` `npx` `perl` `java` `tar` `gzip` `xz` `openssl` `iconv` GNU coreutils

## Initial Python

`pymupdf` `pdfplumber` `pdfminer` `pypdfium2` `tabula` `bs4` `lxml` `httpx` `requests` `pandas` `numpy` `scipy` `sklearn` `matplotlib` `seaborn` `plotly` `yfinance`

## Usually absent

`jq` `rg` `fd` `nkf` `sqlite3` CLI `pandoc` `ffmpeg` `tesseract` `qpdf`

Use `command -v` before assuming availability. Install only through [caps/bootstrap.md](./caps/bootstrap.md).
