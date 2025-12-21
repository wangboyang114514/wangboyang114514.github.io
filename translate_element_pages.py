import os
import re
from string import Template

# 元素名称中英文对照字典
element_names = {
    'Hydrogen': '氢',
    'Helium': '氦',
    'Lithium': '锂',
    'Beryllium': '铍',
    'Boron': '硼',
    'Carbon': '碳',
    'Nitrogen': '氮',
    'Oxygen': '氧',
    'Fluorine': '氟',
    'Neon': '氖',
    'Sodium': '钠',
    'Magnesium': '镁',
    'Aluminum': '铝',
    'Silicon': '硅',
    'Phosphorus': '磷',
    'Sulfur': '硫',
    'Chlorine': '氯',
    'Argon': '氩',
    'Potassium': '钾',
    'Calcium': '钙',
    'Scandium': '钪',
    'Titanium': '钛',
    'Vanadium': '钒',
    'Chromium': '铬',
    'Manganese': '锰',
    'Iron': '铁',
    'Cobalt': '钴',
    'Nickel': '镍',
    'Copper': '铜',
    'Zinc': '锌',
    'Gallium': '镓',
    'Germanium': '锗',
    'Arsenic': '砷',
    'Selenium': '硒',
    'Bromine': '溴',
    'Krypton': '氪',
    'Rubidium': '铷',
    'Strontium': '锶',
    'Yttrium': '钇',
    'Zirconium': '锆',
    'Niobium': '铌',
    'Molybdenum': '钼',
    'Technetium': '锝',
    'Ruthenium': '钌',
    'Rhodium': '铑',
    'Palladium': '钯',
    'Silver': '银',
    'Cadmium': '镉',
    'Indium': '铟',
    'Tin': '锡',
    'Antimony': '锑',
    'Tellurium': '碲',
    'Iodine': '碘',
    'Xenon': '氙',
    'Cesium': '铯',
    'Barium': '钡',
    'Lanthanum': '镧',
    'Cerium': '铈',
    'Praseodymium': '镨',
    'Neodymium': '钕',
    'Promethium': '钷',
    'Samarium': '钐',
    'Europium': '铕',
    'Gadolinium': '钆',
    'Terbium': '铽',
    'Dysprosium': '镝',
    'Holmium': '钬',
    'Erbium': '铒',
    'Thulium': '铥',
    'Ytterbium': '镱',
    'Lutetium': '镥',
    'Hafnium': '铪',
    'Tantalum': '钽',
    'Tungsten': '钨',
    'Rhenium': '铼',
    'Osmium': '锇',
    'Iridium': '铱',
    'Platinum': '铂',
    'Gold': '金',
    'Mercury': '汞',
    'Thallium': '铊',
    'Lead': '铅',
    'Bismuth': '铋',
    'Polonium': '钋',
    'Astatine': '砹',
    'Radon': '氡',
    'Francium': '钫',
    'Radium': '镭',
    'Actinium': '锕',
    'Thorium': '钍',
    'Protactinium': '镤',
    'Uranium': '铀',
    'Neptunium': '镎',
    'Plutonium': '钚',
    'Americium': '镅',
    'Curium': '锔',
    'Berkelium': '锫',
    'Californium': '锎',
    'Einsteinium': '锿',
    'Fermium': '镄',
    'Mendelevium': '钔',
    'Nobelium': '锘',
    'Lawrencium': '铹',
    'Rutherfordium': '𬬻',
    'Dubnium': '𬭊',
    'Seaborgium': '𬭳',
    'Bohrium': '𬭛',
    'Hassium': '𬭶',
    'Meitnerium': '鿏',
    'Darmstadtium': '𫟼',
    'Roentgenium': '𬬭',
    'Copernicium': '鿔',
    'Nihonium': '鿭',
    'Flerovium': '𫓧',
    'Moscovium': '镆',
    'Livermorium': '𫟷',
    'Tennessine': '鿬',
    'Oganesson': '鿫'
}

# 元素名称到元素符号的映射字典
element_symbols = {
    'Hydrogen': 'H',
    'Helium': 'He',
    'Lithium': 'Li',
    'Beryllium': 'Be',
    'Boron': 'B',
    'Carbon': 'C',
    'Nitrogen': 'N',
    'Oxygen': 'O',
    'Fluorine': 'F',
    'Neon': 'Ne',
    'Sodium': 'Na',
    'Magnesium': 'Mg',
    'Aluminum': 'Al',
    'Silicon': 'Si',
    'Phosphorus': 'P',
    'Sulfur': 'S',
    'Chlorine': 'Cl',
    'Argon': 'Ar',
    'Potassium': 'K',
    'Calcium': 'Ca',
    'Scandium': 'Sc',
    'Titanium': 'Ti',
    'Vanadium': 'V',
    'Chromium': 'Cr',
    'Manganese': 'Mn',
    'Iron': 'Fe',
    'Cobalt': 'Co',
    'Nickel': 'Ni',
    'Copper': 'Cu',
    'Zinc': 'Zn',
    'Gallium': 'Ga',
    'Germanium': 'Ge',
    'Arsenic': 'As',
    'Selenium': 'Se',
    'Bromine': 'Br',
    'Krypton': 'Kr',
    'Rubidium': 'Rb',
    'Strontium': 'Sr',
    'Yttrium': 'Y',
    'Zirconium': 'Zr',
    'Niobium': 'Nb',
    'Molybdenum': 'Mo',
    'Technetium': 'Tc',
    'Ruthenium': 'Ru',
    'Rhodium': 'Rh',
    'Palladium': 'Pd',
    'Silver': 'Ag',
    'Cadmium': 'Cd',
    'Indium': 'In',
    'Tin': 'Sn',
    'Antimony': 'Sb',
    'Tellurium': 'Te',
    'Iodine': 'I',
    'Xenon': 'Xe',
    'Cesium': 'Cs',
    'Barium': 'Ba',
    'Lanthanum': 'La',
    'Cerium': 'Ce',
    'Praseodymium': 'Pr',
    'Neodymium': 'Nd',
    'Promethium': 'Pm',
    'Samarium': 'Sm',
    'Europium': 'Eu',
    'Gadolinium': 'Gd',
    'Terbium': 'Tb',
    'Dysprosium': 'Dy',
    'Holmium': 'Ho',
    'Erbium': 'Er',
    'Thulium': 'Tm',
    'Ytterbium': 'Yb',
    'Lutetium': 'Lu',
    'Hafnium': 'Hf',
    'Tantalum': 'Ta',
    'Tungsten': 'W',
    'Rhenium': 'Re',
    'Osmium': 'Os',
    'Iridium': 'Ir',
    'Platinum': 'Pt',
    'Gold': 'Au',
    'Mercury': 'Hg',
    'Thallium': 'Tl',
    'Lead': 'Pb',
    'Bismuth': 'Bi',
    'Polonium': 'Po',
    'Astatine': 'At',
    'Radon': 'Rn',
    'Francium': 'Fr',
    'Radium': 'Ra',
    'Actinium': 'Ac',
    'Thorium': 'Th',
    'Protactinium': 'Pa',
    'Uranium': 'U',
    'Neptunium': 'Np',
    'Plutonium': 'Pu',
    'Americium': 'Am',
    'Curium': 'Cm',
    'Berkelium': 'Bk',
    'Californium': 'Cf',
    'Einsteinium': 'Es',
    'Fermium': 'Fm',
    'Mendelevium': 'Md',
    'Nobelium': 'No',
    'Lawrencium': 'Lr',
    'Rutherfordium': 'Rf',
    'Dubnium': 'Db',
    'Seaborgium': 'Sg',
    'Bohrium': 'Bh',
    'Hassium': 'Hs',
    'Meitnerium': 'Mt',
    'Darmstadtium': 'Ds',
    'Roentgenium': 'Rg',
    'Copernicium': 'Cn',
    'Nihonium': 'Nh',
    'Flerovium': 'Fl',
    'Moscovium': 'Mc',
    'Livermorium': 'Lv',
    'Tennessine': 'Ts',
    'Oganesson': 'Og'
}

# 读取英文页面内容并提取信息
def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else ''
    
    # 提取主要内容
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    h1 = h1_match.group(1) if h1_match else ''
    
    # 提取危险类别（只提取英文页面的信息）
    safety_match = re.search(r'<strong>Hazard Class:</strong>(.*?)</p>', content, re.DOTALL)
    safety = safety_match.group(1).strip() if safety_match else ''
    
    # 提取分子式
    formula_match = re.search(r'<strong>Formula:</strong>(.*?)</p>', content)
    formula = formula_match.group(1).strip() if formula_match else ''
    
    # 提取分子量
    weight_match = re.search(r'<strong>Molecular Weight:</strong>(.*?)</p>', content)
    weight = weight_match.group(1).strip() if weight_match else ''
    
    # 提取CAS号
    cas_match = re.search(r'<strong>CAS Number:</strong>(.*?)</p>', content)
    cas = cas_match.group(1).strip() if cas_match else ''
    
    # 提取同义词
    synonyms_match = re.search(r'<strong>Synonyms:</strong>(.*?)</p>', content)
    synonyms = synonyms_match.group(1).strip() if synonyms_match else ''
    
    # 提取创建日期
    creation_match = re.search(r'<strong>Creation Date:</strong>(.*?)</p>', content)
    creation = creation_match.group(1).strip() if creation_match else ''
    
    # 提取描述
    description_match = re.search(r'<div class="element-description">(.*?)</div>', content, re.DOTALL)
    if description_match:
        description_html = description_match.group(1)
        # 提取描述文本
        p_match = re.search(r'<p>(.*?)</p>', description_html, re.DOTALL)
        description = p_match.group(1).strip() if p_match else ''
    else:
        description = ''
    
    # 清理提取的信息
    def clean_text(text):
        if isinstance(text, str):
            return text.strip().replace('\n', '').replace('\r', '')
        return text
    
    return {
        'title': clean_text(title),
        'h1': clean_text(h1),
        'safety': clean_text(safety),
        'formula': clean_text(formula),
        'weight': clean_text(weight),
        'cas': clean_text(cas),
        'synonyms': clean_text(synonyms),
        'creation': clean_text(creation),
        'description': clean_text(description)
    }

# 翻译默认值
def translate_default(value):
    # 确保输入值是字符串
    if not isinstance(value, str):
        return value
    
    # 移除首尾空白字符和可能的换行符
    value = value.strip().replace('\n', '').replace('\r', '')
    
    translations = {
        'No special hazard information': '无特殊危害信息',
        'No CAS number': '无CAS号',
        'No synonyms': '无同义词'
    }
    
    # 检查是否有完全匹配的翻译（不区分大小写）
    value_lower = value.lower()
    for en, zh in translations.items():
        if value_lower == en.lower():
            return zh
    
    # 如果没有完全匹配，尝试部分匹配
    if 'no special hazard information' in value_lower:
        return '无特殊危害信息'
    if 'no cas number' in value_lower:
        return '无CAS号'
    if 'no synonyms' in value_lower:
        return '无同义词'
    
    return value

