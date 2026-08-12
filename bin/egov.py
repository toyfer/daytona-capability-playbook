#!/usr/bin/env python3
"""e-Gov 法令 API 薄い CLI（keyless・fix 2026-08-12）

使い方:
  python3 egov.py search    '<法令名|法令番号|lawId>' [limit]
  python3 egov.py resolve   '<法令名|法令番号|lawId>'
  python3 egov.py body      '<法令名|法令番号|lawId>' [出力先]
  python3 egov.py text      '<法令名|法令番号|lawId>' [キーワード]
  python3 egov.py article   '<法令名|法令番号|lawId>' <条番号>
  python3 egov.py revisions '<法令名|法令番号|lawId>' [limit]
  python3 egov.py keyword   '<本文キーワード>' [limit]

カスタム指示からは curl で取得して実行:
  curl -fsSL https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main/bin/egov.py -o /tmp/egov.py
  python3 /tmp/egov.py search '地方自治法'
  python3 /tmp/egov.py article '地方自治法' 1
  python3 /tmp/egov.py text '個人情報の保護に関する法律' '仮名加工'
  python3 /tmp/egov.py body '415AC0000000057' /workspace/law.xml
  python3 /tmp/egov.py revisions '405AC0000000088' 5
  python3 /tmp/egov.py keyword 'デジタル庁' 5

ポイント:
  - body/article/text/revisions は法令名・法令番号・lawId から自動解決
  - lawId は実データ形（例: 322AC0000000067, 321CONSTITUTION）を受理
  - text は属性付き <Article ...> を分割して整形表示
  - keyword は V2 本文横断検索。text は単一法令内フィルタ
  - 履歴は /api/2/law_revisions（アンダースコアあり）。lawrevisions は 404
  - 存在しない条・法令でも生 Traceback ではなくメッセージで終了
  - 確定的な法的助言はしない。条文引用時は lawId / 法令番号を残す
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape

BASE = "https://laws.e-gov.go.jp"

# 実 ID 例: 322AC0000000067, 322CO0000000016, 322M40000008029, 321CONSTITUTION
# 履歴 ID 例: 322AC0000000067_20260717_508AC0000000062
LAWID_RE = re.compile(
    r"^(?:"
    r"\d{3}CONSTITUTION"
    r"|\d{3}[A-Z]{1,4}\d{6,12}"
    r")$"
)
REVISION_ID_RE = re.compile(
    r"^\d{3}(?:CONSTITUTION|[A-Z]{1,4}\d{6,12})_\d{8}_[0-9A-Z]+$"
)
# 法令番号っぽい文字列（漢数字・元号を含む）
LAW_NUM_HINT_RE = re.compile(
    r"^(明治|大正|昭和|平成|令和).+(法律|政令|勅令|府令|省令|規則|憲法)"
)
ARTICLE_SPLIT_RE = re.compile(r"(?=<Article\b)", re.I)
ARTICLE_OPEN_RE = re.compile(r"<Article\b", re.I)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n\s*\n+")


def _fetch(url: str, timeout: int = 60) -> bytes:
    """GET して bytes を返す。エラーは親切に表示して sys.exit。"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "daytona-capability-playbook/egov.py",
                "Accept": "application/json, application/xml, text/xml, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[エラー] 404 Not Found: {url}", file=sys.stderr)
            print(
                "  指定した法令・条が存在しない可能性があります。"
                " search で lawId を確認してください。",
                file=sys.stderr,
            )
        else:
            print(f"[エラー] HTTP {e.code}: {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[エラー] 通信に失敗しました: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)


def _fetch_json(url: str, timeout: int = 30) -> dict:
    try:
        return json.loads(_fetch(url, timeout).decode("utf-8"))
    except json.JSONDecodeError:
        print(f"[エラー] JSON を解釈できませんでした: {url}", file=sys.stderr)
        sys.exit(1)


def _strip_tags(s: str) -> str:
    s = TAG_RE.sub("", s)
    s = unescape(s)
    s = WS_RE.sub(" ", s)
    s = BLANK_RE.sub("\n", s)
    return s.strip()


def _is_law_id(ident: str) -> bool:
    return bool(LAWID_RE.match(ident) or REVISION_ID_RE.match(ident))


def _laws_query(**params) -> dict:
    q = {k: v for k, v in params.items() if v is not None and v != ""}
    url = BASE + "/api/2/laws?" + urllib.parse.urlencode(q)
    return _fetch_json(url, 30)


def _pick_best_law(laws: list, ident: str) -> dict | None:
    """完全一致の題名 / 法令番号 / lawId を優先し、なければ先頭。"""
    if not laws:
        return None
    ident_n = ident.strip()
    exact = []
    for law in laws:
        li = law.get("law_info") or {}
        ri = law.get("revision_info") or {}
        title = (ri.get("law_title") or "").strip()
        num = (li.get("law_num") or "").strip()
        lid = (li.get("law_id") or "").strip()
        if ident_n in (title, num, lid):
            exact.append(law)
    if exact:
        # 題名完全一致を最優先
        for law in exact:
            ri = law.get("revision_info") or {}
            if (ri.get("law_title") or "").strip() == ident_n:
                return law
        return exact[0]
    return laws[0]


def _search_laws(ident: str, limit: int = 10) -> list:
    """title / law_num / law_id の順で V2 /laws を試す。"""
    ident = ident.strip()
    if not ident:
        return []

    tried = []

    def run(**kwargs):
        d = _laws_query(limit=limit, **kwargs)
        laws = d.get("laws") or []
        tried.append((kwargs, len(laws), d.get("total_count", 0)))
        return laws, d.get("total_count", 0)

    # lawId / revisionId 直指定
    if _is_law_id(ident):
        # revision id の場合は先頭の lawId 部分で一覧
        base_id = ident.split("_", 1)[0]
        laws, _ = run(law_id=base_id)
        if laws:
            return laws

    # 法令番号っぽい
    if LAW_NUM_HINT_RE.search(ident) or "号" in ident:
        laws, _ = run(law_num=ident)
        if laws:
            return laws

    # 題名（既定）
    laws, _ = run(law_title=ident)
    if laws:
        return laws

    # フォールバック: law_num / law_id を念のため
    for key in ("law_num", "law_id"):
        laws, _ = run(**{key: ident})
        if laws:
            return laws

    return []


def _resolve_law_id(ident: str, quiet: bool = False) -> str:
    """lawId / revisionId ならそのまま、それ以外は search で解決。"""
    ident = ident.strip()
    if REVISION_ID_RE.match(ident):
        return ident
    if LAWID_RE.match(ident):
        return ident

    laws = _search_laws(ident, limit=10)
    if not laws:
        print(f"[エラー] '{ident}' に一致する法令が見つかりませんでした。", file=sys.stderr)
        sys.exit(1)

    best = _pick_best_law(laws, ident)
    li = best.get("law_info") or {}
    ri = best.get("revision_info") or {}
    lid = li.get("law_id")
    if not lid:
        print("[エラー] lawId を取得できませんでした。", file=sys.stderr)
        sys.exit(1)

    if not quiet:
        title = ri.get("law_title") or ""
        num = li.get("law_num") or ""
        print(f"[info] '{ident}' -> {title} | {num} | {lid}", file=sys.stderr)
        if len(laws) > 1:
            # 完全一致でないときだけ候補を軽く出す
            titles = [(x.get("revision_info") or {}).get("law_title") for x in laws[:5]]
            if (ri.get("law_title") or "").strip() != ident.strip():
                print(f"[info] 他候補: {', '.join(t for t in titles if t)}", file=sys.stderr)
    return lid


def search(title: str, limit: int = 5) -> None:
    laws = _search_laws(title, limit=limit)
    # total は API から取り直す（表示用）
    d = None
    ident = title.strip()
    if _is_law_id(ident):
        d = _laws_query(law_id=ident.split("_", 1)[0], limit=limit)
    elif LAW_NUM_HINT_RE.search(ident) or "号" in ident:
        d = _laws_query(law_num=ident, limit=limit)
    else:
        d = _laws_query(law_title=ident, limit=limit)
    total = (d or {}).get("total_count", len(laws))
    print(f"total: {total}")
    shown = laws or (d or {}).get("laws") or []
    for law in shown[:limit]:
        ri, li = law.get("revision_info") or {}, law.get("law_info") or {}
        print(
            f"- {ri.get('law_title')} | {li.get('law_num')} | {li.get('law_id')}"
        )
    if not shown:
        print("  （該当なし）")


def resolve(title: str) -> None:
    laws = _search_laws(title, limit=15)
    if not laws:
        print("  （該当なし）")
        return
    for law in laws:
        ri, li = law.get("revision_info") or {}, law.get("law_info") or {}
        print(f"{li.get('law_id')}  {ri.get('law_title')}  ({li.get('law_num')})")


def body(ident: str, out: str = "/tmp/law.xml") -> None:
    lid = _resolve_law_id(ident)
    # revision id のときは V1 は lawId 部分のみ受け付けることが多いので分離
    path_id = lid.split("_", 1)[0] if REVISION_ID_RE.match(lid) else lid
    url = BASE + "/api/1/lawdata/" + urllib.parse.quote(path_id)
    data = _fetch(url, 90)
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {out} ({len(data)} bytes)  lawId={path_id}")


def _iter_articles(xml: str):
    parts = ARTICLE_SPLIT_RE.split(xml)
    for part in parts:
        if not ARTICLE_OPEN_RE.search(part):
            continue
        # 条ブロックは次のトップレベル要素手前までに限定（雑だが実用）
        # part 自体が split 済みなのでそのまま使う
        yield part


def text(ident: str, keyword: str | None = None) -> None:
    lid = _resolve_law_id(ident)
    path_id = lid.split("_", 1)[0] if REVISION_ID_RE.match(lid) else lid
    url = BASE + "/api/1/lawdata/" + urllib.parse.quote(path_id)
    xml = _fetch(url, 90).decode("utf-8", "replace")

    shown = 0
    max_show = 40 if keyword else 15
    for part in _iter_articles(xml):
        t = _strip_tags(part)
        if not t:
            continue
        if keyword and keyword not in t:
            continue
        # 長すぎる条は先頭を切る
        if len(t) > 2000:
            t = t[:2000] + "…"
        print(t)
        print("----")
        shown += 1
        if shown >= max_show:
            print(f"[info] {max_show} 件で打ち切り（さらに見る場合は keyword を絞る）", file=sys.stderr)
            break

    if shown == 0:
        if keyword:
            print(
                f"[info] 該当条文がありませんでした（キーワード '{keyword}'）。"
                " 横断検索は: egov.py keyword '<語>'",
                file=sys.stderr,
            )
        else:
            print("[info] 条文を抽出できませんでした。", file=sys.stderr)


def article(ident: str, n: str) -> None:
    lid = _resolve_law_id(ident)
    path_id = lid.split("_", 1)[0] if REVISION_ID_RE.match(lid) else lid
    # 条番号は数字・漢数字両対応のため API にそのまま渡す
    n = str(n).strip()
    # 「第一条」や「第1条」を数字に正規化（簡単なケース）
    m = re.match(r"^第?([0-9０-９]+)条?$", n)
    if m:
        n = m.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    url = f"{BASE}/api/1/articles;lawId={urllib.parse.quote(path_id)};article={urllib.parse.quote(n)}"
    xml = _fetch(url, 30).decode("utf-8", "replace")

    # Result code
    code_m = re.search(r"<Code>(\d+)</Code>", xml)
    if code_m and code_m.group(1) != "0":
        msg_m = re.search(r"<Message>(.*?)</Message>", xml, re.S)
        msg = _strip_tags(msg_m.group(1)) if msg_m else ""
        print(f"[info] API Result Code={code_m.group(1)} {msg}", file=sys.stderr)

    captions = re.findall(r"<ArticleCaption[^>]*>(.*?)</ArticleCaption>", xml, re.S)
    titles = re.findall(r"<ArticleTitle[^>]*>(.*?)</ArticleTitle>", xml, re.S)
    for c in captions[:2]:
        print("Caption:", _strip_tags(c))
    for t in titles[:2]:
        print("Title:", _strip_tags(t))

    # 項ごとに出す
    paragraphs = re.findall(r"<Paragraph\b[^>]*>(.*?)</Paragraph>", xml, re.S)
    if paragraphs:
        for i, p in enumerate(paragraphs, 1):
            num_m = re.search(r"<ParagraphNum[^>]*>(.*?)</ParagraphNum>", p, re.S)
            label = _strip_tags(num_m.group(1)) if num_m and num_m.group(1).strip() else str(i)
            sents = re.findall(r"<Sentence\b[^>]*>(.*?)</Sentence>", p, re.S)
            body_txt = "".join(_strip_tags(s) for s in sents)
            if body_txt:
                print(f"¶{label}: {body_txt}")
    else:
        sentences = re.findall(r"<Sentence\b[^>]*>(.*?)</Sentence>", xml, re.S)
        for s in sentences:
            print("Sentence:", _strip_tags(s))

    if not titles and not paragraphs and not re.search(r"<Sentence\b", xml):
        print(
            f"[info] 条 {n} の本文が見つかりませんでした（存在しない条の可能性）。",
            file=sys.stderr,
        )


def revisions(ident: str, limit: int = 10) -> None:
    """V2 /law_revisions（正しいパス。lawrevisions は 404）。"""
    lid = _resolve_law_id(ident)
    path_id = lid.split("_", 1)[0] if REVISION_ID_RE.match(lid) else lid
    url = BASE + "/api/2/law_revisions/" + urllib.parse.quote(path_id)
    d = _fetch_json(url, 30)
    li = d.get("law_info") or {}
    print(f"law: {li.get('law_num')} | {li.get('law_id')}")
    revs = d.get("revisions") or []
    print(f"revisions: {len(revs)} (show {min(limit, len(revs))})")
    for rev in revs[:limit]:
        print(
            f"- {rev.get('law_revision_id')} | "
            f"title={rev.get('law_title')} | "
            f"amend={rev.get('amendment_promulgate_date')} | "
            f"enforce={rev.get('amendment_enforcement_date')} | "
            f"status={rev.get('current_revision_status')} | "
            f"mission={rev.get('mission')} | "
            f"amendment_type={rev.get('amendment_type')}"
        )
    if not revs:
        print("  （履歴なし）")


def keyword(kw: str, limit: int = 10) -> None:
    """V2 /keyword 本文横断検索。"""
    kw = kw.strip()
    if not kw:
        print("[エラー] keyword が空です。", file=sys.stderr)
        sys.exit(1)
    url = BASE + "/api/2/keyword?" + urllib.parse.urlencode(
        {"keyword": kw, "limit": limit, "sentences_limit": 3}
    )
    d = _fetch_json(url, 60)
    print(
        f"total: {d.get('total_count')}  sentence_count: {d.get('sentence_count')}  "
        f"next_offset: {d.get('next_offset')}"
    )
    items = d.get("items") or []
    for item in items[:limit]:
        li = item.get("law_info") or {}
        ri = item.get("revision_info") or {}
        print(
            f"- {ri.get('law_title')} | {li.get('law_num')} | {li.get('law_id')}"
        )
        for s in (item.get("sentences") or [])[:3]:
            pos = s.get("position") or ""
            txt = _strip_tags(s.get("text") or "")
            if len(txt) > 200:
                txt = txt[:200] + "…"
            print(f"    [{pos}] {txt}")
    if not items:
        print("  （該当なし）")


def _usage() -> None:
    print(__doc__)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        _usage()
        sys.exit(0)
    cmd = args[0]
    if cmd in ("-h", "--help", "help"):
        _usage()
    elif cmd == "search" and len(args) >= 2:
        search(args[1], int(args[2]) if len(args) > 2 else 5)
    elif cmd == "resolve" and len(args) >= 2:
        resolve(args[1])
    elif cmd == "body" and len(args) >= 2:
        body(args[1], args[2] if len(args) > 2 else "/tmp/law.xml")
    elif cmd == "text" and len(args) >= 2:
        text(args[1], args[2] if len(args) > 2 else None)
    elif cmd == "article" and len(args) >= 3:
        article(args[1], args[2])
    elif cmd == "revisions" and len(args) >= 2:
        revisions(args[1], int(args[2]) if len(args) > 2 else 10)
    elif cmd == "keyword" and len(args) >= 2:
        keyword(args[1], int(args[2]) if len(args) > 2 else 10)
    else:
        _usage()
        sys.exit(1)
