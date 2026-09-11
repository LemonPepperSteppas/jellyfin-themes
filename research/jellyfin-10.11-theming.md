# How Jellyfin 10.11.8 theming actually works

Research notes gathered from `jellyfin/jellyfin-web` @ `v10.11.8` (released 2026-04-05)
and a survey of the community theme ecosystem. Everything below was verified against
source or reproduced locally — not assumed.

## 1. The big picture: 10.11 has THREE themable surfaces

Jellyfin 10.11 is mid-migration from the legacy Emby-derived UI to React + MUI.
That is why so many pre-10.11 themes broke. There are three distinct layers:

| Layer | Where it renders | How you theme it |
|---|---|---|
| **Legacy DOM** | `src/apps/stable` — home, libraries, item detail, player OSD | Legacy classes: `.skinHeader`, `.card*`, `.emby-*`, `.listItem`, `.detailRibbon` … |
| **MUI (vars)** | `src/apps/dashboard` (all of it) + `src/apps/experimental` chrome (app bar, drawer) | CSS custom properties with the `--jf-` prefix |
| **MUI (structure)** | same as above | MUI class names: `.MuiAppBar-root`, `.MuiDrawer-paper`, `.MuiButton-root` … |

`src/apps/stable/AppLayout.tsx` renders **no MUI chrome at all** — the default
layout's header is still the legacy `.skinHeader`. `src/apps/experimental/AppLayout.tsx`
wraps everything in a MUI `<AppBar>` + `<AppDrawer>`. The dashboard is 100% MUI.

**Consequence:** a theme that only targets legacy classes leaves the dashboard
untouched; a theme that only targets `--jf-*` leaves the main library UI untouched.
A complete theme needs both.

**But read &sect;2b before planning around that.** The dashboard cannot be reached by
custom CSS at all, whatever you write, so the `--jf-*` work only pays off on the
registered-theme profile and in the experimental layout's chrome.

## 2. The MUI variable layer (the part nobody is using)

`src/themes/themes.ts` builds the MUI theme with:

```js
createTheme({
    cssVariables: {
        cssVarPrefix: 'jf',
        colorSchemeSelector: '[data-theme="%s"]',
        disableCssColorScheme: true
    },
    defaultColorScheme: 'dark',
    colorSchemes: { appletv, blueradiance, dark, light, purplehaze, wmc }
})
```

- MUI version is **6.4.12**, React 18.3.1.
- `src/scripts/themeManager.js` sets `document.documentElement.setAttribute('data-theme', id)`,
  so the live selector is `html[data-theme="dark"]` etc.
- MUI emits **1097 CSS custom properties** across the color schemes. The generated
  sheet is checked in at `reference/mui-jf-variables.10.11.8.css`, reproducible with
  `node reference/generate-mui-variables.cjs`.

Key variables worth overriding (dark scheme):

```
--jf-palette-primary-main: #00a4dc;      --jf-palette-primary-light / -dark / -mainChannel
--jf-palette-secondary-main: #aa5cc3;
--jf-palette-background-default: #101010;
--jf-palette-background-paper: #202020;
--jf-palette-text-primary / -secondary / -disabled / -icon
--jf-palette-divider: rgba(255,255,255,0.12);
--jf-palette-action-hover / -selected / -focus / -selectedOpacity
--jf-palette-AppBar-defaultBg
--jf-palette-FilledInput-bg / -hoverBg      (all form fields on the dashboard)
--jf-palette-starIcon-main: #f2b01e;        (Jellyfin custom, community rating stars)
--jf-palette-error-main / warning / info / success
--jf-shape-borderRadius: 4px;
--jf-shadows-0 … --jf-shadows-24
--jf-spacing: 8px;
```

### Gotcha: derived values do NOT recompute
MUI computes `-light`, `-dark`, and `-*Channel` values **in JavaScript at build time**.
Overriding `--jf-palette-primary-main` in CSS does *not* update
`--jf-palette-primary-light`, `--jf-palette-primary-dark`, or
`--jf-palette-primary-mainChannel`. `*Channel` vars are space-separated RGB triples
consumed as `rgba(var(--x) / 0.5)`. **Any accent override must set the whole family**,
or hover/ripple/alpha states will still be Jellyfin blue.

### Gotcha: specificity
MUI's dark sheet is `:root, [data-theme="dark"] { … }` — specificity (0,1,0), same as
`:root`. Custom CSS is injected as a `<style>` inside the React tree (i.e. in `<body>`,
after `<head>`), so equal specificity wins on document order. To be safe, use
`html[data-theme]` (0,1,1), which beats both regardless of injection order.

