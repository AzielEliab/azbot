# ARK envelope

Local immutable-media style vault for AZbot. Format ARK1.

## Seal

`python3 app/ark.py seal FILE --pass PASSPHRASE --out FILE.ark`

- Body encrypted AES-GCM.
- Metadata encrypted separately (original name, size, SHA-256, timestamps, extra tags).
- Outer header is algorithm + salt + nonces + wrapped DEK only. No filename, no GPS, no author.
- Original file is not modified.

## Phoenix loop (authorized local view)

`python3 app/ark.py phoenix FILE.ark --pass PASSPHRASE [--extract OUT]`

- Decrypts with the passphrase.
- Optional extract of plaintext to a path you choose.
- Generates a new DEK, new nonces, gen+1.
- Overwrites the .ark in place. Prior generation ciphertext is gone from that file.

Phoenix does not run when a stranger opens the blob. Without the passphrase they have ciphertext. There is no remote callback and no viewer-side implant.

## Upload

You move the `.ark` on your own channel. AZbot does not proxy the upload and does not claim the transfer is origin-free. Ciphertext still has a hash. The account and IP of the transfer are still the operator's.

## Court originals

Do not ARK-overwrite evidence that must keep byte-for-byte provenance. Seal a copy.
