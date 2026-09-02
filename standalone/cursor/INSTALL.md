# Install AZbot rules into a Cursor repo

From this repo:

```bash
cp -R standalone/.cursor /path/to/your/repo/
cp standalone/AGENTS.md /path/to/your/repo/
```

Or if you are already inside `standalone/`:

```bash
cp -R .cursor /path/to/your/repo/
cp AGENTS.md /path/to/your/repo/
```

Open the repo in Cursor. Rules with `alwaysApply: true` load without extra clicks.

Confirm in Cursor Settings → Rules that `azbot-core`, `azbot-export-lock`, and `azbot-voice` are visible.

AZBot also runs Cursor `SKILL.md` files. Drop them in `.cursor/skills/<name>/SKILL.md` or `skills/cursor/<name>/SKILL.md`, then `azbot skills`.
