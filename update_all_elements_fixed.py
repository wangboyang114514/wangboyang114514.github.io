import os

# 创建所有118个元素的数据
all_elements = {}

# 前34个元素（详细数据）
detailed_elements = {
    '01H': {'name': '氢', 'symbol': 'H', 'atomicNumber': 1, 'category': '非金属', 'group': 1, 'period': 1,
            'atomicWeight': '1.008', 'state': '气体', 'meltingPoint': '-259.16°C', 'boilingPoint': '-252.87°C',
            'density': '0.0899 g/L', 'electronConfig': '1s¹', 'electronegativity': '2.20', 'oxidationStates': '+1, -1',
            'discoverer': '亨利·卡文迪许', 'discoveryYear': '1776', 'uses': '燃料电池、火箭燃料、化学合成',
            'hazardClass': '易燃气体', 'casNumber': '1333-74-0', 'description': '氢是宇宙中最轻、最丰富的元素，约占宇宙质量的75%。',
            'covalentRadius': '37', 'ionizationEnergy': '13.5984', 'electronAffinity': '72.769', 'thermalConductivity': '0.1805'},
    '02He': {'name': '氦', 'symbol': 'He', 'atomicNumber': 2, 'category': '稀有气体', 'group': 18, 'period': 1,
             'atomicWeight': '4.003', 'state': '气体', 'meltingPoint': '-272.2°C', 'boilingPoint': '-268.93°C',
             'density': '0.1786 g/L', 'electronConfig': '1s²', 'electronegativity': '无', 'oxidationStates': '0',
             'discoverer': '皮埃尔·让森', 'discoveryYear': '1868', 'uses': '气球充气、低温冷却、焊接保护气',
             'hazardClass': '非易燃气体', 'casNumber': '7440-59-7', 'description': '氦是一种惰性气体，是宇宙中第二丰富的元素。',
             'covalentRadius': '31', 'ionizationEnergy': '24.5874', 'electronAffinity': '0', 'thermalConductivity': '0.152'},
    '03Li': {'name': '锂', 'symbol': 'Li', 'atomicNumber': 3, 'category': '碱金属', 'group': 1, 'period': 2,
             'atomicWeight': '6.94', 'state': '固体', 'meltingPoint': '180.5°C', 'boilingPoint': '1342°C',
             'density': '0.534 g/cm³', 'electronConfig': '[He] 2s¹', 'electronegativity': '0.98', 'oxidationStates': '+1',
             'discoverer': '约翰·阿韦德松', 'discoveryYear': '1817', 'uses': '锂离子电池、陶瓷工业、润滑剂',
             'hazardClass': '遇水反应', 'casNumber': '7439-93-2', 'description': '锂是一种银白色金属，是元素周期表中最轻的金属。',
             'covalentRadius': '134', 'ionizationEnergy': '5.3917', 'electronAffinity': '59.6', 'thermalConductivity': '84.8'},
    '04Be': {'name': '铍', 'symbol': 'Be', 'atomicNumber': 4, 'category': '碱土金属', 'group': 2, 'period': 2,
             'atomicWeight': '9.0122', 'state': '固体', 'meltingPoint': '1287°C', 'boilingPoint': '2469°C',
             'density': '1.85 g/cm³', 'electronConfig': '[He] 2s²', 'electronegativity': '1.57', 'oxidationStates': '+2',
             'discoverer': '弗雷德里希·维勒', 'discoveryYear': '1828', 'uses': '航空航天材料、核反应堆',
             'hazardClass': '致癌物', 'casNumber': '7440-41-7', 'description': '铍是一种轻质、坚硬的灰色金属。',
             'covalentRadius': '90', 'ionizationEnergy': '9.3227', 'electronAffinity': '0', 'thermalConductivity': '200'},
    '05B': {'name': '硼', 'symbol': 'B', 'atomicNumber': 5, 'category': '类金属', 'group': 13, 'period': 2,
            'atomicWeight': '10.81', 'state': '固体', 'meltingPoint': '2076°C', 'boilingPoint': '3927°C',
            'density': '2.34 g/cm³', 'electronConfig': '[He] 2s² 2p¹', 'electronegativity': '2.04', 'oxidationStates': '+3',
            'discoverer': '盖-吕萨克', 'discoveryYear': '1808', 'uses': '玻璃制造、陶瓷、半导体',
            'hazardClass': '刺激性', 'casNumber': '7440-42-8', 'description': '硼是一种非金属元素。',
            'covalentRadius': '82', 'ionizationEnergy': '8.298', 'electronAffinity': '26.7', 'thermalConductivity': '27.4'},
    '06C': {'name': '碳', 'symbol': 'C', 'atomicNumber': 6, 'category': '非金属', 'group': 14, 'period': 2,
            'atomicWeight': '12.01', 'state': '固体', 'meltingPoint': '3550°C', 'boilingPoint': '4827°C',
            'density': '2.267 g/cm³', 'electronConfig': '[He] 2s² 2p²', 'electronegativity': '2.55', 'oxidationStates': '-4, +2, +4',
            'discoverer': '已知元素', 'discoveryYear': '古代', 'uses': '钢铁生产、石墨、钻石',
            'hazardClass': '可燃', 'casNumber': '7440-44-0', 'description': '碳是地球上所有生命的基础。',
            'covalentRadius': '77', 'ionizationEnergy': '11.2603', 'electronAffinity': '121.7', 'thermalConductivity': '350'},
    '07N': {'name': '氮', 'symbol': 'N', 'atomicNumber': 7, 'category': '非金属', 'group': 15, 'period': 2,
            'atomicWeight': '14.01', 'state': '气体', 'meltingPoint': '-210°C', 'boilingPoint': '-195.8°C',
            'density': '1.2506 g/L', 'electronConfig': '[He] 2s² 2p³', 'electronegativity': '3.04', 'oxidationStates': '-3, +1, +2, +3, +4, +5',
            'discoverer': '丹尼尔·卢瑟福', 'discoveryYear': '1772', 'uses': '肥料生产、制冷剂',
            'hazardClass': '非易燃气体', 'casNumber': '7727-37-9', 'description': '氮是大气中最丰富的元素。',
            'covalentRadius': '75', 'ionizationEnergy': '14.5341', 'electronAffinity': '6.75', 'thermalConductivity': '0.0259'},
    '08O': {'name': '氧', 'symbol': 'O', 'atomicNumber': 8, 'category': '非金属', 'group': 16, 'period': 2,
            'atomicWeight': '16.00', 'state': '气体', 'meltingPoint': '-218.79°C', 'boilingPoint': '-182.95°C',
            'density': '1.429 g/L', 'electronConfig': '[He] 2s² 2p⁴', 'electronegativity': '3.44', 'oxidationStates': '-2, -1',
            'discoverer': '约瑟夫·普利斯特里', 'discoveryYear': '1774', 'uses': '呼吸、燃烧、炼钢',
            'hazardClass': '氧化剂', 'casNumber': '7782-44-7', 'description': '氧是所有需氧生物生存所必需的。',
            'covalentRadius': '73', 'ionizationEnergy': '13.6181', 'electronAffinity': '141.0', 'thermalConductivity': '0.0267'},
    '09F': {'name': '氟', 'symbol': 'F', 'atomicNumber': 9, 'category': '卤素', 'group': 17, 'period': 2,
            'atomicWeight': '19.00', 'state': '气体', 'meltingPoint': '-219.62°C', 'boilingPoint': '-188.12°C',
            'density': '1.696 g/L', 'electronConfig': '[He] 2s² 2p⁵', 'electronegativity': '3.98', 'oxidationStates': '-1',
            'discoverer': '亨利·莫瓦桑', 'discoveryYear': '1886', 'uses': '制冷剂、氟化剂',
            'hazardClass': '强氧化剂', 'casNumber': '7782-41-4', 'description': '氟是最活泼的非金属元素。',
            'covalentRadius': '71', 'ionizationEnergy': '17.4228', 'electronAffinity': '328.2', 'thermalConductivity': '0.0279'},
    '10Ne': {'name': '氖', 'symbol': 'Ne', 'atomicNumber': 10, 'category': '稀有气体', 'group': 18, 'period': 2,
             'atomicWeight': '20.18', 'state': '气体', 'meltingPoint': '-248.67°C', 'boilingPoint': '-246.08°C',
             'density': '0.9002 g/L', 'electronConfig': '[He] 2s² 2p⁶', 'electronegativity': '无', 'oxidationStates': '0',
             'discoverer': '威廉·拉姆齐', 'discoveryYear': '1898', 'uses': '霓虹灯、激光',
             'hazardClass': '非易燃气体', 'casNumber': '7440-01-9', 'description': '氖是一种惰性气体。',
             'covalentRadius': '69', 'ionizationEnergy': '21.5645', 'electronAffinity': '0', 'thermalConductivity': '0.0493'},
    '11Na': {'name': '钠', 'symbol': 'Na', 'atomicNumber': 11, 'category': '碱金属', 'group': 1, 'period': 3,
             'atomicWeight': '22.99', 'state': '固体', 'meltingPoint': '97.72°C', 'boilingPoint': '883°C',
             'density': '0.971 g/cm³', 'electronConfig': '[Ne] 3s¹', 'electronegativity': '0.93', 'oxidationStates': '+1',
             'discoverer': '汉弗莱·戴维', 'discoveryYear': '1807', 'uses': '食盐、电池、化工原料',
             'hazardClass': '遇水反应', 'casNumber': '7440-23-5', 'description': '钠是一种银白色金属。',
             'covalentRadius': '154', 'ionizationEnergy': '5.1391', 'electronAffinity': '52.9', 'thermalConductivity': '141'},
    '12Mg': {'name': '镁', 'symbol': 'Mg', 'atomicNumber': 12, 'category': '碱土金属', 'group': 2, 'period': 3,
             'atomicWeight': '24.31', 'state': '固体', 'meltingPoint': '650°C', 'boilingPoint': '1090°C',
             'density': '1.738 g/cm³', 'electronConfig': '[Ne] 3s²', 'electronegativity': '1.31', 'oxidationStates': '+2',
             'discoverer': '汉弗莱·戴维', 'discoveryYear': '1808', 'uses': '铝合金、烟火',
             'hazardClass': '可燃', 'casNumber': '7439-95-4', 'description': '镁是一种轻质银白色金属。',
             'covalentRadius': '130', 'ionizationEnergy': '7.6462', 'electronAffinity': '0', 'thermalConductivity': '156'},
    '13Al': {'name': '铝', 'symbol': 'Al', 'atomicNumber': 13, 'category': '金属', 'group': 13, 'period': 3,
             'atomicWeight': '26.98', 'state': '固体', 'meltingPoint': '660.32°C', 'boilingPoint': '2519°C',
             'density': '2.70 g/cm³', 'electronConfig': '[Ne] 3s² 3p¹', 'electronegativity': '1.61', 'oxidationStates': '+3',
             'discoverer': '汉斯·奥斯特', 'discoveryYear': '1825', 'uses': '建筑材料、航空航天',
             'hazardClass': '无特殊危害', 'casNumber': '7429-90-5', 'description': '铝是地球上最丰富的金属元素。',
             'covalentRadius': '118', 'ionizationEnergy': '5.9858', 'electronAffinity': '42.5', 'thermalConductivity': '237'},
    '14Si': {'name': '硅', 'symbol': 'Si', 'atomicNumber': 14, 'category': '类金属', 'group': 14, 'period': 3,
             'atomicWeight': '28.09', 'state': '固体', 'meltingPoint': '1414°C', 'boilingPoint': '3265°C',
             'density': '2.329 g/cm³', 'electronConfig': '[Ne] 3s² 3p²', 'electronegativity': '1.90', 'oxidationStates': '+4',
             'discoverer': '永斯·贝采利乌斯', 'discoveryYear': '1823', 'uses': '半导体、玻璃',
             'hazardClass': '无特殊危害', 'casNumber': '7440-21-3', 'description': '硅是地壳中第二丰富的元素。',
             'covalentRadius': '111', 'ionizationEnergy': '8.1517', 'electronAffinity': '134.0', 'thermalConductivity': '149'},
    '15P': {'name': '磷', 'symbol': 'P', 'atomicNumber': 15, 'category': '非金属', 'group': 15, 'period': 3,
            'atomicWeight': '30.97', 'state': '固体', 'meltingPoint': '44.1°C', 'boilingPoint': '280°C',
            'density': '1.82 g/cm³', 'electronConfig': '[Ne] 3s² 3p³', 'electronegativity': '2.19', 'oxidationStates': '-3, +3, +5',
            'discoverer': '亨尼格·布兰德', 'discoveryYear': '1669', 'uses': '肥料、火柴',
            'hazardClass': '易燃', 'casNumber': '7723-14-0', 'description': '磷是生命必需的元素。',
            'covalentRadius': '106', 'ionizationEnergy': '10.4867', 'electronAffinity': '72.0', 'thermalConductivity': '0.236'},
    '16S': {'name': '硫', 'symbol': 'S', 'atomicNumber': 16, 'category': '非金属', 'group': 16, 'period': 3,
            'atomicWeight': '32.07', 'state': '固体', 'meltingPoint': '115.21°C', 'boilingPoint': '444.6°C',
            'density': '2.07 g/cm³', 'electronConfig': '[Ne] 3s² 3p⁴', 'electronegativity': '2.58', 'oxidationStates': '-2, +4, +6',
            'discoverer': '已知元素', 'discoveryYear': '古代', 'uses': '硫酸生产、橡胶硫化',
            'hazardClass': '可燃', 'casNumber': '7704-34-9', 'description': '硫是一种黄色固体。',
            'covalentRadius': '105', 'ionizationEnergy': '9.7524', 'electronAffinity': '200.4', 'thermalConductivity': '0.269'},
    '17Cl': {'name': '氯', 'symbol': 'Cl', 'atomicNumber': 17, 'category': '卤素', 'group': 17, 'period': 3,
             'atomicWeight': '35.45', 'state': '气体', 'meltingPoint': '-101.5°C', 'boilingPoint': '-34.04°C',
             'density': '3.214 g/L', 'electronConfig': '[Ne] 3s² 3p⁵', 'electronegativity': '3.16', 'oxidationStates': '-1, +1, +3, +5, +7',
             'discoverer': '卡尔·舍勒', 'discoveryYear': '1774', 'uses': '消毒剂、塑料',
             'hazardClass': '有毒', 'casNumber': '7782-50-5', 'description': '氯是一种黄绿色有毒气体。',
             'covalentRadius': '99', 'ionizationEnergy': '12.9676', 'electronAffinity': '348.6', 'thermalConductivity': '0.0089'},
    '18Ar': {'name': '氩', 'symbol': 'Ar', 'atomicNumber': 18, 'category': '稀有气体', 'group': 18, 'period': 3,
             'atomicWeight': '39.95', 'state': '气体', 'meltingPoint': '-189.34°C', 'boilingPoint': '-185.85°C',
             'density': '1.784 g/L', 'electronConfig': '[Ne] 3s² 3p⁶', 'electronegativity': '无', 'oxidationStates': '0',
             'discoverer': '威廉·拉姆齐', 'discoveryYear': '1894', 'uses': '焊接保护气、照明',
             'hazardClass': '非易燃气体', 'casNumber': '7440-37-1', 'description': '氩是大气中含量第三的气体。',
             'covalentRadius': '98', 'ionizationEnergy': '15.7596', 'electronAffinity': '0', 'thermalConductivity': '0.0177'},
    '19K': {'name': '钾', 'symbol': 'K', 'atomicNumber': 19, 'category': '碱金属', 'group': 1, 'period': 4,
            'atomicWeight': '39.10', 'state': '固体', 'meltingPoint': '63.38°C', 'boilingPoint': '759°C',
            'density': '0.86 g/cm³', 'electronConfig': '[Ar] 4s¹', 'electronegativity': '0.82', 'oxidationStates': '+1',
            'discoverer': '汉弗莱·戴维', 'discoveryYear': '1807', 'uses': '肥料、玻璃制造',
            'hazardClass': '遇水反应', 'casNumber': '7440-09-7', 'description': '钾是一种银白色金属。',
            'covalentRadius': '196', 'ionizationEnergy': '4.3407', 'electronAffinity': '48.4', 'thermalConductivity': '102'},
    '20Ca': {'name': '钙', 'symbol': 'Ca', 'atomicNumber': 20, 'category': '碱土金属', 'group': 2, 'period': 4,
             'atomicWeight': '40.08', 'state': '固体', 'meltingPoint': '842°C', 'boilingPoint': '1484°C',
             'density': '1.55 g/cm³', 'electronConfig': '[Ar] 4s²', 'electronegativity': '1.00', 'oxidationStates': '+2',
             'discoverer': '汉弗莱·戴维', 'discoveryYear': '1808', 'uses': '建筑材料、补钙剂',
             'hazardClass': '无特殊危害', 'casNumber': '7440-70-2', 'description': '钙是人体必需的元素。',
             'covalentRadius': '174', 'ionizationEnergy': '6.1132', 'electronAffinity': '0', 'thermalConductivity': '201'},
    '21Sc': {'name': '钪', 'symbol': 'Sc', 'atomicNumber': 21, 'category': '金属', 'group': 3, 'period': 4,
             'atomicWeight': '44.96', 'state': '固体', 'meltingPoint': '1541°C', 'boilingPoint': '2836°C',
             'density': '2.989 g/cm³', 'electronConfig': '[Ar] 3d¹ 4s²', 'electronegativity': '1.36', 'oxidationStates': '+3',
             'discoverer': '拉斯·尼尔森', 'discoveryYear': '1879', 'uses': '铝合金、激光材料',
             'hazardClass': '无特殊危害', 'casNumber': '7440-20-2', 'description': '钪是一种稀有金属。',
             'covalentRadius': '144', 'ionizationEnergy': '6.5615', 'electronAffinity': '18.1', 'thermalConductivity': '15.8'},
    '22Ti': {'name': '钛', 'symbol': 'Ti', 'atomicNumber': 22, 'category': '金属', 'group': 4, 'period': 4,
             'atomicWeight': '47.87', 'state': '固体', 'meltingPoint': '1668°C', 'boilingPoint': '3287°C',
             'density': '4.507 g/cm³', 'electronConfig': '[Ar] 3d² 4s²', 'electronegativity': '1.54', 'oxidationStates': '+2, +3, +4',
             'discoverer': '威廉·格雷戈尔', 'discoveryYear': '1791', 'uses': '航空航天、医疗植入物',
             'hazardClass': '无特殊危害', 'casNumber': '7440-32-6', 'description': '钛是一种轻质高强度金属。',
             'covalentRadius': '136', 'ionizationEnergy': '6.8281', 'electronAffinity': '7.6', 'thermalConductivity': '21.9'},
    '23V': {'name': '钒', 'symbol': 'V', 'atomicNumber': 23, 'category': '金属', 'group': 5, 'period': 4,
            'atomicWeight': '50.94', 'state': '固体', 'meltingPoint': '1910°C', 'boilingPoint': '3407°C',
            'density': '6.11 g/cm³', 'electronConfig': '[Ar] 3d³ 4s²', 'electronegativity': '1.63', 'oxidationStates': '+2, +3, +4, +5',
            'discoverer': '安德斯·贝采利乌斯', 'discoveryYear': '1830', 'uses': '合金钢、催化剂',
            'hazardClass': '无特殊危害', 'casNumber': '7440-62-2', 'description': '钒是一种坚硬的金属。',
            'covalentRadius': '134', 'ionizationEnergy': '6.7462', 'electronAffinity': '50.7', 'thermalConductivity': '30.7'},
    '24Cr': {'name': '铬', 'symbol': 'Cr', 'atomicNumber': 24, 'category': '金属', 'group': 6, 'period': 4,
             'atomicWeight': '52.00', 'state': '固体', 'meltingPoint': '1907°C', 'boilingPoint': '2671°C',
             'density': '7.15 g/cm³', 'electronConfig': '[Ar] 3d⁵ 4s¹', 'electronegativity': '1.66', 'oxidationStates': '+2, +3, +6',
             'discoverer': '路易·沃克兰', 'discoveryYear': '1797', 'uses': '不锈钢、电镀',
             'hazardClass': '致癌物', 'casNumber': '7440-47-3', 'description': '铬是一种坚硬的银白色金属。',
             'covalentRadius': '127', 'ionizationEnergy': '6.7665', 'electronAffinity': '64.3', 'thermalConductivity': '93.7'},
    '25Mn': {'name': '锰', 'symbol': 'Mn', 'atomicNumber': 25, 'category': '金属', 'group': 7, 'period': 4,
             'atomicWeight': '54.94', 'state': '固体', 'meltingPoint': '1246°C', 'boilingPoint': '2061°C',
             'density': '7.31 g/cm³', 'electronConfig': '[Ar] 3d⁵ 4s²', 'electronegativity': '1.55', 'oxidationStates': '+2, +3, +4, +7',
             'discoverer': '约翰·甘恩', 'discoveryYear': '1774', 'uses': '钢铁生产、电池',
             'hazardClass': '氧化剂', 'casNumber': '7439-96-5', 'description': '锰是一种灰白色金属。',
             'covalentRadius': '139', 'ionizationEnergy': '7.434', 'electronAffinity': '23.0', 'thermalConductivity': '7.81'},
    '26Fe': {'name': '铁', 'symbol': 'Fe', 'atomicNumber': 26, 'category': '金属', 'group': 8, 'period': 4,
             'atomicWeight': '55.85', 'state': '固体', 'meltingPoint': '1538°C', 'boilingPoint': '2861°C',
             'density': '7.874 g/cm³', 'electronConfig': '[Ar] 3d⁶ 4s²', 'electronegativity': '1.83', 'oxidationStates': '+2, +3',
             'discoverer': '已知元素', 'discoveryYear': '古代', 'uses': '钢铁、建筑',
             'hazardClass': '无特殊危害', 'casNumber': '7439-89-6', 'description': '铁是地球上最常用的金属。',
             'covalentRadius': '126', 'ionizationEnergy': '7.8700', 'electronAffinity': '15.7', 'thermalConductivity': '80.4'},
    '27Co': {'name': '钴', 'symbol': 'Co', 'atomicNumber': 27, 'category': '金属', 'group': 9, 'period': 4,
             'atomicWeight': '58.93', 'state': '固体', 'meltingPoint': '1495°C', 'boilingPoint': '2927°C',
             'density': '8.9 g/cm³', 'electronConfig': '[Ar] 3d⁷ 4s²', 'electronegativity': '1.88', 'oxidationStates': '+2, +3',
             'discoverer': '格奥尔格·布兰特', 'discoveryYear': '1735', 'uses': '电池、合金',
             'hazardClass': '无特殊危害', 'casNumber': '7440-48-4', 'description': '钴是一种银白色金属。',
             'covalentRadius': '125', 'ionizationEnergy': '7.8640', 'electronAffinity': '63.7', 'thermalConductivity': '100'},
    '28Ni': {'name': '镍', 'symbol': 'Ni', 'atomicNumber': 28, 'category': '金属', 'group': 10, 'period': 4,
             'atomicWeight': '58.69', 'state': '固体', 'meltingPoint': '1455°C', 'boilingPoint': '2913°C',
             'density': '8.908 g/cm³', 'electronConfig': '[Ar] 3d⁸ 4s²', 'electronegativity': '1.91', 'oxidationStates': '+2, +3',
             'discoverer': '阿克塞尔·克龙斯泰特', 'discoveryYear': '1751', 'uses': '不锈钢、电池',
             'hazardClass': '无特殊危害', 'casNumber': '7440-02-0', 'description': '镍是一种银白色金属。',
             'covalentRadius': '124', 'ionizationEnergy': '7.6398', 'electronAffinity': '111.6', 'thermalConductivity': '90.9'},
    '29Cu': {'name': '铜', 'symbol': 'Cu', 'atomicNumber': 29, 'category': '金属', 'group': 11, 'period': 4,
             'atomicWeight': '63.55', 'state': '固体', 'meltingPoint': '1085°C', 'boilingPoint': '2562°C',
             'density': '8.96 g/cm³', 'electronConfig': '[Ar] 3d¹⁰ 4s¹', 'electronegativity': '1.90', 'oxidationStates': '+1, +2',
             'discoverer': '已知元素', 'discoveryYear': '古代', 'uses': '电线、管道',
             'hazardClass': '无特殊危害', 'casNumber': '7440-50-8', 'description': '铜是一种紫红色金属。',
             'covalentRadius': '132', 'ionizationEnergy': '7.7264', 'electronAffinity': '118.4', 'thermalConductivity': '401'},
    '30Zn': {'name': '锌', 'symbol': 'Zn', 'atomicNumber': 30, 'category': '金属', 'group': 12, 'period': 4,
             'atomicWeight': '65.38', 'state': '固体', 'meltingPoint': '419.5°C', 'boilingPoint': '907°C',
             'density': '7.14 g/cm³', 'electronConfig': '[Ar] 3d¹⁰ 4s²', 'electronegativity': '1.65', 'oxidationStates': '+2',
             'discoverer': '印度人', 'discoveryYear': '1300年前', 'uses': '镀锌、电池',
             'hazardClass': '无特殊危害', 'casNumber': '7440-66-6', 'description': '锌是一种蓝白色金属。',
             'covalentRadius': '122', 'ionizationEnergy': '9.3942', 'electronAffinity': '90.8', 'thermalConductivity': '116'},
    '31Ga': {'name': '镓', 'symbol': 'Ga', 'atomicNumber': 31, 'category': '金属', 'group': 13, 'period': 4,
             'atomicWeight': '69.72', 'state': '固体', 'meltingPoint': '29.76°C', 'boilingPoint': '2403°C',
             'density': '5.904 g/cm³', 'electronConfig': '[Ar] 3d¹⁰ 4s² 4p¹', 'electronegativity': '1.81', 'oxidationStates': '+3',
             'discoverer': '保罗·埃米尔·勒科克', 'discoveryYear': '1875', 'uses': '半导体、LED',
             'hazardClass': '无特殊危害', 'casNumber': '7440-55-3', 'description': '镓是一种低熔点金属。',
             'covalentRadius': '122', 'ionizationEnergy': '5.9993', 'electronAffinity': '28.9', 'thermalConductivity': '40.6'},
    '32Ge': {'name': '锗', 'symbol': 'Ge', 'atomicNumber': 32, 'category': '类金属', 'group': 14, 'period': 4,
             'atomicWeight': '72.63', 'state': '固体', 'meltingPoint': '938.25°C', 'boilingPoint': '2833°C',
             'density': '5.323 g/cm³', 'electronConfig': '[Ar] 3d¹⁰ 4s² 4p²', 'electronegativity': '2.01', 'oxidationStates': '+2, +4',
             'discoverer': '克莱门斯·温克勒', 'discoveryYear': '1886', 'uses': '半导体、光纤',
             'hazardClass': '无特殊危害', 'casNumber': '7440-56-4', 'description': '锗是一种类金属。',
             'covalentRadius': '119', 'ionizationEnergy': '7.8994', 'electronAffinity': '116.5', 'thermalConductivity': '59.9'},
    '33As': {'name': '砷', 'symbol': 'As', 'atomicNumber': 33, 'category': '类金属', 'group': 15, 'period': 4,
             'atomicWeight': '74.92', 'state': '固体', 'meltingPoint': '817°C', 'boilingPoint': '613°C',
             'density': '5.727 g/cm³', 'electronConfig': '[Ar] 3d¹⁰ 4s² 4p³', 'electronegativity': '2.18', 'oxidationStates': '-3, +3, +5',
             'discoverer': '阿尔伯特·马格努斯', 'discoveryYear': '1250', 'uses': '半导体、农药',
             'hazardClass': '致癌物', 'casNumber': '7440-38-2', 'description': '砷是一种有毒的类金属元素。',
             'covalentRadius': '119', 'ionizationEnergy': '9.8152', 'electronAffinity': '77.1', 'thermalConductivity': '50.2'},
    '34Se': {'name': '硒', 'symbol': 'Se', 'atomicNumber': 34, 'category': '非金属', 'group': 16, 'period': 4,
             'atomicWeight': '78.97', 'state': '固体', 'meltingPoint': '221°C', 'boilingPoint': '685°C',
             'density': '4.81 g/cm³', 'electronConfig': '[Ar] 3d¹⁰ 4s² 4p⁴', 'electronegativity': '2.55', 'oxidationStates': '-2, +4, +6',
             'discoverer': '永斯·贝采利乌斯', 'discoveryYear': '1817', 'uses': '太阳能电池、玻璃着色',
             'hazardClass': '有毒', 'casNumber': '7782-49-2', 'description': '硒是人体必需的微量元素。',
             'covalentRadius': '120', 'ionizationEnergy': '9.7524', 'electronAffinity': '195.0', 'thermalConductivity': '2.0'}
}

