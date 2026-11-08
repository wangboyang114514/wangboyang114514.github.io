# -*- coding: utf-8 -*-
"""测试可用的 Wikipedia 代理链路"""
import json
import urllib.parse
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0'}
SUMMARY = 'https://en.wikipedia.org/api/rest_v1/page/summary/Hydrogen'
IMG = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Hydrogen.jpg/400px-Hydrogen.jpg'

proxies = [
    ('allorigins', 'https://api.allorigins.win/raw?url=' + urllib.parse.quote(SUMMARY, safe='')),
    ('r.jina.ai', 'https://r.jina.ai/' + SUMMARY),
    ('codetabs', 'https://api.codetabs.com/v1/proxy?quest=' + urllib.parse.quote(SUMMARY, safe='')),
    ('corsproxy.io', 'https://corsproxy.io/?url=' + urllib.parse.quote(SUMMARY, safe='')),
    ('thingproxy', 'https://thingproxy.freeboard.io/fetch/' + SUMMARY),
]

print('=== JSON API 代理 ===')
for name, url in proxies:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read().decode('utf-8', errors='replace')
        # 验证是否拿到有效 JSON
        start = body.find('{')
        data = json.loads(body[start:]) if start >= 0 else {}
        img = (data.get('originalimage') or {}).get('source', 'NO-IMG')
        print(f'{name}: OK -> {img[:80]}')
    except Exception as e:
        print(f'{name}: FAIL ({str(e)[:60]})')

print('\n=== 图片代理 (weserv) ===')
for name, url in [
    ('weserv', 'https://images.weserv.nl/?url=' + urllib.parse.quote(IMG, safe='')),
    ('weserv(wsrv)', 'https://wsrv.nl/?url=' + urllib.parse.quote(IMG, safe='')),
]:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            blob = r.read()
        ok = r.headers.get('Content-Type', '').startswith('image/') and len(blob) > 5000
        print(f'{name}: {"OK" if ok else "BAD"} ({len(blob)//1024}KB, {r.headers.get("Content-Type")})')
    except Exception as e:
        print(f'{name}: FAIL ({str(e)[:60]})')
