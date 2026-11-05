#!/usr/bin/env python3
"""Builds README.md and every SVG in assets/ from data/content.json, the GitHub
API and the aimade.games sitemap. Standard library only."""
import base64, glob, html, json, os, random, re, sys, textwrap, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = "elliothimmelfarb"
RAW = f"https://github.com/{USER}"
EMBER = "#f4581f"
THEMES = {
    "dark": {"bg": "#141412", "ink": "#f3f0e8", "quiet": "#a7a297", "off": "rgba(243,240,232,.09)", "line": "rgba(243,240,232,.2)"},
    "light": {"bg": "#f3f0e8", "ink": "#141412", "quiet": "#66635c", "off": "rgba(20,20,18,.09)", "line": "rgba(20,20,18,.18)"},
}
SANS = '"Helvetica Neue",Helvetica,Arial,sans-serif'
MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"
MARK = '<path fill="#f4581f" d="M44.55 19.07A21 21 0 1 0 44.55 44.93L36.83 41.81A13.2 13.2 0 1 1 36.83 22.19Z"/>'
SPARK = '<path fill="#f4581f" d="M45.04 27.44C48.27 24.22 51.63 24.75 56.33 24.49C54.78 26.84 54.38 28.85 54.18 30.67C55.19 30.46 56.13 30.06 57.0 29.32C56.46 31.88 55.66 34.16 53.91 35.91C51.16 38.66 47.33 38.73 44.91 36.31C42.49 33.89 42.22 30.26 45.04 27.44Z"/>'
CALM = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def esc(text):
    return html.escape(text, quote=True)


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def write(name, text):
    with open(os.path.join(ROOT, "assets", name), "w") as f:
        f.write(text)


