#!/usr/bin/env python3
"""Render the front page of THE WORLD TODAY for Saturday, 21 November 2026.

Draws a 1024x1024 newspaper infographic with Pillow only: warm cream paper,
dark slate ink, dark-teal and gold/amber accents. One lead story plus five
story cards, each with a small hand-drawn geometric pictogram. No network,
no downloaded assets, fully deterministic.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- Palette: warm cream paper, slate ink, dark teal + gold/amber ----------
PAPER = (247, 240, 223)
CARD = (253, 249, 238)
INK = (31, 42, 51)
SOFT = (79, 95, 104)
TEAL = (11, 79, 74)
TEAL_SOFT = (23, 112, 105)
GOLD = (176, 124, 22)
GOLD_SOFT = (205, 158, 46)
CREAM = (250, 244, 228)
LINE = (196, 182, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh, max_lines=None):
    """Draw lines top-left anchored; returns y just below the last line."""
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# --- Pictograms: pure Pillow geometry, drawn inside a square box ---------
def pic_missile(d, box, scale=1.0):
    """Lead pictogram: a cruise missile over a burst, in a teal disc."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = (x1 - x0) / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    # dashed flight arc
    for i in range(9):
        a0 = 200 + i * 9
        a1 = a0 + 5
        d.arc([cx - r * 0.95, cy - r * 0.95, cx + r * 0.95, cy + r * 0.95],
              a0, a1, fill=GOLD_SOFT, width=3)
    # missile body, diagonal nose-up
    bx, by = cx - r * 0.52, cy + r * 0.30
    tipx, tipy = cx + r * 0.55, cy - r * 0.42
    ux, uy = (tipx - bx) / 1.0, (tipy - by) / 1.0
    L = (ux ** 2 + uy ** 2) ** 0.5
    ux, uy = ux / L, uy / L
    px, py = -uy, ux  # perpendicular
    wdt = r * 0.16
    nose = (tipx, tipy)
    b1 = (bx + px * wdt, by + py * wdt)
    b2 = (bx - px * wdt, by - py * wdt)
    mid1 = (bx + ux * r * 0.72 + px * wdt, by + uy * r * 0.72 + py * wdt)
    mid2 = (bx + ux * r * 0.72 - px * wdt, by + uy * r * 0.72 - py * wdt)
    d.polygon([nose, mid1, b1, b2, mid2], fill=CREAM)
    d.polygon([nose, mid1, mid2], fill=GOLD_SOFT)
    # tail fins
    f1 = (b1[0] - ux * r * 0.16 + px * r * 0.30, b1[1] - uy * r * 0.16 + py * r * 0.30)
    f2 = (b2[0] - ux * r * 0.16 - px * r * 0.30, b2[1] - uy * r * 0.16 - py * r * 0.30)
    d.polygon([b1, f1, (b1[0] - ux * r * 0.22, b1[1] - uy * r * 0.22)], fill=GOLD)
    d.polygon([b2, f2, (b2[0] - ux * r * 0.22, b2[1] - uy * r * 0.22)], fill=GOLD)
    # amber burst at the tail
    tx, ty = bx - ux * r * 0.18, by - uy * r * 0.18
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        ox, oy = math.cos(rad), math.sin(rad)
        d.line([(tx + ox * r * 0.10, ty + oy * r * 0.10),
                (tx + ox * r * 0.30, ty + oy * r * 0.30)],
               fill=GOLD_SOFT, width=5)
    d.ellipse([tx - r * 0.09, ty - r * 0.09, tx + r * 0.09, ty + r * 0.09],
              fill=GOLD_SOFT)


