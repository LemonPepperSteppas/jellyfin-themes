# -*- coding: utf-8 -*-
"""Assemble the seven directions into ONE presentation artifact."""
import io, os
import dirs as X
import make as K

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

SCREENS = [
    ("01", "signin", "Sign in", "The first thing anyone sees, and the only screen with no artwork to lean on."),
    ("02", "home", "Home", "The screen that decides whether a theme works. Every direction composes this one differently &mdash; billboard, magazine spread, data table, poster wall."),
    ("03", "library", "Library", "A wall of artwork, or deliberately not one. Watch the item count that fits above the fold."),
    ("04", "detail", "Movie detail", "The page a theme lives or dies on: artwork, ribbon, cast, and the media info that explains why a file is transcoding."),
    ("05", "episodes", "Series &amp; episodes", "The densest list in the app. Thumbnail, number, title, air date, synopsis, runtime and watched state, without turning into soup."),
    ("06", "player", "Player", "Controls sit over moving picture, so contrast has to come from the scrim rather than the palette."),
    ("07", "dashboard", "Dashboard", "All React and MUI in 10.11 &mdash; the surface every existing community theme leaves stock. This half is driven entirely by <code>--jf-palette-*</code>."),
    ("08", "components", "Components &amp; states", "Every state the accent has to survive: hover, focus, disabled, selected, and the semantic colours that must stay legible beside it."),
]

DOT = {"glass": "#e8eef6", "editorial": "#b3a369", "terminal": "#ffb000", "warm": "#d98e73",
       "prime": "#e0322b", "plain": "#00a4dc", "immersion": "#f4efe9", "daylight": "#0f6d6f"}
SHORT = {"glass": "billboard, frosted pill nav", "editorial": "no hero, magazine index",
         "warm": "sidebar, greeting, big tiles",
         "prime": "billboard, rails, Top 10", "plain": "no hero, 12-across grid",
         "immersion": "poster wall, artwork wash", "daylight": "light, large, legible"}

FONTS = ("https://fonts.googleapis.com/css2"
         "?family=Manrope:wght@400;500;600;700;800"
         "&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,600;0,6..96,700;1,6..96,400"
         "&family=Libre+Franklin:wght@400;500;600;700"
         "&family=Nunito+Sans:wght@400;500;600;700;800"
         "&family=Archivo:wght@400;500;600;700;800;900"
         "&family=IBM+Plex+Sans:wght@400;500;600;700"
         "&family=Outfit:wght@200;300;400;500;600;700"
         "&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400"
         "&family=IBM+Plex+Mono:wght@400;500&display=swap")

