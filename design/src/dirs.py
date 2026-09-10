# -*- coding: utf-8 -*-
"""Direction specs, each composing its own layout from the kit in make.py."""
import io, os
from make import *   # noqa: F401,F403
import make as K

# "terminal" (Amber Terminal) is still defined below; add it back here to restore it.
ORDER = ["glass", "editorial", "warm", "prime", "plain", "immersion", "daylight"]

# =========================================================== shared screen bits
def vp(cls, inner, style=""):
    return '<div class="vp %s" style="%s">%s</div>' % (cls, style, inner)


def player(kind="classic", extra=""):
    scrub = ('<div class="scrub"><div class="tt">%s<b>1:07:12</b></div>'
             '<span class="buf"></span><span class="pl"></span>'
             '<span class="ch" style="left:12%%"></span><span class="ch" style="left:29%%"></span>'
             '<span class="ch" style="left:58%%"></span><span class="ch" style="left:77%%"></span>'
             '<span class="kn"></span></div>' % K.art(6))
    top = ('<div class="osd-t"><span>&larr;</span><div><span class="t">Blade Runner 2049</span>'
           '<span class="s">&nbsp;&nbsp;2017</span></div>'
           '<div class="r"><span>&#9776;</span><span>CC</span><span>&#9881;</span><span>&#9974;</span></div></div>')
    ctl = ('<div class="ctl"><span>&#9198;</span><span class="play">&#10074;&#10074;</span>'
           '<span>&#9197;</span><span style="font-size:12px;opacity:.8">1.0&times;</span>'
           '<div class="sp"><span>&#9834;</span><span>CC</span><span>&#9636;</span><span>&#10530;</span></div></div>')
    if kind == "line":
        lin = ('<div class="lin"><span class="blk">&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;'
               '&#9617;&#9617;&#9617;&#9617;&#9617;&#9617;&#9617;&#9617;</span>'
               '<span>1:07:12 / 2:44:00</span><span>blade.runner.2049.2160p.hevc</span>'
               '<span class="sp">[cc] [7.1] [direct]</span></div>')
        body = '<div class="osd-b">%s</div>' % lin
    else:
        body = ('<div class="osd-b">%s<div class="times"><span>1:07:12</span>'
                '<span>&minus;1:36:48</span></div>%s</div>' % (scrub, ctl))
    cls = {"classic": "", "float": "float", "line": "line"}[kind]
    return ('<div class="osd %s">%s<div class="osd-veil"></div>%s%s%s</div>'
            % (cls, K.art(1, "osd-art"), top, extra, body))


def dash(nav, body):
    return '<div class="stack">%s<div class="pane"><div class="dash-bar">Dashboard</div>%s</div></div>' % (nav, body)


DASH_BODY = '<div class="dash-b">%s%s</div>' % (K.TILES_S, K.SESSIONS)

DASH_TABLE = ('<div class="dash-b"><div class="panel"><div class="panel-h"><h5>Sessions</h5>'
              '<span>3 active</span></div>%s</div></div>'
              % K.table(["user", "title", "client", "quality", "method", "mbps", "state"],
                        [("Rid", "2017", "chrome", "4K HDR", "direct", "78.2", "ok", "playing"),
                         ("Amina", "2024", "androidtv", "1080p", "transcode", "12.4", "wr", "playing"),
                         ("Guest", "2024", "safari", "720p", "direct", "6.1", "ok", "paused")]))


def signin(kind="card"):
    users = ('<div class="users">'
             '<div class="user on" style="--u1:#3f5f7a;--u2:#1c2c3a"><i></i><span>Rid</span></div>'
             '<div class="user" style="--u1:#6b4a63;--u2:#2e2029"><i></i><span>Amina</span></div>'
             '<div class="user" style="--u1:#4a6b52;--u2:#1f2d23"><i></i><span>Guest</span></div></div>')
    fields = ('<div class="field"><label>Username</label><div class="input">Rid</div></div>'
              '<div class="field"><label>Password</label><div class="input on">'
              '&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;</div></div>')
    qc = '<div class="qc"><span>Quick Connect</span><code>4T9K</code></div>'
    mark = '<div class="login-mark"><i></i><b>Jellyfin</b><span>10.11.8</span></div>'
    btn = '<button class="btn btn-1" style="width:100%;justify-content:center">Sign in</button>'

    if kind == "picker":
        who = "".join('<div class="%s"><i style="--u1:%s;--u2:%s"></i><span>%s</span></div>'
                      % (o, a, b, n) for n, a, b, o in
                      [("Rid", "#3f5f7a", "#1c2c3a", "on"), ("Amina", "#6b4a63", "#2e2029", ""),
                       ("Guest", "#4a6b52", "#1f2d23", ""), ("Kids", "#6b5f4a", "#2d281d", "")])
        return ('%s<div class="login-veil"></div><div class="picker"><h3>Who&rsquo;s watching?</h3>'
                '<div class="who">%s</div><button class="btn btn-2 btn-sm">Manage profiles</button></div>'
                % (K.art(7, "login-art"), who))
    if kind == "prompt":
        return ('<div class="prompt"><span style="color:var(--m-faint)">jellyfin 10.11.8 &mdash; tty1</span><br>'
                '<b>login:</b> <u>rid</u><br><b>password:</b> <u>**********</u><br>'
                '<span style="color:var(--m-faint)">quick-connect code:</span> <b>4T9K</b><br>'
                '<b>$</b> <span class="cur"></span></div>')
    if kind == "bare":
        return ('<div class="login"><div class="card-l bare" style="width:min(300px,100%%)">%s%s'
                '<div class="check"><i>&#10003;</i> Remember me</div>%s</div></div>'
                % (mark, fields, btn))
    if kind == "big":
        big = fields.replace('class="input"', 'class="input big"').replace('class="input on"', 'class="input on big"')
        return ('<div class="login">%s<div class="card-l" style="width:min(430px,100%%)">%s%s'
                '<div class="check"><i>&#10003;</i> Remember me on this device</div>'
                '<button class="btn btn-1 btn-lg" style="width:100%%;justify-content:center">Sign in</button>%s</div></div>'
                % ("", mark, big, qc))
    if kind == "wash":
        return ('%s<div class="wash-veil"></div><div class="login"><div class="card-l bare">%s%s%s</div></div>'
                % (K.art(7, "wash"), mark, fields, btn))
    if kind == "split":
        return ('%s<div class="login-veil"></div><div class="login left">'
                '<div class="card-l bare" style="width:min(330px,100%%)">%s%s%s%s</div></div>'
                % (K.art(7, "login-art"), mark, fields,
                   '<div class="check"><i>&#10003;</i> Remember me</div>' + btn, qc))
    return ('%s<div class="login-veil"></div><div class="login"><div class="card-l">%s%s%s'
            '<div class="check"><i>&#10003;</i> Remember me on this device</div>%s%s</div></div>'
            % (K.art(7, "login-art"), mark, users, fields, btn, qc))


ALPHA = ('<div class="alpha"><span>#</span><b>A</b><span>B</span><span>C</span><b>D</b><span>E</span>'
         '<span>F</span><span>G</span><span>H</span><span>I</span><span>J</span><b>K</b><span>L</span>'
         '<span>M</span><span>N</span><b>O</b><span>P</span><span>S</span><span>T</span></div>')

