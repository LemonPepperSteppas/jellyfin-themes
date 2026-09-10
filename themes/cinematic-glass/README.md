# Cinematic Glass

A theme for **Jellyfin 10.11.x** web. The artwork supplies all the colour; the interface
supplies none. There is no top bar — navigation floats as a frosted pill, card metadata
sits over the poster instead of under it, and the billboard runs edge to edge.

> **Not built yet.** This folder is scaffolded and planned only. See `PLAN.md`.

## Install

Dashboard → **Branding** → Custom CSS. `@import` must be the first line in the box.

```css
@import url("https://cdn.jsdelivr.net/gh/OWNER/REPO@TAG/themes/cinematic-glass/dist/cinematic-glass.css");
```

Per-user instead of server-wide: Settings → Display → Custom CSS. User CSS is injected
after server CSS, so it wins. Applies to Jellyfin Web only — not Android, Swiftfin or the
TV apps.

## Or install it as a real theme

There is a second shipping shape. Instead of layering CSS over the built-in Dark theme,
drop the theme into `jellyfin-web` and register it in `config.json`, and it becomes an
entry in **Settings -> Display -> Theme** that users pick per-account.

Needs filesystem access, and server upgrades wipe it unless you bind-mount. Full
instructions and the `config.json` entry: `standalone/INSTALL.md`.

Why it is nicer: it *replaces* `themes/dark/theme.css` rather than fighting it, so there
is no override layer and no specificity arms race. It also applies to the login screen
before anyone has signed in.

## Options

Each is an extra `@import` on a line *after* the base theme.

| Module | Effect |
|---|---|
| `options/no-blur.css` | Drops every `backdrop-filter`. Use on weak clients and TV boxes. |
| `options/meta-below.css` | Card metadata under the poster instead of over it. |
| `options/solid-header.css` | Conventional solid top bar instead of the floating pill. |
| `options/no-backdrops.css` | No full-bleed backdrops on library and detail pages. |
| `options/compact.css` | Tighter rails, smaller posters, for dense libraries. |

## Accents

Cinematic Glass is achromatic by design. Accent modules exist for anyone who wants a tint;
copy `accents/_template.css`. An accent should be ~15 lines — it changes the accent family
and nothing else.

## Layout

```
src/        numbered source modules, concatenated in filename order
accents/    optional colourway swaps
options/    opt-in behaviour modules, loaded after the base theme
build/      build.py - concatenates src/ into dist/
dist/       the built file people actually import
```

Source order is encoded in the filenames (`00` → `99`) so concatenation is deterministic
and the cascade is predictable. Never edit `dist/` by hand.

## Build

```
python build/build.py                     # both profiles
python build/build.py --profile custom-css
python build/build.py --min               # also emit .min.css
python build/build.py --check             # lint only, writes nothing
```

| Profile | Sources | Output |
|---|---|---|
| `custom-css` | `src/` | `dist/cinematic-glass.css` |
| `standalone` | `standalone/` + `src/` | `dist/standalone/theme.css` (+ INSTALL.md, config snippet) |

The standalone profile prepends an extra base layer. That is not tidiness &mdash; see the
asymmetry note in `standalone/00-jellyfin-base.css`: a registered theme *replaces* the
built-in stylesheet, so anything it fails to cover is left unstyled, whereas the Custom CSS
profile falls back to Jellyfin's Dark theme for anything it does not touch.

`dist/` is committed on purpose &mdash; jsDelivr serves files straight from the repo.

## Compatibility

Built and tested against **10.11.8**. The 10.11.x line shares an identical file tree, so
10.11.5–10.11.11 should all work. Jellyfin **12.0** keeps the same MUI `cssVariables` /
`--jf-` / `data-theme` architecture but renames the apps (`stable` → `legacy`,
`experimental` → `modern`) and moves themes to `src/themes/_base/`. Because this theme is
variable-driven rather than a pile of `!important`, that port should be small — but it is
a port, not a no-op.

## Open questions

Answers needed before the first release, not before the first line of CSS:

1. **Which accents, if any**, for v1. The theme is achromatic by design, so this may be
   none.
