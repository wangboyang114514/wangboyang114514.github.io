// 交互逻辑优化脚本

// 1. 页面加载和过渡动画
function setupPageTransitions() {
    // 创建加载覆盖层
    function createLoadingOverlay() {
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';
        document.body.appendChild(loadingOverlay);
        return loadingOverlay;
    }
    
    // 创建页面过渡元素
    function createPageTransition() {
        const transitionElement = document.createElement('div');
        transitionElement.className = 'page-transition';
        document.body.appendChild(transitionElement);
        return transitionElement;
    }
    
    // 初始化加载状态
    const loadingOverlay = createLoadingOverlay();
    const pageTransition = createPageTransition();
    
    // 页面加载完成后隐藏加载覆盖层
    window.addEventListener('load', function() {
        setTimeout(() => {
            loadingOverlay.style.opacity = '0';
            setTimeout(() => {
                loadingOverlay.remove();
            }, 500);
        }, 500);
    });
    
    // 为所有链接添加页面过渡效果
    const links = document.querySelectorAll('a[href]');
    links.forEach(link => {
        // 跳过锚点链接和外部链接
        if (link.href.startsWith(window.location.origin) && !link.href.includes('#')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetUrl = this.getAttribute('href');
                
                // 激活页面过渡
                pageTransition.classList.add('active');
                
                // 延迟后跳转
                setTimeout(() => {
                    window.location.href = targetUrl;
                }, 300);
            });
        }
    });
}

// 2. 导航交互逻辑
function setupNavigation() {
    // 平滑滚动功能
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetUrl = this.getAttribute('href');
            
            // 检查是否为同一页面内的锚点链接
            if (targetUrl.startsWith('#')) {
                const targetId = targetUrl;
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    // 平滑滚动到目标元素
                    smoothScrollTo(targetElement);
                } else {
                    // 显示提示信息
                    showToast('该板块暂未开放', 1000);
                }
            } else {
                // 跳转到其他页面
                window.location.href = targetUrl;
            }
        });
    });
}

// 2. 平滑滚动函数
function smoothScrollTo(element) {
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
}

// 3. 可点击元素交互反馈 - 已移除
function setupClickableElements() {
    // 已根据用户要求移除所有可点击元素的hover、active、focus状态反馈
    // 保留此函数以保持代码结构完整性
}

// 4. 页面滚动到顶部/底部反馈
function setupScrollFeedback() {
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        // 检测是否为首页，首页不显示滚动反馈
        const currentPath = window.location.pathname;
        const isHomePage = currentPath === '/' || currentPath.endsWith('/index.html');
        
        if (isHomePage) {
            return; // 首页不显示滚动反馈
        }
        
        const scrollTop = window.pageYOffset;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        
        // 检测当前页面语言
        const isEnglishPage = currentPath.includes('/english/') || currentPath.endsWith('/English.html');
        
        // 检测滚动到顶部
        if (scrollTop === 0 && lastScrollTop > 0) {
            const topMessage = isEnglishPage ? 'Reached top' : '已到达顶部';
            showToast(topMessage, 1000);
        }
        
        // 检测滚动到底部
        if (scrollTop + windowHeight >= documentHeight - 100 && lastScrollTop < scrollTop) {
            const bottomMessage = isEnglishPage ? 'Reached bottom' : '已到达底部';
            showToast(bottomMessage, 1000);
        }
        
        lastScrollTop = scrollTop;
    });
}

// 5. 显示提示信息
function showToast(message, duration) {
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
}

// 6. 防抖函数
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

// 7. 页面状态记忆功能
function setupPageStateMemory() {
    // 滚动位置记忆
    window.addEventListener('scroll', function() {
        const scrollPosition = window.pageYOffset;
        localStorage.setItem('scrollPosition', scrollPosition);
    });
    
    // 页面加载时恢复滚动位置
    window.addEventListener('load', function() {
        const savedPosition = localStorage.getItem('scrollPosition');
        if (savedPosition) {
            window.scrollTo(0, parseInt(savedPosition));
        }
    });
    
    // 暗黑模式功能
    function initDarkMode() {
        // 检查本地存储中的模式偏好
        const savedMode = localStorage.getItem('darkMode');
        
        if (savedMode === 'enabled') {
            document.body.classList.add('dark-mode');
        }
        
        // 这里可以添加一个切换按钮的事件监听器
        // 例如：document.getElementById('darkModeToggle').addEventListener('click', toggleDarkMode);
    }
    
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
    }
    
    initDarkMode();
}

