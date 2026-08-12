#!/usr/bin/env python3
"""e-Gov 法令 API 薄い CLI（検証済み 2026-08-12・keyless）

使い方:
  python3 egov.py search '<法令名>' [limit]
  python3 egov.py body '<法令番号 or lawId>'
  python3 egov.py article <lawId> <条番号>

カスタム指示からは curl で取得して実行:
  curl -sS https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main/bin/egov.py -o /tmp/egov.py
  python3 /tmp/egov.py search '地方自治法'
"""
import sys, json, re, urllib.parse, urllib.request

BASE = "https://laws.e-gov.go.jp"


def search(title, limit=5):
    url = BASE + "/api/2/laws?" + urllib.parse.urlencode({"law_title": title, "limit": limit})
    d = json.load(urllib.request.urlopen(url, timeout=30))
    print("total:", d.get("total_count"))
    for law in d.get("laws", []):
        ri, li = law.get("revision_info", {}), law.get("law_info", {})
        print(f"- {ri.get('law_title')} | {li.get('law_num')} | {li.get('law_id')}")


def body(ident):
    url = BASE + "/api/1/lawdata/" + urllib.parse.quote(ident)
    data = urllib.request.urlopen(url, timeout=60).read()
    open("/tmp/law.xml", "wb").write(data)
    print(f"saved /tmp/law.xml ({len(data)} bytes)")


def article(law_id, n):
    url = f"{BASE}/api/1/articles;lawId={law_id};article={n}"
    xml = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "replace")
    for m in re.findall(r"<ArticleTitle[^>]*>(.*?)</ArticleTitle>", xml, re.S)[:2]:
        print("Title:", re.sub(r"<[^>]+>", "", m).strip())
    for m in re.findall(r"<Sentence[^>]*>(.*?)</Sentence>", xml, re.S)[:3]:
        print("Sentence:", re.sub(r"<[^>]+>", "", m).strip())


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "search" and len(sys.argv) > 2:
        search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5)
    elif cmd == "body" and len(sys.argv) > 2:
        body(sys.argv[2])
    elif cmd == "article" and len(sys.argv) > 3:
        article(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        print("usage: egov search '<法令名>' [limit] | egov body '<法令番号 or lawId>' | egov article <lawId> <条>")
