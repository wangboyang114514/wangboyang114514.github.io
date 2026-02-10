// 交互逻辑优化脚本

// 1. 导航交互逻辑
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
                // 这里可以添加关闭展开内容的逻辑
                break;
        }
    });
}

// 初始化所有交互功能
function initInteraction() {
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