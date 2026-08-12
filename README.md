# Daytona Capability Playbook

Scira + Daytona 向けの**追加能力カタログ**。

- Scira のカスタム指示（always-on）は薄い入口だけを持つ
- 詳細・ルーティング・注意・スクリプトは**このリポジトリだけ**に置く
- エージェントは skill と同じく **INDEX → 必要な path だけ curl** で load する
- `retrieve` でここを取らない（コスト高）。shell の `curl` を使う

**Raw base:**
`https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## エージェント向け（最短）

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
# INDEX の description が今のタスクに当たる path だけ:
curl -fsSL "$P/<path>" -o /tmp/cap.md   # or .sh / .py
```

Host tool（検索・bash・code_interpreter・文書 skills 等）が既定。
playbook 能力は host より精度・一次ソース・トークン・速度で勝つときだけ使う。

## 人間向けマップ

| パス | 役割 |
|---|---|
| [`INDEX.md`](./INDEX.md) | 能力カタログ（id / what+when / path / profile） |
| [`ENV.md`](./ENV.md) | 環境インベントリ（実測） |
| [`HARDNO.md`](./HARDNO.md) | 横断の禁止事項 |
| [`OPS.md`](./OPS.md) | 変更履歴・運用 |
| [`CUSTOM_INSTRUCTIONS.md`](./CUSTOM_INSTRUCTIONS.md) | Scira に貼る always-on 完成形 |
| [`caps/`](./caps/) | 能力ごとの使い方・注意 |
| [`bin/bootstrap.sh`](./bin/bootstrap.sh) | install の唯一入口 |
| [`bin/egov.py`](./bin/egov.py) | 法令 API CLI（optional cap） |
| [`profiles/`](./profiles/) | bootstrap profile の論理ツール一覧 |

## 設計（短く）

1. **Progressive disclosure** — always-on に router 表やレシピを二重に書かない
2. **Host 既定** — 迷ったら host
3. **Install は bootstrap のみ** — `sudo` 禁止（root 直）。cli-min は static-first
4. **ドメイン非依存のコア** — 法令などは optional cap。タスクが求めない限り load しない
5. **セッション揮発** — `/workspace` と追加 bin はチャット内のみ。必要なら都度 curl / bootstrap

## 旧ファイル

`router.md` / `tools.md` / `hard-no.md` / `ops.md` / `egov-cli.md` / `daytona-capability-playbook.md` は v3 で廃止。
内容は `INDEX.md` + `caps/*` + `ENV.md` + `HARDNO.md` + `OPS.md` に吸収済み。
