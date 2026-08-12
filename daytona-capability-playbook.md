# Daytona Capability Playbook（詳細版）

> 検証日: 2026-08-12。このファイルはカスタム指示の **§5 外部管理** から必要時に参照される。
> 常時コンテキストには載せない。コマンドレシピ・環境インベントリ・ベンチ・職域 Appendix をここに置く。

---

## 1. 環境インベントリ（実測 2026-08-12）

### プラットフォーム

| 項目 | 実測値 |
|---|---|
| OS | Debian 12 (bookworm), Linux x86_64 |
| ユーザー | `root`（sudo なし・不要） |
| ディスク | overlay 約 10G（site-packages が数 GB 済みのことも） |
| 作業領域 | `/workspace`（同一セッション内で永続） |
| ネット | 一般 HTTPS 可。e-Gov / zipcloud / JMA / data.e-gov 等で 200 確認 |
| Node / Python | Node 18.20.4 / Python 3.12.10 / `uv` あり |
| Java | OpenJDK 17（tabula と併用可） |
| GPU | torch は入るが CUDA 不可（CPU） |

### 初期から使える（入れ直すな）

**CLI / ランタイム**: `bash`, `curl`, `git`, `node`, `npm`, `npx`, `python3`, `pip3`, `uv`, `perl`, `java`, `gcc`/`g++`/`make`, `tar`/`gzip`/`xz`, `openssl`, `ssh`/`scp`, `timeout`, `iconv`, 基本 GNU coreutils, `nohup`

**Python（特に有用・既にあり）**: `pymupdf` (fitz), `pdfplumber`, `pdfminer`, `pypdfium2`, `tabula`, `bs4`, `lxml`, `parsel`, `scrapy`, `httpx`, `requests`, `aiohttp`, `pandas`, `numpy`, `scipy`, `sklearn`, `networkx`, stdlib `sqlite3`/`csv`/`json`/`xml`, `pydantic`, `rich`, `jinja2`, `seaborn`, `matplotlib`, `plotly`, `yfinance`

**なし（必要時 install）**: `jq`, `rg`/`ripgrep`, `fd`, `bat`, `fzf`, `pandoc`, `sqlite3` CLI, `ffmpeg`, `tesseract`, `poppler`/`pdftotext`, `qpdf`, `nkf`, `yq`, `wget`, `docker`, ブラウザ本体, `duckdb`, `openpyxl`, `python-docx`, `reportlab`, `trafilatura`, `jaconv`, `weasyprint`, `playwright`

**注意**: `selenium` は入っているが **Chrome/Chromium/driver なし** → 実質ほぼ使えない。Playwright も初期なし・重い。

---

## 2. コマンドレシピ

### 2.1 e-Gov 法令（検証済み・詳細は egov-cli.md へ）

```bash
# 検索（v2・JSON）
curl -sS --get 'https://laws.e-gov.go.jp/api/2/laws' \
  --data-urlencode 'law_title=地方自治法' \
  --data-urlencode 'limit=5' | python3 -m json.tool | head -200

# 全文（v1・XML）
curl -sS "https://laws.e-gov.go.jp/api/1/lawdata/平成十五年法律第五十七号" -o /tmp/law.xml

# 条文（v1・XML）
curl -sS "https://laws.e-gov.go.jp/api/1/articles;lawId=415AC0000000057;article=1" -o /tmp/art.xml
```

### 2.2 検索・整形（オンデマンド install）

```bash
apt-get update
apt-get install -y ripgrep jq          # cli-min
apt-get install -y nkf                 # jp-text
apt-get install -y sqlite3 && pip install duckdb   # data
apt-get install -y pandoc poppler-utils tesseract-ocr tesseract-ocr-jpn qpdf  # docs-convert
apt-get install -y ffmpeg imagemagick  # media（重い・明示時のみ）
```

### 2.3 大 CSV 集計（duckdb は CLI バイナリが出ないことが多い）

```python
import duckdb
print(duckdb.sql("SELECT col, count(*) FROM 'data.csv' GROUP BY 1 ORDER BY 2 DESC LIMIT 20").fetchdf())
```

### 2.4 日本語レガシー

