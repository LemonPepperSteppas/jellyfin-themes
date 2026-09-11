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
| [Cinematic Glass](themes/cinematic-glass/) | scaffolded, not yet built |

Themes are released under per-theme tags (`cinematic-glass-v0.0.1`) and served by jsDelivr
straight from this repo, so one theme's release never moves another's URL.

## Why the research folder exists

Jellyfin 10.11 is mid-migration from the Emby-derived UI to React + MUI, which is why so
many community themes broke at that release. There are three themable surfaces, not one,
and the entire dashboard is driven by `--jf-palette-*` CSS variables that almost no
community theme touches. `research/jellyfin-10.11-theming.md` documents this;
`research/reference/` holds the generated variable list and the built-in theme sources at
the target version.

## Design

`design/theme-directions.html` is the deck: seven directions, nine screens each, generated
from `design/src/`. Every direction rebuilds the layout rather than just the palette.
