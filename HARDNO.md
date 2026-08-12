# Hard no（横断）

能力固有の禁止は各 `caps/*.md` にも書く。ここは横断だけ。

## 原則

1. **`sudo` 禁止**（root 直で apt / バイナリ配置）
2. **セッション開始フル bootstrap 禁止**（使う profile だけ・使う直前）
3. **手組み apt 禁止** — install は `bin/bootstrap.sh` のみ
4. **playbook を retrieve しない** — shell の `curl`
5. **API キーはチャットでユーザーが渡したときだけ**
6. **巨大 XML/HTML/ログを回答に貼らない** — `/workspace` に置いてスライス
7. **無いコマンドをあると言うな** — `command -v` または bootstrap
8. **MCP を pm2/tmux 常駐させて host tool が増えたように振る舞わない**
9. **多数 JSON を `find … -exec jq` で回さない** — Python 一括
10. **INDEX に無い能力を常設化しない**

## よくある失敗

| 失敗 | 代わり |
|---|---|
| `sudo apt-get install jq` | `bash bootstrap.sh cli-min` |
| apt update なし install → 404 | bootstrap（内部で update 1 回） |
| 毎ターン INDEX も cap も取り直し | `/workspace` に残っていれば再利用 |
| 小 CSV に duckdb | pandas |
| テキスト PDF に tesseract | pymupdf / pdfplumber |
| 綺麗な 1 本 PDF を pandoc | host `pdf` スキル |
| GitHub 上のコードを rg | host `github_search` |
