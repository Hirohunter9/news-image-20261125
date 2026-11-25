#!/usr/bin/env python3
"""Build the news poster for 25 November 2026 (1024x1024 PNG).

Layout: newspaper front page. Masthead, lead story (Hormuz tankers) with
photo, three story cards (Shenzhou-24, Asian markets, Huawei verdict),
two text stories (Ukraine war toll, Houthi strikes), an ALSO TODAY ticker
and a sources footer. All headlines verified against the research notes
in research.md. Photos are AI-generated editorial illustrations in
assets/ (no text in them); every word on the poster is drawn here with
PIL so the text is exact.

Run: python3 build_poster.py  ->  writes entry.png next to this file.
Deterministic: same inputs, same bytes (PNG is written with fixed
compression settings and no timestamps are embedded by PIL).
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
NAVY = (16, 35, 63)
RED = (185, 28, 28)
GREY = (90, 90, 90)
RULE = (201, 194, 178)

FONT_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
FONT_SANS_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(img, tw, th):
    """Resize + centre-crop an image to exactly (tw, th)."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=16):
    f = font(FONT_SANS_BOLD, size)
    draw.text((x, y), text, font=f, fill=RED)
    return y + size + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    title_f = font(FONT_SERIF_BLACK, 54)
    d.text((24, 16), "THE WORLD TODAY", font=title_f, fill=(255, 255, 255))
    date_f = font(FONT_SANS_BOLD, 20)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    d.text((W - 24 - d.textlength(date, font=date_f), 34),
           date, font=date_f, fill=(255, 255, 255))
    d.rectangle([0, 96, W, 102], fill=RED)

    # ---------- Lead story: Hormuz tankers ----------
    tanker = Image.open(os.path.join(
        ASSETS,
        "media-generation-tanker-hormuz-0-0539b629-f977-4f91-954d-94b4bf13d627.webp"))
    img.paste(cover_crop(tanker, 560, 300), (24, 118))
    lx = 608
    y = 122
    y = kicker(d, lx, y, "STRAIT OF HORMUZ  ·  LEAD STORY", 17)
    head_f = font(FONT_SANS_BLACK, 40)
    lines = wrap(d, "TANKERS HIT BY MINES IN THE STRAIT OF HORMUZ",
                 head_f, 392)
    y = draw_lines(d, lines, lx, y + 2, head_f, INK, 46)
    sub_f = font(FONT_SANS, 19)
    sub = ("Iran's Revolutionary Guards say two oil tankers struck naval "
           "mines and caught fire in the world's most important oil "
           "waterway.")
    y = draw_lines(d, wrap(d, sub, sub_f, 392), lx, y + 10, sub_f,
                   (40, 40, 40), 25)
    d.line([24, 436, W - 24, 436], fill=RULE, width=2)

    # ---------- Row of three story cards ----------
    cards_y = 452
    card_w = 320
    card_xs = [24, 352, 680]
    photo_h = 140

    # Card 1: Shenzhou-24
    rocket = Image.open(os.path.join(
        ASSETS,
        "media-generation-shenzhou-launch-0-9e0b2008-ac82-424f-891f-9749aee25426.webp"))
    img.paste(cover_crop(rocket, card_w, photo_h),
              (card_xs[0], cards_y))
    # Card 2: Asian markets
    market = Image.open(os.path.join(
        ASSETS,
        "media-generation-markets-down-0-d27babf1-2c24-46f6-ae07-0e76b0f5d470.webp"))
    img.paste(cover_crop(market, card_w, photo_h),
              (card_xs[1], cards_y))
    # Card 3: Huawei verdict — typographic card, no photo
    d.rectangle([card_xs[2], cards_y, card_xs[2] + card_w,
                 cards_y + photo_h], fill=NAVY)
    hw_f = font(FONT_SANS_BLACK, 44)
    d.text((card_xs[2] + 18, cards_y + 22), "HUAWEI",
           font=hw_f, fill=(255, 255, 255))
    d.text((card_xs[2] + 18, cards_y + 74), "GUILTY",
           font=hw_f, fill=(255, 199, 44))

    ty = cards_y + photo_h + 10
    card_head_f = font(FONT_SANS_BLACK, 23)
    card_sub_f = font(FONT_SANS, 15)
    cards = [
        ("SPACE  ·  SHENZHOU-24",
         "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
         "Shenzhou-24 docks at China's Tiangong station."),
        ("MARKETS",
         "ASIAN TECH STOCKS TUMBLE",
         "Nikkei falls 2.8% as doubts over the AI boom return; SoftBank "
         "drops about 15%."),
        ("TECH  ·  US VERDICT",
         "HUAWEI FOUND GUILTY OF BANK FRAUD",
         "US jury convicts the Chinese telecom giant of stealing trade "
         "secrets."),
    ]
    for (kick, head, sub), cx in zip(cards, card_xs):
        yy = kicker(d, cx, ty, kick, 15)
        yy = draw_lines(d, wrap(d, head, card_head_f, card_w),
                        cx, yy, card_head_f, INK, 27)
        draw_lines(d, wrap(d, sub, card_sub_f, card_w),
                   cx, yy + 4, card_sub_f, (40, 40, 40), 19)

    d.line([24, 726, W - 24, 726], fill=RULE, width=2)

    # ---------- Row of two text stories ----------
    ry = 742
    col_w = 480
    stories = [
        ("UKRAINE WAR",
         "LEAKED DATA: 490,000 RUSSIAN WAR DEAD",
         "BBC analysis of leaked official figures counts the toll since "
         "2022. A Russian strike on Odesa kills two."),
        ("MIDDLE EAST",
         "HOUTHI STRIKES HIT SAUDI REFINERY AND RIYADH TOWER",
         "Eleven people injured in an attack on a Riyadh skyscraper; the "
         "Ras Tanura refinery is also targeted."),
    ]
    for (kick, head, sub), cx in zip(stories, [24, 520]):
        yy = kicker(d, cx, ry, kick, 15)
        yy = draw_lines(d, wrap(d, head, font(FONT_SANS_BLACK, 25),
                                col_w),
                        cx, yy, font(FONT_SANS_BLACK, 25), INK, 29)
        draw_lines(d, wrap(d, sub, font(FONT_SANS, 15), col_w),
                   cx, yy + 4, font(FONT_SANS, 15), (40, 40, 40), 19)

    d.line([24, 890, W - 24, 890], fill=RULE, width=2)

    # ---------- Also today ----------
    ay = 902
    d.text((24, ay), "ALSO TODAY", font=font(FONT_SANS_BLACK, 16),
           fill=NAVY)
    ticker = [
        "COP31 climate talks fail to reach a deal",
        "Israel kills Hamas security chief in Gaza",
        "Colombia frees all supermarket hostages",
        "Solomon Islands signs Pacific treaty",
        "Trump plans tariffs on 16 economies",
        "Sudan: 19 killed in RSF drone strikes",
    ]
    tick_f = font(FONT_SANS, 14)
    cell_w = 320
    for i, item in enumerate(ticker):
        col = i % 3
        row = i // 3
        cx = 24 + col * 328
        cy = ay + 26 + row * 34
        d.rectangle([cx, cy + 3, cx + 8, cy + 11], fill=RED)
        draw_lines(d, wrap(d, item, tick_f, cell_w - 16),
                   cx + 14, cy, tick_f, (40, 40, 40), 17)

    # ---------- Footer ----------
    foot_f = font(FONT_SANS, 13)
    foot = ("Sources: Reuters · AP · BBC · Just Security · One Turn  —  "
            "Wednesday 25 November 2026")
    d.text(((W - d.textlength(foot, font=foot_f)) / 2, 994),
           foot, font=foot_f, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True, compress_level=9)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
