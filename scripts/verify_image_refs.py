# -*- coding: utf-8 -*-
"""校验所有详情页引用的元素图片文件是否存在"""
import glob
import os
import re

root = r'c:\GitHub\wangboyang114514.github.io'
missing = []
total = 0

for sub in ('chinese', 'english'):
    for f in glob.glob(os.path.join(root, sub, '*.html')):
        html = open(f, encoding='utf-8').read()
        for m in re.findall(r'src="(\.\./photo/elements/[^"]+)"', html):
            total += 1
            p = os.path.normpath(os.path.join(root, sub, m))
            if not os.path.exists(p):
                missing.append((os.path.basename(f), m))

print(f'引用总数: {total}, 缺失: {len(missing)}')
for f, m in missing[:10]:
    print(f'  {f} -> {m}')