FILT = ('<div class="filt"><nav class="filt-tabs"><a href="#" class="on">Movies</a>'
        '<a href="#">Collections</a><a href="#">Genres</a><a href="#">Favourites</a></nav>'
        '<div class="sp"><span class="chip on">Unwatched</span><span class="chip">HDR</span>'
        '<span class="chip">Date added &darr;</span></div></div>')

FILT_PLAIN = ('<div class="filt-plain"><span>4,182 items</span><span class="sel">Sort: Date added</span>'
              '<span class="sel">Filter: All</span><span class="sel">View: Grid</span>'
              '<span style="margin-left:auto">Page 1 of 42</span></div>')

FILT_FLOAT = ('<div class="filt-float"><span class="chip on">Unwatched</span>'
              '<span class="chip">HDR</span><span class="chip">A&ndash;Z</span></div>')

MORE_LIKE = K.rail("More Like This", K.lib_items(6)[1:6], "", wide=False)

D_BODY_CAST = ('<h4 class="sect-h">Cast &amp; Crew</h4>%s' % K.cast_html())


# ============================================================ direction specs
D = {}

D["glass"] = dict(
    title="Cinematic Glass", fav="\U0001FA9F",
    thesis=("The artwork supplies all the colour and the interface supplies <strong>none</strong>. "
            "There is no top bar at all &mdash; navigation floats as a frosted pill, card metadata sits "
            "over the poster instead of under it, and the billboard runs edge to edge."),
    ref="tvOS and the Apple TV app. Built for a big panel in a dark room, remote in hand.",
    best="Libraries with strong artwork. Anyone who browses on the TV more than the phone.",
    watch=("Blur costs compositing power on weak clients, and metadata over artwork is always a contrast "
           "gamble. An achromatic accent means state has to be shown by position, not colour."),
    fonts="Manrope:wght@400;500;600;700;800",
    radius="14px",
    tokens="""
  --m-bg:#080a0d; --m-bg-elev:#0f1319; --m-bg-elev2:#161b23; --m-bar:rgba(12,16,22,.55);
  --m-surface:rgba(148,163,184,.12); --m-border:rgba(255,255,255,.08); --m-border-strong:rgba(255,255,255,.17);
  --m-text:#f1f5f9; --m-muted:#9aa7b7; --m-faint:#6d7987;
  --m-accent:#e8eef6; --m-accent-ink:#0b0f14; --m-accent-soft:rgba(232,238,246,.12); --m-accent-hover:#fff;
  --m-star:#f2b01e; --m-ok:#5ec2a0; --m-warn:#e0a94a; --m-err:#e4685f;
  --m-input-bg:rgba(148,163,184,.10); --m-toast-bg:rgba(22,27,35,.86);
  --m-radius:14px; --m-radius-sm:6px; --m-radius-lg:18px; --m-radius-pill:99px;
  --m-lift:0 12px 34px -12px rgba(0,0,0,.9); --m-lift-lg:0 28px 70px -22px rgba(0,0,0,.95);
  --m-frame-lift:0 26px 64px -30px rgba(0,0,0,.9);
  --m-font:"Manrope",system-ui,sans-serif; --m-font-display:"Manrope",system-ui,sans-serif;
  --m-display-weight:800; --m-display-size:40px; --m-display-track:-.03em;
  --m-gap:16px; --cw:120px; --cww:206px;
  --m-bar-blur:blur(22px) saturate(140%); --m-surface-blur:blur(18px); --m-drawer-mark:0px;
  --m-login-veil:rgba(8,10,13,.72); --m-login-card:rgba(22,27,35,.55);
""",
    css=""".drawer,.side{background:rgba(148,163,184,.05);backdrop-filter:blur(18px)}
.filt{background:rgba(148,163,184,.05);backdrop-filter:blur(14px)}
.system > section,.inv > div{background:rgba(148,163,184,.055)}""",
    ramp=[("#080a0d", "--m-bg", "page ground"), ("#0f1319", "--m-bg-elev", "panels"),
          ("#8f9bab", "--m-surface", "12% slate glass"), ("#e8eef6", "--m-accent", "accent"),
          ("#9aa7b7", "--m-muted", "secondary text"), ("#f2b01e", "--m-star", "rating")],
    facts=[("Nav", "Floating pill, no bar"), ("Home", "Full-bleed billboard"),
           ("Cards", "Metadata over artwork"), ("Radius", "14px, pill chips"),
           ("Depth", "22px blur, 34px shadows")],
    jf=[("primary-main", "#e8eef6"), ("primary-mainChannel", "232 238 246"), ("primary-dark", "#c7d2de"),
        ("background-default", "#080a0d"), ("background-paper", "rgba(148,163,184,.12)"),
        ("divider", "rgba(255,255,255,.08)"), ("text-primary", "#f1f5f9"), ("starIcon-main", "#f2b01e")],
    outro=("A colourless chrome layer over blurred surfaces, with the accent left achromatic so artwork is "
           "the only colour on screen. The blur budget gets checked on the weakest client you care about first."),
)
D["glass"]["screens"] = dict(
    signin=vp("vp-m", signin("card")),
    home=vp("vp-xl", nav_pill("Home") + K.billboard(
        "", "Blade Runner 2049",
        "A young blade runner uncovers a secret buried for thirty years.",
        K.ACTS_MAIN, True, 340, 46, 1)
        + K.rail("Continue Watching", K.cont_items(), meta="m-over")
        + K.rail("Next Up", K.next_items(), meta="m-over", wide=True)),
    library=vp("vp-l", nav_pill("Films") + FILT_FLOAT + '<div style="height:58px"></div>'
               + K.grid(K.lib_items(18), 7, meta="m-over") + ALPHA),
    detail=vp("vp-xl", nav_pill("Films") + K.billboard(
        "", "Past Lives", "Two childhood friends are reunited after twenty years apart.",
        K.D_ACTS, False, 360, 52, 5)
        + '<div class="body-pad">%s</div>' % D_BODY_CAST
        + K.rail("More like this", K.lib_items(6)[1:6], "")),
    episodes=vp("vp-l", nav_pill("Series") + K.billboard(
        "", "The Bear", "Season 3 &middot; 10 episodes",
        '<button class="btn btn-1">&#9654; Resume S3:E5</button><button class="btn btn-i">&#10003;</button>',
        False, 240, 36, 3)
        + K.rail("Season 3", [(e[1], e[0] + " &middot; " + e[3].split("&middot;")[-1].strip(), e[4], "")
                              for e in K.EPS] + [("Forks", "E7 &middot; 38m", 10, "")],
                 "", meta="m-over", wide=True)),
    player=vp("vp-m", player("float")),
    dashboard=vp("vp-l", dash(side("nav", "Home"), DASH_BODY)),
    components=vp("vp-a", K.INVENTORY),
)

