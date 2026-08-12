# jp-law-egov (optional)

**What:** Search Japanese statutes and retrieve primary-source articles through the e-Gov API CLI.  
**When:** a statute name, statute number, or article text is explicitly needed.  
**Not when:** general legal explanation, news, or case commentary (use host search), or when no legal source is requested.

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/egov.py" -o /tmp/egov.py
```

No API key is required.

## Use

```bash
python3 /tmp/egov.py search '個人情報の保護に関する法律'
python3 /tmp/egov.py resolve '地方自治法'
python3 /tmp/egov.py article '地方自治法' 1
python3 /tmp/egov.py text '個人情報の保護に関する法律' '仮名加工'
python3 /tmp/egov.py body '415AC0000000057' /workspace/law.xml
python3 /tmp/egov.py revisions '405AC0000000088' 5
python3 /tmp/egov.py keyword 'デジタル庁' 5
```

## Endpoints used

| command | API |
|---|---|
| search / resolve | `GET /api/2/laws` (`law_title` / `law_num` / `law_id`) |
| body / text | `GET /api/1/lawdata/{lawId}` (法令 XML) |
| article | `GET /api/1/articles;lawId=…;article=…` |
| revisions | `GET /api/2/law_revisions/{lawId}` |
| keyword | `GET /api/2/keyword?keyword=…` |

## Notes

- Keep the statute number or lawId in the answer.
- `lawrevisions` (no underscore) returns 404; use `law_revisions` via the `revisions` command.
- Accepts real lawId forms such as `322AC0000000067` and `321CONSTITUTION`.
- Prefer exact statute title when resolving; `resolve` lists candidates if ambiguous.
- Store full XML locally and quote only relevant articles.
- Do not give definitive legal advice.