SHELL_CSS = """
/* ------------------------------------------------- switcher & overview */
html,body{transition:background .26s ease,color .26s ease}
.only{display:none}

.sevenup{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:14px;padding:34px 0 6px}
.mini{display:block;text-align:left;cursor:pointer;font:inherit;padding:0;background:var(--m-bg);position:relative;isolation:isolate;
  color:var(--m-text);border:1px solid var(--m-border-strong);border-radius:var(--m-radius-lg);
  overflow:hidden;transition:border-color .16s,transform .16s}
.mini:hover{border-color:var(--m-accent);transform:translateY(-2px)}
.mini-box{display:block;position:relative;width:100%;aspect-ratio:1180/730;overflow:hidden;background:var(--m-bg)}
.mini-in{position:absolute;top:0;left:0;width:1180px;height:730px;transform:scale(var(--s,.2));
  transform-origin:0 0;pointer-events:none}
.mini-in .vp{height:730px !important}
.mini-in .wash{filter:blur(16px) saturate(150%)}
.mini-cap{display:block;padding:10px 13px;border-top:1px solid var(--m-border);background:var(--m-bg-elev)}
.mini-cap b{display:block;font-size:13px;font-weight:700;letter-spacing:-.01em}
.mini-cap em{display:block;font-style:normal;font-size:11px;color:var(--m-faint);margin-top:2px}
.mini[aria-current="true"]{border-color:var(--m-accent);box-shadow:0 0 0 1px var(--m-accent)}

.switch{position:sticky;top:0;z-index:60;margin-top:30px;background:var(--m-bg);
  border-block:1px solid var(--m-border);backdrop-filter:var(--m-bar-blur,none)}
.switch .wrap{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding-block:10px}
.segs{display:flex;gap:3px;flex-wrap:wrap}
.seg{display:inline-flex;align-items:center;gap:8px;cursor:pointer;font:inherit;padding:7px 13px;
  border-radius:var(--m-radius-pill,var(--m-radius-sm));border:1px solid transparent;background:transparent;
  color:var(--m-muted);font-size:13px;font-weight:600;white-space:nowrap;
  transition:background .16s,color .16s,border-color .16s}
.seg i{width:10px;height:10px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 1px rgba(127,127,127,.4)}
.seg kbd{font-family:var(--m-font-mono);font-size:10px;color:var(--m-faint);border:1px solid var(--m-border-strong);
  border-radius:3px;padding:0 4px;font-weight:400}
.seg:hover{color:var(--m-text);border-color:var(--m-border-strong)}
.seg[aria-pressed="true"]{background:var(--m-accent);color:var(--m-accent-ink);border-color:var(--m-accent)}
.seg[aria-pressed="true"] kbd{color:var(--m-accent-ink);border-color:currentColor;opacity:.6}
.jumps{display:flex;gap:1px;flex-wrap:wrap;margin-left:auto}
.jumps a{padding:6px 9px;font-size:12px;color:var(--m-faint);text-decoration:none;border-radius:var(--m-radius-pill,var(--m-radius-sm));white-space:nowrap}
.jumps a:hover{color:var(--m-accent)}
@media (max-width:900px){.jumps{display:none}}
"""

SCRIPT = """
(function () {
  var ORDER = __ORDER__;
  var root = document.documentElement;
  var segs = [].slice.call(document.querySelectorAll('.seg'));
  var minis = [].slice.call(document.querySelectorAll('.mini'));

  function fit() {
    minis.forEach(function (m) {
      var box = m.querySelector('.mini-box');
      if (box) box.style.setProperty('--s', (box.clientWidth / 1180).toFixed(4));
    });
  }
  function set(dir, keep) {
    if (ORDER.indexOf(dir) < 0) return;
    var y = window.scrollY;
    root.setAttribute('data-dir', dir);
    segs.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.dir === dir)); });
    minis.forEach(function (m) { m.setAttribute('aria-current', String(m.dataset.go === dir)); });
    if (keep) window.scrollTo(0, y);
  }

  segs.forEach(function (b) { b.addEventListener('click', function () { set(b.dataset.dir, true); }); });
  minis.forEach(function (m) {
    function go() {
      set(m.dataset.go, false);
      document.querySelector('.switch').scrollIntoView({ block: 'start' });
    }
    m.addEventListener('click', go);
    m.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
    var i = ORDER.indexOf(root.getAttribute('data-dir') || ORDER[0]);
    if (e.key >= '1' && e.key <= '7' && ORDER[+e.key - 1]) { set(ORDER[+e.key - 1], true); e.preventDefault(); }
    else if (e.key === 'ArrowRight') { set(ORDER[(i + 1) % ORDER.length], true); e.preventDefault(); }
    else if (e.key === 'ArrowLeft') { set(ORDER[(i + ORDER.length - 1) % ORDER.length], true); e.preventDefault(); }
  });
  [].slice.call(document.querySelectorAll('.jl')).forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var dir = root.getAttribute('data-dir') || ORDER[0];
      var el = document.getElementById(dir + '-' + a.dataset.s);
      if (el) el.scrollIntoView({ block: 'start' });
    });
  });
  window.addEventListener('resize', fit);
  fit();
  set(ORDER[0], false);
})();
"""


