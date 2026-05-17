import os
import re

# 元素数据
elements_data = {
    '01H': {'name': '氢', 'symbol': 'H', 'atomicNumber': 1, 'category': '非金属', 'group': 1, 'period': 1,
            'atomicWeight': '1.008', 'state': '气体', 'meltingPoint': '-259.16°C', 'boilingPoint': '-252.87°C',
            'density': '0.0899 g/L', 'electronConfig': '1s¹', 'electronegativity': '2.20', 'oxidationStates': '+1, -1',
            'discoverer': '亨利·卡文迪许', 'discoveryYear': '1776', 'uses': '燃料电池、火箭燃料、化学合成',
            'hazardClass': '易燃气体', 'casNumber': '1333-74-0', 'description': '氢是宇宙中最轻、最丰富的元素，约占宇宙质量的75%。它是一种无色、无味、无臭的气体，在地球上主要以水的形式存在。',
            'covalentRadius': '37', 'ionizationEnergy': '13.5984', 'electronAffinity': '72.769', 'thermalConductivity': '0.1805'},
    '02He': {'name': '氦', 'symbol': 'He', 'atomicNumber': 2, 'category': '稀有气体', 'group': 18, 'period': 1,
             'atomicWeight': '4.003', 'state': '气体', 'meltingPoint': '-272.2°C', 'boilingPoint': '-268.93°C',
             'density': '0.1786 g/L', 'electronConfig': '1s²', 'electronegativity': '无', 'oxidationStates': '0',
             'discoverer': '皮埃尔·让森、诺曼·洛克耶', 'discoveryYear': '1868', 'uses': '气球充气、低温冷却、焊接保护气',
             'hazardClass': '非易燃气体', 'casNumber': '7440-59-7', 'description': '氦是一种惰性气体，是宇宙中第二丰富的元素。它无色、无味、无臭，在标准条件下是气体。',
             'covalentRadius': '31', 'ionizationEnergy': '24.5874', 'electronAffinity': '0', 'thermalConductivity': '0.152'},
    '03Li': {'name': '锂', 'symbol': 'Li', 'atomicNumber': 3, 'category': '碱金属', 'group': 1, 'period': 2,
             'atomicWeight': '6.94', 'state': '固体', 'meltingPoint': '180.5°C', 'boilingPoint': '1342°C',
             'density': '0.534 g/cm³', 'electronConfig': '[He] 2s¹', 'electronegativity': '0.98', 'oxidationStates': '+1',
             'discoverer': '约翰·奥古斯特·阿韦德松', 'discoveryYear': '1817', 'uses': '锂离子电池、陶瓷工业、润滑剂',
             'hazardClass': '遇水反应', 'casNumber': '7439-93-2', 'description': '锂是一种银白色金属，是元素周期表中最轻的金属。它在空气中容易氧化，与水剧烈反应。',
             'covalentRadius': '134', 'ionizationEnergy': '5.3917', 'electronAffinity': '59.6', 'thermalConductivity': '84.8'},
    '04Be': {'name': '铍', 'symbol': 'Be', 'atomicNumber': 4, 'category': '碱土金属', 'group': 2, 'period': 2,
             'atomicWeight': '9.0122', 'state': '固体', 'meltingPoint': '1287°C', 'boilingPoint': '2469°C',
             'density': '1.85 g/cm³', 'electronConfig': '[He] 2s²', 'electronegativity': '1.57', 'oxidationStates': '+2',
             'discoverer': '弗雷德里希·维勒', 'discoveryYear': '1828', 'uses': '航空航天材料、核反应堆、X射线窗口',
             'hazardClass': '致癌物', 'casNumber': '7440-41-7', 'description': '铍是一种轻质、坚硬的灰色金属，具有高熔点和良好的导热性。',
             'covalentRadius': '90', 'ionizationEnergy': '9.3227', 'electronAffinity': '0', 'thermalConductivity': '200'},
    '05B': {'name': '硼', 'symbol': 'B', 'atomicNumber': 5, 'category': '类金属', 'group': 13, 'period': 2,
            'atomicWeight': '10.81', 'state': '固体', 'meltingPoint': '2076°C', 'boilingPoint': '3927°C',
            'density': '2.34 g/cm³', 'electronConfig': '[He] 2s² 2p¹', 'electronegativity': '2.04', 'oxidationStates': '+3',
            'discoverer': '约瑟夫·路易·盖-吕萨克、路易·泰纳尔', 'discoveryYear': '1808', 'uses': '玻璃制造、陶瓷、半导体',
            'hazardClass': '刺激性', 'casNumber': '7440-42-8', 'description': '硼是一种非金属元素，通常以无定形或结晶形式存在。它是植物生长必需的微量元素。',
            'covalentRadius': '82', 'ionizationEnergy': '8.298', 'electronAffinity': '26.7', 'thermalConductivity': '27.4'},
    '06C': {'name': '碳', 'symbol': 'C', 'atomicNumber': 6, 'category': '非金属', 'group': 14, 'period': 2,
            'atomicWeight': '12.01', 'state': '固体', 'meltingPoint': '3550°C', 'boilingPoint': '4827°C',
            'density': '2.267 g/cm³', 'electronConfig': '[He] 2s² 2p²', 'electronegativity': '2.55', 'oxidationStates': '-4, +2, +4',
            'discoverer': '已知元素', 'discoveryYear': '古代', 'uses': '钢铁生产、石墨、钻石、有机化学',
            'hazardClass': '可燃', 'casNumber': '7440-44-0', 'description': '碳是地球上所有生命的基础，以多种同素异形体存在，包括石墨、钻石和富勒烯。',
            'covalentRadius': '77', 'ionizationEnergy': '11.2603', 'electronAffinity': '121.7', 'thermalConductivity': '350'},
    '07N': {'name': '氮', 'symbol': 'N', 'atomicNumber': 7, 'category': '非金属', 'group': 15, 'period': 2,
            'atomicWeight': '14.01', 'state': '气体', 'meltingPoint': '-210°C', 'boilingPoint': '-195.8°C',
            'density': '1.2506 g/L', 'electronConfig': '[He] 2s² 2p³', 'electronegativity': '3.04', 'oxidationStates': '-3, +1, +2, +3, +4, +5',
            'discoverer': '丹尼尔·卢瑟福', 'discoveryYear': '1772', 'uses': '肥料生产、制冷剂、惰性气体',
            'hazardClass': '非易燃气体', 'casNumber': '7727-37-9', 'description': '氮是大气中最丰富的元素，约占空气体积的78%。它是蛋白质和核酸的重要组成部分。',
            'covalentRadius': '75', 'ionizationEnergy': '14.5341', 'electronAffinity': '6.75', 'thermalConductivity': '0.0259'},
    '08O': {'name': '氧', 'symbol': 'O', 'atomicNumber': 8, 'category': '非金属', 'group': 16, 'period': 2,
            'atomicWeight': '16.00', 'state': '气体', 'meltingPoint': '-218.79°C', 'boilingPoint': '-182.95°C',
            'density': '1.429 g/L', 'electronConfig': '[He] 2s² 2p⁴', 'electronegativity': '3.44', 'oxidationStates': '-2, -1',
            'discoverer': '约瑟夫·普利斯特里、卡尔·威廉·舍勒', 'discoveryYear': '1774', 'uses': '呼吸、燃烧、炼钢、医疗',
            'hazardClass': '氧化剂', 'casNumber': '7782-44-7', 'description': '氧是地球大气中第二丰富的元素，是所有需氧生物生存所必需的。',
            'covalentRadius': '73', 'ionizationEnergy': '13.6181', 'electronAffinity': '141.0', 'thermalConductivity': '0.0267'},
    '09F': {'name': '氟', 'symbol': 'F', 'atomicNumber': 9, 'category': '卤素', 'group': 17, 'period': 2,
            'atomicWeight': '19.00', 'state': '气体', 'meltingPoint': '-219.62°C', 'boilingPoint': '-188.12°C',
            'density': '1.696 g/L', 'electronConfig': '[He] 2s² 2p⁵', 'electronegativity': '3.98', 'oxidationStates': '-1',
            'discoverer': '亨利·莫瓦桑', 'discoveryYear': '1886', 'uses': '制冷剂、氟化剂、特氟龙',
            'hazardClass': '强氧化剂', 'casNumber': '7782-41-4', 'description': '氟是最活泼的非金属元素，能与几乎所有元素反应。它是电负性最强的元素。',
            'covalentRadius': '71', 'ionizationEnergy': '17.4228', 'electronAffinity': '328.2', 'thermalConductivity': '0.0279'},
    '10Ne': {'name': '氖', 'symbol': 'Ne', 'atomicNumber': 10, 'category': '稀有气体', 'group': 18, 'period': 2,
             'atomicWeight': '20.18', 'state': '气体', 'meltingPoint': '-248.67°C', 'boilingPoint': '-246.08°C',
             'density': '0.9002 g/L', 'electronConfig': '[He] 2s² 2p⁶', 'electronegativity': '无', 'oxidationStates': '0',
             'discoverer': '威廉·拉姆齐、莫里斯·特拉弗斯', 'discoveryYear': '1898', 'uses': '霓虹灯、激光、低温研究',
             'hazardClass': '非易燃气体', 'casNumber': '7440-01-9', 'description': '氖是一种惰性气体，在空气中含量稀少。它发出特征性的橙红色光。',
             'covalentRadius': '69', 'ionizationEnergy': '21.5645', 'electronAffinity': '0', 'thermalConductivity': '0.0493'},
}

