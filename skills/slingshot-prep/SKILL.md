---
name: slingshot-prep
description: Strip identifying embedded metadata from a copy of a file and write a SHA-256 receipt using standalone/app/sanitize.py. Not an upload proxy.
---

# slingshot-prep

Local export hygiene only. Leave the original file untouched.

From the repo:

```bash
python3 standalone/app/sanitize.py FILE --out out
python3 standalone/app/receipt.py out/FILE
```

Or use the local UI at http://127.0.0.1:7747 (Slingshot Prep).

Do not rewrite content timestamps to fake origin. Do not upload. The operator moves the cleaned copy on their own channel.