def pic_chart(d, box):
    """Falling candlesticks with a down-trend arrow."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=TEAL, width=3)
    # three descending candles
    candles = [(0.18, 0.30, 0.42), (0.44, 0.48, 0.62), (0.70, 0.62, 0.80)]
    for fx, top, bot in candles:
        cx = x0 + w * fx
        cw = w * 0.13
        d.line([(cx, y0 + (y1 - y0) * (top - 0.08)),
                (cx, y0 + (y1 - y0) * (bot + 0.08))], fill=INK, width=3)
        d.rectangle([cx - cw / 2, y0 + (y1 - y0) * top,
                     cx + cw / 2, y0 + (y1 - y0) * bot], fill=TEAL)
    # down arrow
    d.line([(x0 + w * 0.12, y0 + (y1 - y0) * 0.22),
            (x0 + w * 0.86, y0 + (y1 - y0) * 0.78)], fill=GOLD, width=5)
    ax, ay = x0 + w * 0.86, y0 + (y1 - y0) * 0.78
    d.polygon([(ax, ay), (ax - 14, ay - 2), (ax - 2, ay - 14)], fill=GOLD)


def pic_scales(d, box):
    """Scales of justice."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx = x0 + w / 2
    d.line([(cx, y0 + h * 0.12), (cx, y0 + h * 0.86)], fill=TEAL, width=5)
    d.line([(x0 + w * 0.14, y0 + h * 0.24), (x0 + w * 0.86, y0 + h * 0.24)],
           fill=TEAL, width=5)
    d.ellipse([cx - 5, y0 + h * 0.06, cx + 5, y0 + h * 0.16], fill=GOLD)
    for sx in (0.14, 0.86):
        px = x0 + w * sx
        py = y0 + h * 0.24
        d.line([(px, py), (px - w * 0.11, y0 + h * 0.52)], fill=INK, width=3)
        d.line([(px, py), (px + w * 0.11, y0 + h * 0.52)], fill=INK, width=3)
        d.arc([px - w * 0.11, y0 + h * 0.44, px + w * 0.11, y0 + h * 0.62],
              0, 180, fill=GOLD, width=4)
    d.line([(cx - w * 0.16, y0 + h * 0.86), (cx + w * 0.16, y0 + h * 0.86)],
           fill=TEAL, width=5)


def pic_quake(d, box):
    """Seismograph trace with a ground crack."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=TEAL, width=3)
    pts = []
    frac = [(0.06, 0.55), (0.16, 0.55), (0.22, 0.30), (0.28, 0.78),
            (0.34, 0.42), (0.40, 0.62), (0.46, 0.18), (0.52, 0.85),
            (0.58, 0.45), (0.64, 0.58), (0.72, 0.55), (0.82, 0.55),
            (0.94, 0.55)]
    for fx, fy in frac:
        pts.append((x0 + w * fx, y0 + h * fy))
    d.line(pts, fill=TEAL, width=4, joint="curve")
    d.ellipse([x0 + w * 0.46 - 5, y0 + h * 0.18 - 5,
               x0 + w * 0.46 + 5, y0 + h * 0.18 + 5], fill=GOLD)


def pic_rings(d, box):
    """Two interlinked rings: partnership."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    r = w * 0.26
    c1 = (x0 + w * 0.38, y0 + h * 0.50)
    c2 = (x0 + w * 0.62, y0 + h * 0.50)
    d.ellipse([c1[0] - r, c1[1] - r, c1[0] + r, c1[1] + r],
              outline=TEAL, width=6)
    d.ellipse([c2[0] - r, c2[1] - r, c2[0] + r, c2[1] + r],
              outline=GOLD, width=6)
    # small bridge arc above
    d.arc([x0 + w * 0.28, y0 + h * 0.02, x0 + w * 0.72, y0 + h * 0.42],
          200, 340, fill=TEAL_SOFT, width=4)


def pic_globe_clock(d, box):
    """Globe with a small clock: a summit running late."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.46, y0 + h * 0.50
    r = w * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=TEAL_SOFT, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=TEAL_SOFT, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
          fill=TEAL_SOFT, width=3)
    # clock
    kx, ky = x0 + w * 0.80, y0 + h * 0.76
    kr = w * 0.17
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=GOLD)
    d.line([(kx, ky), (kx, ky - kr * 0.62)], fill=INK, width=3)
    d.line([(kx, ky), (kx + kr * 0.55, ky + kr * 0.18)], fill=INK, width=3)


def pic_list(d, box):
    """A short list: the sources panel mark."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i, fy in enumerate((0.24, 0.50, 0.76)):
        y = y0 + h * fy
        d.ellipse([x0 + w * 0.10, y - 4, x0 + w * 0.10 + 8, y + 4], fill=GOLD)
        d.line([(x0 + w * 0.28, y), (x0 + w * 0.88, y)], fill=TEAL, width=4)


