# Cinematic Glass — build plan

Status: **written, untested on a real server.** Every module in `src/`, all five options
and the standalone base layer are done and `dist/` builds for both profiles. Outstanding:
`03-fonts.css` (needs the Manrope woff2), the section 6 test pass, and the tag.

Target: **Jellyfin 10.11.8** (verified against `jellyfin-web` @ `v10.11.8`; the whole 10.11.x
line shares an identical file tree, so 10.11.5–10.11.11 are all in scope).
Chosen by the server's users from the seven-direction deck.

---

## 1. The three surfaces (why this is not one stylesheet)

Jellyfin 10.11 is mid-migration from the Emby-derived UI to React + MUI. Three distinct
layers need covering, and most community themes only ever touch the first:

| Layer | Where it renders | Handled in |
|---|---|---|
| Legacy DOM | Home, libraries, item detail, player OSD (`apps/stable`) | `02` → `60` |
| MUI variables | The entire dashboard, plus experimental-layout chrome | `01-mui-vars.css` |
| MUI structure | same as above | `70-dashboard.css` |

`apps/stable/AppLayout.tsx` renders **no MUI chrome at all** — the default header is still
legacy `.skinHeader`. `apps/dashboard` is 100% MUI. Full notes:
`research/jellyfin-10.11-theming.md`.

## 2. Two gotchas that will bite

**Derived MUI values do not recompute.** MUI computes `-light`, `-dark` and every
`*Channel` in JavaScript at build time. Setting `--jf-palette-primary-main` alone leaves
every hover, ripple and alpha state Jellyfin blue. Set the whole family. `*Channel` values
are space-separated RGB triples consumed as `rgba(var(--x) / 0.5)`.

**Specificity.** MUI's sheet is `:root, [data-theme="dark"]` — (0,1,0), tied with `:root`.
Custom CSS is injected as a `<style>` inside the React tree, so it wins on document order,
but use `html[data-theme]` (0,1,1) to be safe regardless of injection order.

### Consequence: the theme wins over the theme picker

`html[data-theme]` matches the attribute whatever its value, and MUI ships a block
per colour scheme (`dark`, `light`, `appletv`, `blueradiance`, `purplehaze`, `wmc`),
each at (0,1,0). So our variables beat **all six**, and a user choosing Light or
Purple Haze in Display settings keeps Cinematic Glass.

That is deliberate for the custom-css profile - a partly-applied theme is worse than
a forced one, and there is no light variant to fall back to - but it is a real
user-visible effect on a shared server, so it is written down rather than discovered.
Narrowing to `html[data-theme="dark"]` would restore the picker at the cost of
leaving the other five schemes half-styled.

## 3. Approved tokens

From the deck the users picked. Transcribe into `src/00-tokens.css` first; everything else
reads from these and defines no literal colour.

| Role | Value | Notes |
|---|---|---|
| ground | `#080a0d` | near-black, faint blue bias |
| elevated | `#0f1319` | panels, drawer |
| glass surface | `rgba(148,163,184,.12)` | over `backdrop-filter` |
| border | `rgba(255,255,255,.08)` | |
| border strong | `rgba(255,255,255,.17)` | |
| text | `#f1f5f9` | |
| muted | `#9aa7b7` | |
| faint | `#6d7987` | |
| **accent** | `#e8eef6` | achromatic on purpose |
| accent ink | `#0b0f14` | text on accent |
| star | `#f2b01e` | community rating, kept |
| ok / warn / err | `#5ec2a0` / `#e0a94a` / `#e4685f` | semantic, separate from accent |

Geometry: radius `14px` cards, `18px` panels, pill chips, `6px` small.
Depth: `blur(22px) saturate(140%)` on chrome; shadows `0 12px 34px -12px rgba(0,0,0,.9)`.
Type: **Manrope** 400/500/700/800. Display 800 at −0.03em.
Font delivery: **self-hosted, embedded** — see section 3a.
Density: 16px rails, 120px posters.

The accent is achromatic **by design** — colour is supposed to come from the artwork.
That means state cannot be signalled by hue; it has to come from position, weight and
the scrim. Every interactive state needs checking against that.

For the same reason **v1 ships no accent variants.** `accents/` stays empty apart from the
template; it is capacity for a later request, not part of the release.

## 3a. Font delivery — self-hosted, embedded as a data URI

The server is reachable on LAN and over Tailscale only, so **no remote font host.**
Google Fonts is out; the deck's `fonts.googleapis.com` link (`design/src/assemble.py`) was
for a local HTML page and does not carry over to the theme.

Manrope is **OFL-1.1**, so it can be redistributed here. Ship `OFL.txt` beside the file.