def grid(x0, y0, cols, sz, gap, total, loop):
    base, lit = [], []
    for i in range(total):
        x, y = x0 + (i % cols) * (sz + gap), y0 + (i // cols) * (sz + gap)
        base.append(f'<rect class="base" x="{x}" y="{y}" width="{sz}" height="{sz}" rx="4"/>')
        lit.append(f'<rect class="c" x="{x}" y="{y}" width="{sz}" height="{sz}" rx="4" style="animation-delay:{i / total * loop * .72:.2f}s"/>')
    return "".join(base + lit)


def sparks(x_lo, x_hi, y_lo, y_hi):
    rng = random.Random(7)
    out = []
    for _ in range(14):
        out.append('<circle class="p" cx="%d" cy="%d" r="%.1f" style="--dx:%dpx;--dy:%dpx;animation-delay:%.2fs;animation-duration:%.2fs"/>' % (
            rng.uniform(x_lo, x_hi), rng.uniform(y_lo, y_hi), rng.uniform(1.2, 3), rng.uniform(10, 70), -rng.uniform(60, 130), rng.uniform(0, 5), rng.uniform(3, 5.5)))
    return "".join(out)


def hero_style(t, loop):
    return f"""<style>
.h{{font:800 74px {SANS};fill:{t['ink']};letter-spacing:-2.5px}}.s{{font:400 25px {SANS};fill:{t['quiet']}}}
.e{{font:600 22px {SANS};fill:{t['ink']}}}.em{{fill:{EMBER}}}.l{{font:700 13px {MONO};fill:{t['quiet']};letter-spacing:1.4px}}
.base{{fill:{t['off']}}}.c{{fill:{EMBER};opacity:0;animation:burn {loop}s linear infinite}}
@keyframes burn{{0%{{opacity:0}}1.5%{{opacity:1}}3%{{opacity:.78}}88%{{opacity:.78}}96%,100%{{opacity:0}}
.p{{fill:{EMBER};opacity:0;animation:rise 4s ease-out infinite}}
@keyframes rise{{0%{{transform:translate(0,0);opacity:0}}12%{{opacity:.9}}100%{{transform:translate(var(--dx),var(--dy));opacity:0}}
.sp{{transform-box:fill-box;transform-origin:center;animation:fl 3.2s ease-in-out infinite}}
@keyframes fl{{0%,100%{{transform:scale(1)}}42%{{transform:scale(1.13) rotate(-3deg)}}
@media (prefers-reduced-motion:reduce){{.c,.p,.sp{{animation:none}}.c{{opacity:.78}}
</style>"""


def hero(t, drops):
    label = 'Elliot Himmelfarb. AI fluency coach and software consultant. you times AI fluency equals incredible things only you can do.'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400" role="img" aria-label="{label}">
{hero_style(t, 16)}<rect fill="{t['bg']}" width="1280" height="400" rx="18"/>
<g transform="translate(64,62) scale(1.15)">{MARK}<g class="sp">{SPARK}</g></g>{sparks(205, 262, 150, 190)}
<text class="h" x="64" y="218">Elliot Himmelfarb</text>
<text class="s" x="66" y="262">AI fluency coach and software consultant, Lisbon</text>
<text class="e" x="66" y="334">you <tspan class="em">×</tspan> AI fluency <tspan class="em">=</tspan> incredible things only you can do</text>
<text class="l" x="800" y="136">{drops} GAMES SHIPPED BY ONE ROUTINE</text>{grid(800, 158, 22, 14, 4, drops, 16)}
</svg>"""


def hero_phone(t, drops):
    label = 'Elliot Himmelfarb. AI fluency coach and software consultant.'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 800" width="640" height="800" role="img" aria-label="{label}">
{hero_style(t, 16)}<style>.h{{font-size:76px}}.s{{font-size:31px}}.e{{font-size:30px}}.l{{font-size:17px}}</style>
<rect fill="{t['bg']}" width="640" height="800" rx="18"/>
<g transform="translate(40,36) scale(1.15)">{MARK}<g class="sp">{SPARK}</g></g>{sparks(170, 230, 110, 150)}
<text class="h" x="40" y="212">Elliot</text><text class="h" x="40" y="290">Himmelfarb</text>
<text class="s" x="42" y="344">AI fluency coach and</text><text class="s" x="42" y="384">software consultant, Lisbon</text>
<text class="e" x="42" y="448">you <tspan class="em">×</tspan> AI fluency <tspan class="em">=</tspan></text><text class="e" x="42" y="488">incredible things only you can do</text>
<text class="l" x="42" y="546">{drops} GAMES SHIPPED BY ONE ROUTINE</text>{grid(42, 562, 20, 22, 5, drops, 16)}
</svg>"""


def tile(t, site):
    img = data_uri(os.path.join(ROOT, "assets/raw", site["id"] + ".jpg"))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 640 420" width="640" height="420" role="img" aria-label="{esc(site['name'])}. {esc(site['line'])}">
<style>.n{{font:800 28px {SANS};fill:{t['ink']};letter-spacing:-.6px}}.d{{font:400 20px {SANS};fill:{t['quiet']}}}.u{{font:600 16px {MONO};fill:{EMBER}}}
.pan{{animation:pan 22s ease-in-out infinite alternate;transform-origin:50% 30%}}@keyframes pan{{from{{transform:scale(1)}}to{{transform:scale(1.08)}}{CALM}</style>
<clipPath id="c"><path d="M0 18a18 18 0 0 1 18-18h604a18 18 0 0 1 18 18v282H0z"/></clipPath>
<rect fill="{t['bg']}" width="640" height="420" rx="18"/>
<g clip-path="url(#c)"><image class="pan" href="{img}" width="640" height="400" preserveAspectRatio="xMidYMin slice"/></g>
<text class="n" x="24" y="344">{esc(site['name'])}</text><text class="d" x="24" y="374">{esc(site['line'])}</text>
<text class="u" x="24" y="402">{esc(re.sub('^https://', '', site['url']))}</text>
</svg>"""


def tile_wide(t, site):
    img = data_uri(os.path.join(ROOT, "assets/raw", site["id"] + ".jpg"))
    lines = "".join(f'<text class="d" x="40" y="{196 + i * 34}">{esc(l)}</text>' for i, l in enumerate(textwrap.wrap(site["line"], 38)))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400" role="img" aria-label="{esc(site['name'])}. {esc(site['line'])}">
<style>.n{{font:800 44px {SANS};fill:{t['ink']};letter-spacing:-1px}}.d{{font:400 25px {SANS};fill:{t['quiet']}}}.u{{font:600 18px {MONO};fill:{EMBER}}}
.pan{{animation:pan 22s ease-in-out infinite alternate;transform-origin:50% 30%}}@keyframes pan{{from{{transform:scale(1)}}to{{transform:scale(1.08)}}}}{CALM}</style>
<clipPath id="c"><path d="M520 0h742a18 18 0 0 1 18 18v364a18 18 0 0 1-18 18H520z"/></clipPath>
<rect fill="{t['bg']}" width="1280" height="400" rx="18"/>
<g clip-path="url(#c)"><g transform="translate(520,0)"><image class="pan" href="{img}" width="760" height="475" preserveAspectRatio="xMidYMin slice"/></g></g>
<text class="n" x="40" y="146">{esc(site['name'])}</text>{lines}
<text class="u" x="40" y="340">{esc(re.sub('^https://', '', site['url']))}</text>
</svg>"""


def wall(t, count, tools):
    files = sorted(glob.glob(os.path.join(ROOT, "assets/raw/wall/*.jpg")))
    w, h, gap = 240, 150, 10
    defs, rows = [], []
    for i, f in enumerate(files):
        defs.append(f'<image id="g{i}" href="{data_uri(f)}" width="{w}" height="{h}" clip-path="url(#r)"/>')
    half = len(files) // 2
    for row, part, cls in ((0, range(half), "a"), (1, range(half, half * 2), "b")):
        cells = "".join(f'<use href="#g{i}" x="{n * (w + gap)}"/><use href="#g{i}" x="{(n + half) * (w + gap)}"/>' for n, i in enumerate(part))
        rows.append(f'<g transform="translate(0,{18 + row * (h + gap)})"><g class="{cls}">{cells}</g></g>')
    shift = half * (w + gap)
    label = f"A scrolling wall of screenshots from {count} games on aimade.games."
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400" role="img" aria-label="{label}">
<style>.a{{animation:l 70s linear infinite}}.b{{animation:r 70s linear infinite}}@keyframes l{{to{{transform:translateX(-{shift}px)}}@keyframes r{{from{{transform:translateX(-{shift}px)}}to{{transform:translateX(0)}}
.n{{font:800 24px {SANS};fill:{t['ink']}}}.d{{font:400 18px {SANS};fill:{t['quiet']}}}{CALM}</style>
<defs><clipPath id="r"><rect width="{w}" height="{h}" rx="10"/></clipPath><clipPath id="o"><rect width="1280" height="400" rx="18"/></clipPath>{''.join(defs)}</defs>
<g clip-path="url(#o)"><rect fill="{t['bg']}" width="1280" height="400"/>{''.join(rows)}</g>
<text class="n" x="24" y="372">{count} games on aimade.games</text>
<text class="d" x="1256" y="372" text-anchor="end">Humans play. Agents publish through {tools} MCP tools.</text>
</svg>"""


def wall_phone(t, count, tools):
    files = sorted(glob.glob(os.path.join(ROOT, "assets/raw/wall/*.jpg")))[:12]
    w, h, gap = 240, 150, 10
    defs = "".join(f'<image id="g{i}" href="{data_uri(f)}" width="{w}" height="{h}" clip-path="url(#r)"/>' for i, f in enumerate(files))
    rows = []
    for row, cls in ((0, "a"), (1, "b")):
        cells = "".join(f'<use href="#g{row * 6 + n}" x="{n * (w + gap)}"/><use href="#g{row * 6 + n}" x="{(n + 6) * (w + gap)}"/>' for n in range(6))
        rows.append(f'<g transform="translate(0,{18 + row * (h + gap)})"><g class="{cls}">{cells}</g></g>')
    shift = 6 * (w + gap)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 450" width="640" height="450" role="img" aria-label="A scrolling wall of screenshots from {count} games on aimade.games.">
<style>.a{{animation:l 40s linear infinite}}.b{{animation:r 40s linear infinite}}@keyframes l{{to{{transform:translateX(-{shift}px)}}}}@keyframes r{{from{{transform:translateX(-{shift}px)}}to{{transform:translateX(0)}}}}
.n{{font:800 34px {SANS};fill:{t['ink']}}}.d{{font:400 23px {SANS};fill:{t['quiet']}}}{CALM}</style>
<defs><clipPath id="r"><rect width="{w}" height="{h}" rx="10"/></clipPath><clipPath id="o"><rect width="640" height="450" rx="18"/></clipPath>{defs}</defs>
<g clip-path="url(#o)"><rect fill="{t['bg']}" width="640" height="450"/>{''.join(rows)}</g>
<text class="n" x="20" y="384">{count} games on aimade.games</text><text class="d" x="20" y="424">Agents publish through {tools} MCP tools.</text>
</svg>"""


def loop_phone(t):
    steps = ["heartbeat", "read the constitution", "build", "verify", "improve the factory"]
    boxes = ""
    for i, step in enumerate(steps):
        y = 30 + i * 112
        boxes += f'<rect class="b" x="90" y="{y}" width="460" height="82" rx="14"/><rect class="on" x="90" y="{y}" width="460" height="82" rx="14" style="animation-delay:{i * .8}s"/><text class="t" x="320" y="{y + 51}" text-anchor="middle">{step}</text>'
        if i < 4:
            boxes += f'<path class="w" d="M320 {y + 82}V{y + 112}"/>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" width="640" height="640" role="img" aria-label="The loop the factory ran: heartbeat, read the constitution, build, verify, improve the factory. A failed improvement reverted itself.">
<style>.b,.w{{fill:none;stroke:{t['line']};stroke-width:2}}.t{{font:600 28px {SANS};fill:{t['ink']}}}
.on{{fill:none;stroke:{EMBER};stroke-width:4;opacity:0;animation:p 9s linear infinite}}@keyframes p{{0%{{opacity:0}}2%{{opacity:1}}15%{{opacity:1}}19%,100%{{opacity:0}}}}{CALM}</style>
<rect fill="{t['bg']}" width="640" height="640" rx="18"/>{boxes}
<path class="w" stroke-dasharray="6 7" d="M90 519H40V71H90"/>
<circle r="9" fill="{EMBER}"><animateMotion dur="9s" repeatCount="indefinite" path="M90 30H550V560H90V612H40V30Z"/></circle>
</svg>"""


def loop(t):
    steps = [("heartbeat",), ("read the", "constitution"), ("build",), ("verify",), ("improve", "the factory")]
    xs = [110, 330, 550, 770, 990]
    boxes = ""
    for i, (lines, x) in enumerate(zip(steps, xs)):
        text = "".join(f'<text class="t" x="{x}" y="{102 + j * 20 - (len(lines) - 1) * 10}" text-anchor="middle">{l}</text>' for j, l in enumerate(lines))
        boxes += f'<rect class="b" x="{x - 90}" y="60" width="180" height="72" rx="12"/><rect class="on" x="{x - 90}" y="60" width="180" height="72" rx="12" style="animation-delay:{i * .8}s"/>{text}'
    wires = "".join(f'<path class="w" d="M{xs[i] + 90} 96H{xs[i + 1] - 90}"/>' for i in range(4))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 230" width="1100" height="230" role="img" aria-label="The loop the factory ran: heartbeat, read the constitution, build, verify, improve the factory. A failed improvement reverted itself.">
<style>.b,.w{{fill:none;stroke:{t['line']};stroke-width:1.5}}.t{{font:600 17px {SANS};fill:{t['ink']}}}.n{{font:400 14px {MONO};fill:{t['quiet']}}}
.on{{fill:none;stroke:{EMBER};stroke-width:3;opacity:0;animation:p 9s linear infinite}}@keyframes p{{0%{{opacity:0}}2%{{opacity:1}}15%{{opacity:1}}19%,100%{{opacity:0}}{CALM}</style>
<rect fill="{t['bg']}" width="1100" height="230" rx="18"/>{wires}{boxes}
<path class="w" stroke-dasharray="5 6" d="M1080 96V184H20V96"/>
<text class="n" x="550" y="212" text-anchor="middle">a failed improvement reverted itself, then the heartbeat fired again</text>
<circle r="7" fill="{EMBER}"><animateMotion dur="9s" repeatCount="indefinite" path="M20 60H1080V184H20Z"/></circle>
</svg>"""


def blurb(text):
    """First sentence of a repo description, in at most two card lines."""
    first = re.split(r"(?<=[.:])\s", (text or "").replace(" \u2014 ", ", "))[0].rstrip(":.")
    return textwrap.shorten(first, 105, placeholder="...")


def card(t, repo):
    lines = textwrap.wrap(blurb(repo["description"]), 54)
    desc = "".join(f'<text class="d" x="24" y="{86 + i * 28}">{esc(l)}</text>' for i, l in enumerate(lines))
    meta = "  ·  ".join(x for x in (repo.get("language"), repo.get("license")) if x)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 170" width="640" height="170" role="img" aria-label="{esc(repo['name'])}: {esc(repo['description'] or '')}">
<style>.n{{font:700 26px {MONO};fill:{EMBER}}}.d{{font:400 22px {SANS};fill:{t['ink']}}}.m{{font:400 16px {MONO};fill:{t['quiet']}}}</style>
<rect fill="{t['bg']}" stroke="{t['line']}" x=".5" y=".5" width="639" height="169" rx="16"/>
<text class="n" x="24" y="46">{esc(repo['name'])}</text>{desc}<text class="m" x="24" y="152">{esc(meta)}</text>
</svg>"""


def game(t, g):
    frames = sorted(glob.glob(os.path.join(ROOT, f"assets/raw/games/{g['id']}-*.jpg")))
    n = len(frames)
    dur = n * 5
    imgs = "".join(f'<image class="f" href="{data_uri(f)}" width="640" height="360" style="animation-delay:{i * 5 - dur}s"/>' for i, f in enumerate(frames))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 450" width="640" height="450" role="img" aria-label="{esc(g['name'])}. {esc(g['line'])}">
<style>.f{{opacity:0;animation:x {dur}s linear infinite}}@keyframes x{{0%{{opacity:0}}6%{{opacity:1}}{100 / n:.1f}%{{opacity:1}}{100 / n + 6:.1f}%,100%{{opacity:0}}
.n{{font:800 26px {SANS};fill:{t['ink']}}}.d{{font:400 19px {SANS};fill:{t['quiet']}}}@media (prefers-reduced-motion:reduce){{.f{{animation:none;opacity:1}}</style>
<clipPath id="c"><path d="M0 18a18 18 0 0 1 18-18h604a18 18 0 0 1 18 18v342H0z"/></clipPath>
<rect fill="{t['bg']}" width="640" height="450" rx="18"/><g clip-path="url(#c)">{imgs}</g>
<text class="n" x="24" y="402">{esc(g['name'])}</text><text class="d" x="24" y="430">{esc(g['line'])}</text>
</svg>"""


def picture(name, alt, width=None, phone=False):
    size = f' width="{width}"' if width else ""
    src = ""
    if phone:
        src += f'<source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/{name}-phone-dark.svg">'
        src += f'<source media="(max-width: 600px)" srcset="assets/{name}-phone-light.svg">'
    src += f'<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
    return f'<picture>{src}<img src="assets/{name}-light.svg" alt="{esc(alt)}"{size}></picture>'


def public_cards(names, repos):
    """Only public repos get a card, so the page never links to a 404."""
    by_name = {r["name"]: r for r in repos if not r.get("private") and not r.get("archived")}
    return [by_name[n] for n in names if n in by_name]


def readme(c, cards, count):
    tiles = "\n".join(
        f'<a href="{s["url"]}">{picture("live-" + s["id"], s["name"] + ": " + s["line"], "100%", phone=True)}</a><br>' if s.get("wide")
        else f'<a href="{s["url"]}">{picture("live-" + s["id"], s["name"] + ": " + s["line"], "400")}</a>'
        for s in c["live"])
    toolbox = "\n".join(f'<a href="{RAW}/{r["name"]}">{picture("repo-" + r["name"], r["name"], "400")}</a>' for r in cards)
    games = "\n".join(f'<a href="{g["play"]}">{picture("game-" + g["id"], g["name"] + ": " + g["line"], "400")}</a>' for g in c["games"])
    source = " · ".join(f'[{g["name"]} source]({RAW}/{g["repo"]})' for g in c["games"])
    work = "\n".join(f'- [{w["name"]}]({w["url"]}): {w["line"]}' for w in c["work"])
    return f"""<a href="https://chamainteligente.com">{picture("hero", "Elliot Himmelfarb, AI fluency coach and software consultant", "100%", phone=True)}</a>

I coach people on working with AI and build software with it. This page is generated by [a script in this repo](generator/build.py) and refreshes itself every month, so the numbers and screenshots are real.

## Live now

{tiles}

## The arcade

<a href="https://aimade.games">{picture("wall", f"{count} games on aimade.games", "100%", phone=True)}</a>

An arcade where AI agents are first-class users. They publish through a real MCP server, and every game gets identity, saves and leaderboards from one script tag.

## The machines

{picture("loop", "The factory loop", "100%", phone=True)}

[autonomous-factory]({RAW}/autonomous-factory) ran on a 3-hour heartbeat until I stopped it on 2026-07-06, and a routine shipped [{c['drops']} physics games]({RAW}/aimade-drops) to the arcade, the last on 2026-09-10. Both are stopped, and the state files are all there to read.

## Open toolbox

{toolbox}

## Games by hand, with agents

{games}

{source}

## Work with me

[Chama Inteligente](https://chamainteligente.com) is my company. We do one-on-one AI coaching and hands-on software.

<details>
<summary>Client work and links</summary>

{work}

</details>
"""


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER, "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def main():
    with open(os.path.join(ROOT, "data/content.json")) as f:
        c = json.load(f)
    repos = json.loads(fetch(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed"))
    for r in repos:
        r["license"] = (r.get("license") or {}).get("spdx_id")
    count = len(re.findall(r"aimade\.games/g/", fetch("https://aimade.games/sitemap.xml")))
    cards = public_cards(c["toolbox"], repos)
    for name, t in THEMES.items():
        write(f"hero-{name}.svg", hero(t, c["drops"]))
        write(f"hero-phone-{name}.svg", hero_phone(t, c["drops"]))
        write(f"wall-{name}.svg", wall(t, count, c["mcp_tools"]))
        write(f"wall-phone-{name}.svg", wall_phone(t, count, c["mcp_tools"]))
        write(f"loop-{name}.svg", loop(t))
        write(f"loop-phone-{name}.svg", loop_phone(t))
        for s in c["live"]:
            write(f"live-{s['id']}-{name}.svg", tile_wide(t, s) if s.get("wide") else tile(t, s))
            if s.get("wide"):
                write(f"live-{s['id']}-phone-{name}.svg", tile(t, s))
        for g in c["games"]:
            write(f"game-{g['id']}-{name}.svg", game(t, g))
        for r in cards:
            write(f"repo-{r['name']}-{name}.svg", card(t, r))
    with open(os.path.join(ROOT, "README.md"), "w") as f:
        f.write(readme(c, cards, count))


if __name__ == "__main__":
    main()
