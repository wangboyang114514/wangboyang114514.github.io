// 元素数据数组
const elements = [
    { name: 'Hydrogen', symbol: 'H', atomicNumber: 1, category: 'nonmetal', link: 'english/1_Hydrogen.html' },
    { name: 'Helium', symbol: 'He', atomicNumber: 2, category: 'noble-gas', link: 'english/2_Helium.html' },
    { name: 'Lithium', symbol: 'Li', atomicNumber: 3, category: 'alkali-metal', link: 'english/3_Lithium.html' },
    { name: 'Beryllium', symbol: 'Be', atomicNumber: 4, category: 'alkaline-earth-metal', link: 'english/4_Beryllium.html' },
    { name: 'Boron', symbol: 'B', atomicNumber: 5, category: 'metalloid', link: 'english/5_Boron.html' },
    { name: 'Carbon', symbol: 'C', atomicNumber: 6, category: 'nonmetal', link: 'english/6_Carbon.html' },
    { name: 'Nitrogen', symbol: 'N', atomicNumber: 7, category: 'nonmetal', link: 'english/7_Nitrogen.html' },
    { name: 'Oxygen', symbol: 'O', atomicNumber: 8, category: 'nonmetal', link: 'english/8_Oxygen.html' },
    { name: 'Fluorine', symbol: 'F', atomicNumber: 9, category: 'halogen', link: 'english/9_Fluorine.html' },
    { name: 'Neon', symbol: 'Ne', atomicNumber: 10, category: 'noble-gas', link: 'english/10_Neon.html' },
    { name: 'Sodium', symbol: 'Na', atomicNumber: 11, category: 'alkali-metal', link: 'english/11_Sodium.html' },
    { name: 'Magnesium', symbol: 'Mg', atomicNumber: 12, category: 'alkaline-earth-metal', link: 'english/12_Magnesium.html' },
    { name: 'Aluminum', symbol: 'Al', atomicNumber: 13, category: 'metal', link: 'english/13_Aluminum.html' },
    { name: 'Silicon', symbol: 'Si', atomicNumber: 14, category: 'metalloid', link: 'english/14_Silicon.html' },
    { name: 'Phosphorus', symbol: 'P', atomicNumber: 15, category: 'nonmetal', link: 'english/15_Phosphorus.html' },
    { name: 'Sulfur', symbol: 'S', atomicNumber: 16, category: 'nonmetal', link: 'english/16_Sulfur.html' },
    { name: 'Chlorine', symbol: 'Cl', atomicNumber: 17, category: 'halogen', link: 'english/17_Chlorine.html' },
    { name: 'Argon', symbol: 'Ar', atomicNumber: 18, category: 'noble-gas', link: 'english/18_Argon.html' },
    { name: 'Potassium', symbol: 'K', atomicNumber: 19, category: 'alkali-metal', link: 'english/19_Potassium.html' },
    { name: 'Calcium', symbol: 'Ca', atomicNumber: 20, category: 'alkaline-earth-metal', link: 'english/20_Calcium.html' },
    { name: 'Scandium', symbol: 'Sc', atomicNumber: 21, category: 'metal', link: 'english/21_Scandium.html' },
    { name: 'Titanium', symbol: 'Ti', atomicNumber: 22, category: 'metal', link: 'english/22_Titanium.html' },
    { name: 'Vanadium', symbol: 'V', atomicNumber: 23, category: 'metal', link: 'english/23_Vanadium.html' },
    { name: 'Chromium', symbol: 'Cr', atomicNumber: 24, category: 'metal', link: 'english/24_Chromium.html' },
    { name: 'Manganese', symbol: 'Mn', atomicNumber: 25, category: 'metal', link: 'english/25_Manganese.html' },
    { name: 'Iron', symbol: 'Fe', atomicNumber: 26, category: 'metal', link: 'english/26_Iron.html' },
    { name: 'Cobalt', symbol: 'Co', atomicNumber: 27, category: 'metal', link: 'english/27_Cobalt.html' },
    { name: 'Nickel', symbol: 'Ni', atomicNumber: 28, category: 'metal', link: 'english/28_Nickel.html' },
    { name: 'Copper', symbol: 'Cu', atomicNumber: 29, category: 'metal', link: 'english/29_Copper.html' },
    { name: 'Zinc', symbol: 'Zn', atomicNumber: 30, category: 'metal', link: 'english/30_Zinc.html' },
    { name: 'Gallium', symbol: 'Ga', atomicNumber: 31, category: 'metal', link: 'english/31_Gallium.html' },
    { name: 'Germanium', symbol: 'Ge', atomicNumber: 32, category: 'metalloid', link: 'english/32_Germanium.html' },
    { name: 'Arsenic', symbol: 'As', atomicNumber: 33, category: 'metalloid', link: 'english/33_Arsenic.html' },
    { name: 'Selenium', symbol: 'Se', atomicNumber: 34, category: 'nonmetal', link: 'english/34_Selenium.html' },
    { name: 'Bromine', symbol: 'Br', atomicNumber: 35, category: 'halogen', link: 'english/35_Bromine.html' },
    { name: 'Krypton', symbol: 'Kr', atomicNumber: 36, category: 'noble-gas', link: 'english/36_Krypton.html' },
    { name: 'Rubidium', symbol: 'Rb', atomicNumber: 37, category: 'alkali-metal', link: 'english/37_Rubidium.html' },
    { name: 'Strontium', symbol: 'Sr', atomicNumber: 38, category: 'alkaline-earth-metal', link: 'english/38_Strontium.html' },
    { name: 'Yttrium', symbol: 'Y', atomicNumber: 39, category: 'metal', link: 'english/39_Yttrium.html' },
    { name: 'Zirconium', symbol: 'Zr', atomicNumber: 40, category: 'metal', link: 'english/40_Zirconium.html' },
    { name: 'Niobium', symbol: 'Nb', atomicNumber: 41, category: 'metal', link: 'english/41_Niobium.html' },
    { name: 'Molybdenum', symbol: 'Mo', atomicNumber: 42, category: 'metal', link: 'english/42_Molybdenum.html' },
    { name: 'Technetium', symbol: 'Tc', atomicNumber: 43, category: 'metal', link: 'english/43_Technetium.html' },
    { name: 'Ruthenium', symbol: 'Ru', atomicNumber: 44, category: 'metal', link: 'english/44_Ruthenium.html' },
    { name: 'Rhodium', symbol: 'Rh', atomicNumber: 45, category: 'metal', link: 'english/45_Rhodium.html' },
    { name: 'Palladium', symbol: 'Pd', atomicNumber: 46, category: 'metal', link: 'english/46_Palladium.html' },
    { name: 'Silver', symbol: 'Ag', atomicNumber: 47, category: 'metal', link: 'english/47_Silver.html' },
    { name: 'Cadmium', symbol: 'Cd', atomicNumber: 48, category: 'metal', link: 'english/48_Cadmium.html' },
    { name: 'Indium', symbol: 'In', atomicNumber: 49, category: 'metal', link: 'english/49_Indium.html' },
    { name: 'Tin', symbol: 'Sn', atomicNumber: 50, category: 'metal', link: 'english/50_Tin.html' },
    { name: 'Antimony', symbol: 'Sb', atomicNumber: 51, category: 'metalloid', link: 'english/51_Antimony.html' },
    { name: 'Tellurium', symbol: 'Te', atomicNumber: 52, category: 'metalloid', link: 'english/52_Tellurium.html' },
    { name: 'Iodine', symbol: 'I', atomicNumber: 53, category: 'halogen', link: 'english/53_Iodine.html' },
    { name: 'Xenon', symbol: 'Xe', atomicNumber: 54, category: 'noble-gas', link: 'english/54_Xenon.html' },
    { name: 'Cesium', symbol: 'Cs', atomicNumber: 55, category: 'alkali-metal', link: 'english/55_Cesium.html' },
    { name: 'Barium', symbol: 'Ba', atomicNumber: 56, category: 'alkaline-earth-metal', link: 'english/56_Barium.html' },
    { name: 'Lanthanum', symbol: 'La', atomicNumber: 57, category: 'metal', link: 'english/57_Lanthanum.html' },
    { name: 'Cerium', symbol: 'Ce', atomicNumber: 58, category: 'metal', link: 'english/58_Cerium.html' },
    { name: 'Praseodymium', symbol: 'Pr', atomicNumber: 59, category: 'metal', link: 'english/59_Praseodymium.html' },
    { name: 'Neodymium', symbol: 'Nd', atomicNumber: 60, category: 'metal', link: 'english/60_Neodymium.html' },
    { name: 'Promethium', symbol: 'Pm', atomicNumber: 61, category: 'metal', link: 'english/61_Promethium.html' },
    { name: 'Samarium', symbol: 'Sm', atomicNumber: 62, category: 'metal', link: 'english/62_Samarium.html' },
    { name: 'Europium', symbol: 'Eu', atomicNumber: 63, category: 'metal', link: 'english/63_Europium.html' },
    { name: 'Gadolinium', symbol: 'Gd', atomicNumber: 64, category: 'metal', link: 'english/64_Gadolinium.html' },
    { name: 'Terbium', symbol: 'Tb', atomicNumber: 65, category: 'metal', link: 'english/65_Terbium.html' },
    { name: 'Dysprosium', symbol: 'Dy', atomicNumber: 66, category: 'metal', link: 'english/66_Dysprosium.html' },
    { name: 'Holmium', symbol: 'Ho', atomicNumber: 67, category: 'metal', link: 'english/67_Holmium.html' },
    { name: 'Erbium', symbol: 'Er', atomicNumber: 68, category: 'metal', link: 'english/68_Erbium.html' },
    { name: 'Thulium', symbol: 'Tm', atomicNumber: 69, category: 'metal', link: 'english/69_Thulium.html' },
    { name: 'Ytterbium', symbol: 'Yb', atomicNumber: 70, category: 'metal', link: 'english/70_Ytterbium.html' },
    { name: 'Lutetium', symbol: 'Lu', atomicNumber: 71, category: 'metal', link: 'english/71_Lutetium.html' },
    { name: 'Hafnium', symbol: 'Hf', atomicNumber: 72, category: 'metal', link: 'english/72_Hafnium.html' },
    { name: 'Tantalum', symbol: 'Ta', atomicNumber: 73, category: 'metal', link: 'english/73_Tantalum.html' },
    { name: 'Tungsten', symbol: 'W', atomicNumber: 74, category: 'metal', link: 'english/74_Tungsten.html' },
    { name: 'Rhenium', symbol: 'Re', atomicNumber: 75, category: 'metal', link: 'english/75_Rhenium.html' },
    { name: 'Osmium', symbol: 'Os', atomicNumber: 76, category: 'metal', link: 'english/76_Osmium.html' },
    { name: 'Iridium', symbol: 'Ir', atomicNumber: 77, category: 'metal', link: 'english/77_Iridium.html' },
    { name: 'Platinum', symbol: 'Pt', atomicNumber: 78, category: 'metal', link: 'english/78_Platinum.html' },
    { name: 'Gold', symbol: 'Au', atomicNumber: 79, category: 'metal', link: 'english/79_Gold.html' },
    { name: 'Mercury', symbol: 'Hg', atomicNumber: 80, category: 'metal', link: 'english/80_Mercury.html' },
    { name: 'Thallium', symbol: 'Tl', atomicNumber: 81, category: 'metal', link: 'english/81_Thallium.html' },
    { name: 'Lead', symbol: 'Pb', atomicNumber: 82, category: 'metal', link: 'english/82_Lead.html' },
    { name: 'Bismuth', symbol: 'Bi', atomicNumber: 83, category: 'metal', link: 'english/83_Bismuth.html' },
    { name: 'Polonium', symbol: 'Po', atomicNumber: 84, category: 'metal', link: 'english/84_Polonium.html' },
    { name: 'Astatine', symbol: 'At', atomicNumber: 85, category: 'halogen', link: 'english/85_Astatine.html' },
    { name: 'Radon', symbol: 'Rn', atomicNumber: 86, category: 'noble-gas', link: 'english/86_Radon.html' },
    { name: 'Francium', symbol: 'Fr', atomicNumber: 87, category: 'alkali-metal', link: 'english/87_Francium.html' },
    { name: 'Radium', symbol: 'Ra', atomicNumber: 88, category: 'alkaline-earth-metal', link: 'english/88_Radium.html' },
    { name: 'Actinium', symbol: 'Ac', atomicNumber: 89, category: 'metal', link: 'english/89_Actinium.html' },
    { name: 'Thorium', symbol: 'Th', atomicNumber: 90, category: 'metal', link: 'english/90_Thorium.html' },
    { name: 'Protactinium', symbol: 'Pa', atomicNumber: 91, category: 'metal', link: 'english/91_Protactinium.html' },
    { name: 'Uranium', symbol: 'U', atomicNumber: 92, category: 'metal', link: 'english/92_Uranium.html' },
    { name: 'Neptunium', symbol: 'Np', atomicNumber: 93, category: 'metal', link: 'english/93_Neptunium.html' },
    { name: 'Plutonium', symbol: 'Pu', atomicNumber: 94, category: 'metal', link: 'english/94_Plutonium.html' },
    { name: 'Americium', symbol: 'Am', atomicNumber: 95, category: 'metal', link: 'english/95_Americium.html' },
    { name: 'Curium', symbol: 'Cm', atomicNumber: 96, category: 'metal', link: 'english/96_Curium.html' },
    { name: 'Berkelium', symbol: 'Bk', atomicNumber: 97, category: 'metal', link: 'english/97_Berkelium.html' },
    { name: 'Californium', symbol: 'Cf', atomicNumber: 98, category: 'metal', link: 'english/98_Californium.html' },
    { name: 'Einsteinium', symbol: 'Es', atomicNumber: 99, category: 'metal', link: 'english/99_Einsteinium.html' },
    { name: 'Fermium', symbol: 'Fm', atomicNumber: 100, category: 'metal', link: 'english/100_Fermium.html' },
    { name: 'Mendelevium', symbol: 'Md', atomicNumber: 101, category: 'metal', link: 'english/101_Mendelevium.html' },
    { name: 'Nobelium', symbol: 'No', atomicNumber: 102, category: 'metal', link: 'english/102_Nobelium.html' },
    { name: 'Lawrencium', symbol: 'Lr', atomicNumber: 103, category: 'metal', link: 'english/103_Lawrencium.html' },
    { name: 'Rutherfordium', symbol: 'Rf', atomicNumber: 104, category: 'metal', link: 'english/104_Rutherfordium.html' },
    { name: 'Dubnium', symbol: 'Db', atomicNumber: 105, category: 'metal', link: 'english/105_Dubnium.html' },
    { name: 'Seaborgium', symbol: 'Sg', atomicNumber: 106, category: 'metal', link: 'english/106_Seaborgium.html' },
    { name: 'Bohrium', symbol: 'Bh', atomicNumber: 107, category: 'metal', link: 'english/107_Bohrium.html' },
    { name: 'Hassium', symbol: 'Hs', atomicNumber: 108, category: 'metal', link: 'english/108_Hassium.html' },
    { name: 'Meitnerium', symbol: 'Mt', atomicNumber: 109, category: 'metal', link: 'english/109_Meitnerium.html' },
    { name: 'Darmstadtium', symbol: 'Ds', atomicNumber: 110, category: 'metal', link: 'english/110_Darmstadtium.html' },
    { name: 'Roentgenium', symbol: 'Rg', atomicNumber: 111, category: 'metal', link: 'english/111_Roentgenium.html' },
    { name: 'Copernicium', symbol: 'Cn', atomicNumber: 112, category: 'metal', link: 'english/112_Copernicium.html' },
    { name: 'Nihonium', symbol: 'Nh', atomicNumber: 113, category: 'metal', link: 'english/113_Nihonium.html' },
    { name: 'Flerovium', symbol: 'Fl', atomicNumber: 114, category: 'metal', link: 'english/114_Flerovium.html' },
    { name: 'Moscovium', symbol: 'Mc', atomicNumber: 115, category: 'metal', link: 'english/115_Moscovium.html' },
    { name: 'Livermorium', symbol: 'Lv', atomicNumber: 116, category: 'metal', link: 'english/116_Livermorium.html' },
    { name: 'Tennessine', symbol: 'Ts', atomicNumber: 117, category: 'halogen', link: 'english/117_Tennessine.html' },
    { name: 'Oganesson', symbol: 'Og', atomicNumber: 118, category: 'noble-gas', link: 'english/118_Oganesson.html' }
];