D["editorial"] = dict(
    title="Editorial Ink", fav="\U0001F4F0",
    thesis=("A film journal, not a storefront. There is <strong>no hero and no backdrop</strong> &mdash; "
            "the home page is a magazine spread with one feature and a numbered index below it. Posters "
            "shrink to thumbnails; the writing does the work."),
    ref="MUBI, the Criterion Channel, a repertory cinema programme. Quiet, literate, unhurried.",
    best="Curated libraries. People who read the synopsis before they press play.",
    watch=("Fewer items fit above the fold than any other direction here &mdash; this is a browsing "
           "experience, not a resume-in-one-click experience. Didone hairlines need 16px or more."),
    fonts=("Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,600;0,6..96,700;1,6..96,400"
           "&family=Libre+Franklin:wght@400;500;600;700"),
    radius="2px",
    tokens="""
  --m-bg:#131313; --m-bg-elev:#1b1b1b; --m-bg-elev2:#232323; --m-bar:#131313;
  --m-surface:#1f1f1f; --m-border:#262523; --m-border-strong:#3a3835;
  --m-text:#e8e4dd; --m-muted:#8e8a83; --m-faint:#6a6660;
  --m-accent:#b3a369; --m-accent-ink:#16150f; --m-accent-soft:rgba(179,163,105,.12); --m-accent-hover:#c7b67c;
  --m-star:#b3a369; --m-ok:#8a9a72; --m-warn:#c49a52; --m-err:#b5645c;
  --m-input-bg:#1b1b1b; --m-toast-bg:#232323;
  --m-radius:2px; --m-radius-sm:1px; --m-radius-lg:3px; --m-radius-pill:2px;
  --m-lift:none; --m-lift-lg:none; --m-frame-lift:none;
  --m-font:"Libre Franklin",Helvetica,Arial,sans-serif;
  --m-font-display:"Bodoni Moda",Georgia,"Times New Roman",serif;
  --m-display-weight:600; --m-display-size:46px; --m-display-track:-.005em;
  --m-row-font:"Libre Franklin",Helvetica,Arial,sans-serif;
  --m-row-size:11.5px; --m-row-weight:600; --m-row-case:uppercase; --m-row-track:.2em;
  --m-label-track:.2em; --m-label-font:"Libre Franklin",Helvetica,Arial,sans-serif;
  --m-gap:20px; --cw:104px; --cww:184px; --m-tagline-style:italic;
  --m-tbl-font:"Libre Franklin",Helvetica,Arial,sans-serif; --m-tbl-size:12.5px;
  --m-login-veil:rgba(19,19,19,.92);
""",
    css=""".vp::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.05;pointer-events:none;z-index:9}
.rail-h,.panel-h{border-bottom:1px solid var(--m-border);padding-bottom:9px;align-items:flex-end}
.sect-h{border-bottom:1px solid var(--m-border);padding-bottom:9px}
.row-i{border-bottom:1px solid var(--m-border);border-radius:0}
.row-i.on{background:transparent;box-shadow:inset 2px 0 0 var(--m-accent);padding-left:14px}
.chip{border-radius:0}
.c-t{font-weight:500}""",
    ramp=[("#131313", "--m-bg", "page ground"), ("#1b1b1b", "--m-bg-elev", "panels"),
          ("#b3a369", "--m-accent", "antique gold"), ("#e8e4dd", "--m-text", "warm ink"),
          ("#8e8a83", "--m-muted", "secondary"), ("#3a3835", "--m-border-strong", "hairline rules")],
    facts=[("Nav", "Hairline rule, no icons"), ("Home", "Magazine feature + index"),
           ("Cards", "Thumbnails beside text"), ("Radius", "2px, effectively square"),
           ("Depth", "None. Rules and whitespace")],
    jf=[("primary-main", "#b3a369"), ("primary-mainChannel", "179 163 105"), ("primary-dark", "#8f8254"),
        ("background-default", "#131313"), ("background-paper", "#1b1b1b"), ("divider", "#262523"),
        ("text-primary", "#e8e4dd"), ("starIcon-main", "#b3a369")],
    outro=("Bodoni display over Libre Franklin UI, hairline rules instead of cards, and gold rationed to "
           "rules, active tab and star rating. The serif stays above 16px throughout."),
)
D["editorial"]["screens"] = dict(
    signin=vp("vp-m", signin("split")),
    home=vp("vp-xl", nav_rule("Films")
            + '<div class="feature">%s<div class="fbody"><p class="fkick">Now showing</p>'
              '<h3>Past Lives</h3><p>%s</p><div class="h-acts">%s</div></div></div>'
              % (K.art(5, "fart"), K.OVERVIEW[:180] + "&hellip;", K.D_ACTS)
            + '<div style="padding:0 30px"><h4 class="sect-h">The index &middot; recently added</h4></div>'
            + K.tlist([(t, y, n) for t, y, n in K.LIB[:4]])),
    library=vp("vp-l", nav_rule("Films") + FILT_PLAIN + K.tlist([(t, y, n) for t, y, n in K.LIB[:5]])),
    detail=vp("vp-xl", nav_rule("Films")
              + '<div class="d-split">%s<div><p class="kick">Feature &middot; 2023</p>'
                '<h3 class="d-title">Past Lives</h3><p class="d-tag">Two childhood friends are reunited '
                'after twenty years apart.</p>%s%s<div class="h-acts">%s</div>'
                '<p class="d-over">%s</p><div class="d-cols"><div>%s</div><div>%s</div></div></div></div>'
                % (K.art(5, "pst"), K.D_META, K.D_GENRES, K.D_ACTS, K.OVERVIEW, D_BODY_CAST, K.STREAMS)),
    episodes=vp("vp-l", nav_rule("Series")
                + '<div style="padding:22px 30px 0"><p class="kick">Season 3</p>'
                  '<h3 class="d-title" style="font-size:38px;margin-bottom:6px">The Bear</h3>'
                  '<ul class="meta"><li>2024</li><li class="star">&#9733; 8.6</li><li>10 episodes</li></ul></div>'
                + K.tlist([(e[1], e[0], e[4]) for e in K.EPS])),
    player=vp("vp-m", player("classic")),
    dashboard=vp("vp-l", '<div class="pane">%s%s</div>' % (nav_rule("Index"), DASH_TABLE)),
    components=vp("vp-a", K.INVENTORY),
)

