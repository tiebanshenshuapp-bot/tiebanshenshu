#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成品牌视觉位图（社交预览 / 横幅 / Logo）。

GitHub 社交预览只接受 PNG/JPG，SVG 不可用，故用 Pillow 精确绘制。

用法：
    python scripts/build_brand_assets.py

输出：
    assets/social-preview/social-preview.png   1280x640
    assets/brand/banner.png                    1200x320
    assets/brand/logo.png                      512x512

License: PolyForm Noncommercial 1.0.0
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = r"C:\Windows\Fonts"

# 配色（宋版册页：米白宣纸 / 墨色 / 朱砂 / 铜金）
PAPER_1 = (252, 249, 242)
PAPER_2 = (235, 226, 207)
INK = (20, 20, 20)
INK_SOFT = (90, 90, 90)
CINNABAR = (157, 41, 51)
CINNABAR_DEEP = (140, 43, 34)
GOLD = (168, 137, 78)
GOLD_LIGHT = (201, 169, 97)


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS, name), size)
    except Exception:
        return ImageFont.load_default()


def serif_cn(size):
    """中文衬线（思源宋体优先，回退宋体）"""
    for n in ("NotoSerifSC-VF.ttf", "simsun.ttc", "simhei.ttf"):
        p = os.path.join(FONTS, n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def serif_en(size, bold=False):
    return font("georgiab.ttf" if bold else "georgia.ttf", size)


def sans_cn(size, bold=False):
    return font("msyhbd.ttc" if bold else "msyh.ttc", size)


def paper_background(w, h):
    """纵向渐变宣纸底 + 细微纤维纹理"""
    img = Image.new("RGB", (w, h), PAPER_1)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        # 对角渐变近似
        r = int(PAPER_1[0] + (PAPER_2[0] - PAPER_1[0]) * t)
        g = int(PAPER_1[1] + (PAPER_2[1] - PAPER_1[1]) * t)
        b = int(PAPER_1[2] + (PAPER_2[2] - PAPER_1[2]) * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    # 纤维纹理
    rnd = random.Random(20261127)
    for _ in range(w * h // 900):
        x = rnd.randrange(w)
        y = rnd.randrange(h)
        d.point((x, y), fill=(rnd.randint(210, 232), rnd.randint(200, 224), rnd.randint(182, 206)))
    return img


def frame(d, x0, y0, x1, y1, color=INK, width=4):
    d.rectangle([x0, y0, x1, y1], outline=color, width=width)


def draw_seal(img, x, y, size, lines):
    """朱砂印章"""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + size, y + size], fill=CINNABAR_DEEP)
    pad = max(2, size // 16)
    d.rectangle([x + pad, y + pad, x + size - pad, y + size - pad],
                outline=(252, 249, 242), width=max(1, size // 48))
    f = serif_cn(int(size * 0.31))
    lh = size / len(lines)
    for i, ch in enumerate(lines):
        bb = d.textbbox((0, 0), ch, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text((x + (size - tw) / 2 - bb[0], y + lh * i + (lh - th) / 2 - bb[1]),
               ch, font=f, fill=(252, 249, 242))


def draw_banner(path):
    W, H = 1200, 320
    img = paper_background(W, H)
    d = ImageDraw.Draw(img)

    frame(d, 22, 22, W - 22, H - 22, INK, 4)
    frame(d, 32, 32, W - 32, H - 32, (196, 190, 176), 1)

    # 版心竖线
    d.line([(150, 52), (150, H - 52)], fill=(210, 204, 190), width=1)
    d.line([(170, 52), (170, H - 52)], fill=(210, 204, 190), width=1)

    # 左栏竖排：繁体「鐵板神數」单列（宋版书耳）
    f_side = serif_cn(34)
    for i, ch in enumerate(["鐵", "板", "神", "數"]):
        bb = d.textbbox((0, 0), ch, font=f_side)
        d.text((96 - (bb[2] - bb[0]) / 2 - bb[0], 58 + i * 44 - bb[1]),
               ch, font=f_side, fill=CINNABAR_DEEP)

    f_tag = serif_cn(12)
    tag = "公開學術版"
    d.text((96 - d.textlength(tag, font=f_tag) / 2, 246), tag, font=f_tag, fill=INK_SOFT)

    d.text((222, 58), "铁板神数软件", font=serif_cn(62), fill=INK)

    # 英文副题（宽字距）
    f_en = serif_en(20)
    x = 226
    for ch in "TIEBAN SHENSHU":
        d.text((x, 140), ch, font=f_en, fill=GOLD)
        x += d.textlength(ch, font=f_en) + 7.5

    # 铜金分隔
    d.line([(226, 182), (620, 182)], fill=GOLD_LIGHT, width=2)

    d.text((226, 200), "传统文化研究 · 文献索引 · 可运行教学工具",
           font=sans_cn(17), fill=(58, 58, 58))
    d.text((226, 232), "COMMUNITY RESEARCH & EDUCATIONAL DEMOS",
           font=font("arial.ttf", 12) if os.path.exists(os.path.join(FONTS, "arial.ttf")) else serif_en(12),
           fill=(107, 107, 107))
    d.text((226, 262), "商业核心与完整条文库不在此公开 · Private core is not part of this repository",
           font=sans_cn(12), fill=(138, 138, 138))

    draw_seal(img, 1048, 96, 96, ["天命", "鐵板"])
    d.text((1060, 214), "EST. 2026", font=serif_en(11), fill=(154, 154, 154))

    img.save(path, "PNG", optimize=True)
    return path


def draw_logo(path):
    S = 512
    img = paper_background(S, S)
    d = ImageDraw.Draw(img)

    frame(d, 16, 16, S - 16, S - 16, INK, 7)
    frame(d, 34, 34, S - 34, S - 34, (200, 194, 180), 2)
    frame(d, 62, 62, S - 62, S - 62, GOLD_LIGHT, 2)

    # 铁板（朱砂）
    f_big = serif_cn(112)
    t1 = "铁板"
    bb = d.textbbox((0, 0), t1, font=f_big)
    d.text(((S - (bb[2] - bb[0])) / 2 - bb[0], 96 - bb[1]), t1, font=f_big, fill=CINNABAR_DEEP)

    # 神数（墨色）
    t2 = "神数"
    bb2 = d.textbbox((0, 0), t2, font=f_big)
    d.text(((S - (bb2[2] - bb2[0])) / 2 - bb2[0], 214 - bb2[1]), t2, font=f_big, fill=INK)

    d.line([(130, 362), (382, 362)], fill=GOLD_LIGHT, width=2)

    f_en = serif_en(18)
    t3 = "TIEBAN SHENSHU"
    x = (S - sum(d.textlength(c, font=f_en) + 5.5 for c in t3)) / 2
    for c in t3:
        d.text((x, 384), c, font=f_en, fill=GOLD)
        x += d.textlength(c, font=f_en) + 5.5

    t4 = "COMMUNITY EDITION"
    w4 = sum(d.textlength(c, font=f_en) * 0.6 + 2.6 for c in t4)
    x = (S - w4) / 2
    f_small = serif_en(11)
    for c in t4:
        d.text((x, 414), c, font=f_small, fill=(138, 138, 138))
        x += d.textlength(c, font=f_small) + 2.6

    # 四角装饰
    for (cx, cy, dx, dy) in [(62, 96, -1, -1), (450, 96, 1, -1), (450, 416, 1, 1), (62, 416, -1, 1)]:
        d.line([(cx, cy), (cx + dx * 34, cy)], fill=(150, 145, 132), width=3)
        d.line([(cx, cy), (cx, cy + dy * 34)], fill=(150, 145, 132), width=3)

    img.save(path, "PNG", optimize=True)
    return path


def draw_social(path):
    W, H = 1280, 640
    img = paper_background(W, H)
    d = ImageDraw.Draw(img)

    frame(d, 34, 34, W - 34, H - 34, INK, 5)
    frame(d, 48, 48, W - 48, H - 48, (198, 192, 178), 2)
    frame(d, 72, 72, W - 72, H - 72, GOLD_LIGHT, 2)

    # 版心
    d.line([(330, 96), (330, H - 96)], fill=(210, 204, 190), width=1)
    d.line([(352, 96), (352, H - 96)], fill=(210, 204, 190), width=1)

    # 左栏竖排：繁体「鐵板 / 神數」与右侧简体主标题形成繁简对照（宋版界行）
    f_side = serif_cn(62)
    columns = [("鐵", "板"), ("神", "數")]
    col_xs = [252, 174]               # 右 → 左
    for ci, pair in enumerate(columns):
        for ri, ch in enumerate(pair):
            bb = d.textbbox((0, 0), ch, font=f_side)
            d.text((col_xs[ci] - (bb[2] - bb[0]) / 2 - bb[0], 128 + ri * 96 - bb[1]),
                   ch, font=f_side, fill=CINNABAR_DEEP)
    for gx in (213,):
        d.line([(gx, 116), (gx, 322)], fill=(214, 208, 194), width=1)

    f_tag = serif_cn(17)
    tag = "公開學術版"
    d.text((213 - d.textlength(tag, font=f_tag) / 2, 358), tag, font=f_tag, fill=INK_SOFT)

    # 左上角卷首
    d.text((96, 92), "卷首 · VOL. I", font=serif_cn(12), fill=(172, 163, 144))

    # 主标题
    d.text((410, 112), "铁板神数软件", font=serif_cn(92), fill=INK)

    # 英文宽字距
    f_en = serif_en(28)
    x = 414
    for ch in "TIEBAN SHENSHU":
        d.text((x, 236), ch, font=f_en, fill=GOLD)
        x += d.textlength(ch, font=f_en) + 11

    d.line([(414, 292), (900, 292)], fill=GOLD_LIGHT, width=2)

    d.text((414, 318), "传统文化研究 · 文献索引 · 可运行教学工具",
           font=sans_cn(24), fill=(51, 51, 51))
    d.text((414, 358), "COMMUNITY RESEARCH & EDUCATIONAL DEMOS",
           font=serif_en(16), fill=(107, 107, 107))

    # 四语
    f_lang = sans_cn(15)
    x = 414
    for i, lang in enumerate(["简体中文", "繁體中文 (HK)", "正體中文 (TW)", "English"]):
        if i:
            d.text((x, 420), "·", font=f_lang, fill=(192, 185, 170))
            x += d.textlength("·", font=f_lang) + 14
        d.text((x, 420), lang, font=f_lang, fill=(138, 138, 138))
        x += d.textlength(lang, font=f_lang) + 14

    d.text((414, 470), "tiebanshenshuapp.com", font=serif_en(18), fill=CINNABAR_DEEP)

    draw_seal(img, 1064, 300, 128, ["天命", "鐵板"])
    d.text((1110, 452), "EST. 2026", font=serif_en(12), fill=(154, 154, 154))

    img.save(path, "PNG", optimize=True)
    return path


def main():
    out_social = os.path.join(ROOT, "assets", "social-preview", "social-preview.png")
    out_banner = os.path.join(ROOT, "assets", "brand", "banner.png")
    out_logo = os.path.join(ROOT, "assets", "brand", "logo.png")

    for p in (out_social, out_banner, out_logo):
        os.makedirs(os.path.dirname(p), exist_ok=True)

    draw_social(out_social)
    draw_banner(out_banner)
    draw_logo(out_logo)

    for p in (out_social, out_banner, out_logo):
        with Image.open(p) as im:
            print(f"OK  {os.path.relpath(p, ROOT):44s} {im.size[0]}x{im.size[1]}  "
                  f"{os.path.getsize(p)//1024} KB")


if __name__ == "__main__":
    main()