# 简单的描述翻译
def translate_description(text):
    # 确保输入值是字符串
    if not isinstance(text, str):
        return text
    
    # 移除可能的换行符和多余空格
    text = text.replace('\n', ' ').replace('\r', ' ').strip()
    
    # 定义一些完整句子的翻译，这样可以保证翻译的准确性
    full_sentence_translations = {
        # 氢元素
        'Colourless, odourless gaseous chemical element. Lightest and most abundant element in the universe. Present in water and in all organic compounds. Chemically reacts with most elements. Discovered by Henry Cavendish in 1776.':
        '无色、无味的气态化学元素。宇宙中最轻、最丰富的元素。存在于水和所有有机化合物中。能与大多数元素发生化学反应。由亨利·卡文迪许于1776年发现。',
        
        # 碳元素
        'Carbon is a member of group 14 of the periodic table. It has three allotropic forms of it, diamonds, graphite and fullerite. Carbon-14 is commonly used in radioactive dating. Carbon occurs in all organic life and is the basis of organic chemistry. Carbon has the interesting chemical property of being able to bond with itself, and a wide variety of other elements.':
        '碳是元素周期表第14族的成员。它有三种同素异形体：金刚石、石墨和富勒烯。碳-14常用于放射性测年。碳存在于所有有机生命中，是有机化学的基础。碳具有能够与自身以及多种其他元素结合的有趣化学性质。',
        
        # 氧元素
        'A colourless, odourless gaseous element belonging to group 16 of the periodic table. It is the most abundant element present in the earth\'s crust. It also makes up 20.8% of the Earth\'s atmosphere. For industrial purposes, it is separated from liquid air by fractional distillation. It is used in high temperature welding, and in breathing. It commonly comes in the form of Oxygen, but is found as Ozone in the upper atmosphere. It was discovered by Priestley in 1774.':
        '一种属于元素周期表第16族的无色、无味气态元素。它是地壳中含量最丰富的元素，也占地球大气的20.8%。工业上通过液态空气的分馏分离得到。用于高温焊接和呼吸。通常以氧气形式存在，但在上层大气中以臭氧形式存在。由普里斯特利于1774年发现。',
        
        # 硼元素
        'An element of group 13 of the periodic table. There are two allotropes, amorphous boron is a brown power, but metallic boron is black. The metallic form is hard (9.3 on Mohs\' scale) and a bad conductor in room temperatures. It is never found free in nature. Boron-10 is used in nuclear reactor control rods and shields. It was discovered in 1808 by Sir Humphry Davy and by J.L. Gay-Lussac and L.J. Thenard.':
        '周期表中第13族元素。有两种同素异形体，无定形硼是棕色粉末，而金属硼是黑色的。金属形式的硼质地坚硬（莫氏硬度9.3），在室温下是不良导体。它从未在自然界中以游离态存在。硼-10用于核反应堆的控制棒和屏蔽材料。它于1808年由汉弗里·戴维爵士、J.L.盖-吕萨克和L.J.泰纳尔发现。',
        
        # 氮元素
        'Colourless, gaseous element which belongs to group 15 of the periodic table. Constitutes ~78% of the atmosphere and is an essential part of the ecosystem. Nitrogen for industrial purposes is acquired by the fractional distillation of liquid air. Chemically inactive, reactive generally only at high temperatures or in electrical discharges. It was discovered in 1772 by D. Rutherford.':
        '属于周期表第15族的无色气体元素。约占大气的78%，是生态系统的重要组成部分。工业用途的氮通过液态空气的分馏获取。化学性质不活泼，通常仅在高温或放电条件下具有反应性。它于1772年由D.卢瑟福发现。',
        
        # 氦元素
        'A colourless, odourless, inert, gaseous chemical element belonging to group 18 of the periodic table. It is the second lightest and second most abundant element in the universe, making up about 24% of the universe\'s elemental mass. It is extracted from natural gas fields. It is used in cryogenics, deep-sea breathing systems, balloons, and as a protective gas in arc welding and growing silicon crystals.':
        '一种属于元素周期表第18族的无色、无味、惰性气态化学元素。它是宇宙中第二轻和第二丰富的元素，约占宇宙元素质量的24%。从天然气田提取。用于低温学、深海呼吸系统、气球，以及作为电弧焊和硅晶体生长的保护气体。',
        
        # 锂元素
        'A soft, silvery-white metallic element belonging to group 1 of the periodic table. It is the lightest metal and the least dense solid element. It is used in rechargeable batteries, ceramics, glass, lubricants, and pharmaceuticals. It was discovered in 1817 by Johan August Arfwedson.':
        '一种属于元素周期表第1族的柔软、银白色金属元素。它是最轻的金属和密度最小的固体元素。用于充电电池、陶瓷、玻璃、润滑剂和药物。由约翰·奥古斯特·阿夫韦德森于1817年发现。',
        
        # 铍元素
        'A hard, grayish-white metallic element belonging to group 2 of the periodic table. It is light, strong, and has a high melting point. It is used in aerospace components, nuclear reactors, X-ray equipment, and as a moderator in some nuclear reactors. It was discovered in 1798 by Louis Nicolas Vauquelin.':
        '一种属于元素周期表第2族的坚硬、灰白色金属元素。它质轻、坚固，熔点高。用于航空航天部件、核反应堆、X射线设备，以及作为某些核反应堆的慢化剂。由路易斯·尼古拉·沃克兰于1798年发现。',
        
        # 氟元素
        'A poisonous pale yellow gaseous element belonging to group 17 of the periodic table (The halogens). It is the most chemically reactive and electronegative element. It is highly dangerous, causing severe chemical burns on contact with flesh. Fluorine was identified by Scheele in 1771 and first isolated by Moissan in 1886.':
        '一种有毒的淡黄色气态元素，属于元素周期表第17族（卤素）。它是化学反应性最强和电负性最高的元素。它具有高度危险性，与皮肤接触会造成严重的化学灼伤。氟元素由舍勒于1771年发现，由莫瓦桑于1886年首次分离。',
        
        # 钠元素
        'Soft silvery reactive element belonging to group 1 of the periodic table (alkali metals). It is highly reactive, oxidizing in air and reacting violently with water, forcing it to be kept under oil. It was first isolated by Humphrey Davy in 1807.':
        '一种柔软的银白色活性元素，属于元素周期表第1族（碱金属）。它具有高度反应性，在空气中会氧化，与水会剧烈反应，因此必须保存在油中。它由汉弗莱·戴维于1807年首次分离。',
        
        # 镁元素
        'Silvery metallic element belonging to group 2 of the periodic table (alkaline-earth metals). It is essential for living organisms, and is used in a number of light alloys. Chemically very reactive, it forms a protective oxide coating when exposed to air and burns with an intense white flame. It also reacts with sulphur, nitrogen and the halogens. First isolated by Bussy in 1828.':
        '一种银白色金属元素，属于元素周期表第2族（碱土金属）。它对生物体至关重要，用于多种轻合金。化学性质非常活泼，暴露在空气中会形成保护性氧化物涂层，燃烧时产生强烈的白色火焰。它还能与硫、氮和卤素反应。由布西于1828年首次分离。',
        
        # 铝元素
        'Silvery-white lustrous metallic element of group 3 of the periodic table. Highly reactive but protected by a thin transparent layer of the oxide which quickly forms in air. There are many alloys of aluminum, as well as a good number of industrial uses. Makes up 8.1% of the Earth\'s crust, by weight. Isolated in 1825 by H.C. Oersted.':
        '一种银白色有光泽的金属元素，属于元素周期表第3族。高度反应性，但受空气中迅速形成的一层薄而透明的氧化物保护。铝有许多合金，也有许多工业用途。按重量计占地球地壳的8.1%。由H.C.厄斯泰德于1825年分离。',
        
        # 硅元素
        'Metalloid element belonging to group 14 of the periodic table. It is the second most abundant element in the Earth\'s crust, making up 25.7% of it by weight. Chemically less reactive than carbon. First identified by Lavoisier in 1787 and first isolated in 1823 by Berzelius.':
        '一种类金属元素，属于元素周期表第14族。它是地球地壳中第二丰富的元素，按重量计占25.7%。化学性质比碳低。由拉瓦锡于1787年首次鉴定，由贝采利乌斯于1823年首次分离。',
        
        # 磷元素
        'Non-metallic element belonging to group 15 of the periodic table. Has a multiple allotropic forms. Essential element for living organisms. It was discovered by Brandt in 1669.':
        '一种非金属元素，属于元素周期表第15族。具有多种同素异形体。生物体的必需元素。由布兰特于1669年发现。',
        # 钾元素
        'Soft silvery metallic element belonging to group 1 of the periodic table (alkali metals). Occurs naturally in seawater and a many minerals. Highly reactive, chemically, it resembles sodium in its behavior and compounds. Discovered by Sir Humphry Davy in 1807.':
        '一种柔软的银白色金属元素，属于元素周期表第1族（碱金属）。天然存在于海水和多种矿物中。化学性质高度活泼，其行为和化合物与钠相似。由汉弗里·戴维爵士于1807年发现。',
        # 钙元素
        'Soft grey metallic element belonging to group 2 of the periodic table. Used a reducing agent in the extraction of thorium, zirconium and uranium. Essential element for living organisms.':
        '一种柔软的灰色金属元素，属于元素周期表第2族（碱土金属）。在钍、锆和铀的提取中用作还原剂。是生物体的必需元素。',
        # 铁元素
        'Silvery malleable and ductile metallic transition element. Has nine isotopes and is the fourth most abundant element in the earth\'s crust. Required by living organisms as a trace element (used in hemoglobin in humans.) Quite reactive, oxidizes in moist air, displaces hydrogen from dilute acids and combines with nonmetallic elements.':
        '一种银白色的有延展性和可锻性的金属过渡元素。有九种同位素，是地球地壳中第四丰富的元素。生物体需要它作为微量元素（在人类血红蛋白中使用）。相当活泼，在潮湿空气中氧化，从稀酸中置换氢，并与非金属元素结合。',
        # 铜元素
        'Red-brown transition element. Known by the Romans as \'cuprum.\' Extracted and used for thousands of years. Malleable, ductile and an excellent conductor of heat and electricity. When in moist conditions, a greenish layer forms on the outside.':
        '一种红棕色的过渡元素。罗马人称之为"cuprum"。已被提取和使用了数千年。具有延展性和可锻性，是热和电的优良导体。在潮湿条件下，外部会形成一层绿色的物质。',
        # 锌元素
        'Blue-white metallic element. Occurs in multiple compounds naturally. Five stable isotopes are six radioactive isotopes have been found. Chemically a reactive metal, combines with oxygen and other non-metals, reacts with dilute acids to release hydrogen.':
        '一种蓝白色金属元素。天然存在于多种化合物中。已发现五种稳定同位素和六种放射性同位素。化学上是一种活泼金属，能与氧和其他非金属结合，与稀酸反应释放出氢。',
        # 银元素
        'White lustrous soft metallic transition element. Found in both its elemental form and in minerals. Used in jewellery, tableware and so on. Less reactive than silver, chemically.':
        '一种白色有光泽的柔软金属过渡元素。以单质形式和矿物形式存在。用于珠宝、餐具等。化学上比银活泼性低。',
        # 氦元素（另一种描述）
        'Colourless, odourless gaseous nonmetallic element. Belongs to group 18 of the periodic table. Lowest boiling point of all elements and can only be solidified under pressure. Chemically inert, no known compounds. Discovered in the solar spectrum in 1868 by Lockyer.':
        '无色、无味的气态非金属元素。属于元素周期表第18族。所有元素中沸点最低，只能在压力下固化。化学性质不活泼，没有已知的化合物。1868年由洛克耶在太阳光谱中发现。',
        # 锂元素（另一种描述）
        'Socket silvery metal. First member of group 1 of the periodic table. Lithium salts are used in psychomedicine.':
        '一种银白色金属。元素周期表第1族的第一个成员。锂盐用于精神医学。',
        # 铍元素（另一种描述）
        'Grey metallic element of group 2 of the periodic table. Is toxic and can cause severe lung diseases and dermatitis. Shows high covalent character. It was isolated independently by F. Wohler and A.A. Bussy in 1828.':
        '元素周期表第2族的灰色金属元素。有毒，可引起严重的肺部疾病和皮炎。具有高度的共价性。1828年由F·沃勒和A·A·比西独立分离。',
        # 氖元素
        'Colourless gaseous element of group 18 on the periodic table (noble gases). Neon occurs in the atmosphere, and comprises 0.0018% of the volume of the atmosphere. It has a distinct reddish glow when used in discharge tubes and neon based lamps. It forms almost no chemical compounds. Neon was discovered in 1898 by Sir William Ramsey and M.W. Travers.':
        '元素周期表第18族（惰性气体）的无色气态元素。氖存在于大气中，占大气体积的0.0018%。在放电管和霓虹灯中使用时会发出明显的红光。几乎不形成化学化合物。1898年由威廉·拉姆齐爵士和M·W·特拉弗斯发现。',
        # 硫元素
        'Yellow, nonmetallic element belonging to group 16 of the periodic table. It is an essential element in living organisms, needed in the amino acids cysteine and methionine, and hence in many proteins. Absorbed by plants from the soil as sulphate ion.':
        '元素周期表第16族的黄色非金属元素。它是生物体中的必需元素，是氨基酸半胱氨酸和蛋氨酸所必需的，因此也是许多蛋白质所必需的。植物从土壤中以硫酸根离子的形式吸收硫。',
        # 氯元素
        'Halogen element. Poisonous greenish-yellow gas. Occurs widely in nature as sodium chloride in seawater. Reacts directly with many elements and compounds, strong oxidizing agent. Discovered by Karl Scheele in 1774. Humphrey David confirmed it as an element in 1810.':
        '卤素元素。有毒的黄绿色气体。在自然界中广泛存在于海水中的氯化钠中。能直接与许多元素和化合物反应，是强氧化剂。1774年由卡尔·舍勒发现。汉弗莱·戴维在1810年确认它是一种元素。',
        # 氩元素
        'Monatomic noble gas. Makes up 0.93% of the air. Colourless, odorless. Is inert and has no true compounds. Lord Rayleigh and Sir william Ramsey identified argon in 1894.':
        '单原子惰性气体。占空气的0.93%。无色、无味。化学性质不活泼，没有真正的化合物。瑞利勋爵和威廉·拉姆齐爵士于1894年鉴定出氩。',
        # 钪元素
        'Rare soft silvery metallic element belonging to group 3 of the periodic table. There are ten isotopes, nine of which are radioactive and have short half-lives. Predicted in 1869 by Mendeleev, isolated by Nilson in 1879.':
        '元素周期表第3族的稀有柔软银白色金属元素。有10种同位素，其中9种具有放射性且半衰期短。门捷列夫于1869年预言了它的存在，尼尔森于1879年将其分离出来。',
        # 钛元素
        'White metallic transition element. Occurs in numerous minerals. Used in strong, light corrosion-resistant alloys. Forms a passive oxide coating when exposed to air. First discovered by Gregor in 1789.':
        '白色金属过渡元素。存在于多种矿物中。用于制造坚固、轻便的耐腐蚀合金。暴露在空气中时会形成一层钝化的氧化膜。1789年由格雷戈尔首次发现。',
        # 钒元素
        'Soft and ductile, bright white metal. Good resistance to corrosion by alkalis, sulphuric and hydrochloric acid. It oxidizes readily about 933K. There are two naturally occurring isotopes of vanadium, and 5 radioisotopes, V-49 having the longest half-life at 337 days. Vanadium has nuclear applications, the foil is used in cladding titanium to steel, and vanadium-gallium tape is used to produce a superconductive magnet. Originally discovered by Andres Manuel del Rio of Mexico City in 1801. His discovery went unheeded, however, and in 1820, Nils Gabriel Sefstron of Sweden rediscovered it. Metallic vanadium was isolated by Henry Enfield Roscoe in 1867. The name vanadium comes from Vanadis, a goddess of Scandinavian mythology. Silvery-white metallic transition element. Vanadium is essential to Ascidians. Rats and chickens are also known to require it. Metal powder is a fire hazard, and vanadium compounds should be considered highly toxic. May cause lung cancer if inhaled.':
        '柔软且有延展性的亮白色金属。对碱、硫酸和盐酸的腐蚀有良好的抵抗力。在约933K温度下容易氧化。钒有两种天然存在的同位素和5种放射性同位素，其中V-49的半衰期最长，为337天。钒具有核应用，其箔用于将钛包覆到钢上，钒-镓带用于制造超导磁体。最初由墨西哥城的安德烈斯·曼努埃尔·德尔里奥于1801年发现，但他的发现未被重视。1820年，瑞典的尼尔斯·加布里埃尔·塞夫斯特伦重新发现了它。1867年，亨利·恩菲尔德·罗斯科分离出了金属钒。钒的名称来自斯堪的纳维亚神话中的女神瓦娜迪斯。银白色金属过渡元素。钒对海鞘至关重要，老鼠和鸡也需要它。金属粉末有火灾危险，钒化合物应被视为剧毒，吸入可能导致肺癌。',
        # 铬元素
        'Hard silvery transition element. Used in decorative electroplating. Discovered in 1797 by Vauquelin.':
        '坚硬的银白色过渡元素。用于装饰性电镀。1797年由沃克兰发现。',
        # 锰元素
        'Grey brittle metallic transition element. Rather electropositive, combines with some non-metals when heated. Discovered in 1774 by Scheele.':
        '灰色脆性金属过渡元素。电正性较强，加热时与一些非金属结合。1774年由舍勒发现。',
        # 钴元素
        'Light grey transition element. Some meteorites contain small amounts of metallic cobalt. Generally alloyed for use. Mammals require small amounts of cobalt salts. Cobalt-60, an artificially produced radioactive isotope of Cobalt is an important radioactive tracer and cancer-treatment agent. Discovered by G. Brandt in 1737.':
        '浅灰色过渡元素。一些陨石中含有少量金属钴。通常用于合金制造。哺乳动物需要少量钴盐。钴-60是一种人工产生的放射性同位素，是重要的放射性示踪剂和癌症治疗剂。1737年由G·勃兰特发现。',
        # 镍元素
        'Malleable ductile silvery metallic transition element. Discovered by A.F. Cronstedt in 1751.':
        '有延展性的银白色金属过渡元素。1751年由A·F·克朗斯泰特发现。',
        # 镓元素
        'Soft silvery metallic element, belongs to group 13 of the periodic table. The two stable isotopes are Ga-69 and Ga-71. Eight radioactive isotopes are known, all having short half-lives. Gallium Arsenide is used as a semiconductor. Corrodes most other metals by diffusing into their lattice. First identified by Francois Lecoq de Boisbaudran in 1875.':
        '柔软的银白色金属元素，属于元素周期表第13族。两种稳定同位素是Ga-69和Ga-71。已知八种放射性同位素，均具有短半衰期。砷化镓用作半导体。通过扩散到其他金属的晶格中腐蚀大多数其他金属。1875年由弗朗索瓦·勒科克·德·布瓦博德兰首次鉴定。',
        # 锗元素
        'Lustrous hard metalloid element, belongs to group 14 of the periodic table. Forms a large number of organometallic compounds. Predicted by Mendeleev in 1871, it was actually found in 1886 by Winkler.':
        '有光泽的坚硬类金属元素，属于元素周期表第14族。形成大量有机金属化合物。门捷列夫于1871年预测了它的存在，1886年温克勒实际发现了它。',
        # 砷元素
        'Metalloid element of group 15. There are three allotropes, yellow, black, and grey. Reacts with halogens, concentrated oxidizing acids and hot alkalis. Albertus Magnus is believed to have been the first to isolate the element in 1250.':
        '第15族类金属元素。有三种同素异形体：黄色、黑色和灰色。与卤素、浓氧化性酸和热碱反应。据信阿尔伯特·马格努斯于1250年首次分离出该元素。',
        # 硒元素
        'Metalloid element, belongs to group 16 of the periodic table. Multiple allotropic forms exist. Chemically resembles sulphur. Discovered in 1817 by Jons J. Berzelius.':
        '类金属元素，属于元素周期表第16族。存在多种同素异形体。化学性质与硫相似。1817年由约翰·J·贝采利乌斯发现。',
        # 溴元素
        'Halogen element. Red volatile liquid at room temperature. Its reactivity is somewhere between chlorine and iodine. Harmful to human tissue in a liquid state, the vapour irritates eyes and throat. Discovered in 1826 by Antoine Balard.':
        '卤素元素。室温下为红色挥发性液体。其反应性介于氯和碘之间。液态时对人体组织有害，蒸气刺激眼睛和喉咙。1826年由安托万·巴拉尔发现。',
        # 氪元素
        'Colorless gaseous element, belongs to the noble gases. Occurs in the air, 0.0001% by volume. It can be extracted from liquid air by fractional distillation. Generally not isolated, but used with other inert gases in fluorescent lamps. Five natural isotopes, and five radioactive isotopes. Kr-85, the most stable radioactive isotope, has a half-life of 10.76 years and is produced in fission reactors. Practically inert, though known to form compounds with Fluorine.':
        '无色气态元素，属于惰性气体。存在于空气中，体积占比0.0001%。可通过分馏液态空气提取。通常不单独使用，而是与其他惰性气体一起用于荧光灯。有五种天然同位素和五种放射性同位素。Kr-85是最稳定的放射性同位素，半衰期为10.76年，在裂变反应堆中产生。实际上是惰性的，但已知与氟形成化合物。',
        # 铷元素
        'Soft silvery metallic element, belongs to group 1 of the periodic table. Rb-97, the naturally occurring isotope, is radioactive. It is highly reactive, with properties similar to other elements in group 1, like igniting spontaneously in air. Discovered spectroscopically in 1861 by W. Bunsen and G.R. Kirchoff.':
        '柔软的银白色金属元素，属于元素周期表第1族。天然存在的同位素Rb-97具有放射性。它反应性很强，性质与第1族其他元素相似，如在空气中自发燃烧。1861年由W·本生和G·R·基尔霍夫通过光谱法发现。',
        # 锶元素
        'Soft yellowish metallic element, belongs to group 2 of the periodic table. Highly reactive chemically. Sr-90 is present in radioactive fallout and has a half-life of 28 years. Discovered in 1798 by Klaproth and Hope, isolated in 1808 by Humphry Davy.':
        '柔软的淡黄色金属元素，属于元素周期表第2族。化学性质非常活泼。Sr-90存在于放射性尘埃中，半衰期为28年。1798年由克拉普罗特和霍普发现，1808年由汉弗里·戴维分离。',
        # 钇元素
        'Silvery-grey metallic element of group 3 on the periodic table. Found in uranium ores. The only natural isotope is Y-89, there are 14 other artificial isotopes. Chemically resembles the lanthanoids. Stable in the air below 400 degrees, celsius. Discovered in 1828 by Friedrich Wohler.':
        '银灰色金属元素，属于元素周期表第3族。存在于铀矿石中。唯一的天然同位素是Y-89，还有14种人工同位素。化学性质与镧系元素相似。在400摄氏度以下的空气中稳定。1828年由弗里德里希·维勒发现。',
        # 锆元素
        'Grey-white metallic transition element. Five natural isotopes and six radioactive isotopes are known. Used in nuclear reactors for a Neutron absorber. Discovered in 1789 by Martin Klaproth, isolated in 1824 by Berzelius.':
        '灰白色金属过渡元素。已知有五种天然同位素和六种放射性同位素。用于核反应堆中作为中子吸收剂。1789年由马丁·克拉普罗特发现，1824年由贝采利乌斯分离。',
        # 铌元素
        'Soft, ductile grey-blue metallic transition element. Used in special steels and in welded joints to increase strength. Combines with halogens and oxidizes in air at 200 degrees celsius. Discovered by Charles Hatchett in 1801 and isolated by Blomstrand in 1864. Called Columbium originally.':
        '柔软、可延展的灰蓝色金属过渡元素。用于特种钢和焊接接头中以增加强度。与卤素结合，在200摄氏度的空气中氧化。1801年由查尔斯·哈切特发现，1864年由布洛姆斯特兰德分离。最初称为钶。',
        # 钼元素
        'Silvery-white, hard metallic transition element. It is chemically unreactive and is not affected by most acids. It oxidizes at high temperatures. There are seven natural isotopes, and four radioisotopes, Mo-93 being the most stable with a half-life of 3500 years. Molybdenum is used in almost all high-strength steels, it has nuclear applications, and is a catalyst in petroleum refining. Discovered in 1778 by Carl Welhelm Scheele of Sweden. Impure metal was prepared in 1782 by Peter Jacob Hjelm. The name comes from the Greek word molybdos which means lead. Trace amounts of molybdenum are required for all known forms of life. All molybdenum compounds should be considered highly toxic, and will also cause severe birth defects.':
        '银白色、坚硬的金属过渡元素。化学性质不活泼，不受大多数酸的影响。在高温下氧化。有七种天然同位素和四种放射性同位素，Mo-93是最稳定的，半衰期为3500年。钼几乎用于所有高强度钢，具有核应用，是石油精炼中的催化剂。1778年由瑞典的卡尔·威廉·舍勒发现。1782年由彼得·雅各布·赫尔姆制备出不纯的金属。名称来源于希腊语molybdos，意为铅。所有已知生命形式都需要微量的钼。所有钼化合物应被视为剧毒，也会导致严重的出生缺陷。',
        # 锝元素
        'Radioactive metallic transition element. Can be detected in some stars and the fission products of uranium. First made by Perrier and Segre by bombarding molybdenum with deutrons, giving them Tc-97. Tc-99 is the most stable isotope with a half-life of 2.6*10^6 years. Sixteen isotopes are known. Organic technetium compounds are used in bone imaging. Chemical properties are intermediate between rhenium and manganese.':
        '放射性金属过渡元素。可以在某些恒星和铀的裂变产物中检测到。1937年由佩里耶和塞格雷通过用氘核轰击钼首次制得，得到了Tc-97。Tc-99是最稳定的同位素，半衰期为2.6×10^6年。已知有16种同位素。有机锝化合物用于骨骼成像。化学性质介于铼和锰之间。',
        # 钌元素
        'Hard white metallic transition element. Found with platinum, used as a catalyst in some platinum alloys. Dissolves in fused alkalis, and is not attacked by acids. Reacts with halogens and oxygen at high temperatures. Isolated in 1844 by K.K. Klaus.':
        '坚硬的白色金属过渡元素。与铂伴生，在一些铂合金中用作催化剂。溶于熔融碱，不受酸侵蚀。在高温下与卤素和氧气反应。1844年由K.K.克劳斯分离。',
        # 铑元素
        'Silvery white metallic transition element. Found with platinum and used in some platinum alloys. Not attacked by acids, dissolves only in aqua regia. Discovered in 1803 by W.H. Wollaston.':
        '银白色金属过渡元素。与铂伴生，用于一些铂合金中。不受酸侵蚀，仅溶于王水。1803年由W.H.沃拉斯顿发现。',
        # 钯元素
        'Soft white ductile transition element. Found with some copper and nickel ores. Does not react with oxygen at normal temperatures. Dissolves slowly in hydrochloric acid. Discovered in 1803 by W.H. Wollaston.':
        '柔软的白色可延展过渡元素。与一些铜和镍矿石伴生。在常温下不与氧气反应。缓慢溶于盐酸。1803年由W.H.沃拉斯顿发现。',
        # 镉元素
        'Soft bluish metal belonging to group 12 of the periodic table. Extremely toxic even in low concentrations. Chemically similar to zinc, but lends itself to more complex compounds. Discovered in 1817 by F. Stromeyer.':
        '柔软的淡蓝色金属，属于元素周期表第12族。即使在低浓度下也极具毒性。化学性质与锌相似，但能形成更复杂的化合物。1817年由F.斯特罗迈尔发现。',
        # 铟元素
        'Soft silvery element belonging to group 13 of the periodic table. The most common natural isotope is In-115, which has a half-life of 6*10^4 years. Five other radioisotopes exist. Discovered in 1863 by Reich and Richter.':
        '柔软的银白色元素，属于元素周期表第13族。最常见的天然同位素是In-115，半衰期为6×10^4年。还存在五种其他放射性同位素。1863年由赖希和里希特发现。',
        # 锡元素
        'Silvery malleable metallic element belonging to group 14 of the periodic table. Twenty-six isotopes are known, five of which are radioactive. Chemically reactive. Combines directly with chlorine and oxygen and displaces hydrogen from dilute acids.':
        '银白色可延展的金属元素，属于元素周期表第14族。已知有26种同位素，其中5种具有放射性。化学性质活泼。能直接与氯和氧结合，并能从稀酸中置换出氢。',
        # 锑元素
        'Element of group 15. Multiple allotropic forms. The stable form of antimony is a blue-white metal. Yellow and black antimony are unstable non-metals. Used in flame-proofing, paints, ceramics, enamels, and rubber. Attacked by oxidizing acids and halogens. First reported by Tholden in 1450.':
        '元素周期表第15族元素。存在多种同素异形体。锑的稳定形式是蓝白色金属。黄色和黑色锑是不稳定的非金属。用于防火、涂料、陶瓷、搪瓷和橡胶。易被氧化性酸和卤素侵蚀。1450年由托尔登首次报道。',
        # 碲元素
        'Silvery metalloid element of group 16. Eight natural isotopes, nine radioactive isotopes. Used in semiconductors and to a degree in some steels. Chemistry is similar to Sulphur. Discovered in 1782 by Franz Miller.':
        '银白色的类金属元素，属于元素周期表第16族。有8种天然同位素和9种放射性同位素。用于半导体，并在一定程度上用于某些钢中。化学性质与硫相似。1782年由弗朗茨·米勒发现。',
        # 碘元素
        'Dark violet nonmetallic element, belongs to group 17 of the periodic table. Insoluble in water. Required as a trace element for living organisms. One stable isotope, I-127 exists, in addition to fourteen radioactive isotopes. Chemically the least reactive of the halogens, and the most electropositive metallic halogen. Discovered in 1812 by Courtois.':
        '深紫色非金属元素，属于元素周期表第17族。不溶于水。是生物所需的微量元素。存在一种稳定同位素I-127，此外还有十四种放射性同位素。化学性质是卤素中最不活泼的，也是最具电正性的金属卤素。1812年由库图瓦发现。',
        # 氙元素
        'Colourless, odourless gas belonging to group 18 on the periodic table (the noble gases.) Nine natural isotopes and seven radioactive isotopes are known. Xenon was part of the first noble-gas compound synthesized. Several others involving Xenon have been found since then. Xenon was discovered by Ramsey and Travers in 1898.':
        '无色无味的气体，属于元素周期表第18族（稀有气体）。已知有九种天然同位素和七种放射性同位素。氙是第一个合成的稀有气体化合物的组成部分。此后还发现了其他几种含氙的化合物。氙于1898年由拉姆齐和特拉弗斯发现。',
        # 铯元素
        'Soft silvery-white metallic element belonging to group 1 of the periodic table. One of the three metals which are liquid at room temperature. Cs-133 is the natural, and only stable, isotope. Fifteen other radioisotopes exist. Caesium reacts explosively with cold water, and ice at temperatures above 157K. Caesium hydroxide is the strongest base known. Caesium is the most electropositive, most alkaline and has the least ionization potential of all the elements. Known uses include the basis of atomic clocks, catalyst for the hydrogenation of some organic compounds, and in photoelectric cells. Caesium was discovered by Gustav Kirchoff and Robert Bunsen in Germany in 1860 spectroscopically. Its identification was based upon the bright blue lines in its spectrum. The name comes from the latin word caesius, which means sky blue. Caesium should be considered highly toxic. Some of the radioisotopes are even more toxic.':
        '柔软的银白色金属元素，属于元素周期表第1族。是三种在室温下呈液态的金属之一。Cs-133是天然且唯一稳定的同位素。还存在十五种其他放射性同位素。铯与冷水和温度高于157K的冰反应会爆炸。氢氧化铯是已知的最强碱。铯是所有元素中电正性最强、碱性最强、电离势最小的元素。已知用途包括作为原子钟的基础、某些有机化合物氢化的催化剂以及光电池中。1860年，古斯塔夫·基尔霍夫和罗伯特·本生在德国通过光谱法发现了铯。其鉴定基于其光谱中的亮蓝色谱线。名称来源于拉丁词caesius，意为天蓝色。铯应被视为剧毒物质。其中一些放射性同位素的毒性甚至更强。',
        # 钡元素
        'Silvery-white reactive element, belonging to group 2 of the periodic table. Soluble barium compounds are extremely poisonous. Identified in 1774 by Karl Scheele and extracted in 1808 by Humphry Davy.':
        '银白色的活泼元素，属于元素周期表第2族。可溶性钡化合物有剧毒。1774年由卡尔·舍勒识别，1808年由汉弗莱·戴维提取。',
        # 镧元素
        '(From the Greek word lanthanein, to line hidden) Silvery metallic element belonging to group 3 of the periodic table and oft considered to be one of the lanthanoids. Found in some rare-earth minerals. Twenty-five natural isotopes exist. La-139 which is stable, and La-138 which has a half-life of 10^10 to 10^15 years. The other twenty-three isotopes are radioactive. It resembles the lanthanoids chemically. Lanthanum has a low to moderate level of toxicity, and should be handled with care. Discovered in 1839 by C.G. Mosander.':
        '(来自希腊词lanthanein，意为隐藏) 银白色金属元素，属于元素周期表第3族，通常被认为是镧系元素之一。存在于一些稀土矿物中。存在25种天然同位素，其中La-139是稳定的，La-138的半衰期为10^10至10^15年。其他23种同位素具有放射性。化学性质与镧系元素相似。镧具有低至中等的毒性，应小心处理。1839年由C.G.莫桑德尔发现。',
        # 铈元素
        'Silvery metallic element, belongs to the lanthanoids. Four natural isotopes exist, and fifteen radioactive isotopes have been identified. Used in some rare-earth alloys. The oxidized form is used in the glass industry. Discovered by Martin .H. Klaproth in 1803.':
        '银白色金属元素，属于镧系元素。存在四种天然同位素，已鉴定出十五种放射性同位素。用于一些稀土合金。其氧化形式用于玻璃工业。1803年由马丁·H·克拉普罗特发现。',
        # 镨元素
        'Soft silvery metallic element, belongs to the lanthanoids. Only natural isotope is Pr-141 which is not radioactive. Fourteen radioactive isotopes have been artificially produced. Used in rare-earth alloys. Discovered in 1885 by C.A. von Welsbach.':
        '柔软的银白色金属元素，属于镧系元素。唯一的天然同位素是Pr-141，它不具有放射性。已人工制备了十四种放射性同位素。用于稀土合金中。1885年由C.A.冯·韦尔斯巴赫发现。',
        # 钕元素
        "Soft bright silvery metallic element, belongs to the lanthanoids. Seven natural isotopes, Nd-144 being the only radioactive one with a half-life of 10^10 to 10^15 years. Six artificial radioisotopes have been produced. The metal is used in glass works to color class a shade of violet-purple and make it dichroic. One of the more reactive rare-earth metals, quickly reacts with air. Used in some rare-earth alloys. Neodymium is used to color the glass used in welder's glasses. Neodymium is also used in very powerful, permanent magnets (Nd2Fe14B). Discovered by Carl F. Auer von Welsbach in Austria in 1885 by separating didymium into its elemental components Praseodymium and neodymium. The name comes from the Greek words 'neos didymos' which means 'new twin'. Neodymium should be considered highly toxic, however evidence would seem to show that it acts as little more than a skin and eye irritant. The dust however, presents a fire and explosion hazard.":
        "柔软明亮的银白色金属元素，属于镧系元素。存在七种天然同位素，其中Nd-144是唯一具有放射性的同位素，半衰期为10^10至10^15年。已人工制备了六种放射性同位素。该金属用于玻璃制造中，使玻璃呈现紫罗蓝色并具有二色性。是较活泼的稀土金属之一，与空气反应迅速。用于一些稀土合金中。钕用于给焊工眼镜中的玻璃着色。钕还用于制造非常强大的永磁体（Nd2Fe14B）。1885年，卡尔·F·奥尔·冯·韦尔斯巴赫在奥地利通过将钕镨混合物分离成其元素成分镨和钕而发现了钕。名称来自希腊词'neos didymos'，意为'新的孪生兄弟'。钕应被视为剧毒物质，但证据表明它只不过是皮肤和眼睛刺激物。然而，其粉尘具有火灾和爆炸危险。",
        # 钷元素
        'Soft silvery metallic element, belongs to the lanthanoids. Pm-147, the only natural isotope, is radioactive and has a half-life of 252 years. Eighteen radioisotopes have been produced, but all have very short half-lives. Found only in nuclear decay waste. Pm-147 is of interest as a beta-decay source, however Pm-146 and Pm-148 have to be removed from it first, as they generate gamma radiation. Discovered by J.A. Marinsky, L.E. Glendenin and C.D. Coryell in 1947.':
        '柔软的银白色金属元素，属于镧系元素。Pm-147是唯一的天然同位素，具有放射性，半衰期为252年。已制备了十八种放射性同位素，但都具有很短的半衰期。仅存在于核衰变废物中。Pm-147作为β衰变源备受关注，但首先必须从中去除Pm-146和Pm-148，因为它们会产生γ辐射。1947年由J.A.马林斯基、L.E.格伦德宁和C.D.科里尔发现。',
        # 钐元素
        'Soft silvery metallic element, belongs to the lanthanoids. Seven natural isotopes, Sm-147 is the only radioisotope, and has a half-life of 2.5*10^11 years. Used for making special alloys needed in the production of nuclear reactors. Also used as a neutron absorber. Small quantities of samarium oxide is used in special optical glasses. The largest use of the element is its ferromagnetic alloy which produces permanent magnets that are five times stronger than magnets produced by any other material. Discovered by Francois Lecoq de Boisbaudran in 1879.':
        '柔软的银白色金属元素，属于镧系元素。存在七种天然同位素，其中Sm-147是唯一的放射性同位素，半衰期为2.5×10^11年。用于制造核反应堆生产所需的特殊合金，也用作中子吸收剂。少量的氧化钐用于特殊光学玻璃中。该元素的最大用途是其铁磁性合金，可生产出比任何其他材料强五倍的永磁体。1879年由弗朗索瓦·勒科克·德·布瓦博德朗发现。',
        # 铕元素
        'Soft silvery metallic element belonging to the lanthanoids. Eu-151 and Eu-153 are the only two stable isotopes, both of which are Neutron absorbers. Discovered in 1889 by Sir William Crookes.':
        '柔软的银白色金属元素，属于镧系元素。Eu-151和Eu-153是仅有的两种稳定同位素，它们都是中子吸收剂。1889年由威廉·克鲁克斯爵士发现。',
        # 钆元素
        'Soft silvery metallic element belonging to the lanthanoids. Seven natural, stable isotopes are known in addition to eleven artificial isotopes. Gd-155 and Gd-157 and the best neutron absorbers of all elements. Gadolinium compounds are used in electronics. Discovered by J.C.G Marignac in 1880.':
        '柔软的银白色金属元素，属于镧系元素。已知有七种天然稳定同位素，此外还有十一种人工同位素。Gd-155和Gd-157是所有元素中最好的中子吸收剂。钆化合物用于电子领域。1880年由J.C.G.马里尼亚克发现。',
        # 铽元素
        'Silvery metallic element belonging to the lanthanoids. Tb-159 is the only stable isotope, there are seventeen artificial isotopes. Discovered by G.G. Mosander in 1843.':
        '银白色金属元素，属于镧系元素。Tb-159是唯一的稳定同位素，存在十七种人工同位素。1843年由G.G.莫桑德尔发现。',
        # 镝元素
        'Metallic with a bright silvery-white lustre. Dysprosium belongs to the lanthanoids. It is relatively stable in air at room temperatures, it will however dissolve in mineral acids, evolving hydrogen. It is found in from rare-earth minerals. There are seven natural isotopes of dysprosium, and eight radioisotopes, Dy-154 being the most stable with a half-life of 3*10^6 years. Dysprosium is used as a neutron absorber in nuclear fission reactions, and in compact disks. It was discovered by Paul Emile Lecoq de Boisbaudran in 1886 in France. Its name comes from the Greek word dysprositos, which means hard to obtain.':
        '带有明亮银白色光泽的金属元素。镝属于镧系元素。在室温空气中相对稳定，但会溶于无机酸，释放出氢气。存在于稀土矿物中。镝有七种天然同位素和八种放射性同位素，其中Dy-154最稳定，半衰期为3×10^6年。镝用作核裂变反应中的中子吸收剂，也用于光盘中。1886年由保罗·埃米尔·勒科克·德·布瓦博德朗在法国发现。其名称来自希腊词dysprositos，意为难以获得。',
        # 钬元素
        "Relatively soft and malleable silvery-white metallic element, which is stable in dry air at room temperature. It oxidizes in moist air and at high temperatures. It belongs to the lanthanoids. A rare-earth metal, it is found in the minerals monazite and gadolinite. It possesses unusual magnetic properties. One natural isotope, Ho-165 exists, six radioisotopes exist, the most stable being Ho-163 with a half-life of 4570 years. Holmium is used in some metal alloys, it is also said to stimulate the metabolism. Discovered by Per Theodor Cleve and J.L. Soret in Switzerland in 1879. The name homium comes from the Greek word Holmia which means Sweden. While all holmium compounds should be considered highly toxic, initial evidence seems to indicate that they do not pose much danger. The metal's dust however, is a fire hazard.":
        "相对柔软且有延展性的银白色金属元素，在室温干燥空气中稳定。在潮湿空气中和高温下会氧化。属于镧系元素。作为稀土金属，存在于独居石和硅铍钇矿中。具有异常的磁性。存在一种天然同位素Ho-165，六种放射性同位素，其中最稳定的是Ho-163，半衰期为4570年。钬用于一些金属合金中，据说还能刺激新陈代谢。1879年由佩尔·西奥多·克莱夫和J.L.索雷特在瑞士发现。名称来自希腊词Holmia，意为瑞典。虽然所有钬化合物都应被视为剧毒，但初步证据表明它们不会构成太大危险。然而，该金属的粉尘存在火灾危险。",
        # 铒元素
        'Soft silvery metallic element which belongs to the lanthanoids. Six natural isotopes that are stable. Twelve artificial isotopes are known. Used in nuclear technology as a neutron absorber. It is being investigated for other possible uses. Discovered by Carl G. Mosander in 1843.':
        '柔软的银白色金属元素，属于镧系元素。存在六种稳定的天然同位素，已知有十二种人工同位素。在核技术中用作中子吸收剂。目前正在研究其其他可能的用途。1843年由卡尔·G·莫桑德尔发现。',
        # 铥元素
        'Soft grey metallic element that belongs to the lanthanoids. One natural isotope exists, Tm-169, and seventeen artificial isotopes have been produced. No known uses for the element. Discovered in 1879 by Per Theodor Cleve.':
        '柔软的灰色金属元素，属于镧系元素。存在一种天然同位素Tm-169，已制备了十七种人工同位素。该元素目前没有已知的用途。1879年由佩尔·西奥多·克莱夫发现。',
        # 镱元素
        'Silvery metallic element of the lanthanoids. Seven natural isotopes and ten artificial isotopes are known. Used in certain steels. Discovered by J.D.G. Marignac in 1878.':
        '银白色金属元素，属于镧系元素。已知有七种天然同位素和十种人工同位素。用于某些钢中。1878年由J.D.G.马里尼亚克发现。',
        # 镥元素
        'Silvery-white rare-earth metal which is relatively stable in air. It happens to be the most expensive rare-earth metal. Its found with almost all rare-earth metals, but is very difficult to separate from other elements. Least abundant of all natural elements. Used in metal alloys, and as a catalyst in various processes. There are two natural, stable isotopes, and seven radioisotopes, the most stable being Lu-174 with a half-life of 3.3 years. The separation of lutetium from Ytterbium was described by Georges Urbain in 1907. It was discovered at approximately the same time by Carl Auer von Welsbach. The name comes from the Greek word lutetia which means Paris.':
        '银白色稀土金属，在空气中相对稳定。它恰好是最昂贵的稀土金属。几乎与所有稀土金属一起被发现，但很难与其他元素分离。是所有天然元素中丰度最低的。用于金属合金，也用作各种工艺的催化剂。存在两种天然稳定同位素和七种放射性同位素，其中最稳定的是Lu-174，半衰期为3.3年。1907年，乔治·乌尔班描述了从镱中分离镥的方法。大约在同一时间，卡尔·奥尔·冯·韦尔斯巴赫也发现了它。其名称来自希腊词lutetia，意为巴黎。',
        # 铪元素
        'Silvery lustrous metallic transition element. Used in tungsten alloys in filaments and electrodes, also acts as a neutron absorber. First reported by Urbain in 1911, existence was finally established in 1923 by D. Coster, G.C. de Hevesy in 1923.':
        '有光泽的银白色金属过渡元素。用于灯丝和电极中的钨合金，也用作中子吸收剂。1911年由乌尔班首次报道，其存在最终于1923年由D.科斯特和G.C.德赫维西确立。',
        # 钽元素
        'Heavy blue-grey metallic transition element. Ta-181 is a stable isotope, and Ta-180 is a radioactive isotope, with a half-life in excess of 10^7 years. Used in surgery as it is unreactive. Forms a passive oxide layer in air. Identified in 1802 by Ekeberg and isolated in 1820 by Jons J. Berzelius.':
        '重的蓝灰色金属过渡元素。Ta-181是稳定同位素，Ta-180是放射性同位素，半衰期超过10^7年。由于其不活泼性，用于外科手术中。在空气中形成钝化氧化层。1802年由埃克伯格鉴定，1820年由约恩斯·J·贝采利乌斯分离。',
        # 钨元素
        'White or grey metallic transition element,formerly called Wolfram. Forms a protective oxide in air and can be oxidized at high temperature. First isolated by Jose and Fausto de Elhuyer in 1783.':
        '白色或灰色金属过渡元素，以前称为Wolfram（钨锰铁矿）。在空气中形成保护性氧化物，在高温下可被氧化。1783年由何塞和福斯托·德·埃尔休耶首次分离。',
        # 铼元素
        'Silvery-white metallic transition element. Obtained as a by-product of molybdenum refinement. Rhenium-molybdenum alloys are superconducting.':
        '银白色金属过渡元素。作为钼精炼的副产品获得。铼-钼合金具有超导性。',
        # 锇元素
        'Hard blue-white metallic transition element. Found with platinum and used in some alloys with platinum and iridium.':
        '坚硬的蓝白色金属过渡元素。与铂一起被发现，并用于一些与铂和铱的合金中。',
        # 铱元素
        'Very hard and brittle, silvery metallic transition element. It has a yellowish cast to it. Salts of iridium are highly colored. It is the most corrosion resistant metal known, not attacked by any acid, but is attacked by molten salts. There are two natural isotopes of iridium, and 4 radioisotopes, the most stable being Ir-192 with a half-life of 73.83 days. Ir-192 decays into Platinum, while the other radioisotopes decay into Osmium. Iridium is used in high temperature apparatus, electrical contacts, and as a hardening agent for platinumpy. Discovered in 1803 by Smithson Tennant in England. The name comes from the Greek word iris, which means rainbow. Iridium metal is generally non-toxic due to its relative unreactivity, but iridium compounds should be considered highly toxic.':
        '非常坚硬且易碎的银白色金属过渡元素，带有淡黄色调。铱的盐类颜色鲜艳。它是已知最耐腐蚀的金属，不受任何酸的侵蚀，但会被熔融盐侵蚀。铱有两种天然同位素和4种放射性同位素，其中最稳定的是Ir-192，半衰期为73.83天。Ir-192衰变为铂，而其他放射性同位素衰变为锇。铱用于高温设备、电触点，并作为铂的硬化剂。1803年由英国的史密森·坦南特发现。其名称来自希腊词iris，意为彩虹。由于铱的相对不活泼性，金属铱通常无毒，但铱化合物应被视为剧毒。',
        # 铂元素
        'Attractive greyish-white metal. When pure, it is malleable and ductile. Does not oxidize in air, insoluble in hydrochloric and nitric acid. Corroded by halogens, cyandies, sulphur and alkalis. Hydrogen and Oxygen react explosively in the presence of platinumpy. There are six stable isotopes and three radioisotopes, the most stable being Pt-193 with a half-life of 60 years. Platinum is used in jewelry, laboratory equipment, electrical contacts, dentistry, and anti-pollution devices in cars. PtCl2(NH3)2 is used to treat some forms of cancer. Platinum-Cobalt alloys have magnetic properties. It is also used in the definition of the Standard Hydrogen Electrode. Discovered by Antonio de Ulloa in South America in 1735. The name comes from the Spanish word platina which means silver. Platinum metal is generally not a health concern due to its unreactivity, however platinum compounds should be considered highly toxic.':
        '有吸引力的灰白色金属。纯净时具有延展性和韧性。在空气中不氧化，不溶于盐酸和硝酸。受卤素、氰化物、硫和碱的腐蚀。在铂存在下，氢气和氧气会发生爆炸性反应。铂有六种稳定同位素和三种放射性同位素，其中最稳定的是Pt-193，半衰期为60年。铂用于珠宝、实验室设备、电触点、牙科以及汽车的防污染装置。PtCl2(NH3)2用于治疗某些形式的癌症。铂-钴合金具有磁性。它还用于标准氢电极的定义。1735年由安东尼奥·德·乌略亚在南美洲发现。其名称来自西班牙语词platina，意为银。由于铂的不活泼性，金属铂通常对健康无影响，但铂化合物应被视为剧毒。',
        # 金元素
        'Gold is gold colored. It is the most malleable and ductile metal known. There is only one stable isotope of gold, and five radioisotopes of gold, Au-195 being the most stable with a half-life of 186 days. Gold is used as a monetary standard, in jewelry, dentistry, electronics. Au-198 is used in treating cancer and some other medical conditions. Gold has been known to exist as far back as 2600 BC. Gold comes from the Anglo-Saxon word gold. Its symbol, Au, comes from the Latin word aurum, which means gold. Gold is not particularly toxic, however it is known to cause damage to the liver and kidneys in some.':
        '金呈金色。它是已知最具延展性和韧性的金属。金只有一种稳定同位素和五种放射性同位素，其中最稳定的是Au-195，半衰期为186天。金用作货币标准，用于珠宝、牙科、电子设备。Au-198用于治疗癌症和其他一些医疗疾病。早在公元前2600年就已知金的存在。金的名称来自盎格鲁-撒克逊语的gold。其符号Au来自拉丁语aurum，意为金。金不是特别有毒，但已知会对某些人的肝脏和肾脏造成损害。',
        # 汞元素
        'Heavy silvery liquid metallic element, belongs to the zinc group. Used in thermometers, barometers and other scientific apparatus. Less reactive than zinc and cadmium, does not displace hydrogen from acids. Forms a number of complexes and organomercury compounds.':
        '重的银白色液态金属元素，属于锌族。用于温度计、气压计和其他科学仪器。反应性比锌和镉低，不会从酸中置换出氢。形成多种配合物和有机汞化合物。',
        # 铊元素
        'Pure, unreacted thallium appears silvery-white and exhibits a metallic lustre. Upon reacting with air, it begins to turn bluish-grey and looks like lead. It is very malleable, and can be cut with a knife. There are two stable isotopes, and four radioisotopes, Tl-204 being the most stable with a half-life of 3.78 years. Thallium sulphate was used as a rodenticide. Thallium sulphine\'s conductivity changes with exposure to infrared light, this gives it a use in infrared detectors. Discovered by Sir William Crookes via spectroscopy. Its name comes from the Greek word thallos, which means green twig. Thallium and its compounds are toxic and can cause cancer.':
        '纯净、未反应的铊呈现银白色，具有金属光泽。与空气反应后，它开始变成蓝灰色，看起来像铅。它非常有延展性，可以用刀切割。铊有两种稳定同位素和四种放射性同位素，其中最稳定的是Tl-204，半衰期为3.78年。硫酸铊曾被用作杀鼠剂。硫化铊的导电性随暴露于红外光而变化，这使其在红外探测器中有应用。由威廉·克鲁克斯爵士通过光谱学发现。其名称来自希腊词thallos，意为绿色嫩枝。铊及其化合物有毒，可致癌。',
        # 铅元素
        'Heavy dull grey ductile metallic element, belongs to group 14. Used in building construction, lead-place accumulators, bullets and shot, and is part of solder, pewter, bearing metals, type metals and fusible alloys.':
        '重的暗灰色韧性金属元素，属于第14族。用于建筑施工、铅酸蓄电池、子弹和弹丸，也是焊料、锡铅合金、轴承金属、活字金属和易熔合金的组成部分。',
        # 铋元素
        'White crystalline metal with a pink tinge, belongs to group 15. Most diamagnetic of all metals and has the lowest thermal conductivity of all the elements except mercury. Lead-free bismuth compounds are used in cosmetics and medical procedures. Burns in the air and produces a blue flame. In 1753, C.G. Junine first demonstrated that it was different from lead.':
        '带有粉红色调的白色结晶金属，属于第15族。是所有金属中最具抗磁性的，除汞外，其热导率是所有元素中最低的。无铅铋化合物用于化妆品和医疗程序。在空气中燃烧并产生蓝色火焰。1753年，C.G.朱宁首次证明它与铅不同。',
        # 钋元素
        'Rare radioactive metallic element, belongs to group 16 of the periodic table. Over 30 known isotopes exist, the most of all elements. Po-209 has a half-life of 103 years. Possible uses in heating spacecraft. Discovered by Marie Curie in 1898 in a sample of pitchblende.':
        '稀有的放射性金属元素，属于元素周期表第16族。存在超过30种已知同位素，是所有元素中最多的。Po-209的半衰期为103年。可能用于太空船加热。1898年，玛丽·居里在沥青铀矿样品中发现了它。',
        # 砹元素
        'Radioactive halogen element. Occurs naturally from uranium and thorium decay. At least 20 known isotopes. At-210, the most stable, has a half-life of 8.3 hours. Synthesized by nuclear bombardment in 1940 by D.R. Corson, K.R. MacKenzie and E. Segre at the University of California.':
        '放射性卤素元素。天然存在于铀和钍的衰变过程中。至少有20种已知同位素。最稳定的At-210半衰期为8.3小时。1940年，D.R.科尔森、K.R.麦肯齐和E.塞格雷在加利福尼亚大学通过核轰击合成了它。',
        # 氡元素
        'Colorless radioactive gaseous element, belongs to the noble gases. Of the twenty known isotopes, the most stable is Rn-222 with a half-life of 3.8 days. Formed by the radioactive decay of Radium-226. Radon itself decays into Polonium. Used in radiotherapy. As a noble gas, it is effectively inert, though radon fluoride has been synthesized. First isolated in 1908 by Ramsey and Gray.':
        '无色放射性气态元素，属于稀有气体。在已知的二十种同位素中，最稳定的是Rn-222，半衰期为3.8天。由镭-226的放射性衰变形成。氡本身会衰变成钋。用于放射治疗。作为稀有气体，它实际上是惰性的，尽管已合成了氟化氡。1908年由拉姆齐和格雷首次分离。',
        # 钫元素
        'Radioactive element, belongs to group 1 of the periodic table. Found in uranium and thorium ores. The 22 known isotopes are all radioactive, with the most stable being Fr-223. Its existence was confirmed in 1939 by Marguerite Perey.':
        '放射性元素，属于元素周期表第1族。存在于铀矿和钍矿中。已知的22种同位素均具有放射性，其中最稳定的是Fr-223。1939年由玛格丽特·佩雷确认其存在。',
        # 镭元素
        'Radioactive metallic transuranic element, belongs to group 2 of the periodic table. Most stable isotope, Ra-226 has a half-life of 1602 years, which decays into radon. Isolated from pitchblende in 1898 Marie and Pierre Curie.':
        '放射性金属超铀元素，属于元素周期表第2族。最稳定的同位素Ra-226半衰期为1602年，会衰变成氡。1898年玛丽和皮埃尔·居里从沥青铀矿中分离出来。',
        # 锕元素
        'Silvery radioactive metallic element, belongs to group 3 of the periodic table. The most stable isotope, Ac-227, has a half-life of 217 years. Ac-228 (half-life of 6.13 hours) also occurs in nature. There are 22 other artificial isotopes, all radioactive and having very short half-lives. Chemistry similar to lanthanumpy. Used as a source of alpha particles. Discovered by A. Debierne in 1899.':
        '银色放射性金属元素，属于元素周期表第3族。最稳定的同位素Ac-227半衰期为217年。Ac-228（半衰期6.13小时）也存在于自然界中。还有22种人工同位素，均具有放射性且半衰期非常短。化学性质与镧系元素相似。用作α粒子源。1899年由A.德比埃尔内发现。',
        # 钍元素
        'Grey radioactive metallic element. Belongs to actinoids. Found in monazite sand in Brazil, India and the US. Thorium-232 has a half-life of 1.39x10^10 years. Can be used as a nuclear fuel for breeder reactors. Thorium-232 captures slow Neutrons and breeds uranium-233. Discovered by Jons J. Berzelius in 1829.':
        '灰色放射性金属元素。属于锕系元素。存在于巴西、印度和美国的独居石砂中。钍-232半衰期为1.39×10^10年。可用作增殖反应堆的核燃料。钍-232捕获慢中子并增殖铀-233。1829年由约恩斯·J·贝采利乌斯发现。',
        # 镤元素
        'Radioactive metallic element, belongs to the actinoids. The most stable isotope, Pa-231 has a half-life of 2.43*10^4 years. At least 10 other radioactive isotopes are known. No practical applications are known. Discovered in 1917 by Lise Meitner and Otto Hahn.':
        '放射性金属元素，属于锕系元素。最稳定的同位素Pa-231半衰期为2.43×10^4年。已知至少还有10种放射性同位素。目前没有已知的实际应用。1917年由莉泽·迈特纳和奥托·哈恩发现。',
        # 铀元素
        'White radioactive metallic element belonging to the actinoids. Three natural isotopes, U-238, U-235 and U-234. Uranium-235 is used as the fuel for nuclear reactors and weapons. Discovered by Martin H. Klaproth in 1789.':
        '白色放射性金属元素，属于锕系元素。有三种天然同位素：U-238、U-235和U-234。铀-235用作核反应堆和武器的燃料。1789年由马丁·H·克拉普罗特发现。',
        # 镎元素
        'Radioactive metallic transuranic element, belongs to the actinoids. Np-237, the most stable isotope, has a half-life of 2.2*10^6 years and is a by product of nuclear reactors. The other known isotopes have mass numbers 229 through 236, and 238 through 241. Np-236 has a half-life of 5*10^3 years. First produced by Edwin M. McMillan and P.H. Abelson in 1940.':
        '放射性金属超铀元素，属于锕系元素。最稳定的同位素Np-237半衰期为2.2×10^6年，是核反应堆的副产品。其他已知同位素的质量数为229至236，以及238至241。Np-236半衰期为5×10^3年。1940年由埃德温·M·麦克米伦和P·H·艾贝尔森首次制备。',
        # 钚元素
        'Dense silvery radioactive metallic transuranic element, belongs to the actinoids. Pu-244 is the most stable isotope with a half-life of 7.6*10^7 years. Thirteen isotopes are known. Pu-239 is the most important, it undergoes nuclear fission with slow neutrons and is hence important to nuclear weapons and reactors. Plutonium production is monitored down to the gram to prevent military misuse. First produced by Gleen T. Seaborg, Edwin M. McMillan, J.W. Kennedy and A.C. Wahl in 1940.':
        '致密的银白色放射性金属超铀元素，属于锕系元素。最稳定的同位素Pu-244半衰期为7.6×10^7年。已知有13种同位素。Pu-239最重要，它在慢中子作用下发生核裂变，因此对核武器和反应堆很重要。钚的生产被监控到克级，以防止军事滥用。1940年由格伦·T·西博格、埃德温·M·麦克米伦、J·W·肯尼迪和A·C·瓦尔首次制备。',
        # 镅元素
        'Radioactive metallic transuranic element, belongs to the actinoids. Ten known isotopes. Am-243 is the most stable isotope, with a half-life of 7.95*10^3 years. Discovered by Glenn T. Seaborg and associates in 1945, it was obtained by bombarding Uranium-238 with alpha particles.':
        '放射性金属超铀元素，属于锕系元素。已知有10种同位素。Am-243是最稳定的同位素，半衰期为7.95×10^3年。1945年由格伦·T·西博格及其同事发现，通过用α粒子轰击铀-238获得。',
        # 锔元素
        'Radioactive metallic transuranic element. Belongs to actinoid series. Nine known isotopes, Cm-247 has a half-life of 1.64*10^7 years. First identified by Glenn T. Seaborg and associates in 1944, first produced by L.B. Werner and I. Perlman in 1947 by bombarding americium-241 with Neutrons. Named for Marie Curie.':
        '放射性金属超铀元素。属于锕系元素。已知有9种同位素，Cm-247半衰期为1.64×10^7年。1944年由格伦·T·西博格及其同事首次鉴定，1947年由L·B·沃纳和I·珀尔曼通过用中子轰击镅-241首次制备。以玛丽·居里命名。',
        # 锫元素
        'Radioactive metallic transuranic element. Belongs to actinoid series. Eight known isotopes, the most common Bk-247, has a half-life of 1.4*10^3 years. First produced by Glenn T. Seaborg and associates in 1949 by bombarding americium-241 with alpha particles.':
        '放射性金属超铀元素。属于锕系元素。已知有8种同位素，最常见的Bk-247半衰期为1.4×10^3年。1949年由格伦·T·西博格及其同事通过用α粒子轰击镅-241首次制备。',
        # 锎元素
        'Radioactive metallic transuranic element. Belongs to actinoid series. Cf-251 has a half life of about 700 years. Nine isotopes are known. Cf-252 is an intense Neutron source, which makes it an intense Neutron source and gives it a use in Neutron activation analysis and a possible use as a radiation source in medicine. First produced by Glenn T. Seaborg and associates in 1950.':
        '放射性金属超铀元素。属于锕系元素。Cf-251的半衰期约为700年。已知有9种同位素。Cf-252是一种强烈的中子源，使其可用于中子活化分析，并可能作为医学中的辐射源。1950年由格伦·T·西博格及其同事首次制备。',
        # 锿元素
        'Appearance is unknown, however it is most probably metallic and silver or gray in color. Radioactive metallic transuranic element belonging to the actinoids. Es-254 has the longest half-life of the eleven known isotopes at 270 days. First identified by Albert Ghiorso and associates in the debris of the 1952 hydrogen bomb explosion. In 1961 the first microgram quantities of Es-232 were separated. While einsteinium never exists naturally, if a sufficient amount was assembled, it would pose a radiation hazard.':
        '外观未知，但很可能是金属，呈银色或灰色。放射性金属超铀元素，属于锕系元素。在已知的11种同位素中，Es-254的半衰期最长，为270天。1952年由阿尔伯特·乔索及其同事在氢弹爆炸的碎片中首次发现。1961年分离出第一批微克级的Es-232。虽然锿在自然界中不存在，但如果聚集足够数量，它会构成辐射危害。',
        # 镄元素
        'Radioactive metallic transuranic element, belongs to the actinoids. Ten known isotopes, most stable is Fm-257 with a half-life of 10 days. First identified by Albert Ghiorso and associates in the debris of the first hydrogen-bomb explosion in 1952.':
        '放射性金属超铀元素，属于锕系元素。已知有10种同位素，最稳定的是Fm-257，半衰期为10天。1952年由阿尔伯特·乔索及其同事在第一次氢弹爆炸的碎片中首次发现。',
        # 钔元素
        'Radioactive metallic transuranic element. Belongs to the actinoid series. Only known isotope, Md-256 has a half-life of 1.3 hours. First identified by Glenn T. Seaborg, Albert Ghiorso and associates in 1955. Alternative name Unnilunium has been proposed. Named after the \'inventor\' of the periodic table, Dmitri Mendeleev.':
        '放射性金属超铀元素。属于锕系元素。仅知一种同位素Md-256，半衰期为1.3小时。1955年由格伦·T·西博格、阿尔伯特·乔索及其同事首次鉴定。曾提议使用Unnilunium作为替代名称。以元素周期表的“发明者”德米特里·门捷列夫命名。',
        # 锘元素
        'Radioactive metallic transuranic element, belongs to the actinoids. Seven known isotopes exist, the most stable being No-254 with a half-life of 255 seconds. First identified with certainty by Albert Ghiorso and Glenn T. Seaborg in 1966. Unnilbium has been proposed as an alternative name.':
        '放射性金属超铀元素，属于锕系元素。已知有7种同位素，最稳定的是No-254，半衰期为255秒。1966年由阿尔伯特·乔索和格伦·T·西博格首次确定。曾提议使用Unnilbium作为替代名称。',
        # 铹元素
        'Appearance unknown, however it is most likely silvery-white or grey and metallic. Lawrencium is a synthetic rare-earth metal. There are eight known radioisotopes, the most stable being Lr-262 with a half-life of 3.6 hours. Due to the short half-life of lawrencium, and its radioactivity, there are no known uses for it. Identified by Albert Ghiorso in 1961 at Berkeley. It was produced by bombarding californium with boron ions. The name is temporary IUPAC nomenclature, the origin of the name comes from Ernest O. Lawrence, the inventor of the cyclotron. If sufficient amounts of lawrencium were produced, it would pose a radiation hazard.':
        '外观未知，但很可能是银白色或灰色的金属。铹是一种合成的稀土金属。已知有8种放射性同位素，最稳定的是Lr-262，半衰期为3.6小时。由于铹的半衰期短且具有放射性，目前没有已知的用途。1961年由阿尔伯特·乔索在伯克利发现。通过用硼离子轰击锎产生。该名称是临时的IUPAC命名法，名称来源于回旋加速器的发明者欧内斯特·O·劳伦斯。如果产生足够数量的铹，它会构成辐射危害。',
        # 钅卢元素
        'Radioactive transactinide element. Expected to have similar chemical properties to those displayed by hafnium. Rf-260 was discovered by the Joint Nuclear Research Institute at Dubna (U.S.S.R.) in 1964. Researchers at Berkeley discovered Unq-257 and Unq-258 in 1964.':
        '放射性超重元素。预计具有与铪相似的化学性质。1964年由苏联杜布纳联合核研究所发现了Rf-260。1964年伯克利的研究人员发现了Unq-257和Unq-258。',
        # 钅杜元素
        'Also known as Hahnium, Ha. Radioactive transactinide element. Half-life of 1.6s. Discovered in 1970 by Berkeley researchers. So far, seven isotopes have been discovered.':
        '也称为钅罕（Ha）。放射性超重元素。半衰期为1.6秒。1970年由伯克利的研究人员发现。到目前为止，已发现7种同位素。',
        # 钅喜元素
        'Half-life of 0.9 +/- 0.2 s. Discovered by the Joint Institute for Nuclear Research at Dubna (U.S.S.R.) in June of 1974. Its existence was confirmed by the Lawrence Berkeley Laboratory and Livermore National Laboratory in September of 1974.':
        '半衰期为0.9±0.2秒。1974年6月由苏联杜布纳联合核研究所发现。1974年9月，劳伦斯伯克利实验室和利弗莫尔国家实验室证实了其存在。',
        # 钅波元素
        'Radioactive transition metal. Half-life of approximately 1/500 s. Discovered by the Joint Institute for Nuclear Research at Dubna (U.S.S.R.) in 1976. Confirmed by West German physicists at the Heavy Ion Research Laboratory at Darmstadt.':
        '放射性过渡金属。半衰期约为1/500秒。1976年由苏联杜布纳联合核研究所发现。由西德基森的重离子研究实验室的物理学家确认。',
        # 钅黑元素
        'Radioactive transition metal first synthesized in 1984 by a German research team led by Peter Armbruster and Gottfried Muenzenberg at the Institute for Heavy Ion Research at Darmstadt.':
        '放射性过渡金属，1984年由彼得·阿姆布鲁斯特和戈特弗里德·明岑贝格领导的德国研究团队在达姆施塔特的重离子研究所首次合成。',
        # 鿏元素
        'Half-life of approximately 5 ms. The creation of this element demonstrated that fusion techniques could indeed be used to make new, heavy nuclei. Made and identified by physicists of the Heavy Ion Research Laboratory, Darmstadt, West Germany in 1982. Named in honor of Lise Meitner, the Austrian physicist.':
        '半衰期约为5毫秒。该元素的创建证明了融合技术确实可以用来制造新的重核。1982年由西德达姆施塔特重离子研究实验室的物理学家制造和鉴定。以奥地利物理学家莉泽·迈特纳的名字命名。'
    }
    
    # 首先检查是否有完全匹配的完整句子翻译
    if text in full_sentence_translations:
        return full_sentence_translations[text]
    
    # 如果没有完全匹配，尝试部分句子翻译
    # 先处理硼元素的描述
    if 'An element of group 13 of the periodic table' in text:
        text = text.replace('An element of group 13 of the periodic table', '周期表中第13族元素')
        text = text.replace('There are two allotropes', '有两种同素异形体')
        text = text.replace('amorphous boron is a brown power, but metallic boron is black', '无定形硼是棕色粉末，而金属硼是黑色的')
        text = text.replace('The metallic form is hard (9.3 on Mohs\' scale) and a bad conductor in room temperatures', '金属形式的硼质地坚硬（莫氏硬度9.3），在室温下是不良导体')
        text = text.replace('It is never found free in nature', '它从未在自然界中以游离态存在')
        text = text.replace('Boron-10 is used in nuclear reactor control rods and shields', '硼-10用于核反应堆的控制棒和屏蔽材料')
        text = text.replace('It was discovered in', '它于').replace('by', '由')
    
    # 处理氮元素的描述
    elif 'Colourless, gaseous element which belongs to group 15 of the periodic table' in text:
        text = text.replace('Colourless, gaseous element which belongs to group 15 of the periodic table', '属于周期表第15族的无色气体元素')
        text = text.replace('Constitutes ~78% of the atmosphere', '约占大气的78%')
        text = text.replace('is an essential part of the ecosystem', '是生态系统的重要组成部分')
        text = text.replace('Nitrogen for industrial purposes is acquired by the fractional distillation of liquid air', '工业用途的氮通过液态空气的分馏获取')
        text = text.replace('Chemically inactive, reactive generally only at high temperatures or in electrical discharges', '化学性质不活泼，通常仅在高温或放电条件下具有反应性')
        text = text.replace('It was discovered in', '它于').replace('by', '由')
    
    # 处理氢元素的描述
    elif 'Colourless, odourless gaseous chemical element' in text:
        text = text.replace('Colourless, odourless gaseous chemical element', '无色、无味的气态化学元素')
        text = text.replace('Lightest and most abundant element in the universe', '宇宙中最轻、最丰富的元素')
        text = text.replace('Present in water and in all organic compounds', '存在于水和所有有机化合物中')
        text = text.replace('Chemically reacts with most elements', '能与大多数元素发生化学反应')
        text = text.replace('Discovered by', '由').replace('in', '于')
    
    # 处理碳元素的描述
    elif 'Carbon is a member of group 14 of the periodic table' in text:
        text = text.replace('Carbon is a member of group 14 of the periodic table', '碳是元素周期表第14族的成员')
        text = text.replace('It has three allotropic forms of it, diamonds, graphite and fullerite', '它有三种同素异形体：金刚石、石墨和富勒烯')
        text = text.replace('Carbon-14 is commonly used in radioactive dating', '碳-14常用于放射性测年')
        text = text.replace('Carbon occurs in all organic life and is the basis of organic chemistry', '碳存在于所有有机生命中，是有机化学的基础')
        text = text.replace('Carbon has the interesting chemical property of being able to bond with itself, and a wide variety of other elements', '碳具有能够与自身以及多种其他元素结合的有趣化学性质')
    
    # 处理氧元素的描述
    elif 'A colourless, odourless gaseous element belonging to group 16 of the periodic table' in text:
        text = text.replace('A colourless, odourless gaseous element belonging to group 16 of the periodic table', '一种属于元素周期表第16族的无色、无味气态元素')
        text = text.replace('It is the most abundant element present in the earth\'s crust', '它是地壳中含量最丰富的元素')
        text = text.replace('It also makes up 20.8% of the Earth\'s atmosphere', '也占地球大气的20.8%')
        text = text.replace('For industrial purposes, it is separated from liquid air by fractional distillation', '工业上通过液态空气的分馏分离得到')
        text = text.replace('It is used in high temperature welding, and in breathing', '用于高温焊接和呼吸')
        text = text.replace('It commonly comes in the form of Oxygen, but is found as Ozone in the upper atmosphere', '通常以氧气形式存在，但在上层大气中以臭氧形式存在')
        text = text.replace('It was discovered by', '由').replace('in', '于')
    
    # 处理其他常见情况
    else:
        # 替换一些常见的短语
        text = text.replace('An element of', '周期表中第')
        text = text.replace('which belongs to', '属于')
        text = text.replace('There are two', '有两种')
        text = text.replace('It is never found', '从未')
        text = text.replace('It was discovered in', '于')
        text = text.replace('by', '由')
        
        # 替换一些常见的科学术语
        terms = {
            'group': '族',
            'periodic table': '元素周期表',
            'allotropes': '同素异形体',
            'amorphous': '无定形的',
            'metallic': '金属',
            'brown power': '棕色粉末',
            'black': '黑色',
            'hard': '坚硬',
            'Mohs scale': '莫氏硬度',
            'bad conductor': '不良导体',
            'room temperatures': '室温',
            'free in nature': '天然存在',
            'nuclear reactor': '核反应堆',
            'control rods': '控制棒',
            'shields': '屏蔽',
            'discovered': '发现',
            'colourless': '无色',
            'odourless': '无味',
            'gaseous': '气态',
            'chemical element': '化学元素',
            'lightest': '最轻的',
            'most abundant': '最丰富的',
            'universe': '宇宙',
            'present in': '存在于',
            'water': '水',
            'organic compounds': '有机化合物',
            'chemically reacts with': '能与...发生化学反应',
            'most elements': '大多数元素',
            'halogens': '卤素',
            'alkali metals': '碱金属',
            'alkaline-earth metals': '碱土金属',
            'poisonous': '有毒的',
            'pale yellow': '淡黄色',
            'chemically reactive': '化学反应性',
            'electronegative': '电负性',
            'highly dangerous': '高度危险性',
            'severe chemical burns': '严重的化学灼伤',
            'contact with flesh': '与皮肤接触',
            'identified': '鉴定',
            'isolated': '分离',
            'soft': '柔软的',
            'silvery': '银白色',
            'reactive element': '活性元素',
            'oxidizing in air': '在空气中会氧化',
            'reacting violently with water': '与水会剧烈反应',
            'kept under oil': '保存在油中',
            'essential for living organisms': '对生物体至关重要',
            'light alloys': '轻合金',
            'protective oxide coating': '保护性氧化物涂层',
            'exposed to air': '暴露在空气中',
            'burns with an intense white flame': '燃烧时产生强烈的白色火焰',
            'reacts with': '能与...反应',
            'sulphur': '硫',
            'nitrogen': '氮',
            'metalloid': '类金属',
            'non-metallic': '非金属',
            'lustrous': '有光泽的',
            'highly reactive': '高度反应性',
            'protected by': '受...保护',
            'thin transparent layer': '薄而透明的层',
            'oxide': '氧化物',
            'quickly forms in air': '在空气中迅速形成',
            'many alloys': '许多合金',
            'industrial uses': '工业用途',
            'Earth\'s crust': '地球地壳',
            'by weight': '按重量计',
            'second most abundant': '第二丰富的',
            'chemically less reactive': '化学性质比...低',
            'multiple': '多种',
            'non-metallic element': '非金属元素',
            'malleable': '有延展性的',
            'ductile': '可锻的',
            'transition element': '过渡元素',
            'trace element': '微量元素',
            'hemoglobin': '血红蛋白',
            'humans': '人类',
            'moist': '潮湿的',
            'oxidizes': '氧化',
            'displaces': '置换',
            'hydrogen': '氢',
            'dilute': '稀',
            'acids': '酸',
            'combines': '结合',
            'nonmetallic': '非金属',
            'reducing agent': '还原剂',
            'extraction': '提取',
            'thorium': '钍',
            'zirconium': '锆',
            'uranium': '铀',
            'red-brown': '红棕色的',
            'romans': '罗马人',
            'cuprum': 'cuprum',
            'extracted': '提取',
            'used for thousands of years': '已被使用了数千年',
            'excellent conductor': '优良导体',
            'heat': '热',
            'electricity': '电',
            'conditions': '条件',
            'greenish layer': '绿色的物质',
            'forms on the outside': '外部会形成',
            'blue-white': '蓝白色',
            'compounds': '化合物',
            'naturally': '天然地',
            'stable isotopes': '稳定同位素',
            'radioactive isotopes': '放射性同位素',
            'reactive metal': '活泼金属',
            'reacts with': '与...反应',
            'release hydrogen': '释放出氢',
            'white': '白色',
            'elemental form': '单质形式',
            'minerals': '矿物',
            'jewellery': '珠宝',
            'tableware': '餐具',
            'less reactive': '活泼性低'
        }
        
        for en, zh in terms.items():
            text = text.replace(en, zh)
    
    return text