D["terminal"] = dict(
    title="Amber Terminal", fav="\U0001F5A5",
    thesis=("A media server that admits it is a server. The library is a <strong>sortable table</strong>, "
            "not a wall of posters &mdash; title, year, runtime, codec, size, bitrate, state. A tree "
            "sidebar replaces the top bar, and amber phosphor replaces every accent."),
    ref="Amber CRT terminals, tiling window managers, htop. Dense, technical, unapologetic.",
    best="Self-hosters who also run the server. Wide monitors, keyboard navigation, big libraries.",
    watch=("Artwork is almost absent until you open something, which is exactly wrong for anyone who "
           "browses by poster. Monospace eats about 15% more width per string."),
    fonts="JetBrains+Mono:wght@400;500;700;800",
    radius="0px",
    tokens="""
  --m-bg:#080808; --m-bg-elev:#0e0e0e; --m-bg-elev2:#141414; --m-bar:#0b0b0b;
  --m-surface:#111; --m-border:#242424; --m-border-strong:#3a3a3a;
  --m-text:#d4d4d4; --m-muted:#6e6e6e; --m-faint:#525252;
  --m-accent:#ffb000; --m-accent-ink:#0a0800; --m-accent-soft:rgba(255,176,0,.11); --m-accent-hover:#ffc333;
  --m-star:#ffb000; --m-ok:#7fbf5f; --m-warn:#ffb000; --m-err:#e05252;
  --m-input-bg:#0e0e0e; --m-toast-bg:#141414;
  --m-radius:0px; --m-radius-sm:0px; --m-radius-lg:0px; --m-radius-pill:0px;
  --m-radius-avatar:0px; --m-radius-play:0px;
  --m-lift:none; --m-lift-lg:none; --m-frame-lift:none;
  --m-font:"JetBrains Mono",ui-monospace,monospace;
  --m-font-display:"JetBrains Mono",ui-monospace,monospace;
  --m-font-mono:"JetBrains Mono",ui-monospace,monospace;
  --m-display-weight:700; --m-display-size:30px; --m-display-track:-.04em;
  --m-row-size:12px; --m-row-case:uppercase; --m-row-track:.1em; --m-row-weight:700;
  --m-label-track:.1em; --m-track:.02em;
  --m-gap:10px; --cw:104px; --cww:180px; --m-card-border:1px solid #242424;
  --m-tbl-font:"JetBrains Mono",ui-monospace,monospace; --m-tbl-size:11.5px; --m-tbl-name-weight:500;
  --m-ep-border:1px solid #242424; --m-ep-gap:8px; --m-ep-pad:12px; --m-drawer-mark:0px;
  --m-login-veil:rgba(8,8,8,.94);
""",
    css=""".vp::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:9;
  background:repeating-linear-gradient(0deg,rgba(255,255,255,.022) 0 1px,transparent 1px 3px)}
.rail-h h4::before,.sect-h::before{content:"$ ";color:var(--m-accent)}
.tbl td,.tbl th{letter-spacing:-.02em}
.scrub,.scrub .buf,.scrub .pl,.scrub .kn,.prog,.prog i,.sw,.sw::after{border-radius:0}
.sw{width:34px}.sw::after{left:17px;width:14px}.sw.off::after{left:3px}""",
    ramp=[("#080808", "--m-bg", "true black"), ("#0e0e0e", "--m-bg-elev", "panels"),
          ("#ffb000", "--m-accent", "amber phosphor"), ("#d4d4d4", "--m-text", "primary text"),
          ("#6e6e6e", "--m-muted", "secondary"), ("#242424", "--m-border", "1px rules")],
    facts=[("Nav", "Left library tree"), ("Home", "Status header + table"),
           ("Cards", "None. Text rows"), ("Radius", "0 everywhere"),
           ("Depth", "None. 1px borders only")],
    jf=[("primary-main", "#ffb000"), ("primary-mainChannel", "255 176 0"), ("primary-dark", "#cc8d00"),
        ("background-default", "#080808"), ("background-paper", "#0e0e0e"), ("divider", "#242424"),
        ("text-primary", "#d4d4d4"), ("starIcon-main", "#ffb000")],
    outro=("One mono family, zero radius, hard rules, amber used structurally. Truncation gets tested "
           "against your longest actual title before any column width is fixed."),
)
TCOLS = ["title", "year", "runtime", "codec", "size", "mbps", "state"]
D["terminal"]["screens"] = dict(
    signin=vp("vp-s", signin("prompt")),
    home=vp("vp-l", '<div class="stack">%s<div class="pane">'
            '<div class="status"><b>jellyfin</b><span>@</span><u>tower</u> <span>&mdash; 10.11.8, up 18d</span><br>'
            '<span>library:</span> <u>4,182 items</u> <span>/ 6 collections /</span> <u>38.4 TB</u><br>'
            '<span>sessions:</span> <u>3 active</u> <span>/ 1 transcoding</span></div>'
            '<div style="padding:12px 0 0"><h4 class="sect-h" style="padding:0 16px">continue</h4>%s</div>'
            '</div></div>' % (side("tree", "Films"), K.table(TCOLS, K.TROWS[:6]))),
    library=vp("vp-l", '<div class="stack">%s<div class="pane">%s%s</div></div>'
               % (side("tree", "Films"), FILT_PLAIN, K.table(TCOLS, K.TROWS, thumbs=True))),
    detail=vp("vp-l", '<div class="stack">%s<div class="pane">'
              '<div class="d-flat">%s<div><h3 class="d-title">Past Lives</h3>'
              '<p class="d-tag">2023 / drama / 1:46 / hevc</p>%s'
              '<div class="h-acts" style="margin:14px 0">%s</div>'
              '<p class="d-over" style="font-size:12px">%s</p>%s</div></div></div></div>'
              % (side("tree", "Films"), K.art(5, "pst"), K.D_META, K.D_ACTS,
                 K.OVERVIEW[:210] + "&hellip;", K.STREAMS)),
    episodes=vp("vp-l", '<div class="stack">%s<div class="pane">'
                '<div class="status"><b>the.bear</b> <span>/ season.03 /</span> <u>10 episodes</u></div>%s'
                '</div></div>'
                % (side("tree", "Series"),
                   K.table(["ep", "title", "aired", "runtime", "size", "mbps", "state"],
                           [("E4 Violet", "2024", "27 Jun", "36m", "4.1G", "18.2", "ok", "watched"),
                            ("E5 Children", "2024", "27 Jun", "41m", "4.8G", "19.0", "ok", "47m left"),
                            ("E6 Napkins", "2024", "27 Jun", "34m", "3.9G", "17.4", "ok", "unwatched"),
                            ("E7 Forks", "2024", "27 Jun", "38m", "4.4G", "18.1", "wr", "unwatched")]))),
    player=vp("vp-m", player("line")),
    dashboard=vp("vp-l", '<div class="stack">%s<div class="pane">%s</div></div>'
                 % (side("tree", "Films"), DASH_TABLE)),
    components=vp("vp-a", K.INVENTORY),
)

