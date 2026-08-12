# Daytona Capability Playbook

Scira + Daytona ヘッドレス環境の**能力ルーティング詳細版**。

カスタム指示（always-on）は薄い方針・ルーター・Hard no だけを載せ、**詳細はこの playbook を必要時に curl で読む**（progressive disclosure）。

## ファイル構成

| ファイル | 内容 | 読み方 |
|---|---|---|
| `bin/egov.py` | e-Gov 法令 API の薄い CLI（検証済み） | `curl -sS .../bin/egov.py -o /tmp/egov.py && python3 /tmp/egov.py search '地方自治法'` |
| `tools.md` | 追加ツールセット・キーレス API・ベンチ・除外理由 | `curl -sS .../tools.md` |
| `daytona-capability-playbook.md` | 旧詳細版（コマンドレシピ・インベントリ・職域 Appendix） | `curl -sS .../daytona-capability-playbook.md` |
| `egov-cli.md` | e-Gov 専用手順（旧・詳細） | `curl -sS .../egov-cli.md` |

## 使い方

カスタム指示の §5 に従い、法令・ツール詳細が必要になったら、このリポジトリの該当ファイルを `curl` で読んでから実行する。`retrieve` は使わない（コスト高い）。

> 検証日: 2026-08-12。e-Gov API はシェルから到達確認済み（lawrevisions のみ 404）。