# 模板
template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}({symbol})</title>
    <link rel="stylesheet" href="../styles.css">
    <script src="../interaction.js"></script>
    <style>
        body {{
            opacity: 0;
            transform: translateY(50px);
            animation: fadeInUp 0.5s ease-out forwards;
        }}
        
        @keyframes fadeInUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .navbar {{
            animation: fadeInUp 0.5s ease-out 0.1s forwards;
            opacity: 0;
            transform: translateY(50px);
        }}
        
        .container {{
            animation: fadeInUp 0.5s ease-out 0.2s forwards;
            opacity: 0;
            transform: translateY(50px);
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="../index.html" class="site-title">
                <img src="../photo/loge.png" class="logo" alt="Logo">
                Chemistry World
            </a>
            <ul class="nav-links">
                <li><a href="../index.html">首页</a></li>
                <li><a href="../chinese.html">元素列表</a></li>
            </ul>
            <div class="menu-toggle" id="menuToggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="element-detail">
            <h1>{name} ({symbol})</h1>
            
            <div class="element-header">
                <div class="element-image">
                    <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={name}_element_{symbol}_visualization_scientific&image_size=square_hd" alt="{name}元素">
                </div>
                
                <div class="element-basic-info">
                    <div class="basic-info-row">
                        <div class="basic-info-card">
                            <h3>原子序数</h3>
                            <p>{atomicNumber}</p>
                        </div>
                        <div class="basic-info-card">
                            <h3>原子量</h3>
                            <p>{atomicWeight} g/mol</p>
                        </div>
                        <div class="basic-info-card">
                            <h3>元素符号</h3>
                            <p>{symbol}</p>
                        </div>
                    </div>
                    <div class="basic-info-row">
                        <div class="basic-info-card">
                            <h3>分类</h3>
                            <p>{category}</p>
                        </div>
                        <div class="basic-info-card">
                            <h3>族</h3>
                            <p>{group}</p>
                        </div>
                        <div class="basic-info-card">
                            <h3>周期</h3>
                            <p>{period}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="element-info">
                <div class="info-card">
                    <h3>物理性质</h3>
                    <p><strong>状态：</strong>{state}</p>
                    <p><strong>熔点：</strong>{meltingPoint}</p>
                    <p><strong>沸点：</strong>{boilingPoint}</p>
                    <p><strong>密度：</strong>{density}</p>
                </div>

                <div class="info-card">
                    <h3>化学性质</h3>
                    <p><strong>电子构型：</strong>{electronConfig}</p>
                    <p><strong>电负性：</strong>{electronegativity}</p>
                    <p><strong>氧化态：</strong>{oxidationStates}</p>
                    <p><strong>反应性：</strong>中等</p>
                </div>

                <div class="info-card">
                    <h3>发现与用途</h3>
                    <p><strong>发现者：</strong>{discoverer}</p>
                    <p><strong>发现年份：</strong>{discoveryYear}</p>
                    <p><strong>主要用途：</strong>{uses}</p>
                </div>

                <div class="info-card">
                    <h3>安全信息</h3>
                    <p><strong>危险类别：</strong>{hazardClass}</p>
                    <p><strong>CAS号：</strong>{casNumber}</p>
                </div>
            </div>
            
            <div class="element-description">
                <h3>描述</h3>
                <p>{description}</p>
            </div>
            
            <div class="element-properties">
                <table>
                    <thead>
                        <tr>
                            <th>性质</th>
                            <th>数值</th>
                            <th>单位</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>共价半径</td>
                            <td>{covalentRadius}</td>
                            <td>pm</td>
                        </tr>
                        <tr>
                            <td>第一电离能</td>
                            <td>{ionizationEnergy}</td>
                            <td>eV</td>
                        </tr>
                        <tr>
                            <td>电子亲和能</td>
                            <td>{electronAffinity}</td>
                            <td>kJ/mol</td>
                        </tr>
                        <tr>
                            <td>热导率</td>
                            <td>{thermalConductivity}</td>
                            <td>W/(m·K)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <footer class="footer">
        <p>&copy; 2024 Chemistry World. All rights reserved.</p>
    </footer>

    <script>
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.querySelector('.nav-links');
        menuToggle.addEventListener('click', function() {{
            navLinks.classList.toggle('active');
        }});
    </script>
</body>
</html>"""

# 更新元素页面
chinese_dir = 'd:/06-Git/wangboyang114514.github.io/chinese/'

for filename in os.listdir(chinese_dir):
    if filename.endswith('.html') and len(filename) <= 10:
        file_key = filename.replace('.html', '')
        if file_key in elements_data:
            data = elements_data[file_key]
            content = template.format(**data)
            filepath = os.path.join(chinese_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated: {filename}')

print('更新完成！')