D["warm"] = dict(
    title="Warm Ambient", fav="\U0001F56F",
    thesis=("The inverse of stock Jellyfin&rsquo;s clinical blue-black. A <strong>persistent sidebar</strong> "
            "replaces the top bar, the home page opens with a greeting rather than a billboard, and "
            "&ldquo;jump back in&rdquo; is three big landscape tiles instead of a rail of posters."),
    ref="Reading apps in night mode; a lamp-lit living room. Comfortable at eleven at night.",
    best="Households. Shared servers where nobody wants to be woken up by their own interface.",
    watch=("Lowered contrast is the point and also the risk &mdash; body text sits nearer 8:1 than 15:1. "
           "Big tiles mean fewer items above the fold than a poster rail."),
    fonts="Nunito+Sans:wght@400;500;600;700;800",
    radius="18px",
    tokens="""
  --m-bg:#1d1917; --m-bg-elev:#272220; --m-bg-elev2:#322b28; --m-bar:#221d1b;
  --m-surface:#2c2624; --m-border:#332b28; --m-border-strong:#453b37;
  --m-text:#f2eae4; --m-muted:#ab9c93; --m-faint:#87786f;
  --m-accent:#d98e73; --m-accent-ink:#241512; --m-accent-soft:rgba(217,142,115,.14); --m-accent-hover:#e6a288;
  --m-star:#e3b778; --m-ok:#8fb096; --m-warn:#d9ab6a; --m-err:#cf7d72;
  --m-input-bg:#231e1c; --m-toast-bg:#322b28;
  --m-radius:18px; --m-radius-sm:9px; --m-radius-lg:22px; --m-radius-pill:99px;
  --m-lift:0 10px 26px -14px rgba(0,0,0,.7); --m-lift-lg:0 24px 56px -24px rgba(0,0,0,.8);
  --m-frame-lift:0 18px 44px -26px rgba(0,0,0,.7);
  --m-font:"Nunito Sans",system-ui,sans-serif; --m-font-display:"Nunito Sans",system-ui,sans-serif;
  --m-display-weight:800; --m-display-size:36px; --m-display-track:-.022em;
  --m-gap:18px; --cw:124px; --cww:210px;
  --m-ep-gap:12px; --m-ep-pad:14px; --m-ep-bg:#231e1c;
  --m-login-veil:rgba(29,25,23,.84);
""",
    css=""".vp::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.06;pointer-events:none;z-index:9}
.nav-top,.dash-bar{border-bottom:0;box-shadow:0 1px 0 var(--m-border)}
.streams,.tl-s,.panel{border-radius:var(--m-radius-sm)}
.row-i{border:1px solid transparent}""",
    ramp=[("#1d1917", "--m-bg", "warm brown-black"), ("#272220", "--m-bg-elev", "panels"),
          ("#d98e73", "--m-accent", "clay"), ("#f2eae4", "--m-text", "warm off-white"),
          ("#ab9c93", "--m-muted", "secondary"), ("#e3b778", "--m-star", "rating")],
    facts=[("Nav", "Persistent left sidebar"), ("Home", "Greeting + 16:9 tiles"),
           ("Cards", "Few, large, text below"), ("Radius", "18px cards, 22px panels"),
           ("Depth", "Soft low-opacity lift")],
    jf=[("primary-main", "#d98e73"), ("primary-mainChannel", "217 142 115"), ("primary-dark", "#b06c54"),
        ("background-default", "#1d1917"), ("background-paper", "#272220"), ("divider", "#332b28"),
        ("text-primary", "#f2eae4"), ("starIcon-main", "#e3b778")],
    outro=("Warm grounds, clay accent, generous rounding and a contrast floor checked on a dim panel so "
           "the low-contrast intent never crosses into unreadable."),
)
D["warm"]["screens"] = dict(
    signin=vp("vp-m", signin("card")),
    home=vp("vp-xl", '<div class="stack">%s<div class="pane">'
            '<div class="greet"><h3>Evening, Rid</h3><p>Three things waiting for you</p></div>%s%s</div></div>'
            % (side("fat", "Home"),
               K.tiles([(K.CONT[0][0], K.CONT[0][1], K.CONT[0][2], K.bar(62)),
                        (K.CONT[1][0], K.CONT[1][1], K.CONT[1][2], K.bar(18)),
                        (K.CONT[2][0], K.CONT[2][1], K.CONT[2][2], K.bar(81))], 3),
               K.rail("Recently added", K.lib_items(6)))),
    library=vp("vp-l", '<div class="stack">%s<div class="pane">%s%s</div></div>'
               % (side("fat", "Movies"), FILT, K.grid(K.lib_items(10), 5))),
    detail=vp("vp-xl", '<div class="stack">%s<div class="pane" style="position:relative">'
              '%s<div class="wash-veil"></div>'
              '<div class="d-sheet">%s<div><p class="kick">Film</p><h3 class="d-title">Past Lives</h3>'
              '<p class="d-tag">Two childhood friends are reunited after twenty years apart.</p>%s%s'
              '<div class="h-acts">%s</div><p class="d-over">%s</p></div></div>'
              '<div class="body-pad">%s</div></div></div>'
              % (side("fat", "Movies"), K.art(5, "wash"), K.art(5, "pst"), K.D_META, K.D_GENRES,
                 K.D_ACTS, K.OVERVIEW[:200] + "&hellip;", D_BODY_CAST)),
    episodes=vp("vp-l", '<div class="stack">%s<div class="pane">'
                '<div class="greet"><h3>The Bear</h3><p>Season 3 &middot; 10 episodes</p></div>%s</div></div>'
                % (side("fat", "Shows"), K.ep_rows(160))),
    player=vp("vp-m", player("float")),
    dashboard=vp("vp-l", dash(side("fat", "Home"), DASH_BODY)),
    components=vp("vp-a", K.INVENTORY),
)

D["prime"] = dict(
    title="Prime Time", fav="\U0001F37F",
    thesis=("The shape everyone already knows. A <strong>giant billboard</strong> with the title set as "
            "logo art, chrome that fades over the picture instead of sitting above it, dense poster rails, "
            "a numbered Top 10, and a hover card that expands into buttons and a match score."),
    ref="Netflix, Disney+, Prime Video. The most-copied genre in the Jellyfin theme scene.",
    best="Mixed households. Anyone who has never opened a Jellyfin settings page and never wants to.",
    watch=("It is derivative on purpose, which some users read as a downgrade rather than a theme. "
           "Big billboards mean one item gets most of the screen whether or not you care about it."),
    fonts="Archivo:wght@400;500;600;700;800;900",
    radius="4px",
    tokens="""
  --m-bg:#0b0b0b; --m-bg-elev:#161616; --m-bg-elev2:#1f1f1f; --m-bar:rgba(11,11,11,.9);
  --m-surface:rgba(255,255,255,.12); --m-border:#242424; --m-border-strong:#3d3d3d;
  --m-text:#f5f5f5; --m-muted:#a3a3a3; --m-faint:#737373;
  --m-accent:#e0322b; --m-accent-ink:#ffffff; --m-accent-soft:rgba(224,50,43,.16); --m-accent-hover:#f04740;
  --m-star:#f5c518; --m-ok:#46d369; --m-warn:#e8b339; --m-err:#e0322b;
  --m-input-bg:#1f1f1f; --m-toast-bg:#1f1f1f;
  --m-radius:4px; --m-radius-sm:3px; --m-radius-lg:6px; --m-radius-pill:3px;
  --m-lift:0 8px 24px -10px rgba(0,0,0,.9); --m-lift-lg:0 26px 60px -20px rgba(0,0,0,.95);
  --m-frame-lift:0 20px 50px -28px rgba(0,0,0,.9);
  --m-font:"Archivo",system-ui,sans-serif; --m-font-display:"Archivo",system-ui,sans-serif;
  --m-display-weight:900; --m-display-size:42px; --m-display-track:-.035em;
  --m-gap:8px; --cw:126px; --cww:240px;
  --m-login-veil:rgba(11,11,11,.6);
""",
    css=""".rail-h h4{font-size:14px;letter-spacing:-.01em}
.c .art{transition:transform .2s ease}
.bb-logo{text-transform:uppercase;font-stretch:condensed}
.nav-top.nav-fade .brand i{background:var(--m-accent)}
.side a.on{color:#fff;background:transparent;box-shadow:none;border-left:3px solid var(--m-accent)}""",
    ramp=[("#0b0b0b", "--m-bg", "near black"), ("#161616", "--m-bg-elev", "panels"),
          ("#e0322b", "--m-accent", "signal red"), ("#f5f5f5", "--m-text", "primary text"),
          ("#a3a3a3", "--m-muted", "secondary"), ("#46d369", "--m-ok", "match score")],
    facts=[("Nav", "Fades over the picture"), ("Home", "Billboard + rails + Top 10"),
           ("Cards", "Hover expands to preview"), ("Radius", "4px, nearly square"),
           ("Density", "Tight 8px rails")],
    jf=[("primary-main", "#e0322b"), ("primary-mainChannel", "224 50 43"), ("primary-dark", "#b02620"),
        ("background-default", "#0b0b0b"), ("background-paper", "#161616"), ("divider", "#242424"),
        ("text-primary", "#f5f5f5"), ("starIcon-main", "#f5c518")],
    outro=("The familiar shape, built properly: logo-art billboard, hover previews with a match score, and "
           "a numbered Top 10 rail. Ships with the profile picker as the sign-in screen."),
)
POP = ('<div class="c pop"><div class="art" data-art="3"></div><div class="pop-info">'
       '<div class="pop-btns"><i class="p">&#9654;</i><i>+</i><i>&#9825;</i></div>'
       '<div class="l"><b>97% match</b><span>2024</span><span class="badge">TV-MA</span><span>4K</span></div>'
       '</div></div>')
