import os
import re

# 处理元素详情页的函数
def update_animation_speed(directory):
    # 遍历目录下的所有HTML文件
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含动画样式
            if 'fadeInUp' in content:
                # 更新动画持续时间
                modified_content = re.sub(r'fadeInUp\s+0\.8s', 'fadeInUp 0.5s', content)
                modified_content = re.sub(r'0\.2s\s+forwards', '0.1s forwards', modified_content)
                modified_content = re.sub(r'0\.4s\s+forwards', '0.2s forwards', modified_content)
            
                # 写入修改后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                print(f'Updated: {file_path}')

# 处理中文元素详情页
chinese_dir = 'chinese'
if os.path.exists(chinese_dir):
    print('Processing Chinese element pages...')
    update_animation_speed(chinese_dir)

# 处理英文元素详情页
english_dir = 'english'
if os.path.exists(english_dir):
    print('Processing English element pages...')
    update_animation_speed(english_dir)

print('All files have been processed successfully!')
