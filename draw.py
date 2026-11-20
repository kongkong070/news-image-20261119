#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261119.

A one-page newspaper front page summing up Thursday 19 November 2026.
Every story was verified against live reporting on 19-20 Nov 2026:
  1. Trump, Xi and Putin held a historic trilateral summit in Shenzhen
     (APEC sidelines) and issued a joint "peace declaration" after
     90 minutes of talks; Ukraine was raised. -- BBC, Reuters.
  2. The International Court of Justice ruled Myanmar committed
     genocide against the Rohingya in its 2017 campaign -- the first
     time the UN's top court has found a state responsible for
     genocide; reparations ordered. -- BBC, Reuters, UN, Amnesty.
  3. Ukraine struck the Crimea (Kerch) bridge for the third time in a
     week; train services were suspended hours before the summit.
     -- Reuters.
  4. Anthropic began trading on Nasdaq under ANT after pricing the
     largest IPO on record at $83 a share, raising $81.3bn; shares
     opened around $111, about a third above the IPO price.
     -- BBC, TechCrunch, Reuters.
  5. Van Gogh's "Chataigniers en fleurs" (Chestnut Trees in Blossom,
     1890) sold at Sotheby's New York for $190.4m, a record for the
     artist. -- AP, BBC, Reuters.
  6. A migrant boat capsized off Yenne, Senegal; dozens missing, four
     bodies recovered, search under way. -- Reuters, BBC.
