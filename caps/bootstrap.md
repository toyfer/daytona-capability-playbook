# bootstrap

**What:** session-local install entrypoint for optional CLI / Python tools.  
**When:** a selected cap names a profile and `command -v` confirms the required command is absent.  
**Not when:** session start, host tools suffice, or a cap needs no profile.

## Use

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh <profile>
source /workspace/.tools/env
```

Multiple profiles are allowed: `bash /tmp/bootstrap.sh cli-min data`.

| profile | installs | used by |
|---|---|---|
| `cli-min` | jq, rg | workspace-search, json-pipe |
| `cli-dev` | jq, rg, fd, unzip, file | explicit development work |
| `jp-text` | nkf | jp-encoding |
| `data` | duckdb Python package, sqlite3 | data-sql |
| `docs-extra` | pandoc, poppler-utils, qpdf | docs-convert |
| `ocr` | tesseract, Japanese language data | ocr-scan |
| `media` | ffmpeg, ImageMagick | media-ffmpeg |

## Contract

- Installs live under `/workspace/.tools`; they are session-local.
- jq / rg use pinned static releases; apt-backed profiles run `apt-get update` once per session.
- The marker makes repeated profile installs no-op.
- `sudo` and hand-written `apt-get install` commands are not used.
- If setup fails, use the fallback stated by the selected cap or return to host tools.
