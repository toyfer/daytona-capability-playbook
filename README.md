# Daytona Capability Playbook

Scira + Daytona ヘッドレス環境の**能力ルーティング詳細版**。

カスタム指示（always-on）は薄く、**「host tool 以外を選ぶべき状況と代替」だけ**を載せる。詳細はこのリポジトリを必要時に curl で読む（retrieve は使わない・コスト高い）。

## ファイル構成

| ファイル | 内容 | 読み方 |
|---|---|---|
| `router.md` | **ルーター**（host tool 以外を選ぶ状況 → 代替） | `curl -sS .../router.md` |
| `hard-no.md` | **ツール別 Hard no** | `curl -sS .../hard-no.md` |
| `ops.md` | **運用メモ**（変更履歴・方針） | `curl -sS .../ops.md` |
| `tools.md` | 追加ツールセット・キーレス API・ベンチ・除外理由 | `curl -sS .../tools.md` |
| `bin/egov.py` | e-Gov 法令 CLI（検証済み） | `curl -sS .../bin/egov.py -o /tmp/egov.py && python3 /tmp/egov.py search '地方自治法'` |
| `daytona-capability-playbook.md` | 旧詳細版（コマンドレシピ・インベントリ・職域 Appendix） | `curl -sS .../daytona-capability-playbook.md` |
| `egov-cli.md` | e-Gov 専用手順（旧・詳細） | `curl -sS .../egov-cli.md` |

## 使い方

カスタム指示 §2 のルーターで代替を選んだら、該当ファイルを `curl` で読んで実行する。

> 検証日: 2026-08-12。e-Gov API はシェルから到達確認済み（lawrevisions のみ 404）。
