#!/usr/bin/env python3
"""e-Gov 法令 API 薄い CLI（keyless・ブラッシュアップ版 2026-08-12）

使い方:
  python3 egov.py search  '<法令名>' [limit]
  python3 egov.py resolve '<法令名>'
  python3 egov.py body    '<法令番号 or lawId or 法令名>' [出力先]
  python3 egov.py text    '<法令番号 or lawId or 法令名>' [キーワード]
  python3 egov.py article '<法令番号 or lawId or 法令名>' <条番号>

カスタム指示からは curl で取得して実行:
  curl -sS https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main/bin/egov.py -o /tmp/egov.py
  python3 /tmp/egov.py search '地方自治法'
  python3 /tmp/egov.py article '地方自治法施行令' 163
  python3 /tmp/egov.py text '生活保護法' '外国人'

ポイント:
  - body/article/text は法令名・法令番号から lawId を自動解決する
  - 存在しない条・法令でも生の Traceback ではなく親切なメッセージで終了
  - text は生XMLでなく整形済み条文を表示
"""
import sys, json, re, urllib.parse, urllib.request, urllib.error

BASE = "https://laws.e-gov.go.jp"
LAWID_RE = re.compile(r"^\d{3}[A-Z]\d{9}$")


def _fetch(url, timeout=60):
    """GET して bytes を返す。エラーは親切に表示して sys.exit。"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[エラー] 404 Not Found: {url}", file=sys.stderr)
            print("  指定した法令・条が存在しない可能性があります。search で lawId を確認してください。", file=sys.stderr)
        else:
            print(f"[エラー] HTTP {e.code}: {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[エラー] 通信に失敗しました: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)


def _resolve_law_id(ident):
    """lawId ならそのまま、それ以外は search API で解決して最初の lawId を返す。"""
    ident = ident.strip()
    if LAWID_RE.match(ident):
        return ident
    url = BASE + "/api/2/laws?" + urllib.parse.urlencode({"law_title": ident, "limit": 5})
    try:
        d = json.loads(_fetch(url, 30).decode("utf-8"))
    except json.JSONDecodeError:
        print(f"[エラー] 検索APIの応答を解釈できませんでした: {ident}", file=sys.stderr)
        sys.exit(1)
    laws = d.get("laws", [])
    if not laws:
        print(f"[エラー] '{ident}' に一致する法令が見つかりませんでした。", file=sys.stderr)
        sys.exit(1)
    first = laws[0]
    lid = first.get("law_info", {}).get("law_id")
    if not lid:
        print("[エラー] lawId を取得できませんでした。", file=sys.stderr)
        sys.exit(1)
    print(f"[info] '{ident}' -> {first.get('revision_info', {}).get('law_title')} | {lid}", file=sys.stderr)
    return lid


def search(title, limit=5):
    url = BASE + "/api/2/laws?" + urllib.parse.urlencode({"law_title": title, "limit": limit})
    d = json.loads(_fetch(url, 30).decode("utf-8"))
    total = d.get("total_count", 0)
    print(f"total: {total}")
    for law in d.get("laws", []):
        ri, li = law.get("revision_info", {}), law.get("law_info", {})
        print(f"- {ri.get('law_title')} | {li.get('law_num')} | {li.get('law_id')}")
    if not d.get("laws"):
        print("  （該当なし）")


def resolve(title):
    url = BASE + "/api/2/laws?" + urllib.parse.urlencode({"law_title": title, "limit": 10})
    d = json.loads(_fetch(url, 30).decode("utf-8"))
    for law in d.get("laws", []):
        ri, li = law.get("revision_info", {}), law.get("law_info", {})
        print(f"{li.get('law_id')}  {ri.get('law_title')}  ({li.get('law_num')})")


def body(ident, out="/tmp/law.xml"):
    lid = _resolve_law_id(ident)
    url = BASE + "/api/1/lawdata/" + urllib.parse.quote(lid)
    data = _fetch(url, 60)
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {out} ({len(data)} bytes)  lawId={lid}")


def _clean(xml):
    text = re.sub(r"<[^>]+>", "", xml)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def text(ident, keyword=None):
    lid = _resolve_law_id(ident)
    url = BASE + "/api/1/lawdata/" + urllib.parse.quote(lid)
    xml = _fetch(url, 60).decode("utf-8", "replace")
    parts = re.split(r"(?=<Article>)", xml)
    shown = 0
    for part in parts:
        if "<Article>" not in part:
            continue
        t = _clean(part)
        if not t:
            continue
        if keyword and keyword not in t:
            continue
        print(t)
        print("----")
        shown += 1
    if shown == 0:
        print(f"[info] 該当条文がありませんでした（キーワード '{keyword}' の誤り？）", file=sys.stderr)


def article(ident, n):
    lid = _resolve_law_id(ident)
    url = f"{BASE}/api/1/articles;lawId={lid};article={n}"
    xml = _fetch(url, 30).decode("utf-8", "replace")
    titles = re.findall(r"<ArticleTitle[^>]*>(.*?)</ArticleTitle>", xml, re.S)
    for m in titles[:2]:
        print("Title:", re.sub(r"<[^>]+>", "", m).strip())
    sentences = re.findall(r"<Sentence[^>]*>(.*?)</Sentence>", xml, re.S)
    for m in sentences[:3]:
        print("Sentence:", re.sub(r"<[^>]+>", "", m).strip())
    if not titles and not sentences:
        print(f"[info] 条 {n} の本文が見つかりませんでした（存在しない条の可能性）。", file=sys.stderr)


def _usage():
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
    else:
        _usage()
        sys.exit(1)
