# -*- coding: utf-8 -*-
"""Regenerate src/03-fonts.css from the woff2 files in assets/.

    python build/embed-font.py            # write src/03-fonts.css
    python build/embed-font.py --check    # verify it is up to date (CI), write nothing

Why this script exists rather than a hand-pasted blob: src/03-fonts.css is
~53 KB of base64 that nobody can review or edit. The reviewable artefacts are
the two .woff2 files in assets/, which are committed alongside; this turns
them into CSS deterministically, so the generated file can be regenerated and
diffed rather than trusted.

Why the font is embedded at all rather than referenced with url():
see PLAN.md section 3a. Briefly - a relative url() resolves against whichever
origin served the stylesheet, and that differs between the two shipping
profiles (jsDelivr for custom-css, the Jellyfin host for standalone), so no
single relative path can be correct for both.

Provenance: Manrope v20, the variable (wght 200-800) woff2 subsets Google
Fonts serves, fetched from fonts.gstatic.com. Licensed OFL-1.1; the licence
travels with them in assets/OFL.txt, which is what that licence requires when
the font is redistributed. The unicode-range values below are copied verbatim
from the css2 API response for
    https://fonts.googleapis.com/css2?family=Manrope:wght@200..800
and must stay in step with the files if they are ever re-subset.
"""
import base64
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.dirname(HERE)
ASSETS = os.path.join(THEME, "assets")
OUT = os.path.join(THEME, "src", "03-fonts.css")

# (subset name, file in assets/, unicode-range)
SUBSETS = [
    ("latin", "manrope-latin.woff2",
     "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, "
     "U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, "
     "U+2212, U+2215, U+FEFF, U+FFFD"),
    ("latin-ext", "manrope-latin-ext.woff2",
     "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, "
     "U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, "
     "U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF"),
]

HEADER = """/* ==========================================================================
   Cinematic Glass - Manrope, self-hosted and embedded. GENERATED FILE.
   --------------------------------------------------------------------------
   Owns: @font-face for the one typeface the theme uses

   DO NOT EDIT. Regenerate with:

       python build/embed-font.py

   The reviewable sources are assets/manrope-*.woff2 and assets/OFL.txt.

   Manrope v20, variable (wght 200-800), the subsets Google Fonts serves,
   licensed OFL-1.1 and redistributed here with the licence, which is what
   OFL-1.1 asks for. 00-tokens.css asks for weights 400/500/700/800; one
   variable face covers all four from a single `font-weight: 200 800`
   declaration and is smaller than four static cuts would be.

   Embedded as data: URIs rather than referenced with url(). A relative url()
   resolves against whichever origin served the stylesheet, and that differs
   between the two shipping profiles - jsDelivr for custom-css, the Jellyfin
   host for standalone - so no single relative path is correct for both.
   Embedding also removes the standalone failure mode where theme.css is
   installed and the font file is not. See PLAN.md section 3a.

   unicode-range is kept per subset so the browser only activates the face it
   needs. Anything outside these ranges falls back through the rest of the
   stack in --cg-font, which is why that stack has real fonts in it.

   font-display: swap is belt and braces. There is no network fetch here, so
   there is nothing to swap from; it matters only if a client refuses the
   data: URI.
   ========================================================================== */
"""

FACE = """
/* %s - %s, %s KB raw */
@font-face {
    font-family: "Manrope";
    font-style: normal;
    font-weight: 200 800;
    font-display: swap;
    src: url(data:font/woff2;base64,%s) format("woff2");
    unicode-range: %s;
}
"""


def render():
    parts = [HEADER]
    for name, filename, urange in SUBSETS:
        path = os.path.join(ASSETS, filename)
        raw = io.open(path, "rb").read()
        if raw[:4] != b"wOF2":
            raise SystemExit("%s is not a woff2 file (bad magic)" % filename)
        b64 = base64.b64encode(raw).decode("ascii")
        parts.append(FACE % (name, filename, "%.1f" % (len(raw) / 1024.0), b64, urange))
    return "".join(parts)


def main():
    css = render()
    if "--check" in sys.argv[1:]:
        if not os.path.isfile(OUT):
            print("03-fonts.css missing - run: python build/embed-font.py")
            return 1
        current = io.open(OUT, encoding="utf-8").read()
        if current != css:
            print("03-fonts.css is stale - run: python build/embed-font.py")
            return 1
        print("03-fonts.css matches assets/ (%.1f KB)" % (len(css) / 1024.0))
        return 0

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(css)
    print("wrote %s  %.1f KB from %d subset(s)"
          % (os.path.relpath(OUT, THEME).replace("\\", "/"), len(css) / 1024.0, len(SUBSETS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
