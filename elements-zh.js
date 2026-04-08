// 元素数据数组
const elements = [
    { name: '氢', symbol: 'H', atomicNumber: 1, category: 'nonmetal', link: 'chinese/01H.html' },
    { name: '氦', symbol: 'He', atomicNumber: 2, category: 'noble-gas', link: 'chinese/02He.html' },
    { name: '锂', symbol: 'Li', atomicNumber: 3, category: 'alkali-metal', link: 'chinese/03Li.html' },
    { name: '铍', symbol: 'Be', atomicNumber: 4, category: 'alkaline-earth-metal', link: 'chinese/04Be.html' },
    { name: '硼', symbol: 'B', atomicNumber: 5, category: 'metalloid', link: 'chinese/05B.html' },
    { name: '碳', symbol: 'C', atomicNumber: 6, category: 'nonmetal', link: 'chinese/06C.html' },
    { name: '氮', symbol: 'N', atomicNumber: 7, category: 'nonmetal', link: 'chinese/07N.html' },
    { name: '氧', symbol: 'O', atomicNumber: 8, category: 'nonmetal', link: 'chinese/08O.html' },
    { name: '氟', symbol: 'F', atomicNumber: 9, category: 'halogen', link: 'chinese/09F.html' },
    { name: '氖', symbol: 'Ne', atomicNumber: 10, category: 'noble-gas', link: 'chinese/10Ne.html' },
    { name: '钠', symbol: 'Na', atomicNumber: 11, category: 'alkali-metal', link: 'chinese/11Na.html' },
    { name: '镁', symbol: 'Mg', atomicNumber: 12, category: 'alkaline-earth-metal', link: 'chinese/12Mg.html' },
    { name: '铝', symbol: 'Al', atomicNumber: 13, category: 'metal', link: 'chinese/13Al.html' },
    { name: '硅', symbol: 'Si', atomicNumber: 14, category: 'metalloid', link: 'chinese/14Si.html' },
    { name: '磷', symbol: 'P', atomicNumber: 15, category: 'nonmetal', link: 'chinese/15P.html' },
    { name: '硫', symbol: 'S', atomicNumber: 16, category: 'nonmetal', link: 'chinese/16S.html' },
    { name: '氯', symbol: 'Cl', atomicNumber: 17, category: 'halogen', link: 'chinese/17Cl.html' },
    { name: '氩', symbol: 'Ar', atomicNumber: 18, category: 'noble-gas', link: 'chinese/18Ar.html' },
    { name: '钾', symbol: 'K', atomicNumber: 19, category: 'alkali-metal', link: 'chinese/19K.html' },
    { name: '钙', symbol: 'Ca', atomicNumber: 20, category: 'alkaline-earth-metal', link: 'chinese/20Ca.html' },
    { name: '钪', symbol: 'Sc', atomicNumber: 21, category: 'metal', link: 'chinese/21Sc.html' },
    { name: '钛', symbol: 'Ti', atomicNumber: 22, category: 'metal', link: 'chinese/22Ti.html' },
    { name: '钒', symbol: 'V', atomicNumber: 23, category: 'metal', link: 'chinese/23V.html' },
    { name: '铬', symbol: 'Cr', atomicNumber: 24, category: 'metal', link: 'chinese/24Cr.html' },
    { name: '锰', symbol: 'Mn', atomicNumber: 25, category: 'metal', link: 'chinese/25Mn.html' },
    { name: '铁', symbol: 'Fe', atomicNumber: 26, category: 'metal', link: 'chinese/26Fe.html' },
    { name: '钴', symbol: 'Co', atomicNumber: 27, category: 'metal', link: 'chinese/27Co.html' },
    { name: '镍', symbol: 'Ni', atomicNumber: 28, category: 'metal', link: 'chinese/28Ni.html' },
    { name: '铜', symbol: 'Cu', atomicNumber: 29, category: 'metal', link: 'chinese/29Cu.html' },
    { name: '锌', symbol: 'Zn', atomicNumber: 30, category: 'metal', link: 'chinese/30Zn.html' },
    { name: '镓', symbol: 'Ga', atomicNumber: 31, category: 'metal', link: 'chinese/31Ga.html' },
    { name: '锗', symbol: 'Ge', atomicNumber: 32, category: 'metalloid', link: 'chinese/32Ge.html' },
    { name: '砷', symbol: 'As', atomicNumber: 33, category: 'metalloid', link: 'chinese/33As.html' },
    { name: '硒', symbol: 'Se', atomicNumber: 34, category: 'nonmetal', link: 'chinese/34Se.html' },
    { name: '溴', symbol: 'Br', atomicNumber: 35, category: 'halogen', link: 'chinese/35Br.html' },
    { name: '氪', symbol: 'Kr', atomicNumber: 36, category: 'noble-gas', link: 'chinese/36Kr.html' },
    { name: '铷', symbol: 'Rb', atomicNumber: 37, category: 'alkali-metal', link: 'chinese/37Rb.html' },
    { name: '锶', symbol: 'Sr', atomicNumber: 38, category: 'alkaline-earth-metal', link: 'chinese/38Sr.html' },
    { name: '钇', symbol: 'Y', atomicNumber: 39, category: 'metal', link: 'chinese/39Y.html' },
    { name: '锆', symbol: 'Zr', atomicNumber: 40, category: 'metal', link: 'chinese/40Zr.html' },
    { name: '铌', symbol: 'Nb', atomicNumber: 41, category: 'metal', link: 'chinese/41Nb.html' },
    { name: '钼', symbol: 'Mo', atomicNumber: 42, category: 'metal', link: 'chinese/42Mo.html' },
    { name: '锝', symbol: 'Tc', atomicNumber: 43, category: 'metal', link: 'chinese/43Tc.html' },
    { name: '钌', symbol: 'Ru', atomicNumber: 44, category: 'metal', link: 'chinese/44Ru.html' },
    { name: '铑', symbol: 'Rh', atomicNumber: 45, category: 'metal', link: 'chinese/45Rh.html' },
    { name: '钯', symbol: 'Pd', atomicNumber: 46, category: 'metal', link: 'chinese/46Pd.html' },
    { name: '银', symbol: 'Ag', atomicNumber: 47, category: 'metal', link: 'chinese/47Ag.html' },
    { name: '镉', symbol: 'Cd', atomicNumber: 48, category: 'metal', link: 'chinese/48Cd.html' },
    { name: '铟', symbol: 'In', atomicNumber: 49, category: 'metal', link: 'chinese/49In.html' },
    { name: '锡', symbol: 'Sn', atomicNumber: 50, category: 'metal', link: 'chinese/50Sn.html' },
    { name: '锑', symbol: 'Sb', atomicNumber: 51, category: 'metalloid', link: 'chinese/51Sb.html' },
    { name: '碲', symbol: 'Te', atomicNumber: 52, category: 'metalloid', link: 'chinese/52Te.html' },
    { name: '碘', symbol: 'I', atomicNumber: 53, category: 'halogen', link: 'chinese/53I.html' },
    { name: '氙', symbol: 'Xe', atomicNumber: 54, category: 'noble-gas', link: 'chinese/54Xe.html' },
    { name: '铯', symbol: 'Cs', atomicNumber: 55, category: 'alkali-metal', link: 'chinese/55Cs.html' },
    { name: '钡', symbol: 'Ba', atomicNumber: 56, category: 'alkaline-earth-metal', link: 'chinese/56Ba.html' },
    { name: '镧', symbol: 'La', atomicNumber: 57, category: 'metal', link: 'chinese/57La.html' },
    { name: '铈', symbol: 'Ce', atomicNumber: 58, category: 'metal', link: 'chinese/58Ce.html' },
    { name: '镨', symbol: 'Pr', atomicNumber: 59, category: 'metal', link: 'chinese/59Pr.html' },
    { name: '钕', symbol: 'Nd', atomicNumber: 60, category: 'metal', link: 'chinese/60Nd.html' },
    { name: '钷', symbol: 'Pm', atomicNumber: 61, category: 'metal', link: 'chinese/61Pm.html' },
    { name: '钐', symbol: 'Sm', atomicNumber: 62, category: 'metal', link: 'chinese/62Sm.html' },
    { name: '铕', symbol: 'Eu', atomicNumber: 63, category: 'metal', link: 'chinese/63Eu.html' },
    { name: '钆', symbol: 'Gd', atomicNumber: 64, category: 'metal', link: 'chinese/64Gd.html' },
    { name: '铽', symbol: 'Tb', atomicNumber: 65, category: 'metal', link: 'chinese/65Tb.html' },
    { name: '镝', symbol: 'Dy', atomicNumber: 66, category: 'metal', link: 'chinese/66Dy.html' },
    { name: '钬', symbol: 'Ho', atomicNumber: 67, category: 'metal', link: 'chinese/67Ho.html' },
    { name: '铒', symbol: 'Er', atomicNumber: 68, category: 'metal', link: 'chinese/68Er.html' },
    { name: '铥', symbol: 'Tm', atomicNumber: 69, category: 'metal', link: 'chinese/69Tm.html' },
    { name: '镱', symbol: 'Yb', atomicNumber: 70, category: 'metal', link: 'chinese/70Yb.html' },
    { name: '镥', symbol: 'Lu', atomicNumber: 71, category: 'metal', link: 'chinese/71Lu.html' },
    { name: '铪', symbol: 'Hf', atomicNumber: 72, category: 'metal', link: 'chinese/72Hf.html' },
    { name: '钽', symbol: 'Ta', atomicNumber: 73, category: 'metal', link: 'chinese/73Ta.html' },
    { name: '钨', symbol: 'W', atomicNumber: 74, category: 'metal', link: 'chinese/74W.html' },
    { name: '铼', symbol: 'Re', atomicNumber: 75, category: 'metal', link: 'chinese/75Re.html' },
    { name: '锇', symbol: 'Os', atomicNumber: 76, category: 'metal', link: 'chinese/76Os.html' },
    { name: '铱', symbol: 'Ir', atomicNumber: 77, category: 'metal', link: 'chinese/77Ir.html' },
    { name: '铂', symbol: 'Pt', atomicNumber: 78, category: 'metal', link: 'chinese/78Pt.html' },
    { name: '金', symbol: 'Au', atomicNumber: 79, category: 'metal', link: 'chinese/79Au.html' },
    { name: '汞', symbol: 'Hg', atomicNumber: 80, category: 'metal', link: 'chinese/80Hg.html' },
    { name: '铊', symbol: 'Tl', atomicNumber: 81, category: 'metal', link: 'chinese/81Tl.html' },
    { name: '铅', symbol: 'Pb', atomicNumber: 82, category: 'metal', link: 'chinese/82Pb.html' },
    { name: '铋', symbol: 'Bi', atomicNumber: 83, category: 'metal', link: 'chinese/83Bi.html' },
    { name: '钋', symbol: 'Po', atomicNumber: 84, category: 'metal', link: 'chinese/84Po.html' },
    { name: '砹', symbol: 'At', atomicNumber: 85, category: 'halogen', link: 'chinese/85At.html' },
    { name: '氡', symbol: 'Rn', atomicNumber: 86, category: 'noble-gas', link: 'chinese/86Rn.html' },
    { name: '钫', symbol: 'Fr', atomicNumber: 87, category: 'alkali-metal', link: 'chinese/87Fr.html' },
    { name: '镭', symbol: 'Ra', atomicNumber: 88, category: 'alkaline-earth-metal', link: 'chinese/88Ra.html' },
    { name: '锕', symbol: 'Ac', atomicNumber: 89, category: 'metal', link: 'chinese/89Ac.html' },
    { name: '钍', symbol: 'Th', atomicNumber: 90, category: 'metal', link: 'chinese/90Th.html' },
    { name: '镤', symbol: 'Pa', atomicNumber: 91, category: 'metal', link: 'chinese/91Pa.html' },
    { name: '铀', symbol: 'U', atomicNumber: 92, category: 'metal', link: 'chinese/92U.html' },
    { name: '镎', symbol: 'Np', atomicNumber: 93, category: 'metal', link: 'chinese/93Np.html' },
    { name: '钚', symbol: 'Pu', atomicNumber: 94, category: 'metal', link: 'chinese/94Pu.html' },
    { name: '镅', symbol: 'Am', atomicNumber: 95, category: 'metal', link: 'chinese/95Am.html' },
    { name: '锔', symbol: 'Cm', atomicNumber: 96, category: 'metal', link: 'chinese/96Cm.html' },
    { name: '锫', symbol: 'Bk', atomicNumber: 97, category: 'metal', link: 'chinese/97Bk.html' },
    { name: '锎', symbol: 'Cf', atomicNumber: 98, category: 'metal', link: 'chinese/98Cf.html' },
    { name: '锿', symbol: 'Es', atomicNumber: 99, category: 'metal', link: 'chinese/99Es.html' },
    { name: '镄', symbol: 'Fm', atomicNumber: 100, category: 'metal', link: 'chinese/100Fm.html' },
    { name: '钔', symbol: 'Md', atomicNumber: 101, category: 'metal', link: 'chinese/101Md.html' },
    { name: '锘', symbol: 'No', atomicNumber: 102, category: 'metal', link: 'chinese/102No.html' },
    { name: '铹', symbol: 'Lr', atomicNumber: 103, category: 'metal', link: 'chinese/103Lr.html' },
    { name: '𬬻', symbol: 'Rf', atomicNumber: 104, category: 'metal', link: 'chinese/104Rf.html' },
    { name: '𬭊', symbol: 'Db', atomicNumber: 105, category: 'metal', link: 'chinese/105Db.html' },
    { name: '𬭳', symbol: 'Sg', atomicNumber: 106, category: 'metal', link: 'chinese/106Sg.html' },
    { name: '𬭛', symbol: 'Bh', atomicNumber: 107, category: 'metal', link: 'chinese/107Bh.html' },
    { name: '𬭶', symbol: 'Hs', atomicNumber: 108, category: 'metal', link: 'chinese/108Hs.html' },
    { name: '鿏', symbol: 'Mt', atomicNumber: 109, category: 'metal', link: 'chinese/109Mt.html' },
    { name: '𫟼', symbol: 'Ds', atomicNumber: 110, category: 'metal', link: 'chinese/110Ds.html' },
    { name: '𬬭', symbol: 'Rg', atomicNumber: 111, category: 'metal', link: 'chinese/111Rg.html' },
    { name: '鿔', symbol: 'Cn', atomicNumber: 112, category: 'metal', link: 'chinese/112Cn.html' },
    { name: '鿭', symbol: 'Nh', atomicNumber: 113, category: 'metal', link: 'chinese/113Nh.html' },
    { name: '𫓧', symbol: 'Fl', atomicNumber: 114, category: 'metal', link: 'chinese/114Fl.html' },
    { name: '镆', symbol: 'Mc', atomicNumber: 115, category: 'metal', link: 'chinese/115Mc.html' },
    { name: '𫟷', symbol: 'Lv', atomicNumber: 116, category: 'metal', link: 'chinese/116Lv.html' },
    { name: '鿬', symbol: 'Ts', atomicNumber: 117, category: 'halogen', link: 'chinese/117Ts.html' },
    { name: '鿫', symbol: 'Og', atomicNumber: 118, category: 'noble-gas', link: 'chinese/118Og.html' }
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