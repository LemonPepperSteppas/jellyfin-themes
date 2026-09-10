# CLAUDE.md

Custom themes for **Jellyfin 10.11.x** web, for a real shared server with several users.

## Keeping this file current

**This file is the handover between sessions. Update it in the same commit as the change
it describes** — not afterwards, not "later". Specifically:

- Anything in **Current state** stops being true → edit it that session.
- A decision in **Settled decisions** is revisited or reversed → move it, note why.
- A new theme folder, a release tag, a build-script flag, or a new hard-won gotcha →
  add it here, briefly, and link the fuller doc rather than restating it.

Keep it short and high-signal; it loads into every session. Detail belongs in
`research/jellyfin-10.11-theming.md`, `themes/README.md`, or a theme's own `PLAN.md`.
If this file and the repo disagree, the repo is right — fix this file.

## Current state

_Last updated: 2026-09-10._

- **Repo:** https://github.com/LemonPepperSteppas/jellyfin-themes (public, `main`).
  Public because jsDelivr can only serve public repos.
- **Tags:** none yet. First release will be `cinematic-glass-v1.0.0`.
- **Cinematic Glass:** `src/00-tokens.css` is written; every other file in
  `themes/cinematic-glass/src/`, `options/`, `standalone/` and `accents/` is still a stub
  containing only a header comment. `dist/` builds (both profiles) but holds tokens only.
- **Next step:** `themes/cinematic-glass/src/01-mui-vars.css`, then work down the build
  order in `themes/cinematic-glass/PLAN.md` section 5. The `--cg-*-rgb` triples it needs
  for the `*Channel` names already exist in `00-tokens.css`.
- **Font delivery settled:** self-hosted Manrope, variable woff2, embedded as a `data:`
  URI in a new `03-fonts.css`. Rationale and the per-profile reason a relative `url()`
  cannot work: `PLAN.md` section 3a. The font file itself is not in the repo yet.
- **Design is locked.** The seven-direction deck was shown to the server's users and they
  picked Cinematic Glass. Token values are transcribed in `PLAN.md` section 3 — use those,
  do not re-derive them. Deck source: `design/src/`; published page:
  https://claude.ai/code/artifact/0b05bfd0-00d1-4288-b5e7-2eab721eafa8

## Layout

```
themes/     one folder per theme; conventions in themes/README.md
design/     the art-direction deck (generated: python design/src/assemble.py)
research/   how 10.11 theming actually works + generated reference files
```

## The five things that will make you write wrong CSS

Read `research/jellyfin-10.11-theming.md` before touching a theme. The short version:

1. **Three themable surfaces, not one.** Legacy Emby-derived DOM (`.skinHeader`,
   `.emby-*`, `.card*`) in `apps/stable`; MUI **CSS variables** (`--jf-palette-*`) which
   drive the entire dashboard; and MUI **component classes** (`.MuiAppBar-root`). A theme
   that only does the first leaves the whole dashboard stock — which is what nearly every
   community theme does.
2. **MUI derived values do not recompute.** `-light`, `-dark` and every `*Channel` are
   computed in JavaScript at build time. Setting `--jf-palette-primary-main` alone leaves
   every hover, ripple and alpha state Jellyfin blue. Set the whole family. `*Channel` is
   a space-separated RGB triple used as `rgba(var(--x) / 0.5)`.
3. **Specificity.** MUI's sheet is `:root, [data-theme="dark"]` — (0,1,0). Use
   `html[data-theme]` (0,1,1) so it wins regardless of injection order.
4. **The two shipping profiles are not the same CSS in two places.** `custom-css` layers
   *over* the built-in Dark theme, so anything uncovered keeps Jellyfin's look.
   `standalone` *replaces* it, so anything uncovered is **unstyled**. That is why
   `standalone/00-jellyfin-base.css` exists. Test both on the real server.
5. **`backdrop-filter` is expensive.** It measurably stalled the renderer during mockup
   review. Every blur-using theme ships a `no-blur` option *with v1*, not later.

The full generated list of all 1097 `--jf-*` variables is
`research/reference/mui-jf-variables.10.11.8.css` (regenerate:
`node research/reference/generate-mui-variables.cjs`, needs `@mui/material@6.4.12`).
`research/reference/jellyfin-dark-theme.10.11.8.scss` *is* Jellyfin's built-in dark theme
at the target version — it doubles as the canonical list of ~102 themable legacy classes.

## Conventions

- **Numbered source modules** (`00` → `99`); filename order *is* cascade order.
- **`00-tokens.css` is the only file allowed a colour literal.** Everything else reads
  `--cg-*` tokens.
- **`99-fixes.css` is the only file allowed `!important`.** Every rule there carries a
  comment saying why and a version stamp.
- `build.py --check` enforces both, plus incomplete MUI accent families. Run it before
  committing.
- **`dist/` is committed on purpose** — jsDelivr serves straight from the repo. Never edit
  it by hand.
- **Pin tags, never branches**, in install URLs. jsDelivr caches a tag permanently and a
  branch for 7 days; a tag also can't deliver a half-finished push.

## Commands

```bash
cd themes/cinematic-glass
python build/build.py                      # both profiles
python build/build.py --profile custom-css
python build/build.py --min                # also emit .min.css
python build/build.py --check              # lint only, writes nothing

python design/src/assemble.py              # regenerate the direction deck (from repo root)
```

## Settled decisions — do not relitigate without being asked

- **One repo at the root, not one per theme.** `research/` and `design/` are shared by
  every theme. Per-theme *tags* (`cinematic-glass-v1.0.0`) give independent release
  cadence; `git subtree split` can extract a theme with history later if needed.
- **CDN `@import` is the primary install**; the registered-theme (`standalone`) variant is
  a documented extra. The server owner has Dashboard access but not filesystem access.
- **Cinematic Glass v1 ships no accent variants.** The accent is achromatic (`#e8eef6`)
  because the thesis is that artwork supplies the colour and the interface supplies none.
  `accents/` is capacity for a later request, not part of the release.
- **Amber Terminal was cut** from the ballot by the users. Its full spec still lives in
  `design/src/dirs.py`; adding `"terminal"` back to `ORDER` restores it.
- **Target is 10.11.x.** 10.11.5–10.11.11 share an identical file tree. Jellyfin 12.0
  keeps the same MUI/`--jf-`/`data-theme` architecture but renames the apps
  (`stable`→`legacy`, `experimental`→`modern`) and moves themes to `src/themes/_base/`.
  Porting is small but not free.

## Working style

- Verify against `jellyfin-web` source (tag `v10.11.8`) rather than assuming; `gh` is
  authenticated and the repo is public.
- Test claims about rendering by actually rendering — a local `python -m http.server` plus
  the Chrome tools was the loop used throughout. Kill the server and close the tab after.
- Don't add attribution lines to commit messages or PR descriptions.
