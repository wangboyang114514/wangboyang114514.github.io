# -*- coding: utf-8 -*-
"""第三轮: 对存活代理做重试+长超时测试"""
import json
import time
import urllib.parse
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0'}
SUMMARY = 'https://en.wikipedia.org/api/rest_v1/page/summary/Hydrogen'
Q = urllib.parse.quote(SUMMARY, safe='')

candidates = {
    'codetabs': 'https://api.codetabs.com/v1/proxy?quest=' + Q,
    'cors.lol': 'https://api.cors.lol/?url=' + Q,
    'cors.eu.org': 'https://cors.eu.org/' + SUMMARY,
    'allorigins': 'https://api.allorigins.win/raw?url=' + Q,
}


def try_fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')


for name, url in candidates.items():
    for attempt in (1, 2, 3):
        try:
            body = try_fetch(url)
            start = body.find('{')
            data = json.loads(body[start:]) if start >= 0 else {}
            img = (data.get('originalimage') or {}).get('source', 'NO-IMG')
            title = data.get('title', '?')
            print(f'{name} 第{attempt}次: OK (title={title}) -> {img[:80]}')
            break
        except Exception as e:
            print(f'{name} 第{attempt}次: {str(e)[:55]}')
            time.sleep(3)
