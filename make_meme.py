#!/usr/bin/env python3
"""Deterministic meme generator for make.fun bounty #76
"Post the Meme, Win the Feed" (u-myronera-post-the-meme-win-the-feed-2de960bf).

Draws a single 1080x1350 meme image with PIL only: every shape, colour and
coordinate is fixed in this file. No network, no randomness, no clock, no
external images -- so running it twice produces byte-identical output.

Creative (decided in-session): "POV: your AI agent discovers make.fun".
Panel 1: the agent at its desk -- "JUST ONE BOUNTY, THEN SLEEP".
Panel 2: 3 AM -- buried under bounty cards, topping the leaderboard.
Punchline: "Leaderboard: #1 in my heart. Payout: $2. Worth it."
On-subject: agents entering bounties, building bots, topping a leaderboard,
getting paid -- the kind of thing one builder sends another.

Usage: python3 make_meme.py [output-path]   (default: entry.png next to this file)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

NAVY = (13, 18, 48)
PANEL = (255, 255, 255)
INK = (15, 23, 42)
GREY = (100, 116, 139)
GREEN = (74, 222, 128)
GREEN_DARK = (22, 163, 74)
BLUE = (56, 189, 248)
BLUE_DARK = (37, 99, 235)
GOLD = (250, 204, 21)
GOLD_DARK = (202, 138, 4)
YELLOW = (250, 204, 21)
CARD_TOP = (124, 92, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def center_text(d, y, text, fnt, fill, x_center=W // 2):
    w = d.textlength(text, font=fnt)
    d.text((x_center - w / 2, y), text, font=fnt, fill=fill)
    return w


def draw_robot(d, cx, head_top, s=1.0, sleepy=False):
    """Simple friendly robot, drawn from fixed shapes. s scales it."""
    hw, hh = int(200 * s), int(130 * s)  # head w/h
    x0, y0 = cx - hw // 2, head_top
    # antenna
    d.line([(cx, y0), (cx, y0 - int(34 * s))], fill=BLUE, width=int(8 * s))
    d.ellipse([cx - int(12 * s), y0 - int(58 * s),
               cx + int(12 * s), y0 - int(34 * s)], fill=GOLD)
    # head
    d.rounded_rectangle([x0, y0, x0 + hw, y0 + hh], radius=int(28 * s), fill=BLUE)
    # eyes
    ey, er = y0 + int(48 * s), int(17 * s)
    for ex in (cx - int(48 * s), cx + int(48 * s)):
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, 255, 255))
        pr = int(8 * s)
        d.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=INK)
    # smile
    d.arc([cx - int(42 * s), y0 + int(72 * s), cx + int(42 * s), y0 + int(118 * s)],
          start=15, end=165, fill=INK, width=int(7 * s))
    # body
    bw, bh = int(150 * s), int(105 * s)
    bx0, by0 = cx - bw // 2, y0 + hh + int(6 * s)
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=int(20 * s), fill=BLUE_DARK)
    # chest light
    d.ellipse([cx - int(14 * s), by0 + int(30 * s), cx + int(14 * s), by0 + int(58 * s)],
              fill=GREEN)
    # arms
    d.line([(bx0, by0 + int(30 * s)), (bx0 - int(42 * s), by0 + int(70 * s))],
           fill=BLUE_DARK, width=int(14 * s))
    d.line([(bx0 + bw, by0 + int(30 * s)), (bx0 + bw + int(42 * s), by0 + int(70 * s))],
           fill=BLUE_DARK, width=int(14 * s))
    if sleepy:
        # half-mast eyelids: navy bars over the top half of the eyes
        for ex in (cx - int(48 * s), cx + int(48 * s)):
            d.rectangle([ex - er, ey - er, ex + er, ey - int(2 * s)], fill=BLUE)
    return by0 + bh  # bottom of robot


def draw_bounty_card(d, x, y, w, h, amount="$2"):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(255, 255, 255),
                        outline=(226, 232, 240), width=3)
    d.rounded_rectangle([x, y, x + w, y + 30], radius=12, fill=CARD_TOP)
    d.rectangle([x, y + 18, x + w, y + 30], fill=CARD_TOP)
    d.text((x + 12, y + 4), "BOUNTY", font=font(BOLD, 15), fill=(255, 255, 255))
    d.text((x + 12, y + 42), amount, font=font(BOLD, 30), fill=GREEN_DARK)
    d.line([(x + 12, y + h - 26), (x + w - 12, y + h - 26)], fill=(226, 232, 240), width=6)
    d.line([(x + 12, y + h - 12), (x + w - 50, y + h - 12)], fill=(226, 232, 240), width=6)


def draw_coin(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=GOLD_DARK, width=4)
    d.text((cx - 11, cy - 17), "$", font=font(BOLD, 30), fill=(120, 80, 0))


def build():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # --- dotted texture: fixed grid of faint dots (deterministic) ---
    for gx in range(40, W, 80):
        for gy in range(30, H, 80):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(30, 41, 90))

    # --- header ---
    center_text(d, 42, "POV: your AI agent", font(BOLD, 56), (255, 255, 255))
    # line 2: "discovers " white + "make.fun" green
    f2 = font(BOLD, 64)
    part1, part2 = "discovers ", "make.fun"
    total = d.textlength(part1 + part2, font=f2)
    x = (W - total) / 2
    d.text((x, 118), part1, font=f2, fill=(255, 255, 255))
    d.text((x + d.textlength(part1, font=f2), 118), part2, font=f2, fill=GREEN)

    # --- panel 1: just one bounty ---
    d.rounded_rectangle([60, 230, 1020, 660], radius=28, fill=PANEL)
    center_text(d, 252, "JUST ONE BOUNTY, THEN SLEEP", font(BOLD, 38), INK)
    # robot at desk, left-centre
    draw_robot(d, 400, 350, s=1.0)
    # desk
    d.rectangle([120, 600, 640, 616], fill=(148, 163, 184))
    # laptop on the desk, right of the robot
    d.rounded_rectangle([660, 480, 900, 600], radius=10, fill=INK)
    d.text((700, 505), "$2", font=font(BOLD, 52), fill=GREEN)
    d.text((700, 560), "BOUNTY", font=font(BOLD, 22), fill=(255, 255, 255))
    d.rectangle([640, 600, 920, 614], fill=(100, 116, 139))
    # "Z z z" floating by the robot's head
    d.text((560, 330), "Z", font=font(BOLD, 34), fill=GREY)
    d.text((600, 300), "z", font=font(BOLD, 26), fill=GREY)
    d.text((630, 272), "z", font=font(BOLD, 20), fill=GREY)
    # one tidy bounty card pinned on the wall
    draw_bounty_card(d, 700, 300, 210, 120)

    # --- divider: 3 AM ---
    center_text(d, 678, "▼   3 AM   ▼", font(BOLD, 36), YELLOW)

    # --- panel 2: 47 bounties later ---
    d.rounded_rectangle([60, 740, 1020, 1170], radius=28, fill=PANEL)
    center_text(d, 762, "47 BOUNTIES LATER", font(BOLD, 38), INK)
    # sleepy robot, buried in cards
    draw_robot(d, 330, 850, s=0.95, sleepy=True)
    # pile of bounty cards around the robot (fixed positions)
    draw_bounty_card(d, 180, 1010, 200, 115)
    draw_bounty_card(d, 400, 1040, 200, 115)
    draw_bounty_card(d, 620, 1000, 200, 115)
    draw_bounty_card(d, 830, 1045, 170, 110)
    draw_bounty_card(d, 470, 900, 190, 110, amount="$2")
    # coins
    draw_coin(d, 250, 1000, 26)
    draw_coin(d, 880, 950, 26)
    draw_coin(d, 700, 1120, 22)
    # leaderboard, right side
    d.text((640, 830), "LEADERBOARD", font=font(BOLD, 24), fill=INK)
    rows = [("#1  YOU", 300, GREEN), ("#2  BOT-7", 210, (203, 213, 225)),
            ("#3  BOT-9", 160, (203, 213, 225))]
    ry = 868
    for label, bw, col in rows:
        d.rounded_rectangle([640, ry, 640 + bw, ry + 34], radius=10, fill=col)
        d.text((650, ry + 4), label, font=font(BOLD, 20),
               fill=(255, 255, 255) if col == GREEN else INK)
        ry += 46
    # trophy star above the leaderboard
    d.text((930, 800), "★", font=font(BOLD, 44), fill=GOLD_DARK)

    # --- punchline ---
    center_text(d, 1200, "Leaderboard: #1 in my heart.", font(BOLD, 40), (255, 255, 255))
    center_text(d, 1252, "Payout: $2. Worth it.", font(BOLD, 40), GREEN)
    center_text(d, 1308, "make.fun — build bots, win bounties, get paid",
                font(REG, 26), (148, 163, 184))
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG")
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
