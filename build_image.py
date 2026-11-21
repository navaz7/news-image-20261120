#!/usr/bin/env python3
"""Compose entry.png - a newspaper front page for Friday 20 November 2026.

THE WORLD TODAY: hero is the contrast of the day - the Shenzhen
Trump-Xi-Putin peace declaration followed within hours by one of the
largest Russian missile and drone attacks of the war on Kyiv.
Below it: the ICJ Myanmar genocide verdict and Myanmar's Friday
reaction, Cyclone Akvan's landfall at Gopalpur, Anthropic's slide
after its record IPO, and Voyager 1 phoning home from one light-day.
All artwork is drawn with Pillow shapes - no external images.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN

CREAM = (244, 236, 216)
PAPER = (250, 246, 235)
NAVY = (20, 33, 61)
NAVY2 = (32, 52, 92)
CRIMSON = (179, 32, 44)
GOLD = (198, 156, 42)
ORANGE = (232, 119, 34)
SKY = (16, 24, 48)
GREY = (92, 98, 110)
WHITE = (255, 255, 255)
BLACK = (10, 10, 14)
YELLOW = (250, 205, 40)
CHINA_RED = (222, 41, 16)
RUSSIA_BLUE = (0, 57, 166)

FD = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = str(FD / "DejaVuSerif-Bold.ttf")
SANS_B = str(FD / "DejaVuSans-Bold.ttf")
SANS = str(FD / "DejaVuSans.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textlength(s, font=f)


def fit_line(d, s, path, max_w, start, minimum=11):
    size = start
    while size > minimum:
        f = F(path, size)
        if tw(d, s, f) <= max_w:
            return f
        size -= 1
    return F(path, minimum)


def wrap(d, s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_wrap(d, s, path, max_w, max_lines, start, minimum=11):
    size = start
    while size > minimum:
        f = F(path, size)
        lines = wrap(d, s, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = F(path, minimum)
    return f, wrap(d, s, f, max_w)[:max_lines]


def lh(f, ratio=1.22):
    return int(f.size * ratio)


def draw_lines(d, lines, f, x, y, fill, ratio=1.22, cx=None):
    step = lh(f, ratio)
    for ln in lines:
        tx = x if cx is None else cx - tw(d, ln, f) / 2
        d.text((tx, y), ln, font=f, fill=fill)
        y += step
    return y


def tracked(d, s, f, cx, y, fill, gap=3):
    widths = [tw(d, ch, f) for ch in s]
    total = sum(widths) + gap * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += wch + gap
    return y + lh(f, 1.15)


# ---------- drawn graphics ----------

def flag_usa(d, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        col = CRIMSON if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=col)
    d.rectangle([x, y, x + w * 0.45, y + stripe * 4], fill=NAVY2)
    sf = F(SANS_B, 9)
    for r in range(3):
        for c in range(4):
            d.text((x + 4 + c * 11, y + 2 + r * 9), "*", font=sf, fill=WHITE)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=BLACK, width=1)


def flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CHINA_RED)
    sf = F(SANS_B, 16)
    d.text((x + 7, y + 4), "*", font=sf, fill=YELLOW)
    sf2 = F(SANS_B, 9)
    for dx, dy in [(30, 4), (34, 14), (30, 24), (24, 32)]:
        d.text((x + dx, y + dy), "*", font=sf2, fill=YELLOW)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=BLACK, width=1)


def flag_russia(d, x, y, w, h):
    third = h / 3
    d.rectangle([x, y, x + w, y + third], fill=WHITE)
    d.rectangle([x, y + third, x + w, y + 2 * third], fill=RUSSIA_BLUE)
    d.rectangle([x, y + 2 * third, x + w, y + h], fill=CRIMSON)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=BLACK, width=1)


def hero_graphic(page, d, x, y, w, h):
    # Left: Shenzhen summit - three flags over a round table
    left_w = int(w * 0.56)
    d.rectangle([x, y, x + left_w, y + h], fill=NAVY2)
    fw, fh, gap = 118, 62, 22
    total = fw * 3 + gap * 2
    fx = x + (left_w - total) // 2
    fy = y + 20
    flag_usa(d, fx, fy, fw, fh)
    flag_china(d, fx + fw + gap, fy, fw, fh)
    flag_russia(d, fx + 2 * (fw + gap), fy, fw, fh)
    lf = F(SANS_B, 13)
    for i, lab in enumerate(["USA", "CHINA", "RUSSIA"]):
        lx = fx + i * (fw + gap)
        d.text((lx + fw / 2 - tw(d, lab, lf) / 2, fy + fh + 5), lab, font=lf, fill=CREAM)
    # round table
    d.ellipse([x + left_w / 2 - 112, y + h - 52, x + left_w / 2 + 112, y + h - 14],
              fill=GOLD, outline=CREAM, width=2)
    tf = F(SANS_B, 13)
    label = "SHENZHEN SUMMIT"
    d.text((x + left_w / 2 - tw(d, label, tf) / 2, y + h - 44), label, font=tf, fill=NAVY)

    # Right: Kyiv at dawn under fire
    rx = x + left_w
    rw = w - left_w
    d.rectangle([rx, y, x + w, y + h], fill=SKY)
    # missile trails
    for i, sx in enumerate([rx + 30, rx + 110, rx + 210, rx + 300]):
        d.line([(sx, y + 8), (sx + 52, y + 74 + i * 9)], fill=ORANGE, width=3)
        d.line([(sx + 6, y + 8), (sx + 58, y + 74 + i * 9)], fill=YELLOW, width=1)
    # explosion bursts
    for cx0, cy0, r in [(rx + 92, y + 92, 20), (rx + 238, y + 104, 26), (rx + 330, y + 84, 15)]:
        for ang in range(0, 360, 30):
            ex = cx0 + r * math.cos(math.radians(ang))
            ey = cy0 + r * math.sin(math.radians(ang))
            d.line([(cx0, cy0), (ex, ey)], fill=ORANGE, width=3)
        d.ellipse([cx0 - 7, cy0 - 7, cx0 + 7, cy0 + 7], fill=YELLOW)
    # skyline: blocks + a gold-domed cathedral
    base = y + h
    for bx, bw, bh in [(rx + 6, 52, 58), (rx + 64, 40, 82), (rx + 238, 56, 66),
                       (rx + 300, 44, 88), (rx + 350, 52, 54)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=BLACK)
        for wy in range(base - bh + 8, base - 10, 16):
            for wx in range(bx + 6, bx + bw - 6, 13):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=YELLOW)
    d.rectangle([rx + 150, base - 74, rx + 196, base], fill=BLACK)
    d.polygon([(rx + 150, base - 74), (rx + 173, base - 98), (rx + 196, base - 74)], fill=BLACK)
    d.ellipse([rx + 160, base - 112, rx + 186, base - 88], fill=GOLD)
    d.line([(rx + 173, base - 124), (rx + 173, base - 106)], fill=GOLD, width=3)
    kf = F(SANS_B, 14)
    klabel = "KYIV - FRIDAY"
    d.rectangle([rx + 10, y + 10, rx + 10 + tw(d, klabel, kf) + 14, y + 36], fill=CRIMSON)
    d.text((rx + 17, y + 15), klabel, font=kf, fill=WHITE)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=NAVY, width=2)
    d.line([(rx, y), (rx, y + h)], fill=CRIMSON, width=4)


def strip_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx0 = x + w // 2
    d.line([(cx0, y + 10), (cx0, y + h - 12)], fill=GOLD, width=4)
    d.line([(cx0 - 58, y + 20), (cx0 + 58, y + 20)], fill=GOLD, width=3)
    for side in (-1, 1):
        px = cx0 + side * 58
        d.polygon([(px, y + 20), (px - 20, y + 44), (px + 20, y + 44)], outline=CREAM, fill=None)
        d.arc([px - 20, y + 34, px + 20, y + 54], 0, 180, fill=CREAM, width=3)
    d.ellipse([cx0 - 6, y + 4, cx0 + 6, y + 16], fill=CRIMSON)


def strip_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 74, 110))
    cx0, cy0 = x + w // 2, y + h // 2
    for r, start in [(30, 20), (21, 200), (13, 80)]:
        d.arc([cx0 - r, cy0 - r, cx0 + r, cy0 + r], start, start + 270, fill=WHITE, width=4)
    d.ellipse([cx0 - 5, cy0 - 5, cx0 + 5, cy0 + 5], fill=YELLOW)
    # rain streaks
    for i in range(9):
        rx = x + 22 + i * 48
        d.line([(rx, y + h - 16), (rx - 9, y + h - 4)], fill=(150, 200, 235), width=3)


def strip_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 22, 30))
    pts = [(x + 18, y + 14), (x + 78, y + 10), (x + 128, y + 26),
           (x + 188, y + 20), (x + 248, y + 42), (x + 308, y + 38), (x + 368, y + 58),
           (x + 428, y + 64)]
    d.line(pts, fill=CRIMSON, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE)
    cf = F(SANS_B, 15)
    d.text((x + 16, y + h - 24), "ANT  $111.50 -> $88.91", font=cf, fill=YELLOW)


def strip_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    import random
    rng = random.Random(20)
    for _ in range(46):
        sx = rng.randint(x + 4, x + w - 4)
        sy = rng.randint(y + 4, y + h - 4)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    # Earth, signal arc, probe
    d.ellipse([x + 18, y + h - 42, x + 54, y + h - 6], fill=(64, 130, 200), outline=WHITE, width=1)
    d.arc([x + 30, y + 6, x + w - 60, y + h + 30], 200, 320, fill=GOLD, width=3)
    px, py = x + w - 92, y + 16
    d.ellipse([px, py, px + 30, py + 18], fill=GREY, outline=WHITE, width=1)
    d.rectangle([px + 30, py + 6, px + 58, py + 11], fill=GOLD)
    sf = F(SANS_B, 13)
    d.text((x + 62, y + h - 26), "1 LIGHT-DAY", font=sf, fill=CREAM)


STRIPS = {
    "scales": strip_scales,
    "cyclone": strip_cyclone,
    "chart": strip_chart,
    "space": strip_space,
}


def story_panel(d, x, y, w, row_h, kind, kicker, headline, sub):
    strip_h = 64
    STRIPS[kind](d, x, y, w, strip_h)
    d.rectangle([x, y, x + w - 1, y + strip_h - 1], outline=NAVY, width=2)
    cy = y + strip_h + 7
    kf = F(SANS_B, 13)
    d.text((x, cy), kicker, font=kf, fill=CRIMSON)
    cy += lh(kf, 1.1) + 2
    hf, hlines = fit_wrap(d, headline, SERIF_B, w, 2, 25, 18)
    cy = draw_lines(d, hlines, hf, x, cy, NAVY, ratio=1.16)
    sf, slines = fit_wrap(d, sub, SANS, w, 2, 15, 12)
    draw_lines(d, slines, sf, x, cy + 2, NAVY, ratio=1.18)


def main():
    page = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(page)
    cx = W // 2

    # Masthead
    d.line([(MARGIN, 24), (W - MARGIN, 24)], fill=NAVY, width=2)
    mf = fit_line(d, "THE WORLD TODAY", SERIF_B, CW, 104)
    y = 34
    d.text((cx - tw(d, "THE WORLD TODAY", mf) / 2, y), "THE WORLD TODAY", font=mf, fill=NAVY)
    y += lh(mf, 1.02)
    d.rectangle([MARGIN, y + 2, W - MARGIN, y + 8], fill=CRIMSON)
    y += 15
    df = fit_line(d, "FRIDAY - 20 NOVEMBER 2026", SANS_B, CW - 60, 34)
    y = tracked(d, "FRIDAY \u00b7 20 NOVEMBER 2026", df, cx, y, NAVY, gap=3)
    d.line([(MARGIN, y + 2), (W - MARGIN, y + 2)], fill=NAVY, width=2)
    y += 13

    # Hero graphic + headline
    hero_h = 176
    hero_graphic(page, d, MARGIN, y, CW, hero_h)
    y += hero_h + 11
    hf = fit_line(d, "PEACE PLEDGE, THEN FIRE OVER KYIV", SERIF_B, CW, 47)
    d.text((cx - tw(d, "PEACE PLEDGE, THEN FIRE OVER KYIV", hf) / 2, y),
           "PEACE PLEDGE, THEN FIRE OVER KYIV", font=hf, fill=NAVY)
    y += lh(hf, 1.05) + 3
    hero_sub = ("Hours after Trump, Xi and Putin hail their Shenzhen peace declaration, "
                "Russia fires 110 missiles and 400 drones at Ukraine - 8 killed, "
                "Kyiv bridges, power grid and embassies hit")
    sf, slines = fit_wrap(d, hero_sub, SANS_B, CW, 2, 21, 14)
    y = draw_lines(d, slines, sf, 0, y, NAVY, ratio=1.18, cx=cx)
    y += 7
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=NAVY, width=2)
    y += 12

    # Story grid: 2 x 2
    ticker_h = 108
    rows_top = y
    row_h = (H - ticker_h - rows_top - 16) // 2
    col_w = (CW - 44) // 2
    col2_x = MARGIN + col_w + 44
    div_x = MARGIN + col_w + 22

    story_panel(d, MARGIN, rows_top, col_w, row_h, "scales",
                "WORLD COURT \u00b7 THE HAGUE",
                "MYANMAR RULED GUILTY OF GENOCIDE",
                "ICJ's first-ever genocide verdict over the Rohingya. "
                "Myanmar calls it 'unfair'; court orders reparations")
    story_panel(d, col2_x, rows_top, col_w, row_h, "cyclone",
                "WEATHER \u00b7 INDIA",
                "CYCLONE AKVAN HITS GOPALPUR",
                "Landfall at dawn, 70-90 km/h winds. 3.7 lakh evacuated, "
                "423 rescue teams - no major loss of life")
    d.line([(div_x, rows_top + 4), (div_x, rows_top + row_h - 6)], fill=NAVY, width=1)

    row2_y = rows_top + row_h + 16
    d.line([(MARGIN, row2_y - 9), (W - MARGIN, row2_y - 9)], fill=NAVY, width=1)
    story_panel(d, MARGIN, row2_y, col_w, row_h, "chart",
                "MARKETS \u00b7 TECH",
                "ANTHROPIC SLIDES AFTER RECORD IPO",
                "Claude maker falls 8.5% Friday to $88.91, nearly erasing "
                "its debut pop after the $81.3bn record IPO")
    story_panel(d, col2_x, row2_y, col_w, row_h, "space",
                "SPACE \u00b7 NASA",
                "VOYAGER 1 PHONES HOME, 1 LIGHT-DAY AWAY",
                "Signal took a full 24 hours from 16 billion miles. "
                "Launched 1977; science data paused since 14 Nov")
    d.line([(div_x, row2_y + 4), (div_x, row2_y + row_h - 6)], fill=NAVY, width=1)

    # Ticker
    ty = H - ticker_h
    d.rectangle([0, ty, W, H], fill=NAVY)
    d.rectangle([0, ty, W, ty + 5], fill=CRIMSON)
    ticker = ("IN BRIEF - Modi opens first SCO Civilisational Dialogue Forum in New Delhi, "
              "Pakistan minister attends \u00b7 France seeks UN Security Council meeting after Kyiv "
              "strikes \u00b7 India A thrash Nepal by 306 runs, Tilak Varma hits a century \u00b7 "
              "Gold slides for a 9th day")
    tf, tlines = fit_wrap(d, ticker, SANS_B, CW, 3, 19, 13)
    total_h = lh(tf, 1.25) * len(tlines)
    draw_lines(d, tlines, tf, MARGIN, ty + (ticker_h - total_h) // 2 + 2, CREAM, ratio=1.25)

    page.save(OUT, optimize=True)
    size = OUT.stat().st_size
    print(f"saved {OUT} {page.size} {size} bytes")
    if size > 1024 * 1024:
        q = page.quantize(colors=256, method=Image.MEDIANCUT)
        q.save(OUT, optimize=True)
        print(f"quantized -> {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
