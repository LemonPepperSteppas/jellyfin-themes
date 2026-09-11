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
- **Tags:** `cinematic-glass-v0.0.5` is current (2026-09-10). Deliberately `0.x` &mdash; the
  design is locked but the feature set is not, so `v1.0.0` is still free.
  Everything before it is superseded and should not be pinned: v0.0.1 kept a poster
  column on the item page, v0.0.2 predates the centred ElegantFin-derived detail
  composition and the removal of the page veil, v0.0.3 predates the sign-in card, and
  v0.0.4 still clipped every card's hover shadow square (item 8 below).
- **Cinematic Glass is released and verified on the real server.** All thirteen modules in
  `src/`, all five `options/`, and `standalone/00-jellyfin-base.css` are done; `dist/`
  builds both profiles (~181 KB, ~94 KB minified — the font is most of that). `accents/` is
  still just the template, which is the settled decision, not an omission.
- **Manrope is committed and embedded.** `themes/cinematic-glass/assets/*.woff2` (v20,
  variable, latin + latin-ext) with `OFL.txt`, redistributed under OFL-1.1.
  `src/03-fonts.css` is GENERATED from them — never hand-edit it; run
  `python build/embed-font.py`. The theme has no external dependency at runtime.
- **Shipped. What is left is optional:** a transcoding session, and TV focus rings on real
  hardware. Everything else in `PLAN.md` section 6 is checked, on the live server, plus
  mobile confirmed on a real device by the server owner. Seven bugs came out of that pass;
  six of them were invisible to fixtures built from the v10.11.8 stylesheets, which is why
  **fixtures are no longer treated as verification for anything structural.**
- **The MUI layer is verified.** All six colour schemes fall to our variables and no stock
  Jellyfin blue survives in the 233 `--jf-*` names MUI declares. Consequence recorded in
  `PLAN.md` before section 3: the theme overrides the Display-settings theme picker.
- **One decision worth a second opinion**, flagged in the file that made it:
  `01-mui-vars.css` maps MUI's `secondary` and `info` onto the neutral ramp, and
  `PLAN.md` section 3 specifies no such tokens.
- **Sign-in is the deck's single glass card**, not Jellyfin's full-bleed picker. The
  container it hangs on is the wrapper `div.padded-left.padded-right.padded-bottom-page`
  inside `#loginPage` - an earlier version of `60-login.css` claimed no such element
  existed and only panelled the manual form. See `PLAN.md` section 4c.
- **The image editor and image search dialogs are pickers, not shelves** - `80-misc.css`
  widens `.imageEditorCard` (32% wide art / 18% portrait), drops the card scrim, and puts
  `.cardFooter` back into flow under the image. Stock rendered posters at 104px and the
  20-cards.css overlay treatment made the provider line unreadable over pale artwork.
- **The detail page follows ElegantFin's centred composition, not the deck** - the owner's
  call after comparing both on the real server; see `PLAN.md` section 4b. Do not "restore"
  it to the deck. It also shows LOGO ART with the text title as fallback, which the deck's
  own `/* logo-art title */` comment asked for.
- **The detail page was rebuilt in v0.0.2** to match the deck: full-bleed billboard hero,
  title on the artwork, no poster column. v0.0.1 had it wrong because I read `PLAN.md`
  section 4 as the whole specification when it is only the list of what must not be
  dropped. **The deck is the design** — render it (`python -m http.server` in `design/`)
  before arguing with it from prose.
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

## The seven things that will make you write wrong CSS

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

7. **Custom CSS never reaches the dashboard.** `apps/dashboard/AppLayout.tsx` renders
   `<ThemeCss dashboard />` but does **not** import `CustomCss` at all — only
   `apps/stable` and `apps/experimental` do. Verified live and in source
   (`research/jellyfin-10.11-theming.md` §2b). So `01-mui-vars.css` and
   `70-dashboard.css` — the work that makes this theme cover the dashboard — are
   **inert on the CDN `@import` profile**, and only pay off on `standalone`. That
   profile also needs the user to set **Dashboard theme** as well as **Theme**, since
   `ThemeCss` resolves a separate `dashboardTheme` setting.

