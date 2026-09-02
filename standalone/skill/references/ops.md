# AZbot ops — export, queue, gated publish

## Export graphs / findings

```bash
python3 app/export_findings.py --name NAME --in-json rows.json --out out --x t --y v
```

Writes JSONL, CSV, and if x/y given PNG + SVG.

## Autonomous local runner

Queue files in `queue/*.json`. Then:

```bash
python3 app/runner.py
```

Cron example (operator machine):

```
*/15 * * * * cd /path/to/azbot-standalone && python3 app/runner.py
```

Grok-side autonomy: ask AZbot to create a Grok Automation with an explicit prompt and cadence. Connected service is Automations. AZbot will not create a posting automation unless the operator states the exact text and cadence.

## Post / reply / comment on your pages

Supported path: official APIs with tokens you set in the environment.

- `AZBOT_X_BEARER` — X API v2 user-context bearer
- `AZBOT_PUBLISH=1` — required gate before any network post

```bash
python3 app/publish.py draft-x "text stays in queue"
AZBOT_PUBLISH=1 AZBOT_X_BEARER=… python3 app/publish.py post-x "text"
AZBOT_PUBLISH=1 AZBOT_X_BEARER=… python3 app/publish.py reply-x POST_ID "text"
```

Not supported:

- Browser password login
- Saving operator passwords
- Untraceable or unofficial scrape-login posting
- Silent posts without publish=true and the env gate

Reddit / GitHub / Zenodo adapters wait on operator tokens the same way. Do not invent extra unofficial login bots.
