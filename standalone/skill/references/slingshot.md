# Slingshot Prep

Local export hygiene only. Not an anonymous relay. Not an attribution-defeat system.

## What it does

On a **copy** of a file the operator chose for public or third-party release:

- Strip identifying embedded metadata (GPS, camera/device, author, producer, software tags, GPS-bearing fields).
- Leave the original file untouched.
- Write a SHA-256 receipt for the cleaned copy.
- Do not rewrite content timestamps to fake a different creation time. Temporal integrity stays intact.

## What it does not do

- No upload proxy, drop service, or "slingshot to the internet."
- No origin-hiding network path, IP concealment, or "no way to tell where it came from."
- No instruction set for untraceable distribution.
- No sanitizing of court originals that must keep provenance.

If the operator needs a file to leave the machine, they use their own account and channel after prep.

## When AZbot should run it

- Public GitHub/Zenodo/GodLock artifacts.
- Images, PDFs, Office files, and media going off-box.
- Any export covered by the identity/export lock.

## When not to run it

- Evidence originals headed to court (keep provenance).
- Files the operator marked "do not touch metadata."
- Anything where the hash of the original is already an exhibit.

## Implementation

Standalone package script: `sanitize.py` in the AZbot one-click download. In-session, AZbot may run the same script against copies under `/home/workdir/artifacts/`.
