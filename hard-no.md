# ツール別 Hard no

> カスタム指示 §3 から、詳細が必要になったら curl で読む。
> 常時指示には「原則」だけ載せ、ツールごとの禁止はここに集約。

## 原則

- sudo 禁止（多くは root 直。apt-get を直接）。
- セッション開始時のフル tooling bootstrap 禁止。
- バックグラウンド MCP（pm2/tmux）で「tool を増やす」禁止。
- API キーは、ユーザーがこのチャットで渡したときだけ。
- 巨大 XML/HTML をプロンプトに貼らない（/workspace に保存してスライス）。
- npm install した MCP で「新しい host tool が増えた」と主張しない。
- `find | while read; do jq ...` の多プロセス地獄をしない（多数 JSON は Python 一括）。

## ツール別

### e-Gov（法令）
- `lawrevisions` は 404（法令番号・lawId どちらでも不可）。改正履歴は lawdata の XML 内 or host web_search。
- 全文 XML は数百 KB。プロンプトに全文を貼らない。該当条だけ引用。
- 法令番号・lawId は回答に必ず残す。
- 法律相談・確定解釈の断定はしない。

### ripgrep / jq
- rg は /workspace 内のみ。GitHub 上のコード検索は host github_search。
- jq は単発ストリームのみ。多数 JSON は Python 一括（1プロセス/ファイルの jq ループ禁止）。

### duckdb
- CLI バイナリは PATH に出ないことが多い → Python API で呼ぶ。
- 小さい CSV では pandas で十分（duckdb は大きい表・SQL・複数ファイルのとき）。

### colgrep
- 初回 init は重い。一発クエリでは rg の方が安い。
- 同一巨大ツリーに複数回の意味検索のときだけ。

### pandoc
- md→PDF は pdflatex 不在で失敗する。体裁の良い 1 本の PDF は host pdf スキル。
- 一括 md→html/docx のみ。

### e-Stat
- appId なしで叩かない（実測 STATUS 100）。
- ユーザーが appId を渡したときだけ。

### selenium / playwright
- ブラウザバイナリなし。既定メニューに入れない。動的ページは host retrieve 優先。

### ffmpeg / imagemagick
- 重い。明示トリガのみ。
