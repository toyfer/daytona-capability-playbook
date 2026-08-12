# 環境インベントリ

> 実測: 2026-08-12。推測で上書きしない。変わったら日付と内容を更新（OPS に 1 行）。

## プラットフォーム

| 項目 | 値 |
|---|---|
| OS | Debian 12 (bookworm), Linux x86_64 |
| ユーザー | 多くの場合 `root`（**sudo 不要・使うな**） |
| ディスク | overlay 約 10G |
| 作業領域 | `/workspace`（同一チャットセッション内のみ永続） |
| ネット | 一般 HTTPS 可 |
| Python | 3.12.x + pip + **uv** |
| Node | 18.x + npm + npx |
| Java | OpenJDK 17（tabula 用） |
| コンパイラ | gcc/g++/make |

## 初期から使える（入れ直すな）

**CLI:** bash, curl, git, python3, pip3, uv, node, npm, npx, perl, java, gcc/g++, make, tar, gzip, xz, openssl, ssh/scp, timeout, iconv, GNU coreutils, less, nohup

**Python（有用・既備の例）:** pymupdf (fitz), pdfplumber, pdfminer, pypdfium2, tabula, bs4, lxml, parsel, scrapy, httpx, requests, aiohttp, pandas, numpy, scipy, sklearn, networkx, sympy, matplotlib, seaborn, plotly, yfinance, pydantic, rich, jinja2, stdlib sqlite3/csv/json/xml

## 初期に無い（bootstrap 経由）

| 論理名 | bootstrap 内の入れ方 | 典型用途 |
|---|---|---|
| jq | static binary (GitHub release) | JSON パイプ |
| rg | static musl binary | /workspace 文字列検索 |
| fd | static or apt `fd-find` | ファイル名検索（小規模は find で可） |
| nkf | apt | 日本語レガシー符号 |
| unzip / file | apt | アーカイブ・種別 |
| sqlite3 CLI | apt | 軽量 DB |
| duckdb | `uv pip install duckdb`（Python API 推奨） | 大 CSV / SQL |
| pandoc | apt | md 一括 html/docx（PDF は host pdf） |
| poppler / tesseract / qpdf | apt | PDF 周辺（pymupdf を先に） |
| ffmpeg / imagemagick | apt | **明示時のみ** |

## install メモ（実測）

- `apt-get install` は root で可。**index が古いと 404** → bootstrap は apt 前に `apt-get update` をマーカー付き 1 回
- jq/rg は **static の方が apt より新しい・update 不要** → cli-min は static-first
- duckdb CLI バイナリは大きい。**Python パッケージで十分**
- openpyxl / python-docx / pptx / reportlab は host の文書 skills が主。shell で要るときだけ pip
- selenium は入っていても **ブラウザバイナリ無し** → 使うな。動的ページは host `retrieve`
- colgrep 系の意味検索は文字列検索の代替ではない。コア profile に含めない

## ベンチ要約（2026-08-12）

| 勝ち | 負け・使わない |
|---|---|
| rg（大ツリー grep） | 小規模 fd（find で足りる） |
| duckdb（大 CSV） | 多数ファイルを jq ループ |
| pandoc md→html/docx | pandoc md→PDF（tex 不在） |
| 既備 pymupdf | 不用意な poppler 追加 |
| host pdf/docx スキル | MCP 常駐で host tool 増設 |
