import os
import re
from bs4 import BeautifulSoup

# 定义目录路径
source_dir = r"d:\06-Git\wangboyang114514.github.io\english-back"
target_dir = r"d:\06-Git\wangboyang114514.github.io\english"

# 遍历source_dir中的所有HTML文件
for filename in os.listdir(source_dir):
    if filename.endswith(".html"):
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        
        # 检查目标文件是否存在
        if not os.path.exists(target_file):
            print(f"目标文件 {target_file} 不存在，跳过")
            continue
            
        # 读取源文件（english-back中的文件）
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()
        
        # 解析源文件，提取元素数据
        soup = BeautifulSoup(source_content, 'html.parser')
        
        # 初始化数据字典
        element_data = {
            'title': '',
            'element_name': '',
            'formula': '',
            'molecular_weight': '',
            'description': '',
            'safety': '无特殊危害信息',
            'cas': '无CAS号',
            'synonyms': '无同义词',
            'date': '2024-01-01'
        }
        
        # 提取标题
        title_tag = soup.find('title')
        if title_tag:
            element_data['title'] = title_tag.text.strip()
            element_data['element_name'] = title_tag.text.strip()
        
        # 提取表格数据
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    label = cells[0].text.strip()
                    value = cells[1].text.strip()
                    
                    if label == 'Element Name':
                        element_data['element_name'] = value
                        element_data['title'] = value
                    elif label == 'Symbol':
                        element_data['formula'] = value
                    elif label == 'Molecular Weight':
                        element_data['molecular_weight'] = value
                    elif label == 'Description':
                        element_data['description'] = value
        
        # 读取目标文件（english中的模板文件）
        with open(target_file, 'r', encoding='utf-8') as f:
            target_content = f.read()
        
        # 替换所有模板变量
        updated_content = target_content
        for key, value in element_data.items():
            updated_content = updated_content.replace(f'{{{key}}}', value)
        
        # 写入更新后的内容
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"已更新文件: {target_file}")

print("所有文件更新完成！")