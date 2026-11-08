# -*- coding: utf-8 -*-
"""
把 photo/elements/ 下的元素卡片图批量接入详情页

- 中文页 (118): 将 trae API 热链图 src 替换为本地卡片 ../photo/elements/NNN_Sym.png
- 英文页 (118): 在第一个 <h1> 后插入 element-header > element-image 卡片
- 幂等: 已集成过的页面自动跳过
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZH_DIR = os.path.join(ROOT, 'chinese')
EN_DIR = os.path.join(ROOT, 'english')


def parse_elements(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    rows = re.findall(
        r"\{ name: '([^']+)', symbol: '([^']+)', atomicNumber: (\d+), "
        r"category: '([^']+)', link: '([^']+)' \}", content)
    return [
        {'name': n, 'symbol': s, 'number': int(a), 'category': c, 'link': l}
        for n, s, a, c, l in rows
    ]


def image_path(el):
    return f"../photo/elements/{el['number']:03d}_{el['symbol']}.png"


def integrate_zh(el):
    path = os.path.join(ZH_DIR, os.path.basename(el['link']))
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'photo/elements/' in html:
        return 'skip'
    if 'trae-api-cn.mchost.guru' not in html:
        return 'no-slot'

    new_html, n = re.subn(
        r'src="https://trae-api-cn\.mchost\.guru[^"]*"',
        f'src="{image_path(el)}"',
        html, count=1)
    if n == 0:
        return 'no-slot'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return 'ok'


EN_INSERT_TEMPLATE = '''<h1>{name}</h1>

            <div class="element-header">
                <div class="element-image">
                    <img src="{img}" alt="{name}">
                </div>
            </div>'''


def integrate_en(el):
    path = os.path.join(EN_DIR, os.path.basename(el['link']))
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'element-image' in html:
        return 'skip'

    pattern = re.compile(r'<h1>[^<]*</h1>')
    m = pattern.search(html)
    if not m:
        return 'no-h1'

    block = EN_INSERT_TEMPLATE.format(name=el['name'], img=image_path(el))
    new_html = html[:m.start()] + block + html[m.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return 'ok'


def main():
    zh = parse_elements(os.path.join(ROOT, 'elements-zh.js'))
    en = parse_elements(os.path.join(ROOT, 'elements-en.js'))

    stats = {'zh': {}, 'en': {}}
    for el in zh:
        r = integrate_zh(el)
        stats['zh'][r] = stats['zh'].get(r, 0) + 1
        if r not in ('ok', 'skip'):
            print(f"zh 失败: {el['link']} -> {r}")
    for el in en:
        r = integrate_en(el)
        stats['en'][r] = stats['en'].get(r, 0) + 1
        if r not in ('ok', 'skip'):
            print(f"en 失败: {el['link']} -> {r}")

    print(f"\n中文页: {stats['zh']}")
    print(f"英文页: {stats['en']}")


if __name__ == '__main__':
    main()
