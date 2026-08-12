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
python3 /tmp/egov.py article '地方自治法' 1
python3 /tmp/egov.py text '生活保護法' '外国人'
python3 /tmp/egov.py body '415AC0000000057' /workspace/law.xml
```

Keep the statute number or lawId in the answer. `lawrevisions` returns 404; do not use it. Store full XML locally and quote only relevant articles. Do not give definitive legal advice.
