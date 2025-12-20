import os
import re

# 定义目录路径
enlish_dir = r"d:\06-Git\wangboyang114514.github.io\english"

# 要翻译的中文到英文映射
translations = {
    '化学品安全': 'Chemical Safety',
    '危险类别：': 'Hazard Class:',
    '基本信息': 'Basic Information',
    '分子式：': 'Formula:',
    '分子量：': 'Molecular Weight:',
    '识别信息': 'Identification Information',
    'CAS号：': 'CAS Number:',
    '同义词：': 'Synonyms:',
    '创建信息': 'Creation Information',
    '创建日期：': 'Creation Date:',
    '描述': 'Description'
}

# 遍历english目录中的所有HTML文件
for filename in os.listdir(enlish_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(enlish_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换所有中文文本为英文
        updated_content = content
        for chinese, english in translations.items():
            updated_content = updated_content.replace(chinese, english)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"已翻译文件: {file_path}")

print("所有文件翻译完成！")