## 2b. Custom CSS does NOT reach the dashboard

Verified on a live 10.11.8 server, 2026-09-10, then confirmed in the source. This is the
single most consequential fact in this document and it is easy to miss.

`src/apps/*/AppLayout.tsx` decides which stylesheets each app mounts:

| App | `<ThemeCss />` | `<CustomCss />` |
|---|---|---|
| `apps/stable` | yes | **yes** |
| `apps/experimental` | yes | **yes** |
| `apps/dashboard` | yes, as `<ThemeCss dashboard />` | **no — not even imported** |

So **Dashboard -> Branding -> Custom CSS has no effect on the dashboard itself.** Navigating
to `#/dashboard` unmounts the custom-CSS `<style>` entirely; navigating back to `#/home`
remounts it. Round-tripped and reproduced.

The practical consequence: the `--jf-palette-*` work that makes a theme cover the dashboard
**cannot be delivered by the CDN `@import` profile at all.** On the dashboard every MUI
variable stays stock — `--jf-palette-primary-main` reads `#00a4dc`, buttons are Jellyfin
blue, device cards cyan, progress bars green.

This also reframes section 1's claim that most community themes leave the dashboard stock.
That is not only because their authors did not write the CSS. With the community-standard
install, they *could not have*.

Only the registered-theme (standalone) profile reaches it, because `<ThemeCss dashboard />`
does mount. Note the `dashboard` prop: it resolves `dashboardTheme`, a **separate user
setting** from `theme`, so a user must select the theme in *both* dropdowns
(`src/components/ThemeCss.tsx`).

```jsx
const id = dashboard ? dashboardTheme : theme;
if (id) setThemeUrl(getThemeUrl(id));
```

## 2c. CSS containment clips what you draw

Not a Jellyfin-specific quirk, but the place it bites hardest in this codebase, and the
kind of thing that reads as "my rule isn't working" rather than as what it is.

Jellyfin sets containment on two of the elements a theme most wants to add depth to:

| Element | Value | Includes `paint`? |
|---|---|---|
| `.card` | `contain: content` (= `layout paint style`) | yes |
| `.skinHeader` | `contain: layout style paint` | yes |

**Paint containment clips everything the element draws to its own box** — backgrounds,
outlines and `box-shadow` included. Anything that reaches outside the border box is cut
off flat at the edge, silently: no error, nothing odd in the computed style of the rule
you wrote, and the shadow still shows up in DevTools as applied. What you see is a hard
square edge where a soft one should be.

Symptoms this produced here:

- A hover ring 2px outside a 71px avatar, sliced flat on the left, right and top.
- A drop shadow offset 24px down with a 60px blur, drawn *inside* the card's bounds and
  clipped square — which reads as a dark rectangle behind the card rather than as a
  shadow under it.

The fix is to drop `paint` and keep the rest: `contain: layout style` preserves the part
that actually pays off on a grid of a few hundred cards, and neither `layout` nor `style`
affects what is drawn outside the box.

**Specificity note, measured on a live 10.11.8 server:** a bare `.card` **loses** — the
computed value stays `content` — while `.itemsContainer .card` (0,2,0) takes effect. No
readable rule in the document declares `contain` on that element, and the winning sheet
cannot be enumerated from script, so this is out-specified rather than diagnosed. The same
wall appears on `html`'s background colour (see `themes/cinematic-glass/src/02-base.css`).

## 3. How custom CSS is injected

`src/components/CustomCss.tsx`:

```jsx
{!disableCustomCss && brandingOptions?.CustomCss && <style>{brandingOptions.CustomCss}</style>}
{userCustomCss && <style>{userCustomCss}</style>}
```

- **Server-wide:** Dashboard → **Branding** → Custom CSS. (Moved here in 10.11; it was
  under General before.)
- **Per-user:** Settings → Display → Custom CSS, plus a "disable server CSS" toggle.
- User CSS is injected *after* server CSS, so user CSS wins.
- Both are injected after the theme's `<link>` (`ThemeCss.tsx` → `themes/{id}/theme.css`).
- Applies to Jellyfin Web only — not to native clients (Android, TV, Swiftfin, etc.).

## 4. Distribution options (ranked)

### A. `@import` from a CDN into Branding → Custom CSS — *the community standard*
User pastes `@import url("https://cdn.jsdelivr.net/gh/user/repo@tag/theme.css");`.
Zero server access needed, survives updates, instantly updatable, works for remote users.
Downside: external fetch on every page load (offline/LAN-isolated setups suffer), and
`@import` must be the first rule in the block.