Ship the **variable** woff2 (`wght` 200–800), latin subset, not four statics — one file,
smaller than the four weights the spec calls for, and it covers 400/500/700/800 from one
`@font-face` with `font-weight: 200 800`.

**Embed it as a `data:` URI**, not a relative `url()`. A relative URL resolves against the
origin the *stylesheet* came from, which differs per profile — jsDelivr for custom-css,
the Jellyfin host for standalone — so a relative path cannot be correct for both. Embedding
makes the built CSS self-contained, and removes the standalone failure mode where the CSS
is installed but the font file is not. Cost is ~33% base64 inflation on the font bytes.

Checked: the base64 blob survives `build.py --min` (no whitespace inside it for the
minifier's `+ : ; ,` rules to bite) and trips no lint rule (no `#` or `rgb(`).

Always follow with a real fallback stack — `system-ui, sans-serif` — so a failed decode
degrades instead of blanking.

## 4. What makes it this direction, not a palette

Four structural moves. If any one is dropped it stops being Cinematic Glass:

1. **No top bar.** `.skinHeader` becomes a floating frosted pill, centred, over content.
2. **Full-bleed billboard** on home — artwork runs edge to edge behind everything.
3. **Metadata over artwork**, not under it — card titles sit on a gradient scrim.
4. **Real depth** — 22px backdrop blur on chrome, genuine drop shadows on cards.

## 5. Build order

- [x] `00-tokens.css` — palette, geometry, blur, motion scales
- [x] `01-mui-vars.css` — `--jf-*` mapping (whole accent family + Channels)
- [x] `02-base.css` — ground, type, scrollbars, focus, reduced-motion
- [ ] `03-fonts.css` — the embedded Manrope `@font-face` (see section 3a)
- [x] `10-chrome.css` — the pill nav; the defining move, do it early
- [x] `20-cards.css` — cards, rails, metadata-over-artwork scrim
- [x] `30-detail.css` — backdrop hero, logo title, glass media-info chips
- [x] `40-episodes.css`
- [x] `50-player.css` — floating control panel
- [x] `60-login.css`
- [x] `70-dashboard.css` — MUI structure only
- [x] `80-misc.css` — dialogs, menus, toasts, forms
- [~] `99-fixes.css` — in use: two upstream `!important` declarations beaten
- [x] `options/no-blur.css` — shipped with v1; all five options written
- [x] `standalone/00-jellyfin-base.css` — base coverage for the registered variant
- [ ] Test pass on the real server, all nine screens
- [ ] Tag and publish

## 6. Test checklist

Nine screens, on the live server, signed in as a normal user *and* as admin:

sign-in · home · library grid · movie detail · series & episodes · player OSD ·
dashboard · a dialog (metadata editor) · settings forms

Plus: **mobile layout**, **TV layout** (`.layout-tv`, focus states matter far more there),
a **pale poster** to check metadata-over-artwork contrast, and a **transcoding session**
so the dashboard's warning colour gets exercised.

`options/no-blur.css` is not optional polish — backdrop-filter measurably bogged the
renderer during mockup review, and TV boxes are weaker than this laptop. Ship it with v1.

## 7. Distribution — two profiles

**A. Custom CSS (primary).** CDN `@import` into **Dashboard → Branding → Custom CSS**:

```css
@import url("https://cdn.jsdelivr.net/gh/LemonPepperSteppas/jellyfin-themes@cinematic-glass-v1.0.0/themes/cinematic-glass/dist/cinematic-glass.css");
```

`@import` must be the first rule in the block. Options go on the lines *after* it.
Pin a tag; never use a branch. jsDelivr caches a branch URL for 7 days but a tag forever,
so a tag is both faster and immune to a mid-edit push reaching users half-finished.

**B. Registered theme (standalone).** Dropped into `<jellyfin-web>/themes/cinematic-glass/`
and registered in `config.json`; appears in the Display settings dropdown.
See `standalone/INSTALL.md`.

### The asymmetry between them

This is the thing to keep straight while writing CSS:

| | Custom CSS | Standalone |
|---|---|---|
| Loads | *after* `themes/dark/theme.css` | *instead of* it |
| Anything not covered | keeps Jellyfin's Dark look | is **unstyled** |
| Needs | nothing but Dashboard access | filesystem access; wiped by upgrades |

So `src/` alone is enough for A, but B additionally needs `standalone/00-jellyfin-base.css`
to provide a floor for every legacy class the built-in dark theme touched. The canonical
list of those ~102 selectors is `research/reference/jellyfin-dark-theme.10.11.8.scss` —
that file *is* the built-in dark theme at our target version.

Practical consequence: **test profile B on the real server too.** A gap that profile A
hides behind Jellyfin's defaults will be plainly visible in B.
