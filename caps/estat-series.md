# estat-series (optional)

**What:** Retrieve Japanese government-statistics series through the e-Stat API.  
**When:** the task needs an official series **and** the user supplied an appId in this chat.  
**Not when:** no appId is available; do not probe the API repeatedly.

## Setup

```bash
export ESTAT_APPID='user-provided-value'
```

## Use

Follow the official e-Stat API specification with `curl`; save the response in `/workspace` and extract only the requested metrics.

Do not expose the appId in logs, answers, or commits. Include the statistic name, table ID, and reference date in any reported figures.