// 获取导航元素
const elementList = document.getElementById('element-list');

// 遍历元素信息数组
elements.forEach(element => {
    // 创建一个 <a> 标签
    const link = document.createElement('a');
    // 设置链接的 href 属性
    link.href = element.link;
    // 添加 element-link 类
    link.classList.add('element-link');
    // 添加分类类
    if (element.category) {
        link.classList.add(element.category);
    }
    // 设置链接的内容
    link.innerHTML = `
        <div class="element-number">${element.atomicNumber || ''}</div>
        <div class="element-symbol">${element.symbol || ''}</div>
        <div class="element-name">${element.name}</div>
    `;

    // 将 <a> 标签添加到导航元素中
    elementList.appendChild(link);
});

// 添加搜索、筛选和视图切换功能
document.addEventListener('DOMContentLoaded', () => {
    const searchBox = document.getElementById('search-box');
    const searchBtn = document.getElementById('search-btn');
    const elementLinks = document.querySelectorAll('.element-link');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const viewToggleBtns = document.querySelectorAll('.view-toggle-btn');
    const gridView = document.getElementById('element-list');
    const periodicView = document.getElementById('periodic-table');
    let currentFilter = 'all';
    let currentView = 'grid';

    // 搜索函数
    function searchElements() {
        const searchTerm = searchBox.value.toLowerCase().trim();
        
        elementLinks.forEach(link => {
            const elementName = link.textContent.toLowerCase().trim();
            const elementCategory = link.classList.contains('metal') ? 'metal' : 
                                  link.classList.contains('nonmetal') ? 'nonmetal' : 
                                  link.classList.contains('metalloid') ? 'metalloid' : 
                                  link.classList.contains('noble-gas') ? 'noble-gas' : 
                                  link.classList.contains('halogen') ? 'halogen' : 
                                  link.classList.contains('alkali-metal') ? 'alkali-metal' : 
                                  link.classList.contains('alkaline-earth-metal') ? 'alkaline-earth-metal' : 'all';
            
            const matchesSearch = elementName.includes(searchTerm);
            const matchesFilter = currentFilter === 'all' || elementCategory === currentFilter;
            
            if (matchesSearch && matchesFilter) {
                link.style.display = 'flex';
            } else {
                link.style.display = 'none';
            }
        });
    }

    // 筛选函数
    function filterElements(filter) {
        currentFilter = filter;
        
        // 更新筛选按钮状态
        filterBtns.forEach(btn => {
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // 应用筛选
        searchElements();
    }

    // 搜索按钮点击事件
    searchBtn.addEventListener('click', searchElements);

    // 搜索框输入事件
    searchBox.addEventListener('input', searchElements);

    // 回车键搜索
    searchBox.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchElements();
        }
    });

    // 筛选按钮点击事件
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterElements(btn.dataset.filter);
        });
    });

    // 视图切换函数
    function switchView(view) {
        currentView = view;
        
        // 更新视图切换按钮状态
        viewToggleBtns.forEach(btn => {
            if (btn.dataset.view === view) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // 显示/隐藏对应视图
        if (view === 'grid') {
            gridView.style.display = 'flex';
            periodicView.style.display = 'none';
        } else if (view === 'periodic') {
            gridView.style.display = 'none';
            periodicView.style.display = 'grid';
            generatePeriodicTable();
        }
    }

    // 生成周期表
    function generatePeriodicTable() {
        // 清空周期表容器
        periodicView.innerHTML = '';
        
        // 周期表布局数据（简化版，仅包含前20个元素）
        const periodicLayout = [
            [1],
            [2],
            [3, 4, null, null, null, null, null, null, null, null, null, null, 5, 6, 7, 8, 9, 10],
            [11, 12, null, null, null, null, null, null, null, null, null, null, 13, 14, 15, 16, 17, 18],
            [19, 20]
        ];
        
        // 遍历周期表布局
        periodicLayout.forEach(row => {
            row.forEach(atomicNumber => {
                if (atomicNumber) {
                    const element = elements.find(el => el.atomicNumber === atomicNumber);
                    if (element) {
                        const periodicElement = document.createElement('a');
                        periodicElement.href = element.link;
                        periodicElement.classList.add('periodic-element');
                        if (element.category) {
                            periodicElement.classList.add(element.category);
                        }
                        periodicElement.innerHTML = `
                            <div class="element-number">${element.atomicNumber}</div>
                            <div class="element-symbol">${element.symbol}</div>
                            <div class="element-name">${element.name}</div>
                        `;
                        periodicView.appendChild(periodicElement);
                    }
                } else {
                    // 创建空白元素
                    const emptyElement = document.createElement('div');
                    emptyElement.style.minWidth = '60px';
                    emptyElement.style.height = '60px';
                    periodicView.appendChild(emptyElement);
                }
            });
        });
    }

    // 视图切换按钮点击事件
    viewToggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchView(btn.dataset.view);
        });
    });
});