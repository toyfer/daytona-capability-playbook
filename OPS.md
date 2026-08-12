# 運用

## ルール

- 環境の有無は `command -v` または bootstrap 出力で確認（記憶で断言しない）
- 同じ失敗が 2 回起きたら、該当 `caps/*.md` か `HARDNO.md` に **1 行だけ**足す。足す前に削れないか見る
- always-on（`CUSTOM_INSTRUCTIONS.md`）に router 表やレシピを戻さない
- INDEX の description は **what + when** を一行。手順は caps へ
- バージョンピン（jq/rg URL）を上げたら ENV の実測日を更新

## 変更履歴

| 日付 | 内容 |
|---|---|
| 2026-08-12 | v1: e-Gov 実測、router/tools/hard-no 分離 |
| 2026-08-12 | **v3 フルスクラッチ**: progressive disclosure（INDEX + caps）、bootstrap static-first、ドメイン非依存コア、旧散在 md 廃止、CUSTOM_INSTRUCTIONS をリポジトリ同梱 |