Output: 1024x1024 PNG, drawn offline with Pillow only (no network,
no photos, no external assets). Run: python3 draw.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 238)
INK = (20, 20, 20)
NAVY = (13, 38, 68)
NAVY2 = (24, 66, 108)
GOLD = (196, 152, 48)
RED = (176, 32, 32)
TEAL = (13, 106, 106)
GREY = (96, 96, 92)
LIGHT = (232, 226, 214)
SKY = (168, 200, 224)
SEA = (44, 96, 140)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, text, fnt, x, y, max_w, leading, fill=INK):
    """Draw wrapped paragraph; returns y after last line."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, text, x, y, color=RED):
    f = font(SANS_B, 20)
    d.text((x, y), text.upper(), font=f, fill=color)
    return y + 26


def rule(d, x0, x1, y, color=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- figures
def draw_person(d, cx, base_y, suit, skin=(232, 190, 150), hair=(70, 60, 55)):
    """Simple seated figure: head, shoulders, torso."""
    d.ellipse([cx - 26, base_y - 118, cx + 26, base_y - 66], fill=skin)
    d.pieslice([cx - 28, base_y - 122, cx + 28, base_y - 82],
               180, 360, fill=hair)
    d.rounded_rectangle([cx - 52, base_y - 64, cx + 52, base_y + 6],
                        radius=14, fill=suit)
    d.polygon([(cx - 10, base_y - 64), (cx + 10, base_y - 64),
               (cx, base_y - 34)], fill=(255, 255, 255))
    d.polygon([(cx - 5, base_y - 58), (cx + 5, base_y - 58),
               (cx, base_y - 30)], fill=RED)


def draw_flag(d, x, y, w, h, kind):
    """Tiny flag on a pole."""
    d.line([(x + w // 2, y), (x + w // 2, y + h + 26)], fill=(90, 70, 40),
           width=3)
    if kind == "us":
        d.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
        for i in range(4):
            d.rectangle([x, y + i * h // 4, x + w, y + (i + 1) * h // 4],
                        fill=(255, 255, 255) if i % 2 else (178, 34, 52))
        d.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7], fill=(30, 50, 110))
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.text((x + 4, y - 2), "*", font=font(SANS_B, 20), fill=(255, 222, 0))
    else:  # ru
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def summit_scene(d, x0, y0, x1, y1):
    """Three leaders seated at a table with three small flags."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 214, 196))
    d.rectangle([x0, y0, x1, y0 + 118], fill=SKY)
    d.ellipse([x0 + 30, y0 + 18, x0 + 86, y0 + 74], fill=(255, 244, 190))
    # table
    d.rectangle([x0 + 14, y1 - 74, x1 - 14, y1 - 52], fill=(122, 82, 48))
    d.rectangle([x0 + 26, y1 - 52, x1 - 26, y1 - 14], fill=(96, 62, 36))
    base = y1 - 74
    draw_person(d, x0 + 92, base, (28, 48, 84))
    draw_person(d, (x0 + x1) // 2, base, (120, 20, 20), hair=(30, 30, 30))
    draw_person(d, x1 - 92, base, (40, 60, 44), skin=(240, 205, 165))
    draw_flag(d, x0 + 66, y0 + 128, 52, 30, "us")
    draw_flag(d, (x0 + x1) // 2 - 26, y0 + 128, 52, 30, "cn")
    draw_flag(d, x1 - 118, y0 + 128, 52, 30, "ru")


def fit_font(path, text, start, max_w):
    """Largest font size <= start whose text fits max_w."""
    size = start
    while size > 8:
        f = font(path, size)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def scales_scene(d, x0, y0, x1, y1):
    """Scales of justice in front of a court facade."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 206, 188))
    d.rectangle([x0, y0, x1, y0 + 22], fill=NAVY)
    for i in range(5):
        cx = x0 + 28 + i * ((x1 - x0 - 56) // 4)
        d.rectangle([cx - 7, y0 + 22, cx + 7, y1 - 84], fill=(240, 236, 224))
    d.rectangle([x0, y1 - 84, x1, y1 - 74], fill=(240, 236, 224))
    cx = (x0 + x1) // 2
    cy = y0 + (y1 - y0) // 2 + 6
    d.line([(cx, cy - 24), (cx, cy + 62)], fill=GOLD, width=5)
    d.line([(cx - 46, cy - 24), (cx + 46, cy - 24)], fill=GOLD, width=4)
    for sgn in (-1, 1):
        px = cx + sgn * 46
        d.line([(px, cy - 24), (px - 18, cy + 18)], fill=GOLD, width=3)
        d.line([(px, cy - 24), (px + 18, cy + 18)], fill=GOLD, width=3)
        d.pieslice([px - 20, cy + 14, px + 20, cy + 32], 0, 180, fill=GOLD)
    d.ellipse([cx - 7, cy - 30, cx + 7, cy - 16], fill=GOLD)
    d.rectangle([cx - 24, cy + 62, cx + 24, cy + 72], fill=GOLD)


def bridge_scene(d, x0, y0, x1, y1):
    """A long bridge over water with its middle span broken."""
    bw = x1 - x0
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y1 - 58, x1, y1], fill=SEA)
    for i in range(3):
        wx = x0 + 24 + i * (bw - 80) // 2
        d.arc([wx, y1 - 74, wx + 56, y1 - 40], 0, 180, fill=(255, 255, 255),
              width=3)
    mid = (x0 + x1) // 2
    g = bw // 7  # half-width of the broken gap
    deck_y = y0 + (y1 - y0) // 2 + 8
    # deck, left and right of the gap
    d.rectangle([x0 + 6, deck_y, mid - g, deck_y + 14], fill=(70, 70, 72))
    d.rectangle([mid + g, deck_y, x1 - 6, deck_y + 14], fill=(70, 70, 72))
    # broken ends drooping into the gap
    d.polygon([(mid - g, deck_y), (mid - g + 14, deck_y),
               (mid - 6, deck_y + 44), (mid - 20, deck_y + 44)],
              fill=(70, 70, 72))
    d.polygon([(mid + g, deck_y), (mid + g - 14, deck_y),
               (mid + 6, deck_y + 44), (mid + 20, deck_y + 44)],
              fill=(70, 70, 72))
    # pillars
    for px in (x0 + bw // 4, x1 - bw // 4):
        d.rectangle([px - 6, deck_y + 14, px + 6, y1 - 58],
                    fill=(90, 90, 92))
    # smoke from the gap
    for i, r in enumerate((9, 12, 15)):
        d.ellipse([mid - r + i * 4, deck_y - 28 - i * 10,
                   mid + r + i * 4, deck_y - 28 - i * 10 + 2 * r],
                  fill=(120, 120, 118))
    d.text((x0 + 10, y0 + 8), "KERCH STRAIT", font=font(SANS_B, 15),
           fill=(255, 255, 255))


def chart_scene(d, x0, y0, x1, y1):
    """A rising stock chart with a big green arrow."""
    d.rectangle([x0, y0, x1, y1], fill=(226, 238, 226))
    pts = []
    n = 7
    span = x1 - x0 - 44
    rise = (y1 - y0) - 44
    for i in range(n):
        px = x0 + 22 + i * span // (n - 1)
        py = y1 - 22 - i * rise // (n - 1) - (3 if i % 2 else 0)
        pts.append((px, py))
    d.line(pts, fill=(16, 120, 60), width=6, joint="curve")
    for px, py in pts:
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(16, 120, 60))
    d.polygon([(x1 - 66, y0 + 22), (x1 - 66, y0 + 46), (x1 - 34, y0 + 34)],
              fill=(16, 120, 60))
    d.text((x0 + 14, y0 + 8), "$83  ->  $111", font=font(SANS_B, 22),
           fill=(16, 120, 60))


def painting_scene(d, x0, y0, x1, y1):
    """A small framed landscape in Van Gogh's manner: sun, trees, road."""
    d.rectangle([x0, y0, x1, y1], fill=(236, 222, 190))
    fx0, fy0, fx1, fy1 = x0 + 16, y0 + 14, x1 - 16, y1 - 14
    hh = fy1 - fy0
    d.rectangle([fx0 - 6, fy0 - 6, fx1 + 6, fy1 + 6], fill=GOLD)
    d.rectangle([fx0, fy0, fx1, fy1], fill=(150, 190, 225))
    d.ellipse([fx1 - 52, fy0 + 6, fx1 - 18, fy0 + 40], fill=(250, 220, 90))
    for tx in (fx0 + 26, fx0 + 66, fx1 - 66, fx1 - 30):
        d.rectangle([tx - 3, fy0 + hh // 2, tx + 3, fy1 - 6],
                    fill=(110, 72, 34))
        d.ellipse([tx - 22, fy0 + hh // 4, tx + 22, fy0 + hh // 2 + 12],
                  fill=(44, 130, 60))
        d.ellipse([tx - 13, fy0 + hh // 3, tx + 17, fy0 + hh // 2 + 4],
                  fill=(90, 170, 70))
    d.polygon([(fx0 + 96, fy1), (fx1 - 96, fy1), (fx1 - 130, fy0 + hh * 2 // 3),
               (fx0 + 130, fy0 + hh * 2 // 3)], fill=(214, 190, 140))
    d.rectangle([fx0, fy1 - 16, fx1, fy1], fill=(96, 150, 70))


def boat_scene(d, x0, y0, x1, y1):
    """A capsized boat in rough Atlantic waves off Senegal."""
    hh = y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(200, 216, 228))
    d.rectangle([x0, y0 + hh // 2, x1, y1], fill=SEA)
    for i in range(4):
        wx = x0 + 18 + i * 70
        d.arc([wx, y0 + hh // 2 + 4, wx + 52, y0 + hh // 2 + 30], 180, 360,
              fill=(255, 255, 255), width=4)
    cx = (x0 + x1) // 2
    top = y0 + hh // 2 - 6
    d.polygon([(cx - 78, top), (cx + 78, top), (cx + 52, top + 24),
               (cx - 52, top + 24)], fill=(140, 84, 44))
    d.polygon([(cx - 78, top), (cx - 52, top + 24), (cx - 30, top + 24),
               (cx - 56, top)], fill=(96, 56, 28))
    d.ellipse([cx + 84, top + 10, cx + 100, top + 26], fill=(232, 190, 150))
    d.arc([cx - 30, top + 30, cx + 30, top + 52], 0, 180,
          fill=(255, 255, 255), width=3)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26  # margin

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 122], fill=GOLD)
    d.text((M, 12), "THE WORLD IN ONE DAY",
           font=font(SERIF, 46), fill=(255, 255, 255))
    d.text((M, 72), "THURSDAY  19  NOVEMBER  2026",
           font=font(SANS_B, 30), fill=GOLD)

    # ---- lead story: the trilateral summit -----------------------------
    ly0, ly1 = 130, 440
    d.rectangle([M, ly0, W - M, ly1], outline=INK, width=2)
    d.rectangle([M, ly0, W - M, ly0 + 4], fill=RED)
    tx = M + 22
    y = ly0 + 20
    y = kicker(d, "Lead story  ·  Shenzhen, China", tx, y)
    y = para(d, "THREE LEADERS,", font(SERIF, 46), tx, y, 520, 54)
    y = para(d, "ONE TABLE", font(SERIF, 46), tx, y, 520, 54)
    y += 6
    y = para(d, "Trump, Xi and Putin hold a historic "
                "trilateral summit and issue a joint "
                "peace declaration after 90 minutes "
                "of talks; Ukraine is raised.",
           font(SERIF_R, 23), tx, y, 500, 31)
    summit_scene(d, M + 560, ly0 + 16, W - M - 16, ly1 - 16)

    # ---- middle row: two stories, picture left, text right --------------
    my0, my1 = 454, 688
    mid = W // 2
    gap = 12
    # left: ICJ genocide ruling
    d.rectangle([M, my0, mid - gap, my1], outline=INK, width=2)
    scales_scene(d, M + 12, my0 + 12, M + 182, my1 - 12)
    tx = M + 196
    tw = mid - gap - tx - 14
    y = my0 + 16
    y = kicker(d, "The Hague  ·  Justice", tx, y)
    y = para(d, "GENOCIDE, THE COURT RULES",
           font(SERIF, 27), tx, y, tw, 33)
    para(d, "The UN's top court finds Myanmar committed "
            "genocide against the Rohingya in 2017 -- the "
            "first such ruling against a state.",
         font(SERIF_R, 18), tx, y + 6, tw, 24)
    # right: Crimea bridge
    d.rectangle([mid + gap, my0, W - M, my1], outline=INK, width=2)
    bridge_scene(d, mid + gap + 12, my0 + 12, mid + gap + 182, my1 - 12)
    tx = mid + gap + 196
    tw = W - M - tx - 14
    y = my0 + 16
    y = kicker(d, "Ukraine  ·  War", tx, y)
    y = para(d, "BRIDGE HIT A THIRD TIME",
           font(SERIF, 27), tx, y, tw, 33)
    para(d, "Ukraine strikes the Crimea bridge again in a "
            "week; trains are halted hours before the "
            "Shenzhen summit.",
         font(SERIF_R, 18), tx, y + 6, tw, 24)

    # ---- bottom row: three stories --------------------------------------
    by0, by1 = 702, 908
    cols = [(M, M + 338), (M + 348, M + 686), (M + 696, W - M)]
    scenes = [chart_scene, painting_scene, boat_scene]
    kickers = ["New York  ·  Markets", "New York  ·  Culture",
               "Senegal  ·  Migration"]
    heads = ["$81bn DEBUT", "A $190.4m VAN GOGH", "DOZENS MISSING"]
    bodies = [
        "Anthropic starts trading on Nasdaq after the "
        "biggest IPO on record; shares open near $111.",
        "\"Chestnut Trees in Blossom\" (1890) sets a record "
        "for the artist at Sotheby's in New York.",
        "A migrant boat capsizes off Yenne; four bodies "
        "recovered, dozens still missing.",
    ]
    for (cx0, cx1), scene, kick, head, body in zip(
            cols, scenes, kickers, heads, bodies):
        d.rectangle([cx0, by0, cx1, by1], outline=INK, width=2)
        scene(d, cx0 + 12, by0 + 10, cx1 - 12, by0 + 74)
        y = by0 + 80
        d.text((cx0 + 14, y), kick.upper(), font=font(SANS_B, 18), fill=RED)
        y += 24
        d.text((cx0 + 14, y), head, font=font(SERIF, 23), fill=INK)
        y += 29
        para(d, body, font(SERIF_R, 16), cx0 + 14, y, cx1 - cx0 - 28, 20)

    # ---- ticker strip ----------------------------------------------------
    ty0, ty1 = 920, 958
    d.rectangle([M, ty0, W - M, ty1], fill=NAVY)
    ticker = ("ALSO TODAY:  Europe's allies meet in Berlin  ·  Macron "
              "reopens Ukraine's NATO question  ·  Jeffries nominated "
              "US House Speaker")
    tf = fit_font(SANS_B, ticker, 16, W - 2 * M - 24)
    d.text((M + 12, ty0 + (ty1 - ty0 - tf.size) // 2 - 2), ticker,
           font=tf, fill=(255, 255, 255))

    # ---- footer -----------------------------------------------------------
    d.text((M, 968), "All stories from reporting of Thursday 19 November "
                     "2026  ·  Sources: BBC, Reuters, AP, UN",
           font=font(SANS, 15), fill=GREY)
    d.text((W - M - 130, 968), "19 NOV 2026", font=font(SANS_B, 15),
           fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