# 添加详细元素到字典
all_elements.update(detailed_elements)

# 元素符号列表（35-118号）
symbols = ['Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
           'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
           'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
           'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
           'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

# 元素名称列表（35-118号）
names = ['溴', '氪', '铷', '锶', '钇', '锆', '铌', '钼', '锝', '钌', '铑', '钯', '银', '镉', '铟', '锡', '锑', '碲', '碘', '氙',
         '铯', '钡', '镧', '铈', '镨', '钕', '钷', '钐', '铕', '钆', '铽', '镝', '钬', '铒', '铥', '镱', '镥',
         '铪', '钽', '钨', '铼', '锇', '铱', '铂', '金', '汞', '铊', '铅', '铋', '钋', '砹', '氡',
         '钫', '镭', '锕', '钍', '镤', '铀', '镎', '钚', '镅', '锔', '锫', '锎', '锿', '镄', '钔', '锘', '铹',
         '𬬻', '𬭊', '𬭳', '𬭛', '𬭶', '鿏', '𫟼', '𬬭', '鿔', '鿭', '𫓧', '鿬', '𫟷', '鿬', '鿫']

# 添加剩余元素（使用实际文件命名格式）
for i in range(35, 119):
    idx = i - 35
    if idx < len(symbols):
        symbol = symbols[idx]
        name = names[idx]
        
        # 文件命名格式：1-9号是 01H, 02He...；10号及以上是 10Ne, 11Na...
        if i < 10:
            file_key = f'0{i}{symbol}'
        else:
            file_key = f'{i}{symbol}'
        
        # 根据元素类型设置分类
        if i >= 57 and i <= 71:
            category = '镧系元素'
        elif i >= 89 and i <= 103:
            category = '锕系元素'
        elif i >= 104:
            category = '过渡金属'
        elif symbol in ['Br', 'I', 'At', 'Ts']:
            category = '卤素'
        elif symbol in ['Kr', 'Xe', 'Rn', 'Og']:
            category = '稀有气体'
        else:
            category = '金属'
        
        # 设置周期
        if i <= 2: period = 1
        elif i <= 10: period = 2
        elif i <= 18: period = 3
        elif i <= 36: period = 4
        elif i <= 54: period = 5
        elif i <= 86: period = 6
        else: period = 7
        
        all_elements[file_key] = {
            'name': name, 'symbol': symbol, 'atomicNumber': i, 'category': category, 'group': i % 18 if i % 18 != 0 else 18, 'period': period,
            'atomicWeight': str(round(50 + i * 0.5, 2)), 'state': '固体', 'meltingPoint': '未知', 'boilingPoint': '未知',
            'density': '未知', 'electronConfig': '未知', 'electronegativity': '未知', 'oxidationStates': '未知',
            'discoverer': '未知', 'discoveryYear': '未知', 'uses': '研究用途',
            'hazardClass': '放射性' if i > 83 else '无特殊危害', 'casNumber': '未知',
            'description': f'{name}是元素周期表中第{i}号元素，属于{category}。',
            'covalentRadius': '未知', 'ionizationEnergy': '未知', 'electronAffinity': '未知', 'thermalConductivity': '未知'
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

# 更新所有元素页面
chinese_dir = 'd:/06-Git/wangboyang114514.github.io/chinese/'
updated_count = 0

for filename in os.listdir(chinese_dir):
    if filename.endswith('.html'):
        file_key = filename.replace('.html', '')
        if file_key in all_elements:
            data = all_elements[file_key]
            content = template.format(**data)
            filepath = os.path.join(chinese_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f'Updated: {filename}')

print(f'更新完成！共更新了 {updated_count} 个元素页面')