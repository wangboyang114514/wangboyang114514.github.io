# -*- coding: utf-8 -*-
"""
为 118 个化学元素批量生成兜底卡片图 (PIL, 离线可用)

- 解析 elements-zh.js / elements-en.js 获取元素数据
- 按站点分类配色生成统一风格卡片, 输出到 photo/elements/
- 文件名: {原子序数:03d}_{符号}.png (如 001_H.png, 118_Og.png)
- 若目标文件已存在且不是占位卡片(如真实照片), 默认跳过, --force 覆盖
"""
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'photo', 'elements')

# 与 styles.css 中分类颜色保持一致
CATEGORY_COLORS = {
    'alkali-metal': '#ff6b6b',
    'alkaline-earth-metal': '#4ecdc4',
    'metal': '#45b7d1',
    'metalloid': '#96ceb4',
    'nonmetal': '#ffeaa7',
    'halogen': '#dda0dd',
    'noble-gas': '#98d8c8',
}

CATEGORY_ZH = {
    'alkali-metal': '碱金属',
    'alkaline-earth-metal': '碱土金属',
    'metal': '金属',
    'metalloid': '类金属',
    'nonmetal': '非金属',
    'halogen': '卤素',
    'noble-gas': '稀有气体',
}

FONT_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'
FONT_REG = r'C:\Windows\Fonts\msyh.ttc'

W, H = 800, 1000
CARD_STEM_RE = re.compile(r'^\d{3}_[A-Za-z]{1,2}$')


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def parse_elements(path):
    """从 JS 数据文件解析元素列表"""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    rows = re.findall(
        r"\{ name: '([^']+)', symbol: '([^']+)', atomicNumber: (\d+), "
        r"category: '([^']+)', link: '[^']+' \}", content)
    return [
        {'name': n, 'symbol': s, 'number': int(a), 'category': c}
        for n, s, a, c in rows
    ]


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def load_font(path, size):
    return ImageFont.truetype(path, size)


def make_card(el, out_path):
    num_color = hex_to_rgb(CATEGORY_COLORS[el['category']])
    bg_top = (26, 26, 46)      # #1a1a2e
    bg_bottom = (22, 33, 62)   # #16213e

    img = Image.new('RGB', (W, H), bg_top)
    draw = ImageDraw.Draw(img)

    # 垂直渐变背景
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=lerp(bg_top, bg_bottom, y / H))

    # 顶部分类色条 (呼应站点卡片 ::before 样式)
    draw.rectangle([0, 0, W, 14], fill=num_color)

    # 符号背后的柔和光晕
    glow = Image.new('L', (W, H), 0)
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([W // 2 - 320, H // 2 - 260, W // 2 + 320, H // 2 + 340], fill=45)
    glow = glow.filter(__import__('PIL.ImageFilter', fromlist=['GaussianBlur']).GaussianBlur(120))
    img = Image.composite(Image.new('RGB', (W, H), num_color), img, glow)
    draw = ImageDraw.Draw(img)

    # 原子序数 (左上角)
    f_num = load_font(FONT_BOLD, 96)
    draw.text((60, 48), str(el['number']), font=f_num, fill=num_color)

    # 符号 (居中, 巨大)
    f_sym = load_font(FONT_BOLD, 300)
    bbox = draw.textbbox((0, 0), el['symbol'], font=f_sym)
    sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((W - sw) / 2 - bbox[0], H * 0.38 - sh / 2 - bbox[1]),
              el['symbol'], font=f_sym, fill=(255, 255, 255))

    # 中文名
    f_zh = load_font(FONT_BOLD, 84)
    bbox = draw.textbbox((0, 0), el['name'], font=f_zh)
    zw = bbox[2] - bbox[0]
    draw.text(((W - zw) / 2 - bbox[0], H * 0.68), el['name'],
              font=f_zh, fill=(255, 255, 255, 235))

    # 英文名
    f_en = load_font(FONT_REG, 40)
    bbox = draw.textbbox((0, 0), el['name_en'], font=f_en)
    ew = bbox[2] - bbox[0]
    draw.text(((W - ew) / 2 - bbox[0], H * 0.68 + 110), el['name_en'],
              font=f_en, fill=(255, 255, 255))

    # 底部分类标签
    label = CATEGORY_ZH[el['category']]
    f_cat = load_font(FONT_REG, 36)
    bbox = draw.textbbox((0, 0), label, font=f_cat)
    cw = bbox[2] - bbox[0]
    draw.text(((W - cw) / 2 - bbox[0], H - 110), label,
              font=f_cat, fill=num_color)

    img.save(out_path, 'PNG')


def main():
    force = '--force' in sys.argv

    zh = {e['number']: e for e in parse_elements(os.path.join(ROOT, 'elements-zh.js'))}
    en = {e['number']: e for e in parse_elements(os.path.join(ROOT, 'elements-en.js'))}

    os.makedirs(OUT_DIR, exist_ok=True)

    created, skipped = [], []
    for number in sorted(zh):
        el = dict(zh[number])
        el['name_en'] = en[number]['name']
        stem = f"{number:03d}_{el['symbol']}"
        out_path = os.path.join(OUT_DIR, stem + '.png')

        if not force and os.path.exists(out_path):
            skipped.append(stem)
            continue

        make_card(el, out_path)
        created.append(stem)
        print(f'  生成 {stem}.png')

    print(f'\n完成: 新生成 {len(created)} 张, 跳过已存在 {len(skipped)} 张')
    print(f'输出目录: {OUT_DIR}')


if __name__ == '__main__':
    main()
