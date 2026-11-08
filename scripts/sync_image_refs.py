# -*- coding: utf-8 -*-
"""
抓取实物照片后同步页面引用:
  1. 扫描 photo/elements/ 实际存在的文件 (优先 .jpg 实物照片, 其次 .png 卡片)
  2. 将 236 个详情页 src 更新为实际扩展名
  3. 删除已被实物照片替代、不再被引用的 .png 卡片
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, 'photo', 'elements')


def actual_image(number):
    """返回某元素实际存在的图片文件名 (有 jpg 用 jpg, 否则 png)"""
    for ext in ('.jpg', '.jpeg', '.png'):
        stem = f'{number:03d}_'
        for f in os.listdir(IMG_DIR):
            if f.startswith(stem) and f.lower().endswith(ext):
                return f
    return None


def main():
    if not os.path.isdir(IMG_DIR):
        print('photo/elements 不存在')
        return

    files = {f for f in os.listdir(IMG_DIR) if re.match(r'^\d{3}_', f)}
    referenced = set()

    for sub in ('chinese', 'english'):
        for path in glob.glob(os.path.join(ROOT, sub, '*.html')):
            number = int(re.search(r'(\d+)', os.path.basename(path)).group(1))
            actual = actual_image(number)
            if not actual:
                print(f'警告: {os.path.basename(path)} 无对应图片文件')
                continue
            referenced.add(actual)

            with open(path, encoding='utf-8') as f:
                html = f.read()
            new_html, n = re.subn(
                r'src="\.\./photo/elements/[^"]*"',
                f'src="../photo/elements/{actual}"',
                html, count=1)
            if n and new_html != html:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_html)

    # 删除未被引用的旧卡片
    unused = files - referenced
    for f in sorted(unused):
        os.remove(os.path.join(IMG_DIR, f))
        print(f'删除未引用卡片: {f}')

    jpg_count = sum(1 for f in referenced if f.lower().endswith(('.jpg', '.jpeg')))
    print(f'\n完成: 实物照片 {jpg_count} 张, 保留卡片 {len(referenced) - jpg_count} 张, '
          f'删除 {len(unused)} 张')


if __name__ == '__main__':
    main()
