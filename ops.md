# 運用メモ（変更履歴・方針の変遷）

> カスタム指示 §5 から、必要になったら curl で読む。
> 運用メモは GitHub で履歴管理する（カスタム指示には載せない）。

## 運用ルール

- 環境の有無は推測せず、使う直前に command -v / 小さな疎通で確認。
- 同じ失敗が 2 回起きたら、Hard no か Router 1 行だけ足す（足すより削るを先に）。
- カスタム指示が効かないときは長い版を疑って削る。
- カスタム指示は薄く保つ。詳細はこのリポジトリへ。

## 変更履歴

| 日付 | 内容 |
|---|---|
| 2026-08-12 | 初期版。e-Gov API 到達を実測確認（lawrevisions のみ 404）。lawdata/articles の正解を確定。 |
| 2026-08-12 | カスタム指示を薄型化。法令は bin/egov.py に、ツール詳細は tools.md に分離。 |
| 2026-08-12 | ルーター・ツール別 Hard no・運用メモを router.md / hard-no.md / ops.md に分離。カスタム指示は「host tool 以外を選ぶ状況 + 代替」のみに。 |

## 設計方針（なぜこうなっているか）

- **host tool が既定**。web_search / retrieve / shell / code_context / github_search / docx/pdf/artifact / weather は常時使える。
- カスタム指示は **host tool が最適でないときの代替**だけを指す。
- 詳細（ルーター・hard no・レシピ・ベンチ・職域）は GitHub に置き、curl で skills 的に参照する。
- カスタム指示は自己完結（シェルの中身・/workspace は引き継がれない）。