D["prime"]["screens"] = dict(
    signin=vp("vp-m", signin("picker")),
    home=vp("vp-xl", nav_top("Home", "nav-fade") + K.billboard(
        '&#9654; #1 in Films today', "Blade Runner 2049", K.BR_DESC,
        '<button class="btn btn-1 btn-lg">&#9654; Play</button>'
        '<button class="btn btn-2 btn-lg">More Info</button>', True, 356, 50, 1)
        + K.rail("Continue Watching", K.cont_items())
        + '<div class="rail top10"><div class="rail-h"><h4>Top 10 in your library</h4><span></span></div>'
          '<div class="cards">%s</div></div>'
          % "".join('<span class="rank"><em>%d</em>%s</span>'
                    % (i + 1, K.card(t, y, n, "", "")) for i, (t, y, n) in enumerate(K.LIB[:5]))),
    library=vp("vp-l", nav_top("Movies") + FILT + K.grid(K.lib_items(18), 6) + ALPHA),
    detail=vp("vp-xl", nav_top("Movies", "nav-fade")
              + '<div class="d-take">%s<div class="bb-scrim"></div><div class="bb-body">'
                '<h3 class="bb-logo" style="--bb-size:46px">Past Lives</h3>%s'
                '<p class="bb-tag">%s</p><div class="bb-acts">%s</div></div></div>'
                % (K.art(5, "bb-art"), K.D_META, K.OVERVIEW[:150] + "&hellip;", K.D_ACTS)
              + MORE_LIKE),
    episodes=vp("vp-l", nav_top("Shows") + K.backdrop(
        "Season 3", "The Bear",
        '<ul class="meta"><li>2024</li><li class="star">&#9733; 8.6</li><li>10 episodes</li></ul>',
        "", '<button class="btn btn-1">&#9654; Resume S3:E5</button>', 3, 180)
        + K.ep_rows(150)),
    player=vp("vp-m", player("classic", '<button class="btn btn-2 skip">Skip Intro</button>')),
    dashboard=vp("vp-l", dash(side("nav", "Home"), DASH_BODY)),
    components=vp("vp-a", K.INVENTORY),
)

D["plain"] = dict(
    title="Plain &amp; Fast", fav="⚡",
    thesis=("The anti-theme. <strong>No hero, no backdrop, no blur, no animation</strong> &mdash; the grid "
            "starts eighteen pixels below the navigation and twelve posters fit across. Everything is "
            "visible at once and nothing moves. It is stock Jellyfin with the waste taken out."),
    ref="Abyss, Zesty, finimalism, NeutralFin &mdash; the biggest genre in the ecosystem by stars.",
    best="Big libraries, slow clients, and anyone who will resent a redesign on principle.",
    watch=("It is deliberately unremarkable, so it will never win a beauty contest. Twelve across means "
           "small posters, which is a real loss on a TV across the room."),
    fonts="IBM+Plex+Sans:wght@400;500;600;700",
    radius="3px",
    tokens="""
  --m-bg:#16181a; --m-bg-elev:#1e2124; --m-bg-elev2:#262a2e; --m-bar:#1e2124;
  --m-surface:#262a2e; --m-border:#2c3135; --m-border-strong:#3d444a;
  --m-text:#e6e9ec; --m-muted:#9aa2aa; --m-faint:#767e86;
  --m-accent:#00a4dc; --m-accent-ink:#04222c; --m-accent-soft:rgba(0,164,220,.14); --m-accent-hover:#33b6e3;
  --m-star:#f2b01e; --m-ok:#5cb85c; --m-warn:#d9a13a; --m-err:#d9534f;
  --m-input-bg:#16181a; --m-toast-bg:#262a2e;
  --m-radius:3px; --m-radius-sm:2px; --m-radius-lg:4px; --m-radius-pill:2px;
  --m-lift:none; --m-lift-lg:none; --m-frame-lift:none;
  --m-font:"IBM Plex Sans",system-ui,sans-serif; --m-font-display:"IBM Plex Sans",system-ui,sans-serif;
  --m-display-weight:600; --m-display-size:26px; --m-display-track:-.015em;
  --m-row-size:13px; --m-row-weight:600;
  --m-gap:8px; --cw:84px; --cww:150px;
  --m-tbl-size:11.5px; --m-ep-gap:1px; --m-ep-pad:8px;
  --m-login-veil:rgba(22,24,26,.97);
""",
    css=""".c-t{font-size:11px;margin-top:5px}.c-s{font-size:10px}
.rail{padding-bottom:14px}.grid{padding:12px 16px}
.row-i{border-bottom:1px solid var(--m-border);border-radius:0}
.row-th{--rth:104px}
.btn{padding:7px 13px;font-size:12px}""",
    ramp=[("#16181a", "--m-bg", "neutral ground"), ("#1e2124", "--m-bg-elev", "panels"),
          ("#00a4dc", "--m-accent", "Jellyfin blue, kept"), ("#e6e9ec", "--m-text", "primary text"),
          ("#9aa2aa", "--m-muted", "secondary"), ("#2c3135", "--m-border", "dividers")],
    facts=[("Nav", "Compact text links, 40px"), ("Home", "No hero. Grid immediately"),
           ("Cards", "84px, 12 across"), ("Radius", "3px"),
           ("Motion", "None at all")],
    jf=[("primary-main", "#00a4dc"), ("primary-mainChannel", "0 164 220"), ("primary-dark", "#00729a"),
        ("background-default", "#16181a"), ("background-paper", "#1e2124"), ("divider", "#2c3135"),
        ("text-primary", "#e6e9ec"), ("starIcon-main", "#f2b01e")],
    outro=("Keeps Jellyfin blue on purpose so nothing feels foreign, then takes out the padding, the "
           "backdrops and the animation. The fastest of the eight on a weak client, by a wide margin."),
)
D["plain"]["screens"] = dict(
    signin=vp("vp-s", signin("bare")),
    home=vp("vp-l", nav_plain("Home")
            + '<div style="padding:14px 16px 0"><h4 class="sect-h">Continue watching</h4></div>'
            + K.grid(K.cont_items(), 12)
            + '<div style="padding:4px 16px 0"><h4 class="sect-h">Recently added</h4></div>'
            + K.grid(K.lib_items(12), 12)),
    library=vp("vp-l", nav_plain("Movies") + FILT_PLAIN + K.grid(K.lib_items(18) * 2, 12)),
    detail=vp("vp-m", nav_plain("Movies")
              + '<div class="d-flat">%s<div><h3 class="d-title">Past Lives</h3>%s%s'
                '<div class="h-acts" style="margin:12px 0">%s</div>'
                '<p class="d-over" style="font-size:12.5px;margin:8px 0 14px">%s</p>%s</div></div>'
                % (K.art(5, "pst"), K.D_META, K.D_GENRES, K.D_ACTS, K.OVERVIEW, K.STREAMS)),
    episodes=vp("vp-m", nav_plain("Shows")
                + '<div style="padding:12px 16px 0"><h4 class="sect-h">The Bear &middot; Season 3</h4></div>'
                + K.ep_rows(104)),
    player=vp("vp-m", player("classic")),
    dashboard=vp("vp-l", '<div class="pane">%s%s</div>' % (nav_plain("Home"), DASH_TABLE)),
    components=vp("vp-a", K.INVENTORY),
)

