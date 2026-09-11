# Jellyfin themes

Custom themes for **Jellyfin 10.11.x** web, plus the research and the art-direction work
they came out of.

```
themes/      the themes themselves - one folder each, see themes/README.md
design/      the art-direction deck the server's users chose from
research/    how Jellyfin 10.11 theming actually works, with generated references
CLAUDE.md    project state and conventions; start here
```

## Themes

| Theme | Status |
|---|---|
| [Cinematic Glass](themes/cinematic-glass/) | released, `cinematic-glass-v0.0.6` |

Themes are released under per-theme tags (`cinematic-glass-v0.0.6`) and served by jsDelivr
straight from this repo, so one theme's release never moves another's URL.

## Install

Dashboard &rarr; **Branding** &rarr; Custom CSS, as the first line in the box:

```css
@import url("https://cdn.jsdelivr.net/gh/LemonPepperSteppas/jellyfin-themes@cinematic-glass-v0.0.6/themes/cinematic-glass/dist/cinematic-glass.css");
```

Per-user instead: Settings &rarr; Display &rarr; Custom CSS, which is injected after the
server's and wins. Options, the registered-theme install, and what each option does are in
[the theme's README](themes/cinematic-glass/).

Pin a tag, never a branch &mdash; jsDelivr caches a tag permanently, so it can never serve
a half-finished push, and can never be re-pointed either. New release, new tag.

## Why the research folder exists

Jellyfin 10.11 is mid-migration from the Emby-derived UI to React + MUI, which is why so
many community themes broke at that release. There are three themable surfaces, not one,
and the entire dashboard is driven by `--jf-palette-*` CSS variables that almost no
community theme touches. `research/jellyfin-10.11-theming.md` documents this;
`research/reference/` holds the generated variable list and the built-in theme sources at
the target version.

The sharpest finding in there, and the one that cost the most to learn: **Jellyfin never
applies custom CSS to the admin dashboard at all.** `apps/dashboard` mounts the theme
`<link>` but not the custom-CSS component, so no `@import` install can reach it &mdash;
this theme's or anyone's. That reframes "community themes leave the dashboard stock" from
an oversight into a structural limit. See &sect;2b.

## Design

`design/theme-directions.html` is the deck: seven directions, nine screens each, generated
from `design/src/`. Every direction rebuilds the layout rather than just the palette.
