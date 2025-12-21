// 元素数据数组
const elements = [
    { name: 'Hydrogen', link: 'english/1_Hydrogen.html' },
    { name: 'Helium', link: 'english/2_Helium.html' },
    { name: 'Lithium', link: 'english/3_Lithium.html' },
    { name: 'Beryllium', link: 'english/4_Beryllium.html' },
    { name: 'Boron', link: 'english/5_Boron.html' },
    { name: 'Carbon', link: 'english/6_Carbon.html' },
    { name: 'Nitrogen', link: 'english/7_Nitrogen.html' },
    { name: 'Oxygen', link: 'english/8_Oxygen.html' },
    { name: 'Fluorine', link: 'english/9_Fluorine.html' },
    { name: 'Neon', link: 'english/10_Neon.html' },
    { name: 'Sodium', link: 'english/11_Sodium.html' },
    { name: 'Magnesium', link: 'english/12_Magnesium.html' },
    { name: 'Aluminum', link: 'english/13_Aluminum.html' },
    { name: 'Silicon', link: 'english/14_Silicon.html' },
    { name: 'Phosphorus', link: 'english/15_Phosphorus.html' },
    { name: 'Sulfur', link: 'english/16_Sulfur.html' },
    { name: 'Chlorine', link: 'english/17_Chlorine.html' },
    { name: 'Argon', link: 'english/18_Argon.html' },
    { name: 'Potassium', link: 'english/19_Potassium.html' },
    { name: 'Calcium', link: 'english/20_Calcium.html' },
    { name: 'Scandium', link: 'english/21_Scandium.html' },
    { name: 'Titanium', link: 'english/22_Titanium.html' },
    { name: 'Vanadium', link: 'english/23_Vanadium.html' },
    { name: 'Chromium', link: 'english/24_Chromium.html' },
    { name: 'Manganese', link: 'english/25_Manganese.html' },
    { name: 'Iron', link: 'english/26_Iron.html' },
    { name: 'Cobalt', link: 'english/27_Cobalt.html' },
    { name: 'Nickel', link: 'english/28_Nickel.html' },
    { name: 'Copper', link: 'english/29_Copper.html' },
    { name: 'Zinc', link: 'english/30_Zinc.html' },
    { name: 'Gallium', link: 'english/31_Gallium.html' },
    { name: 'Germanium', link: 'english/32_Germanium.html' },
    { name: 'Arsenic', link: 'english/33_Arsenic.html' },
    { name: 'Selenium', link: 'english/34_Selenium.html' },
    { name: 'Bromine', link: 'english/35_Bromine.html' },
    { name: 'Krypton', link: 'english/36_Krypton.html' },
    { name: 'Rubidium', link: 'english/37_Rubidium.html' },
    { name: 'Strontium', link: 'english/38_Strontium.html' },
    { name: 'Yttrium', link: 'english/39_Yttrium.html' },
    { name: 'Zirconium', link: 'english/40_Zirconium.html' },
    { name: 'Niobium', link: 'english/41_Niobium.html' },
    { name: 'Molybdenum', link: 'english/42_Molybdenum.html' },
    { name: 'Technetium', link: 'english/43_Technetium.html' },
    { name: 'Ruthenium', link: 'english/44_Ruthenium.html' },
    { name: 'Rhodium', link: 'english/45_Rhodium.html' },
    { name: 'Palladium', link: 'english/46_Palladium.html' },
    { name: 'Silver', link: 'english/47_Silver.html' },
    { name: 'Cadmium', link: 'english/48_Cadmium.html' },
    { name: 'Indium', link: 'english/49_Indium.html' },
    { name: 'Tin', link: 'english/50_Tin.html' },
    { name: 'Antimony', link: 'english/51_Antimony.html' },
    { name: 'Tellurium', link: 'english/52_Tellurium.html' },
    { name: 'Iodine', link: 'english/53_Iodine.html' },
    { name: 'Xenon', link: 'english/54_Xenon.html' },
    { name: 'Cesium', link: 'english/55_Cesium.html' },
    { name: 'Barium', link: 'english/56_Barium.html' },
    { name: 'Lanthanum', link: 'english/57_Lanthanum.html' },
    { name: 'Cerium', link: 'english/58_Cerium.html' },
    { name: 'Praseodymium', link: 'english/59_Praseodymium.html' },
    { name: 'Neodymium', link: 'english/60_Neodymium.html' },
    { name: 'Promethium', link: 'english/61_Promethium.html' },
    { name: 'Samarium', link: 'english/62_Samarium.html' },
    { name: 'Europium', link: 'english/63_Europium.html' },
    { name: 'Gadolinium', link: 'english/64_Gadolinium.html' },
    { name: 'Terbium', link: 'english/65_Terbium.html' },
    { name: 'Dysprosium', link: 'english/66_Dysprosium.html' },
    { name: 'Holmium', link: 'english/67_Holmium.html' },
    { name: 'Erbium', link: 'english/68_Erbium.html' },
    { name: 'Thulium', link: 'english/69_Thulium.html' },
    { name: 'Ytterbium', link: 'english/70_Ytterbium.html' },
    { name: 'Lutetium', link: 'english/71_Lutetium.html' },
    { name: 'Hafnium', link: 'english/72_Hafnium.html' },
    { name: 'Tantalum', link: 'english/73_Tantalum.html' },
    { name: 'Tungsten', link: 'english/74_Tungsten.html' },
    { name: 'Rhenium', link: 'english/75_Rhenium.html' },
    { name: 'Osmium', link: 'english/76_Osmium.html' },
    { name: 'Iridium', link: 'english/77_Iridium.html' },
    { name: 'Platinum', link: 'english/78_Platinum.html' },
    { name: 'Gold', link: 'english/79_Gold.html' },
    { name: 'Mercury', link: 'english/80_Mercury.html' },
    { name: 'Thallium', link: 'english/81_Thallium.html' },
    { name: 'Lead', link: 'english/82_Lead.html' },
    { name: 'Bismuth', link: 'english/83_Bismuth.html' },
    { name: 'Polonium', link: 'english/84_Polonium.html' },
    { name: 'Astatine', link: 'english/85_Astatine.html' },
    { name: 'Radon', link: 'english/86_Radon.html' },
    { name: 'Francium', link: 'english/87_Francium.html' },
    { name: 'Radium', link: 'english/88_Radium.html' },
    { name: 'Actinium', link: 'english/89_Actinium.html' },
    { name: 'Thorium', link: 'english/90_Thorium.html' },
    { name: 'Protactinium', link: 'english/91_Protactinium.html' },
    { name: 'Uranium', link: 'english/92_Uranium.html' },
    { name: 'Neptunium', link: 'english/93_Neptunium.html' },
    { name: 'Plutonium', link: 'english/94_Plutonium.html' },
    { name: 'Americium', link: 'english/95_Americium.html' },
    { name: 'Curium', link: 'english/96_Curium.html' },
    { name: 'Berkelium', link: 'english/97_Berkelium.html' },
    { name: 'Californium', link: 'english/98_Californium.html' },
    { name: 'Einsteinium', link: 'english/99_Einsteinium.html' },
    { name: 'Fermium', link: 'english/100_Fermium.html' },
    { name: 'Mendelevium', link: 'english/101_Mendelevium.html' },
    { name: 'Nobelium', link: 'english/102_Nobelium.html' },
    { name: 'Lawrencium', link: 'english/103_Lawrencium.html' },
    { name: 'Rutherfordium', link: 'english/104_Rutherfordium.html' },
    { name: 'Dubnium', link: 'english/105_Dubnium.html' },
    { name: 'Seaborgium', link: 'english/106_Seaborgium.html' },
    { name: 'Bohrium', link: 'english/107_Bohrium.html' },
    { name: 'Hassium', link: 'english/108_Hassium.html' },
    { name: 'Meitnerium', link: 'english/109_Meitnerium.html' },
    { name: 'Darmstadtium', link: 'english/110_Darmstadtium.html' },
    { name: 'Roentgenium', link: 'english/111_Roentgenium.html' },
    { name: 'Copernicium', link: 'english/112_Copernicium.html' },
    { name: 'Nihonium', link: 'english/113_Nihonium.html' },
    { name: 'Flerovium', link: 'english/114_Flerovium.html' },
    { name: 'Moscovium', link: 'english/115_Moscovium.html' },
    { name: 'Livermorium', link: 'english/116_Livermorium.html' },
    { name: 'Tennessine', link: 'english/117_Tennessine.html' },
    { name: 'Oganesson', link: 'english/118_Oganesson.html' }
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
    // 设置链接的文本内容
    link.textContent = element.name;

    // 将 <a> 标签添加到导航元素中
    elementList.appendChild(link);
});

// 添加搜索功能
document.addEventListener('DOMContentLoaded', () => {
    const searchBox = document.getElementById('search-box');
    const searchBtn = document.getElementById('search-btn');
    const elementLinks = document.querySelectorAll('.element-link');

    // 搜索函数
    function searchElements() {
        const searchTerm = searchBox.value.toLowerCase().trim();
        
        elementLinks.forEach(link => {
            const elementName = link.textContent.toLowerCase().trim();
            if (elementName.includes(searchTerm)) {
                link.style.display = 'flex';
            } else {
                link.style.display = 'none';
            }
        });
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
});