D["immersion"] = dict(
    title="Immersion", fav="\U0001F30C",
    thesis=("The interface gets out of the way completely. The page background <strong>is</strong> the "
            "artwork you are looking at, blurred to a wash; posters tile edge to edge with no gaps, no "
            "boxes and no text until you land on one. Chrome is four floating icons."),
    ref="A cinema foyer, an album wall, the Apple TV screensaver. Made to be looked at.",
    best="Showing the library off. Big screens where artwork is the whole point.",
    watch=("Without labels you navigate by memory of cover art, which is fine for films you know and "
           "hopeless for ones you do not. The heaviest of the eight to render."),
    fonts="Outfit:wght@200;300;400;500;600;700",
    radius="0px",
    tokens="""
  --m-bg:#0a0a0c; --m-bg-elev:rgba(255,255,255,.06); --m-bg-elev2:rgba(255,255,255,.1);
  --m-bar:transparent; --m-surface:rgba(255,255,255,.11);
  --m-border:rgba(255,255,255,.09); --m-border-strong:rgba(255,255,255,.2);
  --m-text:#f6f2ee; --m-muted:rgba(246,242,238,.66); --m-faint:rgba(246,242,238,.42);
  --m-accent:#f4efe9; --m-accent-ink:#111013; --m-accent-soft:rgba(244,239,233,.14); --m-accent-hover:#fff;
  --m-star:#f2b01e; --m-ok:#6fd3a8; --m-warn:#e8bd6a; --m-err:#e88178;
  --m-input-bg:rgba(255,255,255,.08); --m-toast-bg:rgba(28,28,32,.86);
  --m-radius:0px; --m-radius-sm:0px; --m-radius-lg:0px; --m-radius-pill:99px;
  --m-lift:0 20px 50px -18px rgba(0,0,0,.85); --m-lift-lg:0 34px 80px -26px rgba(0,0,0,.9);
  --m-frame-lift:0 24px 60px -30px rgba(0,0,0,.85);
  --m-font:"Outfit",system-ui,sans-serif; --m-font-display:"Outfit",system-ui,sans-serif;
  --m-display-weight:300; --m-display-size:52px; --m-display-track:-.02em;
  --m-row-size:11px; --m-row-weight:500; --m-row-case:uppercase; --m-row-track:.24em;
  --m-gap:0px; --cw:112px; --cww:196px;
  --m-surface-blur:blur(20px); --m-bar-blur:blur(20px);
  --m-login-veil:rgba(10,10,12,.45);
""",
    css=""".mosaic .art::after{display:none}
.rail-h h4{opacity:.75}
.grid,.rail{padding-left:22px;padding-right:22px}
.panel,.tl-s,.streams{background:rgba(255,255,255,.05);backdrop-filter:blur(16px)}
.system > section,.inv > div{background:rgba(255,255,255,.045)}
.tbl td,.tbl th{border-color:rgba(255,255,255,.08)}""",
    ramp=[("#0a0a0c", "--m-bg", "ground beneath wash"), ("#8a8a92", "--m-bg-elev", "6% white glass"),
          ("#f4efe9", "--m-accent", "warm white"), ("#f6f2ee", "--m-text", "primary text"),
          ("#a8a49f", "--m-muted", "secondary"), ("#f2b01e", "--m-star", "rating")],
    facts=[("Nav", "Four floating icons"), ("Home", "Edge-to-edge poster wall"),
           ("Cards", "No boxes, no labels"), ("Radius", "0 - artwork meets artwork"),
           ("Ground", "Blurred crop of current item")],
    jf=[("primary-main", "#f4efe9"), ("primary-mainChannel", "244 239 233"), ("primary-dark", "#d6cfc6"),
        ("background-default", "#0a0a0c"), ("background-paper", "rgba(255,255,255,.06)"),
        ("divider", "rgba(255,255,255,.09)"), ("text-primary", "#f6f2ee"), ("starIcon-main", "#f2b01e")],
    outro=("Uses the backdrop element Jellyfin already renders, blurred and scaled to fill the page. The "
           "poster wall is the navigation; labels appear on focus only."),
)
D["immersion"]["screens"] = dict(
    signin=vp("vp-m", signin("wash")),
    home=vp("vp-xl", K.art(1, "wash") + '<div class="wash-veil"></div>' + nav_min()
            + '<div class="d-wash" style="padding:74px 40px 18px;flex:none">'
              '<p class="kick" style="opacity:.7">Continue watching</p><h3>Blade Runner 2049</h3>'
              '<ul class="meta" style="margin-bottom:16px"><li>2017</li><li class="star">&#9733; 8.0</li>'
              '<li>47m left</li></ul><div class="h-acts">%s</div></div>' % K.ACTS_MAIN
            + K.mosaic(K.lib_items(18) * 2, 9)),
    library=vp("vp-l", K.art(5, "wash") + '<div class="wash-veil"></div>' + nav_min()
               + '<div style="height:52px"></div>' + K.mosaic(K.lib_items(18) * 4, 12)),
    detail=vp("vp-xl", K.art(5, "wash") + '<div class="wash-veil"></div>' + nav_min()
              + '<div class="d-wash"><p class="kick" style="opacity:.75">Film &middot; 2023</p>'
                '<h3>Past Lives</h3>%s<p class="d-over" style="max-width:52ch">%s</p>'
                '<div class="h-acts">%s</div></div>'
                % (K.D_META, K.OVERVIEW[:180] + "&hellip;", K.D_ACTS)
              + K.mosaic(K.lib_items(18), 9)),
    episodes=vp("vp-l", K.art(3, "wash") + '<div class="wash-veil"></div>' + nav_min()
                + '<div class="d-wash" style="padding-top:76px;flex:none">'
                  '<p class="kick" style="opacity:.7">Season 3</p><h3 style="font-size:44px">The Bear</h3></div>'
                + K.rail("Episodes", [(e[1], e[0], e[4], "") for e in K.EPS]
                         + [("Forks", "E7", 10, "")], "", meta="m-over", wide=True)),
    player=vp("vp-m", player("float")),
    dashboard=vp("vp-l", K.art(9, "wash") + '<div class="wash-veil"></div>'
                 + '<div class="stack" style="position:relative;z-index:2">%s<div class="pane">'
                   '<div class="dash-bar">Dashboard</div>%s</div></div>' % (side("nav", "Home"), DASH_BODY)),
    components=vp("vp-a", K.INVENTORY),
)