// 8. 趣味交互功能
function setupFunInteractions() {
    // 打字机效果
    function typewriterEffect(element, text, speed = 100) {
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
    }
    
    // 应用打字机效果到欢迎语
    window.addEventListener('load', function() {
        const welcomeElement = document.getElementById('main-title');
        if (welcomeElement) {
            const text = welcomeElement.textContent;
            typewriterEffect(welcomeElement, text, 100);
        }
    });
    
    // 访问时长统计
    function initVisitDuration() {
        // 检查是否为首页，首页不显示访问时长
        const currentPath = window.location.pathname;
        const isHomePage = currentPath === '/' || currentPath.endsWith('/index.html');
        
        if (isHomePage) {
            return; // 首页不显示访问时长
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
        let totalSeconds = parseInt(localStorage.getItem('totalVisitSeconds') || '0');
        
        // 更新访问时长
        function updateDuration() {
            currentSeconds++;
            totalSeconds++;
            
            // 保存总时长到本地存储
            localStorage.setItem('totalVisitSeconds', totalSeconds.toString());
            
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
    
    initVisitDuration();
}

// 9. 快捷键辅助功能
function setupKeyboardShortcuts() {
    window.addEventListener('keydown', function(e) {
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
}

// 10. 化学相关装饰元素
function setupChemicalDecorations() {
    // 创建背景分子结构
    function createMoleculeBackground() {
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
    }
    
    // 创建原子轨道线条
    function createAtomicOrbitals() {
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
    
    createMoleculeBackground();
    createAtomicOrbitals();
}

// 11. 收藏功能
function setupFavoriteFunctionality() {
    // 为元素详情页添加收藏按钮
    const elementDetail = document.querySelector('.element-detail');
    if (elementDetail) {
        const elementName = document.querySelector('h1').textContent;
        const favoriteBtn = document.createElement('button');
        favoriteBtn.className = 'favorite-btn';
        favoriteBtn.innerHTML = '❤️';
        
        // 检查是否已收藏
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        if (favorites.includes(elementName)) {
            favoriteBtn.classList.add('favorited');
        }
        
        // 收藏/取消收藏
        favoriteBtn.addEventListener('click', function() {
            let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
            if (favoriteBtn.classList.contains('favorited')) {
                // 取消收藏
                favorites = favorites.filter(item => item !== elementName);
                favoriteBtn.classList.remove('favorited');
                showToast('已取消收藏', 1000);
            } else {
                // 添加收藏
                favorites.push(elementName);
                favoriteBtn.classList.add('favorited');
                showToast('已添加到收藏', 1000);
            }
            localStorage.setItem('favorites', JSON.stringify(favorites));
        });
        
        elementDetail.style.position = 'relative';
        elementDetail.appendChild(favoriteBtn);
    }
}

// 12. 元素对比功能
function setupElementComparison() {
    // 为元素详情页添加对比按钮
    const elementDetail = document.querySelector('.element-detail');
    if (elementDetail) {
        const elementName = document.querySelector('h1').textContent;
        const compareBtn = document.createElement('button');
        compareBtn.className = 'compare-btn';
        compareBtn.textContent = '添加到对比';
        
        // 添加到对比
        compareBtn.addEventListener('click', function() {
            let compareElements = JSON.parse(localStorage.getItem('compareElements') || '[]');
            if (!compareElements.includes(elementName)) {
                compareElements.push(elementName);
                // 最多对比3个元素
                if (compareElements.length > 3) {
                    compareElements.shift();
                }
                localStorage.setItem('compareElements', JSON.stringify(compareElements));
                showToast('已添加到对比', 1000);
            } else {
                showToast('该元素已在对比列表中', 1000);
            }
        });
        
        elementDetail.appendChild(compareBtn);
    }
    
    // 创建对比面板
    function createComparePanel() {
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
        closeBtn.addEventListener('click', function() {
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
        
        showCompareBtn.addEventListener('click', function() {
            comparePanel.classList.add('active');
            updateComparePanel();
        });
        
        document.body.appendChild(showCompareBtn);
    }
    
    // 更新对比面板
    function updateComparePanel() {
        const compareContent = document.querySelector('.compare-content');
        if (compareContent) {
            compareContent.innerHTML = '';
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
        }
    }
    
    createComparePanel();
}

// 初始化所有交互功能
function initInteraction() {
    // 页面加载和过渡动画
    setupPageTransitions();
    
    // 导航交互
    setupNavigation();
    
    // 可点击元素交互反馈
    setupClickableElements();
    
    // 页面滚动反馈
    setupScrollFeedback();
    
    // 页面状态记忆功能
    setupPageStateMemory();
    
    // 趣味交互功能
    setupFunInteractions();
    
    // 快捷键辅助功能
    setupKeyboardShortcuts();
    
    // 化学相关装饰元素
    setupChemicalDecorations();
    
    // 收藏功能
    setupFavoriteFunctionality();
    
    // 元素对比功能
    setupElementComparison();
    
    // 添加防抖处理
    const debouncedScroll = debounce(() => {
        // 这里可以添加需要防抖的滚动处理逻辑
    }, 200);
    
    window.addEventListener('scroll', debouncedScroll);
}

// 当DOM加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInteraction);
} else {
    initInteraction();
}