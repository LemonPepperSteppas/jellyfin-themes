# Cinematic Glass — registered-theme install

This variant makes Cinematic Glass a **real entry in the theme dropdown** (Settings →
Display → Theme) instead of a stylesheet layered over the built-in Dark theme.

It needs filesystem access to the `jellyfin-web` directory. If you only have the Dashboard,
use the CDN `@import` variant in the theme README instead.

## Why bother

- It **replaces** `themes/dark/theme.css` rather than fighting it — no override layer, no
  specificity arms race, far less CSS.
- `html[data-theme="cinematic-glass"]` is set for you by Jellyfin's `themeManager`.
- Users pick it per-account, and can switch back to Dark without you touching anything.
- It applies to the login screen before any user has signed in.

## Where jellyfin-web lives

| Install | Path |
|---|---|
| Debian/Ubuntu package | `/usr/share/jellyfin-web/` |
| Official Docker image | `/jellyfin/jellyfin-web/` |
| Windows | `C:\Program Files\Jellyfin\Server\jellyfin-web\` |
| macOS | `/Applications/Jellyfin.app/Contents/Resources/jellyfin-web/` |

## Install

1. Copy the theme in:

   ```
   <jellyfin-web>/themes/cinematic-glass/theme.css
   ```

2. Add one entry to the `themes` array in `<jellyfin-web>/config.json`:

   ```json
   { "name": "Cinematic Glass", "id": "cinematic-glass", "color": "#080a0d" }
   ```

   `id` must match the folder name. `color` becomes the browser's `<meta name="theme-color">`.
   To make it the default for new users, add `"default": true` and remove that key from the
   existing Dark entry.

3. Hard-refresh the browser (Ctrl/Cmd + Shift + R). `config.json` is cached aggressively.

## It will be wiped by server updates

Upgrading Jellyfin replaces the whole `jellyfin-web` directory. Pick one:

**Docker — bind-mount (survives updates):**

```yaml
services:
  jellyfin:
    volumes:
      - ./cinematic-glass:/jellyfin/jellyfin-web/themes/cinematic-glass:ro
      - ./config.json:/jellyfin/jellyfin-web/config.json:ro
```

Note the mounted `config.json` must be a full copy of the image's own file with your entry
added — it replaces, not merges. Re-check it after a major Jellyfin upgrade in case
upstream added keys.

**Bare metal — re-run after each upgrade.** Keep the two steps above in a short script and
run it as a post-upgrade hook.

## Uninstall

Delete `themes/cinematic-glass/` and remove the `config.json` entry. Anyone still on the
theme falls back to Dark on next load.