# --- Story data: only the verified facts from the task ---------------------
LEAD = {
    "kicker": "LEAD STORY  ·  EUROPE",
    "headline": "Russian missiles hit Poland",
    "body": ("Kh-101 cruise missiles fell near Nowy Lipowiec, 50 km from the "
             "Ukrainian border, at 06:30 local time. Three objects entered "
             "Polish airspace: two missiles and a jet drone. PM Donald Tusk "
             "called it an \u201cintentional provocation\u201d; NATO jets "
             "scrambled and NATO\u2019s Mark Rutte condemned \u201cgrave "
             "violations\u201d. No casualties."),
    "source": "SOURCES: BBC  ·  REUTERS",
}

CARDS = [
    {
        "kicker": "MARKETS  ·  USA",
        "headline": "Wall Street enters correction",
        "body": ("S&P 500 \u22123.70% to 6,910.39, 10% off record. "
                 "Nasdaq \u22125.28%; Nvidia \u221214.01% to $125.53."),
        "source": "REUTERS  ·  CNBC  ·  MOTLEY FOOL",
        "pic": pic_chart,
    },
    {
        "kicker": "JUSTICE  ·  THE HAGUE",
        "headline": "ICJ: Myanmar committed genocide",
        "body": ("Ruled 9\u20136: genocide against the Rohingya in 2017. "
                 "Investigation and compensation ordered."),
        "source": "ICJ",
        "pic": pic_scales,
    },
    {
        "kicker": "DISASTER  ·  PERU",
        "headline": "Magnitude 6.8 quake hits central Peru",
        "body": ("A 6.8 quake shook Jun\u00edn in central Peru; tremors were "
                 "felt in Lima, about 320 km away."),
        "source": "INSTITUT GEOFISIKA PERU",
        "pic": pic_quake,
    },
    {
        "kicker": "DIPLOMACY  ·  BRUSSELS",
        "headline": "UK and EU seal Brussels deals",
        "body": ("Food checks end March 2028; carbon markets link Jan 2028. "
                 "Youth: 100,000 aged 18\u201331."),
        "source": "GOV.UK  ·  BBC",
        "pic": pic_rings,
    },
    {
        "kicker": "CLIMATE  ·  ANTALYA",
        "headline": "COP31 summit misses deadline",
        "body": ("COP31 in Antalya passed its deadline; the draft drops any "
                 "mention of fossil fuels."),
        "source": "UN NEWS  ·  REUTERS",
        "pic": pic_globe_clock,
    },
]

