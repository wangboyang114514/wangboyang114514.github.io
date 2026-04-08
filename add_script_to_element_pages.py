import os
import re

# 定义要处理的目录
chinese_dir = 'chinese'
english_dir = 'english'

# 要添加的脚本标签
script_tag = '<script src="../interaction.js"></script>'

# 处理函数
def add_script_to_files(directory):
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return
    
    files = os.listdir(directory)
    html_files = [f for f in files if f.endswith('.html')]
    
    for file_name in html_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经包含 interaction.js
        if 'interaction.js' in content:
            print(f"文件 {file_path} 已经包含 interaction.js")
            continue
        
        # 在 </head> 标签前添加脚本标签
        updated_content = re.sub(r'(</head>)', f'    {script_tag}\n\1', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"已更新文件: {file_path}")

# 执行处理
print("处理中文元素详情页...")
add_script_to_files(chinese_dir)

print("处理英文元素详情页...")
add_script_to_files(english_dir)

print("处理完成！")