# 主函数
def main():
    # 确保中文目录存在
    chinese_dir = 'chinese'
    if not os.path.exists(chinese_dir):
        os.makedirs(chinese_dir)
    
    # 遍历英文目录下的所有元素页面
    english_dir = 'english'
    for filename in os.listdir(english_dir):
        if filename.endswith('.html'):
            # 提取元素编号
            match = re.match(r'^(\d+)_(.*?)\.html$', filename)
            if match:
                number = match.group(1).zfill(2)  # 确保两位数
                element_name = match.group(2)
                
                # 获取中文元素名称
                chinese_name = element_names.get(element_name, element_name)
                
                # 构建英文和中文文件路径
                english_file = os.path.join(english_dir, filename)
                
                # 获取元素符号
                element_symbol = element_symbols.get(element_name, '')
                
                # 使用元素符号命名中文页面文件
                chinese_file = os.path.join(chinese_dir, f'{number}{element_symbol}.html')
                
                # 提取英文页面信息
                info = extract_info(english_file)
                
                # 直接处理危险类别翻译（确保覆盖所有情况）
                info['safety'] = translate_default(info['safety'])
                
                # 确保CAS号和同义词被正确翻译
                info['cas'] = translate_default(info['cas'])
                info['synonyms'] = translate_default(info['synonyms'])
                
                # 确保描述被正确翻译
                info['description'] = translate_description(info['description'])
                
                # 替换标题中的英文元素名称为中文
                info['title'] = chinese_name + '(' + info['formula'] + ')' if info['formula'] else chinese_name
                info['h1'] = chinese_name + ' (' + info['formula'] + ')' if info['formula'] else chinese_name
                
                # 直接翻译危险类别（确保覆盖所有情况）
                if isinstance(info['safety'], str):
                    if info['safety'].strip().lower() == 'no special hazard information':
                        safety_text = '无特殊危害信息'
                    else:
                        safety_text = translate_default(info['safety'])
                else:
                    safety_text = ''
                
                # 直接构建HTML内容，确保结构完全正确
                chinese_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + info['title'] + '''</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <!-- 导航栏 -->
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

    <!-- 主要内容 -->
    <div class="container">
        <div class="element-detail">
            <h1>''' + info['h1'] + '''</h1>
            
            <div class="element-info">
                <div class="info-card">
                    <p><strong>危险类别：</strong>''' + safety_text + '''</p>
                </div>

                <div class="info-card">
                    <p><strong>分子式：</strong>''' + info['formula'] + '''</p>
                    <p><strong>分子量：</strong>''' + info['weight'] + '''</p>
                </div>

                <div class="info-card">
                    <p><strong>CAS号：</strong>''' + info['cas'] + '''</p>
                    <p><strong>同义词：</strong>''' + info['synonyms'] + '''</p>
                </div>

                <div class="info-card">
                    <p><strong>创建日期：</strong>''' + info['creation'] + '''</p>
                </div>
            </div>
            
            <div class="element-description">
                <h3>描述</h3>
                <p>''' + info['description'] + '''</p>
            </div>
        </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
        <p>&copy; 2024 Chemistry World. All rights reserved.</p>
    </footer>

    <script>
        // 汉堡菜单功能
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.querySelector('.nav-links');

        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    </script>
</body>
</html>'''
                
                # 写入中文页面
                with open(chinese_file, 'w', encoding='utf-8') as f:
                    f.write(chinese_content)
                
                print(f'已创建中文页面：{chinese_file}')

if __name__ == '__main__':
    main()
    print('所有中文元素页面创建完成！')
