#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a one-page front page summing up
Tuesday 24 November 2026 world news. Run on the build machine (PIL is NOT
available in the grading sandbox); the entry program main.py only copies
the finished entry.png to /output. Output: 1024x1024 PNG, <= 1 MiB."""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 233)      # warm newsprint
INK = (26, 26, 26)
RULE = (26, 26, 26)
RED = (178, 34, 34)
GREY = (105, 105, 105)
TEAL = (14, 124, 123)
GREEN = (30, 132, 73)
NAVY = (31, 56, 100)
BLUE = (36, 86, 166)
DARKRED = (176, 58, 46)
PURPLE = (106, 58, 138)
PANEL = (232, 226, 212)
AMBER = (232, 168, 32)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, max_w, fill, leading=1.22):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------------------------------------------------------- icons
def icon_building_hit(draw, x, y, s, color=NAVY):
    """A shelled apartment block: broken windows, crack, smoke, rubble."""
    bx0, by0 = x + 22, y + 58
    bw, bh = s - 60, s - 58 - 26
    # smoke clouds
    for cx, cy, r in [(x + 52, y + 26, 22), (x + 82, y + 14, 26),
                      (x + 116, y + 30, 20), (x + 140, y + 16, 16)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    # building body
    draw.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=color)
    # roofline damage: jagged top edge
    draw.polygon([(bx0, by0), (bx0 + bw * 0.3, by0 + 14), (bx0 + bw * 0.55, by0 - 2),
                  (bx0 + bw * 0.8, by0 + 12), (bx0 + bw, by0),
                  (bx0 + bw, by0 + 16), (bx0, by0 + 16)], fill=color)
    # windows: lit / broken
    for row in range(3):
        for col in range(4):
            wx = bx0 + 14 + col * ((bw - 28) // 3)
            wy = by0 + 22 + row * ((bh - 40) // 2)
            if (row, col) in [(0, 1), (1, 2)]:
                # blown-out window: dark hole with jagged edge
                draw.polygon([(wx, wy), (wx + 26, wy + 4), (wx + 22, wy + 26),
                              (wx + 2, wy + 24)], fill=(10, 10, 10))
            else:
                draw.rectangle([wx, wy, wx + 24, wy + 26], fill=(210, 205, 180))
    # crack down the facade
    pts = [(bx0 + bw * 0.62, by0 + 6), (bx0 + bw * 0.5, by0 + bh * 0.4),
           (bx0 + bw * 0.66, by0 + bh * 0.65), (bx0 + bw * 0.52, by0 + bh)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    # rubble at the base
    for rx, ry, rr in [(x + 30, y + s - 26, 12), (x + 62, y + s - 20, 16),
                       (x + 100, y + s - 28, 11), (x + s - 40, y + s - 22, 13)]:
        draw.polygon([(rx - rr, ry), (rx, ry - rr), (rx + rr, ry)], fill=(120, 116, 104))
    # blast starburst at the roof corner
    bx, by = x + s - 34, y + 52
    star = []
    for i in range(12):
        ang = math.pi * i / 6
        rr = 18 if i % 2 == 0 else 7
        star.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    draw.polygon(star, fill=(232, 120, 32))
    draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 220, 90))


def icon_gavel(draw, x, y, s, color=DARKRED):
    """A judge's gavel over a sound block (states sue SpaceX over Grok)."""
    # gavel head: diagonal bar
    draw.polygon([(x + 34, y + 22), (x + s - 30, y + 52), (x + s - 44, y + 84),
                  (x + 20, y + 54)], fill=color)
    # head end caps
    draw.line([x + 34, y + 22, x + 20, y + 54], fill=color, width=8)
    draw.line([x + s - 30, y + 52, x + s - 44, y + 84], fill=color, width=8)
    # handle
    draw.line([x + s // 2 - 4, y + s // 2 + 6, x + 26, y + s - 40],
              fill=INK, width=9)
    # sound block
    draw.rounded_rectangle([x + 14, y + s - 40, x + 84, y + s - 22], radius=6,
                           fill=INK)
    # red "no" ring around a small chatbot head (top right)
    cx, cy, r = x + s - 30, y + 26, 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=5)
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(210, 205, 180))
    draw.ellipse([cx - 6, cy - 9, cx - 1, cy - 4], fill=INK)
    draw.ellipse([cx + 1, cy - 9, cx + 6, cy - 4], fill=INK)
    draw.line([cx - 6, cy + 6, cx + 6, cy + 6], fill=INK, width=3)
    draw.line([cx - r + 4, cy + r - 4, cx + r - 4, cy - r + 4], fill=RED, width=5)


