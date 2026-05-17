// 交互逻辑优化脚本 - 模块化重构

const ChemistryWorld = {
    // 工具函数
    utils: {
        // 防抖函数
        debounce(func, wait) {
            let timeout;
            return function() {
                const context = this;
                const args = arguments;
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    func.apply(context, args);
                }, wait);
            };
        },
        
        // 平滑滚动函数
        smoothScrollTo(element) {
            const duration = 600;
            const start = window.pageYOffset;
            const targetTop = element.offsetTop - 100; // 减去导航栏高度
            const distance = targetTop - start;
            const startTime = performance.now();
            
            function animation(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easeProgress = progress < 0.5 ? 4 * progress * progress * progress : 1 - Math.pow(-2 * progress + 2, 3) / 2;
                
                window.scrollTo(0, start + distance * easeProgress);
                
                if (elapsed < duration) {
                    requestAnimationFrame(animation);
                }
            }
            
            requestAnimationFrame(animation);
        },
        
        // 显示提示信息
        showToast(message, duration) {
            try {
                // 检查是否已存在提示元素
                let toast = document.getElementById('toast');
                if (!toast) {
                    toast = document.createElement('div');
                    toast.id = 'toast';
                    toast.style.position = 'fixed';
                    toast.style.bottom = '20px';
                    toast.style.left = '50%';
                    toast.style.transform = 'translateX(-50%)';
                    toast.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
                    toast.style.color = 'white';
                    toast.style.padding = '12px 24px';
                    toast.style.borderRadius = '24px';
                    toast.style.zIndex = '1000';
                    toast.style.transition = 'opacity 0.3s ease';
                    toast.style.opacity = '0';
                    document.body.appendChild(toast);
                }
                
                toast.textContent = message;
                toast.style.opacity = '1';
                
                setTimeout(() => {
                    toast.style.opacity = '0';
                }, duration);
            } catch (error) {
                console.error('Toast error:', error);
            }
        },
        
        // 检测是否为首页
        isHomePage() {
            const currentPath = window.location.pathname;
            return currentPath === '/' || currentPath.endsWith('/index.html');
        },
        
        // 检测是否为英文页面
        isEnglishPage() {
            const currentPath = window.location.pathname;
            return currentPath.includes('/english/') || currentPath.endsWith('/English.html');
        }
    },
    
    // 页面过渡动画
    pageTransitions: {
        init() {
            try {
                // 创建加载覆盖层
                this.createLoadingOverlay();
                // 创建页面过渡元素
                this.createPageTransition();
                // 为链接添加过渡效果
                this.setupLinkTransitions();
            } catch (error) {
                console.error('Page transitions error:', error);
            }
        },
        
        createLoadingOverlay() {
            const loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';
            document.body.appendChild(loadingOverlay);
            
            // 页面加载完成后隐藏加载覆盖层
            window.addEventListener('load', () => {
                setTimeout(() => {
                    loadingOverlay.style.opacity = '0';
                    setTimeout(() => {
                        loadingOverlay.remove();
                    }, 500);
                }, 500);
            });
        },
        
        createPageTransition() {
            const transitionElement = document.createElement('div');
            transitionElement.className = 'page-transition';
            document.body.appendChild(transitionElement);
            return transitionElement;
        },
        
        setupLinkTransitions() {
            document.addEventListener('click', (e) => {
                const link = e.target.closest('a[href]');
                if (link) {
                    // 跳过锚点链接和外部链接
                    if (link.href.startsWith(window.location.origin) && !link.href.includes('#')) {
                        e.preventDefault();
                        const targetUrl = link.getAttribute('href');
                        
                        // 激活页面过渡
                        const pageTransition = document.querySelector('.page-transition');
                        if (pageTransition) {
                            pageTransition.classList.add('active');
                            
                            // 延迟后跳转
                            setTimeout(() => {
                                window.location.href = targetUrl;
                            }, 300);
                        } else {
                            window.location.href = targetUrl;
                        }
                    }
                }
            });
        }
    },
    
    // 导航交互
    navigation: {
        init() {
            try {
                this.setupSmoothScroll();
            } catch (error) {
                console.error('Navigation error:', error);
            }
        },
        
        setupSmoothScroll() {
            document.addEventListener('click', (e) => {
                const navLink = e.target.closest('.nav-links a');
                if (navLink) {
                    e.preventDefault();
                    const targetUrl = navLink.getAttribute('href');
                    
                    // 检查是否为同一页面内的锚点链接
                    if (targetUrl.startsWith('#')) {
                        const targetId = targetUrl;
                        const targetElement = document.querySelector(targetId);
                        
                        if (targetElement) {
                            // 平滑滚动到目标元素
                            ChemistryWorld.utils.smoothScrollTo(targetElement);
                        } else {
                            // 显示提示信息
                            ChemistryWorld.utils.showToast('该板块暂未开放', 1000);
                        }
                    } else {
                        // 跳转到其他页面
                        window.location.href = targetUrl;
                    }
                }
            });
        }
    },
    
    // 页面滚动反馈
    scrollFeedback: {
        init() {
            try {
                let lastScrollTop = 0;
                
                window.addEventListener('scroll', ChemistryWorld.utils.debounce(() => {
                    // 检测是否为首页，首页不显示滚动反馈
                    if (ChemistryWorld.utils.isHomePage()) {
                        return;
                    }
                    
                    const scrollTop = window.pageYOffset;
                    const windowHeight = window.innerHeight;
                    const documentHeight = document.documentElement.scrollHeight;
                    
                    // 检测当前页面语言
                    const isEnglishPage = ChemistryWorld.utils.isEnglishPage();
                    
                    // 检测滚动到顶部
                    if (scrollTop === 0 && lastScrollTop > 0) {
                        const topMessage = isEnglishPage ? 'Reached top' : '已到达顶部';
                        ChemistryWorld.utils.showToast(topMessage, 1000);
                    }
                    
                    // 检测滚动到底部
                    if (scrollTop + windowHeight >= documentHeight - 100 && lastScrollTop < scrollTop) {
                        const bottomMessage = isEnglishPage ? 'Reached bottom' : '已到达底部';
                        ChemistryWorld.utils.showToast(bottomMessage, 1000);
                    }
                    
                    lastScrollTop = scrollTop;
                }, 100));
            } catch (error) {
                console.error('Scroll feedback error:', error);
            }
        }
    },
    
    // 页面状态记忆
    pageState: {
        init() {
            try {
                this.setupScrollMemory();
                this.setupDarkMode();
            } catch (error) {
                console.error('Page state error:', error);
            }
        },
        
        setupScrollMemory() {
            // 滚动位置记忆
            window.addEventListener('scroll', ChemistryWorld.utils.debounce(() => {
                const scrollPosition = window.pageYOffset;
                try {
                    localStorage.setItem('scrollPosition', scrollPosition);
                } catch (e) {
                    console.error('LocalStorage error:', e);
                }
            }, 200));
            
            // 页面加载时恢复滚动位置
            window.addEventListener('load', () => {
                try {
                    const savedPosition = localStorage.getItem('scrollPosition');
                    if (savedPosition) {
                        window.scrollTo(0, parseInt(savedPosition));
                    }
                } catch (e) {
                    console.error('LocalStorage error:', e);
                }
            });
        },
        
        setupDarkMode() {
            // 检查本地存储中的模式偏好
            try {
                const savedMode = localStorage.getItem('darkMode');
                if (savedMode === 'enabled') {
                    document.body.classList.add('dark-mode');
                }
            } catch (e) {
                console.error('LocalStorage error:', e);
            }
        }
    },
    
    // 趣味交互功能
    funInteractions: {
        init() {
            try {
                this.setupTypewriterEffect();
                this.setupVisitDuration();
            } catch (error) {
                console.error('Fun interactions error:', error);
            }
        },
        
        setupTypewriterEffect() {
            window.addEventListener('load', () => {
                const welcomeElement = document.getElementById('main-title');
                if (welcomeElement) {
                    const text = welcomeElement.textContent;
                    this.typewriterEffect(welcomeElement, text, 100);
                }
            });
        },
        
        typewriterEffect(element, text, speed = 100) {
            let index = 0;
            element.textContent = '';
            
            function type() {
                if (index < text.length) {
                    element.textContent += text.charAt(index);
                    index++;
                    setTimeout(type, speed);
                }
            }
            
            type();
        },
        
        setupVisitDuration() {
            // 检查是否为首页，首页不显示访问时长
            if (ChemistryWorld.utils.isHomePage()) {
                return;
            }
            
            // 创建访问时长显示元素
            const durationElement = document.createElement('div');
            durationElement.id = 'visit-duration';
            durationElement.style.position = 'fixed';
            durationElement.style.bottom = '20px';
            durationElement.style.left = '20px';
            durationElement.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
            durationElement.style.color = 'var(--white)';
            durationElement.style.padding = '16px 24px';
            durationElement.style.borderRadius = '32px';
            durationElement.style.zIndex = '1000';
            durationElement.style.fontSize = '0.9rem';
            durationElement.style.fontWeight = '600';
            durationElement.style.backdropFilter = 'blur(25px)';
            durationElement.style.border = '1px solid rgba(255, 255, 255, 0.3)';
            durationElement.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2)';
            durationElement.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            
            // 添加悬停效果
            durationElement.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'rgba(255, 255, 255, 0.25)';
                this.style.transform = 'translateY(-2px)';
                this.style.borderColor = 'rgba(255, 255, 255, 0.4)';
                this.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.3)';
            });
            
            durationElement.addEventListener('mouseleave', function() {
                this.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
                this.style.transform = 'translateY(0)';
                this.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                this.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2)';
            });
            document.body.appendChild(durationElement);
            
            // 当前访问时长（刷新后重置）
            let currentSeconds = 0;
            
            // 总共访问时长（刷新后不重置）
            let totalSeconds = 0;
            try {
                totalSeconds = parseInt(localStorage.getItem('totalVisitSeconds') || '0');
            } catch (e) {
                console.error('LocalStorage error:', e);
            }
            
            // 更新访问时长
            function updateDuration() {
                currentSeconds++;
                totalSeconds++;
                
                // 保存总时长到本地存储
                try {
                    localStorage.setItem('totalVisitSeconds', totalSeconds.toString());
                } catch (e) {
                    console.error('LocalStorage error:', e);
                }
                
                // 格式化时间
                const currentMinutes = Math.floor(currentSeconds / 60);
                const currentRemainingSeconds = currentSeconds % 60;
                
                const totalMinutes = Math.floor(totalSeconds / 60);
                const totalRemainingSeconds = totalSeconds % 60;
                
                // 更新显示
                durationElement.innerHTML = `当前访问时长：${currentMinutes}分${currentRemainingSeconds}秒<br>总共访问时长：${totalMinutes}分${totalRemainingSeconds}秒`;
            }
            
            // 每秒更新一次
            setInterval(updateDuration, 1000);
        }
    },
    
    // 快捷键功能
    keyboardShortcuts: {
        init() {
            try {
                window.addEventListener('keydown', (e) => {
                    switch(e.key) {
                        case 'ArrowUp':
                            // 向上滚动页面
                            window.scrollBy(0, -50);
                            e.preventDefault();
                            break;
                        case 'ArrowDown':
                            // 向下滚动页面
                            window.scrollBy(0, 50);
                            e.preventDefault();
                            break;
                        case 'Home':
                            // 回顶部
                            window.scrollTo(0, 0);
                            e.preventDefault();
                            break;
                        case 'End':
                            // 到页底
                            window.scrollTo(0, document.documentElement.scrollHeight);
                            e.preventDefault();
                            break;
                        case 'Escape':
                            // 关闭所有展开的内容
                            const comparePanel = document.querySelector('.compare-panel');
                            if (comparePanel && comparePanel.classList.contains('active')) {
                                comparePanel.classList.remove('active');
                            }
                            break;
                    }
                });
            } catch (error) {
                console.error('Keyboard shortcuts error:', error);
            }
        }
    },
    
    // 化学装饰元素
    chemicalDecorations: {
        init() {
            try {
                this.createMoleculeBackground();
                this.createAtomicOrbitals();
            } catch (error) {
                console.error('Chemical decorations error:', error);
            }
        },
        
        createMoleculeBackground() {
            const moleculeBackground = document.createElement('div');
            moleculeBackground.className = 'molecule-background';
            
            // 创建多个分子
            for (let i = 0; i < 5; i++) {
                const molecule = document.createElement('div');
                molecule.className = 'molecule';
                molecule.style.left = `${Math.random() * 100}%`;
                molecule.style.top = `${Math.random() * 100}%`;
                molecule.style.animationDelay = `${Math.random() * 5}s`;
                molecule.style.animationDuration = `${15 + Math.random() * 10}s`;
                
                // 简单的分子结构SVG
                molecule.innerHTML = `
                    <svg width="100%" height="100%" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="5" fill="var(--primary-color)" />
                        <circle cx="20" cy="30" r="3" fill="var(--secondary-color)" />
                        <circle cx="80" cy="30" r="3" fill="var(--secondary-color)" />
                        <circle cx="20" cy="70" r="3" fill="var(--secondary-color)" />
                        <circle cx="80" cy="70" r="3" fill="var(--secondary-color)" />
                        <line x1="50" y1="50" x2="20" y2="30" stroke="rgba(255,255,255,0.5)" stroke-width="1" />
                        <line x1="50" y1="50" x2="80" y2="30" stroke="rgba(255,255,255,0.5)" stroke-width="1" />
                        <line x1="50" y1="50" x2="20" y2="70" stroke="rgba(255,255,255,0.5)" stroke-width="1" />
                        <line x1="50" y1="50" x2="80" y2="70" stroke="rgba(255,255,255,0.5)" stroke-width="1" />
                    </svg>
                `;
                
                moleculeBackground.appendChild(molecule);
            }
            
            document.body.appendChild(moleculeBackground);
        },
        
        createAtomicOrbitals() {
            const atomicOrbitals = document.createElement('div');
            atomicOrbitals.className = 'atomic-orbitals';
            
            // 创建多个轨道
            for (let i = 1; i <= 3; i++) {
                const orbital = document.createElement('div');
                orbital.className = 'orbital';
                const size = 100 * i;
                orbital.style.width = `${size}px`;
                orbital.style.height = `${size}px`;
                orbital.style.left = `calc(50% - ${size / 2}px)`;
                orbital.style.top = `calc(50% - ${size / 2}px)`;
                orbital.style.animationDelay = `${Math.random() * 5}s`;
                orbital.style.animationDuration = `${20 + Math.random() * 10}s`;
                
                atomicOrbitals.appendChild(orbital);
            }
            
            document.body.appendChild(atomicOrbitals);
        }
    },
    
    // 收藏功能
    favoriteFunctionality: {
        init() {
            try {
                this.setupFavoriteButtons();
            } catch (error) {
                console.error('Favorite functionality error:', error);
            }
        },
        
        setupFavoriteButtons() {
            const elementDetail = document.querySelector('.element-detail');
            if (elementDetail) {
                const elementName = document.querySelector('h1')?.textContent;
                if (!elementName) return;
                
                const favoriteBtn = document.createElement('button');
                favoriteBtn.className = 'favorite-btn';
                favoriteBtn.innerHTML = '❤️';
                
                // 检查是否已收藏
                try {
                    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
                    const isFavorited = favorites.some(item => item.name === elementName);
                    if (isFavorited) {
                        favoriteBtn.classList.add('favorited');
                    }
                } catch (e) {
                    console.error('LocalStorage error:', e);
                }
                
                // 收藏/取消收藏
                favoriteBtn.addEventListener('click', () => {
                    try {
                        let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
                        
                        // 提取元素信息
                        const elementInfo = {
                            name: elementName,
                            symbol: document.querySelector('.element-symbol')?.textContent || '',
                            atomicNumber: parseInt(document.querySelector('.element-number')?.textContent || '0'),
                            category: elementDetail.classList.contains('metal') ? 'metal' : 
                                      elementDetail.classList.contains('nonmetal') ? 'nonmetal' : 
                                      elementDetail.classList.contains('metalloid') ? 'metalloid' : 
                                      elementDetail.classList.contains('noble-gas') ? 'noble-gas' : 
                                      elementDetail.classList.contains('alkali-metal') ? 'alkali-metal' : 
                                      elementDetail.classList.contains('alkaline-earth-metal') ? 'alkaline-earth-metal' : 
                                      elementDetail.classList.contains('halogen') ? 'halogen' : 'other'
                        };
                        
                        if (favoriteBtn.classList.contains('favorited')) {
                            // 取消收藏
                            favorites = favorites.filter(item => item.name !== elementName);
                            favoriteBtn.classList.remove('favorited');
                            ChemistryWorld.utils.showToast('已取消收藏', 1000);
                        } else {
                            // 添加收藏
                            favorites.push(elementInfo);
                            favoriteBtn.classList.add('favorited');
                            ChemistryWorld.utils.showToast('已添加到收藏', 1000);
                        }
                        localStorage.setItem('favorites', JSON.stringify(favorites));
                    } catch (e) {
                        console.error('LocalStorage error:', e);
                        ChemistryWorld.utils.showToast('操作失败，请重试', 1000);
                    }
                });
                
                elementDetail.style.position = 'relative';
                elementDetail.appendChild(favoriteBtn);
            }
        }
    },
    
    // 元素对比功能
    elementComparison: {
        init() {
            try {
                this.setupCompareButtons();
                this.createComparePanel();
            } catch (error) {
                console.error('Element comparison error:', error);
            }
        },
        
        setupCompareButtons() {
            const elementDetail = document.querySelector('.element-detail');
            if (elementDetail) {
                const elementName = document.querySelector('h1')?.textContent;
                if (!elementName) return;
                
                const compareBtn = document.createElement('button');
                compareBtn.className = 'compare-btn';
                compareBtn.textContent = '添加到对比';
                
                // 添加到对比
                compareBtn.addEventListener('click', () => {
                    try {
                        let compareElements = JSON.parse(localStorage.getItem('compareElements') || '[]');
                        if (!compareElements.includes(elementName)) {
                            compareElements.push(elementName);
                            // 最多对比3个元素
                            if (compareElements.length > 3) {
                                compareElements.shift();
                            }
                            localStorage.setItem('compareElements', JSON.stringify(compareElements));
                            ChemistryWorld.utils.showToast('已添加到对比', 1000);
                        } else {
                            ChemistryWorld.utils.showToast('该元素已在对比列表中', 1000);
                        }
                    } catch (e) {
                        console.error('LocalStorage error:', e);
                        ChemistryWorld.utils.showToast('操作失败，请重试', 1000);
                    }
                });
                
                elementDetail.appendChild(compareBtn);
            }
        },
        
        createComparePanel() {
            const comparePanel = document.createElement('div');
            comparePanel.className = 'compare-panel';
            comparePanel.innerHTML = `
                <h3>元素对比</h3>
                <div class="compare-content"></div>
                <button class="close-compare">×</button>
            `;
            
            document.body.appendChild(comparePanel);
            
            // 关闭按钮
            const closeBtn = comparePanel.querySelector('.close-compare');
            closeBtn.addEventListener('click', () => {
                comparePanel.classList.remove('active');
            });
            
            // 显示对比面板
            const showCompareBtn = document.createElement('button');
            showCompareBtn.textContent = '对比元素';
            showCompareBtn.style.position = 'fixed';
            showCompareBtn.style.bottom = '100px';
            showCompareBtn.style.right = '20px';
            showCompareBtn.style.background = 'rgba(255, 255, 255, 0.15)';
            showCompareBtn.style.color = 'var(--white)';
            showCompareBtn.style.padding = '0.75rem 1.5rem';
            showCompareBtn.style.border = '1px solid rgba(255, 255, 255, 0.3)';
            showCompareBtn.style.borderRadius = '32px';
            showCompareBtn.style.fontWeight = '600';
            showCompareBtn.style.cursor = 'pointer';
            showCompareBtn.style.backdropFilter = 'blur(10px)';
            showCompareBtn.style.zIndex = '1000';
            
            showCompareBtn.addEventListener('click', () => {
                comparePanel.classList.add('active');
                this.updateComparePanel();
            });
            
            document.body.appendChild(showCompareBtn);
        },
        
        updateComparePanel() {
            const compareContent = document.querySelector('.compare-content');
            if (compareContent) {
                compareContent.innerHTML = '';
                try {
                    const compareElements = JSON.parse(localStorage.getItem('compareElements') || '[]');
                    
                    if (compareElements.length === 0) {
                        compareContent.innerHTML = '<p>暂无对比元素</p>';
                        return;
                    }
                    
                    compareElements.forEach(elementName => {
                        const elementDiv = document.createElement('div');
                        elementDiv.className = 'compare-element';
                        elementDiv.innerHTML = `<h3>${elementName}</h3><p>加载中...</p>`;
                        compareContent.appendChild(elementDiv);
                        
                        // 这里可以添加从API或本地数据加载元素信息的逻辑
                        // 暂时使用模拟数据
                        setTimeout(() => {
                            elementDiv.innerHTML = `
                                <h3>${elementName}</h3>
                                <p>原子序数: ${Math.floor(Math.random() * 100) + 1}</p>
                                <p>原子量: ${(Math.random() * 200 + 1).toFixed(2)}</p>
                                <p>分类: ${['金属', '非金属', '类金属', '稀有气体'][Math.floor(Math.random() * 4)]}</p>
                            `;
                        }, 500);
                    });
                } catch (e) {
                    console.error('LocalStorage error:', e);
                    compareContent.innerHTML = '<p>加载失败，请重试</p>';
                }
            }
        }
    },
    
    // 初始化所有功能
    init() {
        try {
            // 页面加载和过渡动画
            this.pageTransitions.init();
            
            // 导航交互
            this.navigation.init();
            
            // 页面滚动反馈
            this.scrollFeedback.init();
            
            // 页面状态记忆功能
            this.pageState.init();
            
            // 趣味交互功能
            this.funInteractions.init();
            
            // 快捷键辅助功能
            this.keyboardShortcuts.init();
            
            // 化学相关装饰元素
            this.chemicalDecorations.init();
            
            // 收藏功能
            this.favoriteFunctionality.init();
            
            // 元素对比功能
            this.elementComparison.init();
            
            // 访客统计功能
            this.visitorStats.init();
        } catch (error) {
            console.error('Initialization error:', error);
        }
    },
    
    // 访客统计模块
    visitorStats: {
        sessionStart: null,
        maxScrollDepth: 0,
        isTrackable: false,
        
        init() {
            // 只在可统计的页面统计（首页和元素页面）
            const currentPage = window.location.pathname;
            const trackablePages = ['index.html', 'elements.html', '/', ''];
            
            if (trackablePages.some(page => currentPage.endsWith(page))) {
                this.isTrackable = true;
                this.sessionStart = Date.now();
                this.recordVisit();
                this.setupEventListeners();
            }
        },
        
        setupEventListeners() {
            if (!this.isTrackable) return;
            
            // 监听页面滚动，记录最大滚动深度
            window.addEventListener('scroll', this.utils.debounce(() => {
                const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
                const currentScroll = window.pageYOffset;
                const scrollPercent = scrollHeight > 0 ? (currentScroll / scrollHeight) * 100 : 0;
                if (scrollPercent > this.maxScrollDepth) {
                    this.maxScrollDepth = Math.round(scrollPercent);
                }
            }, 100));
            
            // 页面离开时记录访问时长
            window.addEventListener('beforeunload', () => {
                this.recordVisitEnd();
            });
            
            // 隐藏页面时也记录（移动端切换tab）
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') {
                    this.recordVisitEnd();
                }
            });
        },
        
        recordVisit() {
            const visitData = {
                date: new Date().toISOString().split('T')[0],
                timestamp: new Date().toISOString(),
                page: window.location.pathname.split('/').pop() || 'index.html',
                userAgent: navigator.userAgent.substring(0, 100),
                screenWidth: window.screen.width,
                screenHeight: window.screen.height
            };
            
            let stats = this.getStats();
            if (!stats.dailyVisits) {
                stats.dailyVisits = {};
            }
            
            const today = visitData.date;
            if (!stats.dailyVisits[today]) {
                stats.dailyVisits[today] = {
                    visits: 0,
                    totalDuration: 0,
                    avgDuration: 0
                };
            }
            
            stats.dailyVisits[today].visits++;
            stats.currentSession = {
                startTime: visitData.timestamp,
                scrollDepth: 0
            };
            
            this.saveStats(stats);
        },
        
        recordVisitEnd() {
            if (!this.sessionStart || !this.isTrackable) return;
            
            const duration = Date.now() - this.sessionStart;
            const stats = this.getStats();
            const today = new Date().toISOString().split('T')[0];
            
            if (stats.dailyVisits && stats.dailyVisits[today]) {
                stats.dailyVisits[today].totalDuration += duration;
                stats.dailyVisits[today].avgDuration = Math.round(
                    stats.dailyVisits[today].totalDuration / stats.dailyVisits[today].visits
                );
                
                if (stats.currentSession) {
                    stats.dailyVisits[today].lastScrollDepth = this.maxScrollDepth;
                }
            }
            
            stats.currentSession = null;
            this.saveStats(stats);
            
            this.sessionStart = null;
        },
        
        getStats() {
            const data = localStorage.getItem('visitorStats');
            return data ? JSON.parse(data) : { dailyVisits: {}, totalVisits: 0 };
        },
        
        saveStats(stats) {
            localStorage.setItem('visitorStats', JSON.stringify(stats));
        }
    }
};

// 当DOM加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ChemistryWorld.init());
} else {
    ChemistryWorld.init();
}