import os
import re

# 定义目录路径
enlish_dir = r"d:\06-Git\wangboyang114514.github.io\english"

# 要翻译的默认值（中文到英文映射）
default_translations = {
    '无特殊危害信息': 'No special hazard information',
    '无CAS号': 'No CAS number',
    '无同义词': 'No synonyms'
}

# 遍历english目录中的所有HTML文件
for filename in os.listdir(enlish_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(enlish_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换所有中文默认值为英文
        updated_content = content
        for chinese, english in default_translations.items():
            updated_content = updated_content.replace(chinese, english)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"已更新默认值: {file_path}")

print("所有默认值翻译完成！")