```bash
nkf --guess file.csv
nkf -w -Lu file.csv > file.utf8.csv
curl -sS 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=1000001' | python3 -m json.tool
curl -sS --get 'https://data.e-gov.go.jp/data/api/action/package_search' --data-urlencode 'q=自治体' --data-urlencode 'rows=5' | python3 -m json.tool | head -100
```

---

## 3. ベンチ（実測）

| タスク | 素のシェル | 拡張 | 勝敗 |
|---|---|---|---|
| 大ツリー grep | grep -R 0.085s | rg 0.022s | **rg 約3.8倍速** |
| ファイル名検索 | find 0.009s | fd 0.15s | **find の勝ち（小規模）** |
| 多数 JSON 集計 | ファイル毎 jq 7.7s/500件 | Python 一括 0.1s | **Python 一括** |
| 100万行 CSV | pandas 0.9-1.1s | duckdb 0.48-0.5s | **duckdb 約2倍** |
| md→html/docx | — | pandoc 0.03-0.04s | pandoc 有効 |
| md→PDF | — | 失敗（pdflatex 不在） | host pdf 優先 |
| MCP 常駐 | — | — | **host tool は増えない** |

**結論**: 勝ちは `rg` / `duckdb` / `pandoc`(html/docx) / `sqlite3`。負けは乱用 jq、小規模 fd、常時 trafilatura、**MCP 常駐**、pandoc PDF。

---

## 4. MCP の扱い

```
MCP = 「パッケージされたドメイン能力」の別名であって、「host に新しい tool カードを生やす装置」ではない。
```

| やり方 | 可否 |
|---|---|
| ドメイン API/CLI を直接叩く | 推奨 |
| 一発 stdio で spawn→tools/call→終了 | 中身に非自明ロジックがあるときだけ |
| pm2/tmux 常駐で host tool 増設 | **不可** |
| キー必須 SaaS MCP | キーがチャットに無いなら不可 |

---

## 5. 職域 Appendix（あとがき）

### A-1. 法令検索（自治体職員・優先）

- **Trigger**: 条例案務、国の法律・政省令の根拠確認、法令番号確定、改正の有無、事務の法的根拠
- **Primary**: e-Gov API v2 検索 → v1 lawdata / articles（egov-cli.md 参照）
- **Auth**: keyless
- **Fallback**: 公式 e-Gov 法令検索ページを host retrieve。それでもダメなら web_search
- **Token notes**: 回答に載せるのは該当条項 + 法令番号 + 改正の要点。XML 全文禁止
- **Do not**: ブログ要約を一次根拠扱い；法的助言の断定；MCP 常駐

### A-2. 政府統計（e-Stat・キー必須）

- **Trigger**: 人口・産業など公的統計の数値系列
- **Primary**: e-Stat API（要 application ID）
- **Auth**: user-provided-key（ユーザーが appId を渡したときだけ）
- **Fallback**: ユーザーに appId を求める / e-Stat 画面から CSV を落としてもらい duckdb
- **Do not**: appId なしで認証エラーを連打

### A-3. コーディング docs（Context7）

- **Trigger**: 実装タスクで現行 API が要る
- **Primary**: Context7 CLI（キー無し・レート制限あり）→ host code_context
- **Auth**: keyless。ユーザーが CONTEXT7_API_KEY を渡したら使う
- **Fallback**: code_context → 公式 docs

---

## 6. 除外理由（入れないもの）

| 候補 | 理由 |
|---|---|
| filesystem/memory MCP 常駐 | host の bash/read/write と重複。tool 面も増えない |
| e-Stat をキーレス既定 | 実測 STATUS 100（要 appId） |
| selenium/playwright 既定化 | ブラウザバイナリなし / 重い |
| RESAS API | 提供終了・新規停止の案内あり |
| 毎回 colgrep init | 一発クエリでは rg の方が安い |
| cargo 依存の大量 CLI | toolchain 前提が脆い |
| フル texlive で pandoc PDF | ディスク破壊的。1 本の PDF は host pdf スキル |

---

## 7. 変更履歴

| 日付 | 内容 |
|---|---|
| 2026-08-12 | e-Gov API 到達を実測確認（lawrevisions のみ 404）。lawdata/articles の正解を確定。常時指示から詳細を分離して外部管理化。 |
