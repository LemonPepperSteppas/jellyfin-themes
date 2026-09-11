# Themes

One folder per theme. Each is self-contained and builds independently, so a second theme
can be added without touching the first.

```
themes/
  cinematic-glass/     picked by the server's users, Sept 2026; released v0.0.5
  <next-theme>/        copy the layout below
```

## Conventions

Every theme folder follows the same shape:

```
README.md          what it is, how to install, what the options do
PLAN.md            the build plan and the approved token spec
src/               numbered modules (00 -> 99), concatenated in filename order
assets/            binaries the theme ships (fonts) + their licences
accents/           optional colourway swaps; _template.css to copy
options/           opt-in behaviour modules, imported AFTER the base theme
standalone/        extra base layer + install docs for the registered-theme profile
build/build.py     concatenates src/ into dist/
build/*.py         other generators; anything they emit into src/ is committed
dist/              the built files people import; never edited by hand, but committed
                   (jsDelivr serves straight from the repo)
```

**Numbered source files.** Order is encoded in the filename so concatenation is
deterministic and the cascade is predictable. `00-tokens.css` is always the only file
allowed to contain a colour literal; `99-fixes.css` is always the only file allowed to
use `!important`. `build.py --check` enforces both.

**Two shipping profiles.** `custom-css` layers over Jellyfin's built-in Dark theme;
`standalone` replaces it and is registered in `config.json`. The second needs an extra base
layer, because anything a replacement theme omits is left unstyled rather than falling back.
Any new theme should decide up front whether it ships both.

**Two layers, always.** A Jellyfin 10.11 theme that only styles legacy classes leaves the
whole dashboard stock. Every theme here covers the legacy DOM *and* the `--jf-palette-*`
MUI variables. See `research/jellyfin-10.11-theming.md` for why, and
`research/reference/mui-jf-variables.10.11.8.css` for the full generated variable list.

**Tokens in, literals out.** A theme's identity should live in `00-tokens.css` such that
an alternate colourway costs about fifteen lines. If a colourway needs more than that, the
tokens are not doing enough work.

## Releasing

Tags are prefixed per theme, so one theme's release never moves another theme's URL:

```
cinematic-glass-v0.0.5
<next-theme>-v0.0.1
```

Build, commit `dist/`, tag, push the tag. jsDelivr picks it up on first request and caches
it permanently, so a tag is never re-pointed &mdash; cut a new one instead.

Start a theme at `v0.0.1`, not `v1.0.0`. A tag is immutable once jsDelivr has served it, so
the version number is the only thing left to signal "this will still move". Save `v1.0.0`
for a theme whose feature set has actually settled.

## Starting a new theme

1. `cp -r cinematic-glass <new-slug>` and empty `src/`, `assets/`, `accents/`, `options/`,
   `dist/`
2. Rewrite `PLAN.md` sections 3 and 4 — the token spec and the structural moves
3. Update `NAME`, `SLUG` at the top of `build/build.py`
4. Work down the build order in `PLAN.md`

The seven art directions the users chose from are in `design/` — the deck at
`design/theme-directions.html`, generated from `design/src/`. Direction specs (tokens,
structure, copy) live in `design/src/dirs.py` and are the starting point for any new
theme's `PLAN.md`, including Amber Terminal, which was cut from the ballot but is still
defined there.
