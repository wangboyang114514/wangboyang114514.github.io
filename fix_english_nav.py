import os
import re

# 英文元素页面目录
english_dir = 'english'

# 遍历英文目录下的所有HTML文件
for filename in os.listdir(english_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(english_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修改导航链接，将 ../chinese.html 改为 ../English.html
        modified_content = re.sub(r'<a href="\.\./chinese\.html">Element List</a>', '<a href="../English.html">Element List</a>', content)
        
        # 如果内容有变化，写入文件
        if modified_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f'Updated: {filename}')

print('All files have been processed successfully!')
