# jp-encoding

**What:** Detect and convert Japanese legacy encodings and line endings with `nkf`.  
**When:** a SJIS / CP932 / EUC text or CSV must become UTF-8.  
**Not when:** the file is already UTF-8.

## Setup

Profile: `jp-text`. Follow [bootstrap](./bootstrap.md).

## Use

```bash
nkf --guess file.csv
nkf -w -Lu file.csv > file.utf8.csv
```

## Fallback

```bash
iconv -f CP932 -t UTF-8 file.csv > file.utf8.csv
```

Guess first; an arbitrary `iconv -f` can corrupt data.
