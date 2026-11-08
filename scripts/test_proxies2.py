# -*- coding: utf-8 -*-
"""第二轮代理测试"""
import json
import urllib.parse
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0'}
SUMMARY = 'https://en.wikipedia.org/api/rest_v1/page/summary/Hydrogen'
Q = urllib.parse.quote(SUMMARY, safe='')

tests = [
    ('allorigins/get', 'https://api.allorigins.win/get?url=' + Q),
    ('allorigins raw 重试', 'https://api.allorigins.win/raw?url=' + Q),
    ('cors.lol', 'https://api.cors.lol/?url=' + Q),
    ('whateverorigin', 'https://whateverorigin.org/get?url=' + Q),
    ('cors.eu.org', 'https://cors.eu.org/' + SUMMARY),
    ('yacdn', 'https://yacdn.org/proxy/' + SUMMARY),
    ('hancel英文维基', 'https://en.wikipedia.hancel.org/api/rest_v1/page/summary/Hydrogen'),
    ('hancel中文维基', 'https://zh.wikipedia.hancel.org/api/rest_v1/page/summary/%E6%B0%A2'),
]

print('=== JSON API 代理 第二轮 ===')
for name, url in tests:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=12) as r:
            body = r.read().decode('utf-8', errors='replace')
        start = body.find('{')
        data = json.loads(body[start:]) if start >= 0 else {}
        # allorigins/get 和 whateverorigin 是 JSON 包裹
        if 'contents' in data and isinstance(data.get('contents'), str):
            inner = json.loads(data['contents'][data['contents'].find('{'):])
            data = inner
        img = (data.get('originalimage') or {}).get('source', 'NO-IMG')
        print(f'{name}: OK -> {img[:90]}')
    except Exception as e:
        print(f'{name}: FAIL ({str(e)[:60]})')
