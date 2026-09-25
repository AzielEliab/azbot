# AZbot Local

Local page for prep, ARK seal, and skill files. It binds to 127.0.0.1.

**Author:** Aziel Eliab  
**Version:** 0.2.0

## Start

1. From this folder:

```bash
chmod +x launch.sh
./launch.sh
```

Windows: `launch.bat`

2. Open http://127.0.0.1:7747/

3. Choose **Prep copies**.

Python 3. Pillow and pypdf prepare images and PDFs. ffmpeg is optional for media container tags. cryptography is used for ARK seal.

## On the page

- **Prep copies** writes a cleaned copy and a SHA-256 receipt. The original file stays in place.
- **Advanced** holds ARK seal, Phoenix view, and skill files.

From the repo root, `azbot skills` and `azbot skill run NAME` print skill files in the terminal.

## Notes

Public identity on this package is Aziel Eliab.

Prep strips identifying embedded metadata from a copy. It does not rewrite content timestamps to invent an origin. This server does not upload the file.

Service → Clarity → Peace.
