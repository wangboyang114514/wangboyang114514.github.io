import os
import re

def check_links():
    html_path = 'chinese.html'
    chinese_dir = 'chinese'
    
    # 读取chinese.html文件内容
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有元素链接
    links = re.findall(r'href="chinese/(\d+[A-Za-z]+)\.html"', content)
    
    missing_files = []
    
    # 检查每个链接对应的文件是否存在
    for link in links:
        file_path = os.path.join(chinese_dir, f'{link}.html')
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print('缺失以下文件:')
        for file in missing_files:
            print(file)
    else:
        print('所有链接都指向存在的文件！')

if __name__ == '__main__':
    check_links()