# -*- coding: utf-8 -*-
"""Build the merged eight-direction Jellyfin deck.

Each direction composes its OWN layout from the kit in deck.css - different
navigation, different home composition, different card system, different detail
page. Tokens carry colour and type; structure is chosen per direction.
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'"
         "%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/"
         "%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E\")")
MONO = '"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,monospace'

# ------------------------------------------------------------------- content
CONT = [("Dune: Part Two", "1h 03m left", 2, 62), ("The Bear", "S3:E5 &middot; 24m left", 3, 18),
        ("Chernobyl", "S1:E4 &middot; 12m left", 4, 81), ("Past Lives", "1h 14m left", 5, 34),
        ("Arrival", "1h 42m left", 6, 9), ("The Zone of Interest", "55m left", 8, 47)]
NEXT = [("Severance", "S2:E4 &middot; Woe&rsquo;s Hollow", 7), ("The Bear", "S3:E6 &middot; Napkins", 3),
        ("Sh&#333;gun", "S1:E7 &middot; A Stick of Time", 9), ("Slow Horses", "S4:E2 &middot; Hard Truths", 10)]
LIB = [("Blade Runner 2049", "2017", 1), ("Dune: Part Two", "2024", 2), ("Past Lives", "2023", 5),
       ("Arrival", "2016", 6), ("The Zone of Interest", "2023", 8), ("Anatomy of a Fall", "2023", 4),
       ("Killers of the Flower Moon", "2023", 12), ("Poor Things", "2023", 10), ("Oppenheimer", "2023", 9),
       ("The Holdovers", "2023", 11), ("Sicario", "2015", 7), ("First Cow", "2019", 3),
       ("Aftersun", "2022", 5), ("Tar", "2022", 4), ("Nope", "2022", 12), ("The Northman", "2022", 8),
       ("Decision to Leave", "2022", 7), ("Everything Everywhere", "2022", 10)]
TROWS = [("Blade Runner 2049", "2017", "2:44", "HEVC", "61.4G", "78.2", "ok", "47m left"),
         ("Dune: Part Two", "2024", "2:46", "HEVC", "54.9G", "71.0", "ok", "1h03 left"),
         ("Past Lives", "2023", "1:46", "HEVC", "38.2G", "62.4", "ok", "watched"),
         ("Arrival", "2016", "1:56", "H264", "24.1G", "31.8", "wr", "unwatched"),
         ("Anatomy of a Fall", "2023", "2:31", "HEVC", "44.7G", "58.1", "ok", "unwatched"),
         ("The Zone of Interest", "2023", "1:45", "HEVC", "31.9G", "49.3", "ok", "55m left"),
         ("Oppenheimer", "2023", "3:00", "HEVC", "88.3G", "92.7", "ok", "watched"),
         ("First Cow", "2019", "2:02", "H264", "19.4G", "26.2", "wr", "unwatched")]
CAST = [("Greta Lee", "Nora", "#5a4a63", "#241d29"), ("Teo Yoo", "Hae Sung", "#4a5f6b", "#1d272d"),
        ("John Magaro", "Arthur", "#6b5a4a", "#2d251d"), ("Celine Song", "Director", "#4a6b57", "#1d2d24"),
        ("S. Kirchner", "Cinematography", "#63524a", "#29211d")]
OVERVIEW = ("Nora and Hae Sung, two deeply connected childhood friends, are wrested apart after Nora&rsquo;s "
            "family emigrates from South Korea. Twenty years later, they are reunited in New York for one "
            "fateful week as they confront notions of destiny, love, and the choices that make a life.")
EPS = [("E4", "Violet", "27 Jun 2024", "36m &middot; Watched", 3, "done",
        "Sydney weighs an offer she cannot talk about. Carmy tries to hold the line on a menu that changes every night."),
       ("E5", "Children", "27 Jun 2024", "41m &middot; 24m left", 8, "now",
        "A wedding pulls the whole crew out of the kitchen for one afternoon, and the restaurant is left in unexpected hands."),
       ("E6", "Napkins", "27 Jun 2024", "34m &middot; Unwatched", 11, "",
        "Tina&rsquo;s story, told from the beginning: a layoff, a long walk through the city, and one open door.")]


# ------------------------------------------------------------------- helpers
def art(n, cls="", inner=""):
    return '<div class="art %s" data-art="%d">%s</div>' % (cls, n, inner)


def bar(pct):
    return '<span class="bar"><i style="width:%d%%"></i></span>' % pct


def card(title, sub, n, cls="", extra=""):
    return ('<div class="c %s">%s<p class="c-t">%s</p><p class="c-s">%s</p></div>'
            % (cls, art(n, "", extra), title, sub))


def cards(items, cls="", meta="", wide=False):
    inner = "".join(card(t, s, n, "w" if wide else "", x) for t, s, n, x in items)
    return '<div class="cards %s">%s</div>' % (meta, inner)


def rail(title, items, more="See all", meta="", wide=False, cls=""):
    return ('<div class="rail %s"><div class="rail-h"><h4>%s</h4><span>%s</span></div>%s</div>'
            % (cls, title, more, cards(items, meta=meta, wide=wide)))


def cont_items():
    return [(t, s, n, bar(p)) for t, s, n, p in CONT]


def next_items():
    return [(t, s, n, "") for t, s, n in NEXT]


def lib_items(k=12):
    return [(t, y, n, "") for t, y, n in LIB[:k]]


def nav_top(active="Home", extra=""):
    links = "".join('<a href="#" class="%s">%s</a>' % ("on" if l == active else "", l)
                    for l in ["Home", "Movies", "Shows", "Music", "Live TV"])
    return ('<div class="nav-top %s"><div class="brand"><i></i>Jellyfin</div>'
            '<nav class="nav-links">%s</nav>'
            '<div class="nav-acts"><span>&#9906;</span><span>&#9744;</span><span class="ava">R</span></div></div>'
            % (extra, links))


def nav_rule(active="Films"):
    links = "".join('<a href="#" class="%s">%s</a>' % ("on" if l == active else "", l)
                    for l in ["Films", "Series", "Index", "Search"])
    return ('<div class="nav-rule"><span class="word">Jellyfin</span>'
            '<nav class="links">%s</nav></div>' % links)


def nav_pill(active="Home"):
    links = "".join('<a href="#" class="%s">%s</a>' % ("on" if l == active else "", l)
                    for l in ["Home", "Films", "Series", "Search"])
    return '<nav class="nav-pill">%s</nav>' % links


def nav_min():
    return ('<div class="nav-min"><span>&#9776;</span><span>&#9906;</span>'
            '<span class="sp"><span>&#9825;</span><span class="ava">R</span></span></div>')


def nav_plain(active="Home"):
    links = "".join('<a href="#" class="%s">%s</a>' % ("on" if l == active else "", l)
                    for l in ["Home", "Movies", "Shows", "Music", "Live TV"])
    return ('<div class="nav-plain"><b>Jellyfin</b>%s'
            '<span class="sp"><span>Search</span><span>Settings</span><span>Rid</span></span></div>' % links)


def side(kind="nav", active="Home"):
    if kind == "tree":
        items = [("Films", "Home"), ("Series", ""), ("Music", ""), ("Photos", "")]
        body = '<div class="side-h">library</div>'
        for name, _ in items:
            on = "on" if name == active else ""
            body += '<a href="#" class="%s">%s/</a>' % (on, name.lower())
        body += ('<a href="#" class="kid">4k-remux/</a><a href="#" class="kid">1080p/</a>'
                 '<div class="side-h" style="padding-top:14px">system</div>'
                 '<a href="#">sessions</a><a href="#">tasks</a><a href="#">logs</a>')
        return '<nav class="side side-tree" style="--side-w:170px">%s</nav>' % body
    fat = "side-fat" if kind == "fat" else ""
    items = [("&#9750;", "Home"), ("&#9707;", "Movies"), ("&#9744;", "Shows"),
             ("&#9834;", "Music"), ("&#9825;", "Favourites"), ("&#9202;", "Recent")]
    body = '<div class="side-brand"><i></i>Jellyfin</div>'
    for ico, name in items:
        body += '<a href="#" class="%s"><i>%s</i>%s</a>' % ("on" if name == active else "", ico, name)
    return '<nav class="side %s">%s</nav>' % (fat, body)


def billboard(kick="", title="Blade Runner 2049", tag="", acts="", dots=True, h=300, size=42, n=1):
    d = ('<div class="bb-dots"><i class="on"></i><i></i><i></i><i></i></div>') if dots else ""
    k = '<span class="bb-rank">%s</span>' % kick if kick else ""
    return ('<div class="bb" style="--bb-h:%dpx">%s<div class="bb-scrim"></div>'
            '<div class="bb-body">%s<h3 class="bb-logo" style="--bb-size:%dpx">%s</h3>'
            '<p class="bb-tag">%s</p><div class="bb-acts">%s</div></div>%s</div>'
            % (h, art(n, "bb-art"), k, size, title, tag, acts, d))


def backdrop(kick, title, meta_html, desc, acts, n=1, h=286):
    return ('<div class="bd" style="--bd-h:%dpx">%s<div class="bd-scrim"></div>'
            '<div class="bd-body"><p class="kick">%s</p><h3 class="h-title">%s</h3>%s'
            '<p class="h-desc">%s</p><div class="h-acts">%s</div></div></div>'
            % (h, art(n, "bd-art"), kick, title, meta_html, desc, acts))


META_FULL = ('<ul class="meta"><li>2017</li><li class="star">&#9733; 8.0</li><li>2h 44m</li>'
             '<li class="badge">4K</li><li class="badge">HDR10</li><li class="badge">DTS-HD MA</li></ul>')
BR_DESC = ("A young blade runner uncovers a secret buried for thirty years, and goes looking for a man "
           "who stopped wanting to be found.")
ACTS_MAIN = ('<button class="btn btn-1">&#9654; Resume &middot; 47m left</button>'
             '<button class="btn btn-2">Details</button>'
             '<button class="btn btn-i">&#10003;</button><button class="btn btn-i">&#9825;</button>')


def grid(items, cols=7, meta=""):
    inner = "".join(card(t, s, n, "", x) for t, s, n, x in items)
    return '<div class="grid %s" style="--cols:%d">%s</div>' % (meta, cols, inner)


def mosaic(items, cols=9):
    out = []
    for i, (t, s, n, x) in enumerate(items):
        out.append(art(n, "dim" if i % 5 == 3 else ""))
    return '<div class="mosaic" style="--cols:%d">%s</div>' % (cols, "".join(out))


def tiles(items, cols=3):
    inner = "".join('<div class="tile-c">%s<b>%s</b><span>%s</span></div>' % (art(n, "", x), t, s)
                    for t, s, n, x in items)
    return '<div class="tiles" style="--cols:%d">%s</div>' % (cols, inner)


def table(cols, rows, sortcol=0, thumbs=False):
    head = "".join('<th class="%s">%s</th>' % ("s" if i == sortcol else "", c) for i, c in enumerate(cols))
    body = ""
    for r in rows:
        title, year, run, codec, size, br, state, watched = r
        th = ('<td><span class="th art" data-art="%d"></span></td>' % (LIB[rows.index(r) % len(LIB)][2])) if thumbs else ""
        body += ('<tr class="%s">%s<td class="n">%s</td><td>%s</td><td>%s</td><td>%s</td>'
                 '<td>%s</td><td class="%s">%s</td><td>%s</td></tr>'
                 % ("on" if watched.endswith("left") and "47m" in watched else "", th,
                    title, year, run, codec, size, state, br, watched))
    return '<table class="tbl">%s%s</table>' % ("<thead><tr>%s</tr></thead>" % head, "<tbody>%s</tbody>" % body)


def tlist(items):
    out = []
    for i, (t, s, n) in enumerate(items):
        out.append('<div class="tl"><span class="no">%02d</span>%s'
                   '<div class="b"><h5>%s</h5><p>%s</p></div>'
                   '<div class="r"><b>%s</b>Added today</div></div>'
                   % (i + 1, art(n, "th"), t, OVERVIEW[:96] + "&hellip;", s))
    return '<div class="tlist">%s</div>' % "".join(out)


def ep_rows(rth=150):
    out = []
    for no, name, when, foot, n, state in [(e[0], e[1], e[2], e[3], e[4], e[5]) for e in EPS]:
        mark = '<span class="tick">&#10003;</span>' if state == "done" else (bar(18) if state == "now" else "")
        desc = [e[6] for e in EPS if e[0] == no][0]
        out.append('<div class="row-i %s"><div class="row-th art" data-art="%d" style="--rth:%dpx">%s</div>'
                   '<div class="row-b"><div class="row-top"><span class="row-no">%s</span>'
                   '<h5 class="row-n">%s</h5><span class="row-w">%s</span></div>'
                   '<p class="row-d">%s</p><div class="row-a"><span>%s</span></div></div></div>'
                   % ("on" if state == "now" else "", n, rth, mark, no, name, when, desc, foot))
    return '<div class="rows">%s</div>' % "".join(out)


def cast_html():
    return '<div class="cast">%s</div>' % "".join(
        '<figure style="--u1:%s;--u2:%s"><i></i><b>%s</b><span>%s</span></figure>' % (a, b, n, r)
        for n, r, a, b in CAST)


STREAMS = ('<div class="streams"><h5>Media info</h5>'
           '<dl><dt>Container</dt><dd>MKV &middot; 61.4 GB</dd><dt>Video</dt><dd>HEVC 3840&times;2160</dd>'
           '<dt>Bitrate</dt><dd>78.2 Mbps</dd><dt>Range</dt><dd>HDR10</dd></dl><hr>'
           '<dl><dt>Audio</dt><dd>TrueHD 7.1</dd><dt>Subtitles</dt><dd>3 tracks</dd></dl></div>')

D_META = ('<ul class="meta"><li>2023</li><li class="star">&#9733; 7.8</li><li class="crit">95% critics</li>'
          '<li>1h 46m</li><li class="badge">PG-13</li><li class="badge">4K</li><li class="badge">HDR10</li></ul>')
D_GENRES = '<div class="genres"><span class="chip">Drama</span><span class="chip">Romance</span><span class="chip">A24</span></div>'
D_ACTS = ('<button class="btn btn-1">&#9654; Play</button><button class="btn btn-2">Trailer</button>'
          '<button class="btn btn-i">&#10003;</button><button class="btn btn-i">&#9825;</button>')

SESSIONS = ('<div class="panel"><div class="panel-h"><h5>Active sessions</h5><span>3 now</span></div>'
            '<div class="sess"><div class="th art" data-art="1"></div><div class="who">'
            '<b>Rid &middot; Blade Runner 2049</b><span>Chrome on Windows &middot; 4K HDR</span></div>'
            '<span class="pill d">Direct play</span><span class="pc">78.2 Mbps</span></div>'
            '<div class="sess"><div class="th art" data-art="3"></div><div class="who">'
            '<b>Amina &middot; The Bear S3:E5</b><span>Android TV &middot; 1080p</span></div>'
            '<span class="pill t">Transcode</span><span class="pc">12.4 Mbps</span></div>'
            '<div class="sess"><div class="th art" data-art="9"></div><div class="who">'
            '<b>Guest &middot; Sh&#333;gun S1:E7</b><span>Safari on iPad &middot; 720p</span></div>'
            '<span class="pill d">Direct stream</span><span class="pc">6.1 Mbps</span></div></div>')

TILES_S = ('<div class="tiles-s">'
           '<div class="tl-s"><b>Sessions</b><strong>3</strong><span>2 streaming now</span></div>'
           '<div class="tl-s"><b>Library</b><strong>4,182</strong><span>across 6 libraries</span></div>'
           '<div class="tl-s"><b>Transcodes</b><strong>1</strong><span>HEVC &rarr; H.264</span></div>'
           '<div class="tl-s"><b>Uptime</b><strong>18d</strong><span>since last restart</span></div></div>')

INVENTORY = ('<div class="inv">'
             '<div><h5>Buttons</h5>'
             '<div class="ir"><span class="il">Default</span><button class="btn btn-1">Play</button>'
             '<button class="btn btn-2">Details</button><button class="btn btn-i">&#8943;</button></div>'
             '<div class="ir"><span class="il">Focus &amp; disabled</span>'
             '<button class="btn btn-1 focus">Play</button><button class="btn btn-2" disabled>Unavailable</button></div>'
             '<div class="ir"><span class="il">Small</span><button class="btn btn-1 btn-sm">Save</button>'
             '<button class="btn btn-2 btn-sm">Cancel</button></div></div>'
             '<div><h5>Inputs</h5>'
             '<div class="field"><label>Server address</label><div class="input ph">http://jellyfin.local:8096</div></div>'
             '<div class="field"><label>Display name</label><div class="input on">Living room</div></div>'
             '<div class="ir" style="margin-top:14px"><span class="check" style="margin:0"><i>&#10003;</i> Hardware acceleration</span></div>'
             '<div class="ir"><span class="sw"></span><span style="font-size:12.5px;color:var(--m-muted)">Remote access</span></div>'
             '<div class="ir"><span class="sw off"></span><span style="font-size:12.5px;color:var(--m-muted)">Auto-discovery</span></div></div>'
             '<div><h5>Chips &amp; badges</h5>'
             '<div class="ir"><span class="chip on">Unwatched</span><span class="chip">HDR</span>'
             '<span class="chip">Drama</span><span class="chip">A24</span></div>'
             '<div class="ir"><span class="badge">4K</span><span class="badge">HDR10</span>'
             '<span class="badge">DTS-HD</span><span class="badge">TV-MA</span></div>'
             '<div class="ir"><span class="il">Semantic</span><span class="pill d">Direct play</span>'
             '<span class="pill t">Transcode</span></div>'
             '<div class="ir" style="margin-top:14px"><span class="prog"><i></i></span></div></div>'
             '<div><h5>Overlays</h5>'
             '<div class="ir" style="display:block"><div class="toast"><i></i>Library scan finished &middot; 42 items added</div></div>'
             '<div class="ir" style="display:block;margin-top:14px"><div class="menu">'
             '<a href="#" class="on">Mark as played</a><a href="#">Add to playlist</a>'
             '<a href="#">Edit metadata</a><a href="#">Refresh</a></div></div></div>'
             '<div><h5>Type scale</h5><div class="scale">'
             '<div class="scale-row"><b>Display</b><em class="s-display">Blade Runner 2049</em></div>'
             '<div class="scale-row"><b>Title</b><em class="s-title">Continue Watching</em></div>'
             '<div class="scale-row"><b>Body</b><em class="s-body">Two childhood friends, reunited</em></div>'
             '<div class="scale-row"><b>Label</b><em class="s-label">Media info</em></div>'
             '<div class="scale-row"><b>Data</b><em class="s-mono">78.2 Mbps &middot; HEVC</em></div>'
             '</div></div></div>')
