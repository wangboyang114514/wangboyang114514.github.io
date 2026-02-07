import os
import re

# 处理元素详情页的函数
def add_animation_to_element_pages(directory):
    # 遍历目录下的所有HTML文件
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经添加了动画
            if 'fadeInUp' not in content:
                # 在head标签内添加动画样式
                modified_content = re.sub(r'(<link rel="stylesheet" href="\.\./styles\.css">)', r'\1\n    <style>\n        /* 页面进入动画 */\n        body {\n            opacity: 0;\n            transform: translateY(50px);\n            animation: fadeInUp 0.8s ease-out forwards;\n        }\n        \n        @keyframes fadeInUp {\n            to {\n                opacity: 1;\n                transform: translateY(0);\n            }\n        }\n        \n        /* 导航栏和内容的延迟动画 */\n        .navbar {\n            animation: fadeInUp 0.8s ease-out 0.2s forwards;\n            opacity: 0;\n            transform: translateY(50px);\n        }\n        \n        .container {\n            animation: fadeInUp 0.8s ease-out 0.4s forwards;\n            opacity: 0;\n            transform: translateY(50px);\n        }\n    </style>', content)
            
                # 写入修改后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                print(f'Updated: {file_path}')

# 处理中文元素详情页
chinese_dir = 'chinese'
if os.path.exists(chinese_dir):
    print('Processing Chinese element pages...')
    add_animation_to_element_pages(chinese_dir)

# 处理英文元素详情页
english_dir = 'english'
if os.path.exists(english_dir):
    print('Processing English element pages...')
    add_animation_to_element_pages(english_dir)

print('All files have been processed successfully!')