SOURCES_NOTE = ("All six stories happened, or were first reported, on "
                "Saturday, 21 November 2026. Sources: BBC, Reuters, CNBC, "
                "Motley Fool, ICJ, Institut Geofisika Peru, GOV.UK, UN News.")


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([36, 26, W - 36, 31], fill=TEAL)
    d.rectangle([36, 35, W - 36, 37], fill=GOLD)
    title = "THE WORLD TODAY"
    tf = SERIF_B(64)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 42), title, font=tf, fill=INK)
    # date line with flanking rules
    date = "Saturday, 21 November 2026"
    df = SANS_B(25)
    dw = d.textlength(date, font=df)
    cy = 122
    d.line([(36, cy + 12), ((W - dw) / 2 - 24, cy + 12)], fill=GOLD, width=2)
    d.line([((W + dw) / 2 + 24, cy + 12), (W - 36, cy + 12)], fill=GOLD, width=2)
    d.text(((W - dw) / 2, cy), date, font=df, fill=TEAL)
    sub = "SIX STORIES  ·  ONE DAY  ·  FROM AROUND THE WORLD"
    sf = SANS(16)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 150), sub, font=sf, fill=SOFT)

    # ---- Lead story -----------------------------------------------------
    lx0, ly0, lx1, ly1 = 36, 182, W - 36, 462
    d.rounded_rectangle([lx0, ly0, lx1, ly1], radius=10, fill=CARD,
                        outline=TEAL, width=3)
    d.rounded_rectangle([lx0, ly0, lx0 + 10, ly1], radius=5, fill=TEAL)
    tx = lx0 + 30
    ty = ly0 + 16
    kf = SANS_B(21)
    d.text((tx, ty), LEAD["kicker"], font=kf, fill=TEAL)
    ty += 30
    hf = SERIF_B(43)
    d.text((tx, ty), LEAD["headline"], font=hf, fill=INK)
    ty += 54
    bf = SANS(19)
    lines = wrap(d, LEAD["body"], bf, 660)
    ty = draw_lines(d, tx, ty, lines, bf, INK, 23, max_lines=5)
    ty += 8
    srf = SANS_B(15)
    d.text((tx, ty), LEAD["source"], font=srf, fill=GOLD)
    # lead pictogram, right side
    pic_missile(d, (lx1 - 218, ly0 + 34, lx1 - 30, ly0 + 222))

    # ---- Story cards: 3 columns x 2 rows -------------------------------
    gx0, gy0 = 36, 478
    gap = 16
    cw = (W - 2 * 36 - 2 * gap) // 3
    ch = 230
    cells = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)]
    for idx, card in enumerate(CARDS):
        col, row = cells[idx]
        x0 = gx0 + col * (cw + gap)
        y0 = gy0 + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                            outline=LINE, width=2)
        # pictogram top-left, kicker beside it
        card["pic"](d, (x0 + 14, y0 + 12, x0 + 66, y0 + 64))
        kf2 = SANS_B(16)
        klines = wrap(d, card["kicker"], kf2, cw - 84)
        draw_lines(d, x0 + 76, y0 + 16, klines, kf2, TEAL, 20, max_lines=2)
        # headline
        hf2 = SERIF_B(25)
        hlines = wrap(d, card["headline"], hf2, cw - 28)
        hy = y0 + 72
        hy = draw_lines(d, x0 + 14, hy, hlines, hf2, INK, 29, max_lines=2)
        # body
        bf2 = SANS(16)
        blines = wrap(d, card["body"], bf2, cw - 28)
        by = hy + 6
        draw_lines(d, x0 + 14, by, blines, bf2, INK, 20, max_lines=3)
        # source tag at the bottom
        srf2 = SANS_B(13)
        d.text((x0 + 14, y1 - 24), card["source"], font=srf2, fill=GOLD)

    # ---- Sixth cell: sources & note --------------------------------------
    col, row = cells[5]
    x0 = gx0 + col * (cw + gap)
    y0 = gy0 + row * (ch + gap)
    x1, y1 = x0 + cw, y0 + ch
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=TEAL)
    pic_list(d, (x0 + 14, y0 + 12, x0 + 66, y0 + 64))
    d.text((x0 + 76, y0 + 18), "SOURCES", font=SANS_B(17), fill=GOLD_SOFT)
    d.text((x0 + 76, y0 + 40), "& NOTE", font=SANS_B(17), fill=GOLD_SOFT)
    nf = SANS(17)
    nlines = wrap(d, SOURCES_NOTE, nf, cw - 28)
    draw_lines(d, x0 + 14, y0 + 76, nlines, nf, CREAM, 21, max_lines=6)

    # ---- Footer ----------------------------------------------------------
    d.line([(36, 964), (W - 36, 964)], fill=LINE, width=2)
    foot = "THE WORLD TODAY  ·  Drawn with Python and Pillow  ·  No photographs"
    ff = SANS(15)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 972), foot, font=ff, fill=SOFT)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", compress_level=9)
    return out


if __name__ == "__main__":
    print(render())
