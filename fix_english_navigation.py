import os
import re

# 定义目录路径
enlish_dir = r"d:\06-Git\wangboyang114514.github.io\english"

# 要替换的导航链接文本
replacements = {
    '首页': 'Home',
    '元素列表': 'Element List'
}

# 遍历english目录中的所有HTML文件
for filename in os.listdir(enlish_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(enlish_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换导航链接文本
        updated_content = content
        for chinese, english in replacements.items():
            updated_content = updated_content.replace(chinese, english)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"已更新文件: {file_path}")

print("所有文件导航链接更新完成！")