6. **Cards come in two shapes, and one screen does not tell you which.** On home and
   library grids the text lines are *direct children* of `.cardBox` with no wrapper — 43
   cards, zero `.cardFooter`. On the sign-in screen's square user cards it is the
   opposite — 3 cards, 3 `.cardFooter` wrappers, zero direct `.cardText`. A rule written
   for one shape silently does nothing on the other, and `card.scss` defining a selector
   proves nothing about whether a given card type renders it. `20-cards.css` handles
   both. Read the live DOM, on more than one page.

8. **`contain` clips what you draw.** `.card` computes to `contain: content`
   (= `layout paint style`) and `.skinHeader` to `contain: layout style paint`. **Paint
   containment clips everything the element draws to its own box, `box-shadow`
   included** — so a hover ring or lift shadow that reaches outside the box is sliced
   flat, with no error and no sign of it in the rule you wrote. `20-cards.css` drops
   `paint` on cards; `10-chrome.css` had to work around the same thing on the header.
   Note the specificity: a bare `.card` **loses** — the winning declaration is not
   enumerable from script, and `.itemsContainer .card` (0,2,0) is what measured as
   taking effect.

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
  comment saying why and a version stamp. In practice it holds exactly one category:
  declarations upstream marks `!important`, which a normal rule loaded later cannot beat
  no matter how specific. It is inert on the standalone profile, which replaces that
  stylesheet rather than layering over it.
- **Durations are always `var(--cg-dur*)`, never literals.** `02-base.css` implements
  `prefers-reduced-motion` by collapsing those tokens, because the usual
  `* { transition: none !important }` reset is not available outside `99-fixes.css`.
- `build.py --check` enforces both, plus incomplete MUI accent families. Run it before
  committing. It masks comments first, so a comment may name the stock value a variable
  replaces without reading as a colour literal.
- **`dist/` is committed on purpose** — jsDelivr serves straight from the repo. Never edit
  it by hand. Same for `src/03-fonts.css`, which is generated from `assets/`.
- **`.gitattributes` normalises everything to LF**, so any new binary asset needs a
  `binary` line there or git will corrupt it. `*.woff2` is already covered.
- **Pin tags, never branches**, in install URLs. jsDelivr caches a tag permanently and a
  branch for 7 days; a tag also can't deliver a half-finished push.

## Commands

```bash
cd themes/cinematic-glass
python build/build.py                      # both profiles
python build/build.py --profile custom-css
python build/build.py --min                # also emit .min.css
python build/build.py --check              # lint only, writes nothing

python build/embed-font.py                 # regenerate src/03-fonts.css from assets/*.woff2
python build/embed-font.py --check         # verify it is in step with assets/ (writes nothing)

python design/src/assemble.py              # regenerate the direction deck (from repo root)
```

## Settled decisions — do not relitigate without being asked

- **One repo at the root, not one per theme.** `research/` and `design/` are shared by
  every theme. Per-theme *tags* (`cinematic-glass-v0.0.5`) give independent release
  cadence; `git subtree split` can extract a theme with history later if needed.
- **CDN `@import` is the primary install**; the registered-theme (`standalone`) variant is
  a documented extra. The server owner has Dashboard access but not filesystem access.
  **Reaffirmed 2026-09-10 with the dashboard limitation known and accepted** (item 7
  above): the admin dashboard stays stock Jellyfin on the primary profile. Judged the
  right trade — it is an admin surface a handful of people see occasionally, and the
  alternative costs filesystem access plus a bind-mount to survive upgrades. `standalone`
  remains available for anyone who wants the dashboard covered too.
- **Do not delete `01-mui-vars.css` or `70-dashboard.css` as dead code.** They are inert
  on the *dashboard* under the primary profile, but they are not unused: `apps/experimental`
  renders `CustomCss`, so the `--jf-*` layer drives the experimental layout's MUI chrome
  there, and the whole file pays off on `standalone`. This is the obvious wrong conclusion
  to draw from the decision above, so it is written down.
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