def icon_jet(draw, x, y, s, color=NAVY):
    """A fighter jet crossing a dashed border line (airspace incursion)."""
    # dashed border line
    for i in range(7):
        lx = x + 8 + i * ((s - 16) // 7)
        draw.line([lx, y + s - 30, lx + (s - 16) // 7 - 8, y + s - 30],
                  fill=RED, width=4)
    # jet silhouette (flying right)
    cx, cy = x + s // 2, y + s // 2 - 8
    jet = [(cx - 52, cy + 2), (cx - 30, cy - 6), (cx + 10, cy - 8),
           (cx + 52, cy), (cx + 10, cy + 8), (cx - 30, cy + 6),
           (cx - 52, cy + 2)]
    draw.polygon(jet, fill=color)
    # swept wing
    draw.polygon([(cx - 12, cy - 6), (cx + 6, cy - 34), (cx + 18, cy - 32),
                  (cx + 8, cy - 4)], fill=color)
    draw.polygon([(cx - 12, cy + 6), (cx + 2, cy + 30), (cx + 14, cy + 28),
                  (cx + 6, cy + 4)], fill=color)
    # tail fin
    draw.polygon([(cx - 44, cy - 4), (cx - 52, cy - 28), (cx - 38, cy - 26),
                  (cx - 30, cy - 4)], fill=color)
    # cockpit
    draw.ellipse([cx + 18, cy - 5, cx + 34, cy + 5], fill=(210, 230, 240))
    # warning triangle
    tx, ty = x + s - 26, y + 18
    draw.polygon([(tx, ty - 14), (tx + 15, ty + 12), (tx - 15, ty + 12)],
                 fill=AMBER, outline=INK)
    draw.text((tx - 2, ty - 8), "!", font=font(SANS_BOLD, 18), fill=INK)


def icon_candle(draw, x, y, s, color=PURPLE):
    """A lit candle (UN femicide report: five women killed every hour)."""
    cx = x + s // 2
    # flame
    draw.polygon([(cx, y + 8), (cx + 13, y + 34), (cx + 5, y + 44),
                  (cx - 5, y + 44), (cx - 13, y + 34)], fill=AMBER)
    draw.ellipse([cx - 5, y + 30, cx + 5, y + 42], fill=(232, 120, 32))
    # wick
    draw.line([cx, y + 44, cx, y + 52], fill=INK, width=4)
    # candle body
    draw.rounded_rectangle([cx - 20, y + 52, cx + 20, y + s - 26], radius=8,
                           fill=color)
    # drips
    draw.ellipse([cx - 20, y + 52, cx - 8, y + 70], fill=color)
    draw.ellipse([cx + 10, y + 52, cx + 20, y + 66], fill=color)
    # saucer
    draw.ellipse([cx - 34, y + s - 30, cx + 34, y + s - 16], fill=(210, 205, 180))
    draw.ellipse([cx - 34, y + s - 30, cx + 34, y + s - 16],
                 outline=INK, width=3)
    # small heart
    hx, hy = x + s - 30, y + s - 30
    draw.ellipse([hx - 9, hy - 6, hx + 1, hy + 4], fill=RED)
    draw.ellipse([hx - 1, hy - 6, hx + 9, hy + 4], fill=RED)
    draw.polygon([(hx - 9, hy), (hx + 9, hy), (hx, hy + 11)], fill=RED)


def icon_scales(draw, x, y, s, color=TEAL):
    """Scales of justice (ICJ Rohingya genocide ruling recognised)."""
    cx = x + s // 2
    # base and post
    draw.rectangle([cx - 26, y + s - 26, cx + 26, y + s - 16], fill=color)
    draw.line([cx, y + 22, cx, y + s - 26], fill=color, width=7)
    # finial
    draw.ellipse([cx - 6, y + 12, cx + 6, y + 24], fill=color)
    # beam
    draw.line([cx - 52, y + 34, cx + 52, y + 34], fill=color, width=7)
    for side in (-1, 1):
        px = cx + side * 52
        # chains
        draw.line([px, y + 34, px - 16, y + 66], fill=color, width=3)
        draw.line([px, y + 34, px + 16, y + 66], fill=color, width=3)
        draw.line([px, y + 34, px, y + 66], fill=color, width=3)
        # pan
        draw.pieslice([px - 18, y + 58, px + 18, y + 86], 0, 180, fill=color)
        draw.line([px - 18, y + 72, px + 18, y + 72], fill=color, width=4)
    # globe in the middle bottom
    draw.ellipse([cx - 12, y + s - 52, cx + 12, y + s - 28],
                 outline=color, width=4)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead
    d.text((M, 26), "THE WORLD IN ONE IMAGE", font=font(SANS_BOLD, 22), fill=GREY)
    tag = "TUESDAY"
    d.text((W - M - d.textlength(tag, font=font(SANS_BOLD, 22)), 26), tag,
           font=font(SANS_BOLD, 22), fill=GREY)
    d.line([M, 58, W - M, 58], fill=RULE, width=2)
    date_f = font(SERIF_BOLD, 62)
    date = "24 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 66), date, font=date_f, fill=INK)
    d.line([M, 142, W - M, 142], fill=RULE, width=5)
    d.line([M, 150, W - M, 150], fill=RED, width=2)

    # ---- lead story: Zaporizhzhia
    lx, ly = M, 172
    lw = 600
    d.text((lx, ly), "WAR  ·  UKRAINE", font=font(SANS_BOLD, 23), fill=RED)
    y = ly + 34
    head_f = font(SERIF_BOLD, 62)
    for ln in ["RUSSIA HITS", "ZAPORIZHZHIA"]:
        d.text((lx, y), ln, font=head_f, fill=INK)
        y += 70
    y += 6
    y = draw_text_block(d, lx, y,
                        "Overnight strike kills 2 and wounds about 40, "
                        "including children, as a house is destroyed and a "
                        "five-storey apartment block is hit.",
                        font(SANS, 26), lw, INK)
    # lead illustration panel
    px0, py0, px1, py1 = 672, 172, W - M, 440
    d.rounded_rectangle([px0, py0, px1, py1], radius=14, fill=PANEL)
    icon_building_hit(d, px0 + 63, py0 + 12, 190)
    cap_f = font(SANS_BOLD, 21)
    cap = "2 DEAD, 40 HURT"
    d.text((px0 + (px1 - px0 - d.textlength(cap, font=cap_f)) / 2, py1 - 38),
           cap, font=cap_f, fill=NAVY)

    # ---- divider
    d.line([M, 466, W - M, 466], fill=RULE, width=3)

    # ---- secondary grid 2x2
    cells = [
        ("TECH  ·  USA", "Two states sue SpaceX over Grok deepfakes",
         "Virginia and Oregon say the chatbot made sexual images, including of children.",
         icon_gavel, DARKRED),
        ("ASIA  ·  KOREA", "North Korean jet enters South Korean airspace",
         "Island residents ordered to shelters near Ulleung.",
         icon_jet, NAVY),
        ("UN  ·  WOMEN", "Five women killed every hour, UN says",
         "47,000 women and girls were killed by a partner or family member last year.",
         icon_candle, PURPLE),
        ("LAW  ·  THE HAGUE", "14 nations back ICJ Rohingya ruling",
         "UK, Canada, Spain and others recognise the court's genocide finding on Myanmar.",
         icon_scales, TEAL),
    ]
    gx, gy = M, 482
    cw, chh, gap = 468, 164, 10
    for i, (kicker, head, summ, icon, color) in enumerate(cells):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (chh + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + chh], radius=12,
                            outline=(210, 203, 186), width=2)
        icon(d, cx + 12, cy + 20, 124, color)
        tx = cx + 150
        d.text((tx, cy + 12), kicker, font=font(SANS_BOLD, 19), fill=color)
        y = draw_text_block(d, tx, cy + 36, head, font(SANS_BOLD, 22), cw - 162, INK,
                            leading=1.12)
        draw_text_block(d, tx, y + 4, summ, font(SANS, 20), cw - 162, (60, 60, 60),
                        leading=1.18)

    # ---- also today strip
    ay = 832
    d.line([M, ay, W - M, ay], fill=RULE, width=3)
    d.text((M, ay + 12), "ALSO TODAY", font=font(SANS_BOLD, 21), fill=RED)
    also = [
        "COP31 autopsy: first climate summit since 2009 to end with no deal",
        "Colombia marks 10 years since its peace deal",
        "5.6 quake hits Nepal near the China border",
        "US, Mexico, Costa Rica and Jamaica to host the 2031 Women's World Cup",
    ]
    ayy = ay + 44
    for i, item in enumerate(also):
        ix = M + (i % 2) * 476
        iy = ayy + (i // 2) * 56
        d.ellipse([ix, iy + 8, ix + 9, iy + 17], fill=RED)
        draw_text_block(d, ix + 18, iy, item, font(SANS, 21), 440, INK, leading=1.1)

    # ---- footer
    d.line([M, 986, W - M, 986], fill=(210, 203, 186), width=2)
    foot = "All stories reported on Tuesday 24 November 2026  ·  Sources: AP, Reuters, Al Jazeera, UN News"
    ff = font(SANS, 19)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 992), foot, font=ff, fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {img.size} {size} bytes (limit 1048576)")


if __name__ == "__main__":
    main()