### B. First-class registered theme — *underused, and the nicest result*
`jellyfin-web`'s deployed `config.json` has a `themes` array:

```json
{ "name": "Dark", "id": "dark", "color": "#202020", "default": true }
```

Add an entry + drop `themes/<id>/theme.css` into the web root, and your theme appears
in the **Display settings theme dropdown** as a real theme, with `html[data-theme="<id>"]`
set for you and no `!important` arms race against the built-in theme (it *replaces*
`themes/dark/theme.css` rather than layering over it).
Caveats: needs filesystem access to the web root; wiped by server updates (so pair with
a Docker volume mount or a post-update script); unknown `data-theme` ids fall back to
MUI's `:root` block, which equals the dark scheme — a predictable base.

### C. Skin Manager plugin store
`Jellyfin-PG/Skin-Manager-Themes` hosts a live `skins.json` the plugin fetches; themes are
submitted by GitHub issue. Entry schema:
`name, author, description, version, jellyfin, tags[], previewUrl, sourceUrl, cssUrl,
preconnect[]?, vars[]?`. The `vars` field lets the plugin render a settings UI for
CSS variables — worth designing the variable API around.

## 5. Ecosystem survey (Sept 2026)

| Theme | Stars | Last push | Architecture |
|---|---|---|---|
| lscambo13/ElegantFin | 2101 | 2026-09-04 | One monolithic dated CSS per release (108 KB) + add-on modules |
| prayag17/JellySkin | 1022 | 2024-07 (stale) | Single file, icon replacement |
| CTalvio/Ultrachromic | 989 | 2026-09-05 | **Most modular:** `base.css` + `type/*` (color) + `presets/*` + opt-in effect modules |
| loof2736/scyfin | 730 | 2026-05-24 | Base + accent-color modules + feature toggles |
| AumGupta/abyss-jellyfin | 624 | 2026-08-29 | — |
| tedhinklater/finimalism | 457 | 2026-02-16 | — |
| n00bcodr/Jellyfish | 280 | 2026-09-08 | Base + `colors/*` palette modules w/ background images |
| catppuccin/jellyfin | 127 | 2026-08-06 | **Templated build:** one `theme.css` + `.tera` template → 4 flavour files |

**Finding:** every one of these themes still works by enumerating legacy classes and
slamming `!important`. A GitHub code search for `jf-palette` across all of GitHub returns
*no* community theme — only jellyfin-web itself and a few plugins. `MuiAppBar-root`
appears in ElegantFin and Jellyfish, but as structural patches, not as a variable strategy.
Driving the MUI layer through `--jf-*` is a genuinely open lane.

**Amended 2026-09-10, after building one.** That lane is narrower than this survey
implies, and the reason is &sect;2b: the dashboard receives no custom CSS, so none of these
themes *could* have reached it through the install they all ship with. The open lane is
real but it only opens on the registered-theme profile, plus the experimental layout's
app bar and drawer, which `apps/experimental` does mount `CustomCss` for.

Worth stating plainly because the original wording reads as "nobody thought of this",
when the truth is closer to "the standard install cannot do it".

## 6. Version landscape

| Version | Date | Note |
|---|---|---|
| 10.11.5 | 2025-12-15 | |
| **10.11.8** | **2026-04-05** | **our target** |
| 10.11.11 | 2026-06-06 | last of the 10.11 line; CSS-compatible with .8 |
| 12.0 | 2026-09-08 | released yesterday |

10.11.8 → 10.11.11 has an identical file tree (1455 paths), so targeting "10.11.x"
costs nothing over pinning to .8.

**v12 forward-compat:** v12 keeps the same MUI `cssVariables` + `--jf-` + `data-theme`
architecture, but refactors themes into `src/themes/_base/_palette.scss` (SCSS vars) and
renames the apps `stable → legacy` and `experimental → modern`. A variable-driven theme
ports to v12 far more cheaply than an `!important`-driven one.

## 7. Reference files in this folder

- `reference/mui-jf-variables.10.11.8.css` — all 1097 generated `--jf-*` vars, per scheme
- `reference/generate-mui-variables.cjs` — regenerate the above (needs `@mui/material@6.4.12`, `lodash`)
- `reference/jellyfin-dark-theme.10.11.8.scss` — the built-in dark theme; doubles as the
  canonical list of ~102 themable legacy classes
- `reference/jellyfin-site.10.11.8.scss`, `reference/jellyfin-card.10.11.8.scss` — base layout & card structure