def prefix_css(block, prefix):
    out, i = [], 0
    while True:
        j = block.find("{", i)
        if j < 0:
            break
        k = block.find("}", j)
        sel = block[i:j].strip()
        body = block[j + 1:k]
        parts = [p.strip() for p in sel.split(",") if p.strip()]
        out.append("%s{%s}" % (", ".join(prefix + " " + p for p in parts), body))
        i = k + 1
    return "\n".join(out)


def ramp_html(rows):
    return "\n".join('<div class="ramp-row"><i style="background:%s"></i><code>%s</code><span>%s</span></div>'
                     % r for r in rows)


def facts_html(rows):
    return '<dl class="facts">%s</dl>' % "".join("<dt>%s</dt><dd>%s</dd>" % r for r in rows)


def jf_html(rows, radius):
    lines = ["<em>/* the MUI half: dashboard, drawer, dialogs, every form field */</em>",
             "<u>html[data-theme]</u> {"]
    lines += ["  <b>--jf-palette-%s</b>: %s;" % r for r in rows]
    lines.append("  <b>--jf-shape-borderRadius</b>: %s;" % radius)
    lines.append("}")
    return "\n".join(lines)


def main():
    css = io.open(os.path.join(HERE, "deck.css"), encoding="utf-8").read()

    tok, over = [], []
    for i, s in enumerate(X.ORDER):
        d = X.D[s]
        t = d["tokens"].rstrip()
        if "--m-font-mono" not in t:
            t += "\n  --m-font-mono:%s;" % K.MONO
        page = ':root, :root[data-dir="%s"]' % s if i == 0 else ':root[data-dir="%s"]' % s
        tok.append("%s{%s\n}" % (page, t))
        tok.append(".scope-%s{%s\n}" % (s, t))
        over.append(prefix_css(d["css"], ':root[data-dir="%s"]' % s))
        over.append(prefix_css(d["css"], ".scope-%s" % s))
        if i == 0:
            over.append(prefix_css(d["css"], ":root:not([data-dir])"))
    tok.append(":root{--grain:%s}" % K.GRAIN)

    show = [':root:not([data-dir]) .only[data-for="%s"]' % X.ORDER[0]]
    show += [':root[data-dir="%s"] .only[data-for="%s"]' % (s, s) for s in X.ORDER]
    show_css = ",\n".join(show) + "{display:block}"

    # ---- overview: a real scaled snapshot of each direction's home
    minis = ""
    for s in X.ORDER:
        d = X.D[s]
        minis += ('<div class="mini scope-%s" data-go="%s" role="button" tabindex="0" aria-label="%s">'
                  '<div class="mini-box"><div class="mini-in">%s</div></div>'
                  '<div class="mini-cap"><b>%s</b><em>%s</em></div></div>'
                  % (s, s, d["title"], d["screens"]["home"], d["title"], SHORT[s]))

    # ---- per-direction body: header, system panel, nine screens, tokens, outro
    bodies = ""
    for s in X.ORDER:
        d = X.D[s]
        scr = ""
        for num, sid, name, blurb in SCREENS:
            scr += ('<article class="screen" id="%s-%s"><div class="screen-head">'
                    '<span class="screen-num">%s</span><h2>%s</h2><p>%s</p></div>'
                    '<div class="frame"><div class="frame-bar"><i></i><i></i><i></i>'
                    '<span>jellyfin.local/web/#/%s</span></div>%s</div></article>'
                    % (s, sid, num, name, blurb, sid, d["screens"][sid]))
        bodies += ('<div class="only" data-for="%s">'
                   '<header class="dirhead"><h2>%s</h2><p class="thesis">%s</p>'
                   '<dl class="mast-meta">'
                   '<div><dt>Reference points</dt><dd>%s</dd></div>'
                   '<div><dt>Best for</dt><dd>%s</dd></div>'
                   '<div><dt>Trade-off</dt><dd>%s</dd></div></dl></header>'
                   '<div class="system"><section><h3>Palette</h3>%s</section>'
                   '<section><h3>Structure</h3>%s</section></div>'
                   '%s'
                   '<article class="screen" id="%s-tokens"><div class="screen-head">'
                   '<span class="screen-num">09</span><h2>What ships</h2>'
                   '<p>The variable block behind everything above. Overriding the whole accent family is '
                   'mandatory &mdash; MUI computes <code>light</code>, <code>dark</code> and '
                   '<code>Channel</code> values in JavaScript, so setting <code>main</code> alone leaves '
                   'every hover and ripple Jellyfin blue.</p></div><pre class="tokens">%s</pre></article>'
                   '<section class="outro"><h2>Taking %s forward</h2><p>%s</p>'
                   '<p>It installs as one line pasted into <strong>Dashboard &rarr; Branding &rarr; '
                   'Custom CSS</strong>. Because the accent lives in variables rather than a few hundred '
                   '<code>!important</code> rules, an alternate colourway costs about fifteen lines.</p>'
                   '</section></div>'
                   % (s, d["title"], d["thesis"], d["ref"], d["best"], d["watch"],
                      ramp_html(d["ramp"]), facts_html(d["facts"]), scr, s,
                      jf_html(d["jf"], d["radius"]), d["title"], d["outro"]))

    segs = "".join('<button class="seg" type="button" data-dir="%s" aria-pressed="false">'
                   '<i style="background:%s"></i>%s<kbd>%d</kbd></button>'
                   % (s, DOT[s], X.D[s]["title"], i + 1) for i, s in enumerate(X.ORDER))

    jumps = "".join('<a class="jl" href="#" data-s="%s">%s</a>' % (sid, name)
                    for _, sid, name, _ in SCREENS)

    html = (
        "<title>Seven Directions for Jellyfin</title>\n"
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="' + FONTS + '">\n'
        "<style>\n" + "\n".join(tok) + "\n" + css + "\n" + SHELL_CSS + "\n"
        "/* ---- per-direction overrides ---- */\n" + "\n".join(over) + "\n"
        "/* ---- per-direction visibility ---- */\n" + show_css + "\n</style>\n\n"
        '<div class="wrap">\n'
        '  <header class="idhead">\n'
        '    <p class="kicker">Art direction &middot; Jellyfin 10.11.x web</p>\n'
        "    <h1>Seven Directions for Jellyfin</h1>\n"
        '    <p class="lede">Seven ways the server could work &mdash; not seven colour schemes. Each one '
        'rebuilds the <strong>layout</strong>: where navigation lives, whether there is a hero at all, '
        'whether the library is posters or a table, how much fits on a screen. Pick one below and the whole '
        'page becomes it, across nine screens.</p>\n'
        "  </header>\n"
        '  <div class="sevenup">' + minis + "</div>\n"
        "</div>\n\n"
        '<nav class="switch"><div class="wrap"><div class="segs">' + segs + "</div>"
        '<div class="jumps">' + jumps + "</div></div></nav>\n\n"
        '<div class="wrap">\n' + bodies +
        '  <p style="color:var(--m-faint);font-size:13px;padding-bottom:60px">Mockups, not screenshots. '
        "Artwork is procedural stand-in; titles and metadata are real so every layout carries real text "
        "lengths.</p>\n</div>\n\n"
        "<script>" + SCRIPT.replace("__ORDER__", str(X.ORDER).replace("'", '"')) + "</script>\n"
    )

    bad = sorted(set(c for c in html if ord(c) > 127))
    assert not bad, "non-ascii: %r" % bad
    p = os.path.join(OUT, "theme-directions.html")
    io.open(p, "w", encoding="utf-8").write(html)
    print("wrote %s  %.0f KB" % (os.path.basename(p), len(html) / 1024.0))


if __name__ == "__main__":
    main()
