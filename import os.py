import os
import pandas as pd
from translate import Translator

# 创建 Translator 对象 (修改这里)
translator = Translator(to_lang="zh")

# 定义源文件夹和目标文件夹
source_folder = 'english'
target_folder = 'chinese'

# 确保目标文件夹存在
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):
        # 读取 CSV 文件
        file_path = os.path.join(source_folder, filename)
        df = pd.read_csv(file_path)

        # 遍历 DataFrame 中的每个单元格
        for col in df.columns:
            for idx, value in df[col].items():
                if isinstance(value, str):
                    # 翻译单元格内容 (修改这里)
                    translation = translator.translate(value)
                    df.at[idx, col] = translation

        # 保存翻译后的文件到目标文件夹
        target_file_path = os.path.join(target_folder, filename)
        df.to_csv(target_file_path, index=False)

print("翻译完成，文件已保存到 'chinese' 文件夹。")