D["daylight"] = dict(
    title="Daylight", fav="☀",
    thesis=("The only <strong>light</strong> theme here, and the only one built for legibility first. "
            "Atkinson Hyperlegible &mdash; a face designed for low vision &mdash; at 16px body, titles that "
            "wrap instead of truncating, 44px tap targets and a focus ring you can actually see."),
    ref=("awesome-jellyfin lists no light theme and no accessibility theme at all. This is the gap."),
    best="Daylight rooms, phones, tablets, and anyone on the server who has ever squinted at it.",
    watch=("Bright surfaces behind film artwork is a genuine tension &mdash; posters lose some drama. "
           "Bigger type and targets mean noticeably fewer items per screen."),
    fonts="Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400",
    radius="8px",
    tokens="""
  --m-bg:#f7f6f4; --m-bg-elev:#ffffff; --m-bg-elev2:#eeecea; --m-bar:#ffffff;
  --m-surface:#ffffff; --m-border:#dcd9d5; --m-border-strong:#b4afa9;
  --m-text:#14181d; --m-muted:#4a5560; --m-faint:#6b7681;
  --m-accent:#0f6d6f; --m-accent-ink:#ffffff; --m-accent-soft:#dcefef; --m-accent-hover:#0b5557;
  --m-star:#a86a00; --m-ok:#1c6b3a; --m-warn:#8a5a00; --m-err:#a51f1f;
  --m-input-bg:#ffffff; --m-toast-bg:#ffffff;
  --m-radius:8px; --m-radius-sm:5px; --m-radius-lg:10px; --m-radius-pill:99px;
  --m-lift:0 1px 2px rgba(20,24,29,.08),0 6px 16px -8px rgba(20,24,29,.16);
  --m-lift-lg:0 2px 4px rgba(20,24,29,.08),0 18px 40px -16px rgba(20,24,29,.24);
  --m-frame-lift:0 10px 30px -18px rgba(20,24,29,.3);
  --m-font:"Atkinson Hyperlegible",system-ui,sans-serif;
  --m-font-display:"Atkinson Hyperlegible",system-ui,sans-serif;
  --m-display-weight:700; --m-display-size:36px; --m-display-track:-.015em;
  --m-row-size:17px; --m-row-weight:700;
  --m-gap:20px; --cw:148px; --cww:250px;
  --m-login-veil:rgba(247,246,244,.9);
""",
    css=""".c-t{white-space:normal;font-size:15px;line-height:1.35;font-weight:700}
.c-s{white-space:normal;font-size:13px;color:var(--m-muted)}
.btn{padding:13px 20px;font-size:15px;min-height:44px}
.btn-i{padding:13px 15px}
.chip{padding:7px 14px;font-size:13px}
.badge{font-size:12px;padding:3px 8px;color:var(--m-text)}
.meta{font-size:14px;color:var(--m-muted)}
.nav-links{font-size:15px}
.nav-links a{padding-bottom:6px}
.bd-scrim{background:linear-gradient(96deg,var(--m-bg) 12%,color-mix(in srgb,var(--m-bg) 72%,transparent) 52%,color-mix(in srgb,var(--m-bg) 28%,transparent) 88%),linear-gradient(0deg,var(--m-bg) 2%,transparent 60%)}
.h-desc,.row-d{font-size:15px;color:var(--m-muted)}
.side a{padding:13px 16px;font-size:15px}
.row-n{font-size:17px}
.osd-veil{background:linear-gradient(0deg,rgba(0,0,0,.88) 0%,rgba(0,0,0,.2) 38%,transparent 62%)}
.ctl .play{width:56px;height:56px;font-size:20px}
.streams dl,.streams dd{font-size:14px}
.streams dt{font-size:12px}""",
    ramp=[("#f7f6f4", "--m-bg", "page ground"), ("#ffffff", "--m-bg-elev", "cards &amp; panels"),
          ("#0f6d6f", "--m-accent", "deep teal, 6.1:1 on white"), ("#14181d", "--m-text", "body, 15.8:1"),
          ("#4a5560", "--m-muted", "secondary, 7.4:1"), ("#b4afa9", "--m-border-strong", "visible borders")],
    facts=[("Nav", "High contrast, visible focus"), ("Home", "Backdrop + large cards"),
           ("Cards", "148px, titles wrap"), ("Body", "16px Atkinson Hyperlegible"),
           ("Targets", "44px minimum")],
    jf=[("primary-main", "#0f6d6f"), ("primary-mainChannel", "15 109 111"), ("primary-dark", "#0b5557"),
        ("background-default", "#f7f6f4"), ("background-paper", "#ffffff"), ("divider", "#dcd9d5"),
        ("text-primary", "#14181d"), ("starIcon-main", "#a86a00")],
    outro=("Light, high contrast, and typeset in a face designed for low vision. Every ratio in the palette "
           "above is measured, and no title truncates &mdash; it wraps."),
)
D["daylight"]["screens"] = dict(
    signin=vp("vp-m", signin("big")),
    home=vp("vp-xl", nav_top("Home") + K.backdrop(
        "Continue watching", "Blade Runner 2049", K.META_FULL, K.BR_DESC, K.ACTS_MAIN, 1, 292)
        + K.rail("Continue watching", K.cont_items()[:4])),
    library=vp("vp-l", nav_top("Movies") + FILT + K.grid(K.lib_items(10), 5)),
    detail=vp("vp-xl", nav_top("Movies")
              + '<div class="d-split" style="--dsplit:210px 1fr">%s<div>'
                '<p class="kick">Film &middot; 2023</p><h3 class="d-title">Past Lives</h3>'
                '<p class="d-tag">Two childhood friends are reunited after twenty years apart.</p>%s%s'
                '<div class="h-acts">%s</div><p class="d-over">%s</p>'
                '<div class="d-cols"><div>%s</div><div>%s</div></div></div></div>'
                % (K.art(5, "pst"), K.D_META, K.D_GENRES, K.D_ACTS, K.OVERVIEW, D_BODY_CAST, K.STREAMS)),
    episodes=vp("vp-l", nav_top("Shows") + K.backdrop(
        "Season 3", "The Bear",
        '<ul class="meta"><li>2024</li><li class="star">&#9733; 8.6</li><li>10 episodes</li></ul>',
        "", '<button class="btn btn-1">&#9654; Resume S3:E5</button>', 3, 190)
        + K.ep_rows(190)),
    player=vp("vp-m", player("classic")),
    dashboard=vp("vp-l", dash(side("nav", "Home"), DASH_BODY)),
    components=vp("vp-a", K.INVENTORY),
)
