# Cinematic Glass

A theme for **Jellyfin 10.11.x** web. The artwork supplies all the colour; the interface
supplies none. There is no top bar — navigation floats as a frosted pill, card metadata
sits over the poster instead of under it, and the billboard runs edge to edge.

> **Released as `cinematic-glass-v0.0.5`.** Every module is written, the font is embedded,
> and the whole thing has been through the `PLAN.md` section 6 test pass on a real server.
> The `0.x` version is deliberate: the design is settled but the feature set is not, so
> expect additions before `v1.0.0`.
>
> Every earlier tag is superseded and should not be pinned: `v0.0.1`'s item-detail page did
> not match the approved design, `v0.0.2` predates the centred detail composition, `v0.0.3`
> predates the sign-in card, and `v0.0.4` still clipped every card's hover shadow square.

Three screens are rebuilt rather than restyled, and are worth knowing about before you
decide whether this is the theme you want:

- **Sign-in** is one narrow glass card over veiled artwork &mdash; the lockup, a row of
  round avatars, the fields and the buttons, all in a single panel, instead of Jellyfin's
  full-width row of square user tiles.
- **Item detail** is a centred composition: logo art over a full-bleed backdrop that fades
  into the page, with no poster column. This follows ElegantFin rather than the deck, which
  was the server owner's call after seeing both live; `PLAN.md` section 4b has the
  reasoning.
- **The image editor and image search dialogs** are treated as pickers rather than
  shelves: bigger thumbnails, no scrim over the artwork, and the provider line under the
  image instead of on it.

## Install

Dashboard → **Branding** → Custom CSS. `@import` must be the first line in the box.

```css
@import url("https://cdn.jsdelivr.net/gh/LemonPepperSteppas/jellyfin-themes@cinematic-glass-v0.0.5/themes/cinematic-glass/dist/cinematic-glass.css");
```

> Pin a tag, never a branch. jsDelivr caches a tag permanently, so a tag can never serve
> you a half-finished push &mdash; and can never be re-pointed either. New release, new tag.

Per-user instead of server-wide: Settings → Display → Custom CSS. User CSS is injected
after server CSS, so it wins. Applies to Jellyfin Web only — not Android, Swiftfin or the
TV apps.

> **The admin dashboard stays stock, by design.** Jellyfin does not apply Custom CSS to it —
> `apps/dashboard` mounts only the theme `<link>`, never the custom-CSS component — so no
> `@import` install can reach it, this theme's or anyone else's. That is accepted here
> rather than worked around: it is an admin screen, and the fix costs filesystem access.
> If you do want it themed, use the registered-theme install below, which does reach it.
> Details: `research/jellyfin-10.11-theming.md` §2b.

## Or install it as a real theme

There is a second shipping shape. Instead of layering CSS over the built-in Dark theme,
drop the theme into `jellyfin-web` and register it in `config.json`, and it becomes an
entry in **Settings -> Display -> Theme** that users pick per-account.

Needs filesystem access, and server upgrades wipe it unless you bind-mount. Full
instructions and the `config.json` entry: `standalone/INSTALL.md`.

Why it is nicer: it *replaces* `themes/dark/theme.css` rather than fighting it, so there
is no override layer and no specificity arms race. It also applies to the login screen
before anyone has signed in — **and it is the only install that themes the admin
dashboard.**

Note the dashboard uses a *separate* setting: Jellyfin resolves `dashboardTheme` there and
`theme` everywhere else, so pick Cinematic Glass in **both** dropdowns under
Settings → Display.

## Options

Each is an extra `@import` on a line *after* the base theme. They are served straight from
the repo rather than from `dist/`, since they are single files with nothing to concatenate:

```css
@import url("https://cdn.jsdelivr.net/gh/LemonPepperSteppas/jellyfin-themes@cinematic-glass-v0.0.5/themes/cinematic-glass/dist/cinematic-glass.css");
@import url("https://cdn.jsdelivr.net/gh/LemonPepperSteppas/jellyfin-themes@cinematic-glass-v0.0.5/themes/cinematic-glass/options/no-blur.css");
```

| Module | Effect |
|---|---|
| `options/no-blur.css` | Drops every `backdrop-filter` and makes the glass opaque. Use on weak clients and TV boxes. |
| `options/meta-below.css` | Card metadata under the poster instead of over it. Also makes cards taller. |
| `options/solid-header.css` | Conventional solid top bar instead of the floating pill. |
| `options/no-backdrops.css` | No full-bleed backdrops on library and detail pages. |
| `options/compact.css` | Tighter rails, smaller posters, for dense libraries. |

`no-blur.css` is not a downgrade path bolted on afterwards &mdash; every blur in the theme
is written as `var(--cg-blur)`, so the option turns them all off by redefining two tokens,
and it re-opaques the glass in the same breath. A translucent surface with the blur removed
is a window, not a cheaper pane.

## Typography

**Manrope**, self-hosted and embedded &mdash; no request leaves the server to render this
theme, and no Google Fonts dependency.

The font ships in this repo: `assets/manrope-latin.woff2` and `assets/manrope-latin-ext.woff2`
(Manrope v20, variable `wght 200-800`, the subsets Google Fonts serves), redistributed under
the SIL Open Font License 1.1 with `assets/OFL.txt` alongside, as that licence requires.

`src/03-fonts.css` is **generated** from those files &mdash; do not edit it:

```
python build/embed-font.py            # regenerate
python build/embed-font.py --check    # verify it matches assets/
```

They are embedded as `data:` URIs rather than referenced with `url()` because a relative URL
resolves against whichever origin served the stylesheet, and that differs between the two
profiles &mdash; jsDelivr for Custom CSS, your Jellyfin host for standalone. See `PLAN.md`
section 3a. It costs about 54 KB of the built file and buys a theme with no external
dependency at all.

`unicode-range` is kept per subset, so anything outside Latin falls back through the rest of
the stack in `--cg-font` rather than rendering as boxes.

## Accents

**v1 ships no accents, on purpose.** The accent is `#e8eef6` — achromatic — because the
thesis is that the artwork supplies all the colour and the interface supplies none. A
tinted accent partly undoes that.

The `accents/` folder exists as capacity, not a plan. If someone on the server eventually
asks for their copy in coral, copy `accents/_template.css`: an accent module changes the
accent family and nothing else, so it should be about fifteen lines. If it needs more, the
tokens in `00-tokens.css` are not doing enough work.

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

## What is still open

Everything in `PLAN.md` section 6 has been checked on a live 10.11.8 server &mdash; every
screen, signed in as a normal user and as admin, plus mobile on a real device. Two items
are outstanding and neither blocks a release:

- **A transcoding session**, which exercises the dashboard's warning colour. Moot on the
  `@import` profile anyway, since custom CSS never reaches the dashboard.
- **TV focus rings on real hardware.** Testing via the `.layout-tv` class confirms the
  layout flattens, but a remote actually driving `.show-focus` is a different thing.

Live review is also where essentially every real bug came from. Fixtures built from the
v10.11.8 stylesheets caught one of eleven, because the questions that matter &mdash; which
card shape a given screen emits, what `contain` clips, which upstream declarations are
`!important` &mdash; are answered by the DOM, not by the stylesheet. **Read the live DOM,
on more than one page.**
