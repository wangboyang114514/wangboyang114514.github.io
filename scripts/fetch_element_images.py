# -*- coding: utf-8 -*-
"""
从 Wikipedia 抓取 118 个元素的实物照片 (代理版, 大陆网络可用)

链路:
  1. JSON: allorigins / cors.lol / cors.eu.org (依次重试) -> Wikipedia summary API
  2. 图片: wsrv.nl 图片代理 -> upload.wikimedia.org, 统一压缩为 900px 宽 JPG

输出: photo/elements/{原子序数:03d}_{符号}.jpg
报告: photo/elements/fetch_report.json

用法: python fetch_element_images.py [--delay 1.5] [--only-missing]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'photo', 'elements')

UA = {'User-Agent': 'Mozilla/5.0 (educational-site-image-fetch)'}

# 英文 Wikipedia 标题与数据文件拼写差异
EN_TITLE_ALIASES = {13: 'Aluminium', 55: 'Caesium'}


def parse_elements(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    rows = re.findall(
        r"\{ name: '([^']+)', symbol: '([^']+)', atomicNumber: (\d+), "
        r"category: '([^']+)', link: '([^']+)' \}", content)
    return [{'name': n, 'symbol': s, 'number': int(a)} for n, s, a, _, _ in rows]


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _try_proxy(purl, timeout=10):
    body = http_get(purl, timeout=timeout).decode('utf-8', errors='replace')
    start = body.find('{')
    if start < 0:
        raise ValueError('非 JSON 响应')
    return json.loads(body[start:])


def fetch_json(url, deadline_seconds=40):
    """3 个公共代理并发竞速, 谁先返回有效 JSON 用谁; 整体限时重试"""
    q = urllib.parse.quote(url, safe='')
    proxies = [
        f'https://api.allorigins.win/raw?url={q}',
        f'https://api.cors.lol/?url={q}',
        f'https://cors.eu.org/{url}',
    ]
    deadline = time.time() + deadline_seconds
    while time.time() < deadline:
        with ThreadPoolExecutor(max_workers=3) as ex:
            futures = {ex.submit(_try_proxy, p): p for p in proxies}
            for fut in as_completed(futures):
                try:
                    return fut.result()
                except Exception:
                    pass
        time.sleep(0.5)
    return None


def fetch_image_bytes(img_url, width=900, attempts=3):
    """通过 wsrv.nl 抓图(自动跟随跳转), 失败时用 allorigins 兜底"""
    q = urllib.parse.quote(img_url, safe='')
    primary = f'https://wsrv.nl/?url={q}&w={width}&output=jpg&q=85'
    fallback = f'https://api.allorigins.win/raw?url={q}'
    for _ in range(attempts):
        for url in (primary, fallback):
            try:
                blob = http_get(url, timeout=30)
                if len(blob) > 3000:
                    return blob
            except Exception:
                continue
        time.sleep(2)
    return None


def get_element_image(el, lang, delay_used=None):
    """返回 (blob|None, 说明)"""
    title = EN_TITLE_ALIASES.get(el['number'], el['name']) if lang == 'en' else el['name']
    api = (f'https://{lang}.wikipedia.org/api/rest_v1/page/summary/'
           + urllib.parse.quote(title))

    data = fetch_json(api)
    if not data:
        return None, 'API 不可达'

    img_url = (data.get('originalimage') or {}).get('source')
    if not img_url:
        return None, '词条无图片'

    blob = fetch_image_bytes(img_url)
    if not blob:
        return None, '图片下载失败'
    return blob, 'ok'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--delay', type=float, default=1.2)
    ap.add_argument('--lang', default='en', choices=['en', 'zh'])
    args = ap.parse_args()

    zh = {e['number']: e for e in parse_elements(os.path.join(ROOT, 'elements-zh.js'))}
    en = {e['number']: e for e in parse_elements(os.path.join(ROOT, 'elements-en.js'))}
    os.makedirs(OUT_DIR, exist_ok=True)

    ok, failed = [], []
    for i, number in enumerate(sorted(zh), 1):
        el = {'number': number, 'symbol': zh[number]['symbol'], 'name': en[number]['name']}
        stem = f"{number:03d}_{el['symbol']}"
        out_path = os.path.join(OUT_DIR, stem + '.jpg')

        if os.path.exists(out_path):
            print(f'[{i}/118] 跳过 {stem} (已存在)', flush=True)
            continue

        blob, msg = get_element_image(el, args.lang)
        if blob is None and args.lang == 'en':
            blob, msg = get_element_image({'number': number, 'symbol': el['symbol'],
                                           'name': zh[number]['name']}, 'zh')
        if blob:
            with open(out_path, 'wb') as f:
                f.write(blob)
            ok.append(stem)
            print(f'[{i}/118] OK   {stem} ({len(blob)//1024}KB)', flush=True)
        else:
            failed.append({'stem': stem, 'reason': msg})
            print(f'[{i}/118] FAIL {stem}: {msg}', flush=True)

        time.sleep(args.delay)

    with open(os.path.join(OUT_DIR, 'fetch_report.json'), 'w', encoding='utf-8') as f:
        json.dump({'success': ok, 'failed': failed}, f, ensure_ascii=False, indent=2)
    print(f'\n完成: 成功 {len(ok)}, 失败 {len(failed)}')
    for item in failed:
        print(f"  缺图: {item['stem']} ({item['reason']})")


if __name__ == '__main__':
    main()
