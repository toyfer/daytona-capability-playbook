# Daytona Capability Playbook

Scira + Daytona 向けの**追加能力カタログ**（progressive disclosure）。

- Scira のカスタム指示（always-on）は薄い入口だけ
- 詳細・注意・スクリプトは**このリポジトリだけ**
- エージェントは **INDEX → 必要な path だけ curl** で load
- playbook の取得は shell の `curl`（`retrieve` 禁止・コスト高）

**Raw base:**  
`https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

**Repo:** https://github.com/toyfer/daytona-capability-playbook

## エージェント向け（最短）

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
# INDEX の description が今のタスクに当たる path だけ:
curl -fsSL "$P/<path>" -o /tmp/cap.md   # or .sh / .py
```

Host tool（検索・bash・code_interpreter・文書 skills 等）が既定。  
playbook 能力は host より精度・一次ソース・トークン・速度で勝つときだけ使う。

## ツリー

```
.
├── INDEX.md                 # 最初に読むカタログ（what + when + path）
├── CUSTOM_INSTRUCTIONS.md   # Scira に貼る always-on 完成形
├── README.md
├── ENV.md                   # 環境インベントリ
├── HARDNO.md                # 横断の禁止
├── OPS.md                   # 運用・変更履歴
├── bin/
│   ├── bootstrap.sh         # install 唯一入口（static-first jq/rg）
│   ├── with-tools.sh
│   └── egov.py              # optional: 法令 API CLI
├── caps/                    # 能力ごとの使い方・注意
└── profiles/                # bootstrap profile の論理名一覧
```

| パス | 役割 |
|---|---|
| [INDEX.md](./INDEX.md) | 能力カタログ |
| [CUSTOM_INSTRUCTIONS.md](./CUSTOM_INSTRUCTIONS.md) | always-on 完成形 |
| [ENV.md](./ENV.md) | 何が最初からあるか |
| [HARDNO.md](./HARDNO.md) | 横断 Hard no |
| [OPS.md](./OPS.md) | 変更履歴 |
| [caps/](./caps/) | 各能力の how-to |
| [bin/bootstrap.sh](./bin/bootstrap.sh) | install |
| [bin/egov.py](./bin/egov.py) | 法令 CLI（optional） |

## 設計

1. **Progressive disclosure** — always-on に router / レシピを二重に書かない
2. **Host 既定** — 迷ったら host
3. **Install は bootstrap のみ** — `sudo` 禁止（root 直）。cli-min は static-first
4. **ドメイン非依存のコア** — 法令・e-Stat 等は optional。タスクが求めない限り load しない
5. **セッション揮発** — `/workspace` と追加 bin はチャット内のみ

## install profiles

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh cli-min    # jq + rg
# bash /tmp/bootstrap.sh data     # duckdb + sqlite3
source /workspace/.tools/env
```

| profile | 主な用途 |
|---|---|
| cli-min | jq, rg |
| cli-dev | + fd, unzip, file |
| jp-text | nkf |
| data | duckdb (py), sqlite3 |
| docs-extra | pandoc 等 |
| ocr / media | 明示時のみ（重い） |
