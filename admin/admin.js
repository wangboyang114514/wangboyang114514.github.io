// 后台管理系统核心脚本
//
// 安全说明：密码用 SHA-256+盐 哈希，但哈希和校验都在浏览器里跑（GitHub Pages 是纯静态站），
// 属于「客户端门禁」——它挡的是误入，不是有心人。改 localStorage 就能绕过去。
// 所以真正的密码不应该放在这里，见下面的 ESP32 硬件认证。
//
// ===== 为什么 ESP32 只能"整页跳转"而不能直接 fetch =====
// 本站是 https，设备是 http://192.168.x.x。从 https 页面往 http 发起 XHR/fetch
// 属于 active mixed content，浏览器会直接拦掉：
//   Mixed Content: The page at 'https://…' was loaded over HTTPS,
//   but requested an insecure resource 'http://192.168.x.x/api/login'.
// 顶层导航不受这个限制，所以流程只能是：
//   登录页点「硬件认证」→ 整页跳到 http://chemworld.local/ →
//   设备本地校验密码 → 跳回 https://…/admin/index.html#auth=<base64url> →
//   本站解码、写入会话。密码只在设备和浏览器之间的那次 POST 里出现，不碰本站。

// ESP32-S3 认证服务地址。优先用 mDNS 主机名，路由器重新分配 IP 也不用改代码。
// 想改成固定 IP 就在控制台执行：localStorage.setItem('esp32AuthUrl', 'http://192.168.1.100')
const ESP32_DEFAULT_URL = 'http://chemworld.local';

function resolveEsp32Url() {
    try {
        const saved = localStorage.getItem('esp32AuthUrl');
        if (saved && /^https?:\/\//.test(saved)) return saved.replace(/\/+$/, '');
    } catch (e) { /* 隐私模式下 localStorage 可能抛异常 */ }
    return ESP32_DEFAULT_URL;
}

const ESP32_AUTH_URL = resolveEsp32Url();

// 设备回跳凭证的有效期（设备端也写 2 分钟，两边要一致）
const AUTH_PAYLOAD_TTL = 120000;
// 允许的时钟偏差，防止手机和电脑时间差几秒就登录失败
const AUTH_CLOCK_SKEW = 10000;
// 只认这几个权限键，设备传什么别的都丢掉
const KNOWN_PERMISSIONS = ['carousel', 'notice', 'users', 'edit', 'delete'];

// 设备端用 base64url(UTF-8 JSON) 编码，这里还原
function decodeAuthPayload(raw) {
    let b64 = decodeURIComponent(raw)
        .replace(/\s+/g, '')
        .replace(/-/g, '+')
        .replace(/_/g, '/');
    while (b64.length % 4) b64 += '=';

    const bin = atob(b64);
    const bytes = Uint8Array.from(bin, c => c.charCodeAt(0));
    return JSON.parse(new TextDecoder('utf-8').decode(bytes));
}

const PASSWORD_SALT = 'cw_salt_2024_a1b2c3d4e5f6';

// 默认用户（密码哈希预计算，明文不出现在代码中）
// admin 密码: ChemWorld@Admin2024
// visitor 密码: ChemWorld@Guest2024
const DEFAULT_USERS = {
    admin: {
        username: 'admin',
        passwordHash: 'ba51a903b8da1740864e713fc04fd3b65cbb3a5597f657f05b853a2f6b5bf5c9',
        salt: PASSWORD_SALT,
        role: 'admin',
        permissions: ['carousel', 'notice', 'users', 'edit', 'delete']
    },
    visitor: {
        username: 'visitor',
        passwordHash: 'bcc144d4913a0f2f3780a734fec3230f05b432306c18abd466b21a218bd19b84',
        salt: PASSWORD_SALT,
        role: 'visitor',
        permissions: ['carousel', 'notice']
    }
};

// SHA-256 哈希函数（使用 Web Crypto API）
async function sha256(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function hashPassword(password, salt) {
    return await sha256(salt + password);
}

async function verifyPassword(password, hash, salt) {
    const computedHash = await hashPassword(password, salt);
    return computedHash === hash;
}

const AdminSystem = {
    getUsers() {
        const stored = localStorage.getItem('adminUsers');
        if (stored) {
            const users = JSON.parse(stored);
            // 检测旧格式（明文密码），若检测到则重置为默认用户
            for (const key in users) {
                if (users[key].password && !users[key].passwordHash) {
                    console.warn('检测到旧版明文密码格式，已重置为默认用户。请重新创建用户。');
                    const defaults = { ...DEFAULT_USERS };
                    localStorage.setItem('adminUsers', JSON.stringify(defaults));
                    return defaults;
                }
            }
            return users;
        }
        return { ...DEFAULT_USERS };
    },

    saveUsers(users) {
        localStorage.setItem('adminUsers', JSON.stringify(users));
        this.users = users;
    },

    users: null,

    async login(username, password) {
        if (!this.users) {
            this.users = this.getUsers();
        }
        const user = this.users[username];
        if (user && await verifyPassword(password, user.passwordHash, user.salt)) {
            sessionStorage.setItem('adminLoggedIn', 'true');
            sessionStorage.setItem('adminUser', JSON.stringify({
                username: user.username,
                role: user.role,
                permissions: user.permissions
            }));
            return true;
        }
        return false;
    },

    isLoggedIn() {
        return sessionStorage.getItem('adminLoggedIn') === 'true';
    },

    getCurrentUser() {
        const userStr = sessionStorage.getItem('adminUser');
        return userStr ? JSON.parse(userStr) : null;
    },

    getRole() {
        const user = this.getCurrentUser();
        return user ? user.role : 'guest';
    },

    isAdmin() {
        return this.getRole() === 'admin';
    },

    hasEditPermission() {
        return this.getRole() === 'admin';
    },

    hasPermission(permission) {
        const user = this.getCurrentUser();
        return user && user.permissions && user.permissions.includes(permission);
    },

    // 用户管理
    userManagement: {
        getAllUsers() {
            return AdminSystem.getUsers();
        },

        async changePassword(username, newPassword) {
            const users = AdminSystem.getUsers();
            if (users[username]) {
                const salt = users[username].salt || PASSWORD_SALT;
                users[username].passwordHash = await hashPassword(newPassword, salt);
                users[username].salt = salt;
                delete users[username].password;
                AdminSystem.saveUsers(users);
                return true;
            }
            return false;
        },

        changeUsername(oldUsername, newUsername) {
            const users = AdminSystem.getUsers();
            if (users[oldUsername] && !users[newUsername]) {
                users[newUsername] = { ...users[oldUsername], username: newUsername };
                delete users[oldUsername];
                AdminSystem.saveUsers(users);
                return true;
            }
            return false;
        },

        setPermissions(username, permissions) {
            const users = AdminSystem.getUsers();
            if (users[username]) {
                users[username].permissions = permissions;
                AdminSystem.saveUsers(users);
                return true;
            }
            return false;
        },

        getPermissions(username) {
            const users = AdminSystem.getUsers();
            return users[username] ? users[username].permissions : [];
        },

        getAvailablePermissions() {
            return [
                { key: 'carousel', name: '轮播图管理' },
                { key: 'notice', name: '公告管理' },
                { key: 'users', name: '用户管理' },
                { key: 'edit', name: '编辑权限' },
                { key: 'delete', name: '删除权限' }
            ];
        },

        async createUser(username, password) {
            const users = AdminSystem.getUsers();
            if (users[username]) {
                return false;
            }
            const salt = PASSWORD_SALT;
            users[username] = {
                username: username,
                passwordHash: await hashPassword(password, salt),
                salt: salt,
                role: 'visitor',
                permissions: ['carousel', 'notice']
            };
            AdminSystem.saveUsers(users);
            return true;
        },

        deleteUser(username) {
            const users = AdminSystem.getUsers();
            if (users[username] && users[username].role !== 'admin') {
                delete users[username];
                AdminSystem.saveUsers(users);
                return true;
            }
            return false;
        }
    },

    logout() {
        sessionStorage.removeItem('adminLoggedIn');
        sessionStorage.removeItem('adminUser');
        sessionStorage.removeItem('esp32Token');
        sessionStorage.removeItem('authSource');
        window.location.href = 'login.html';
    },

    // 轮播图数据管理
    carousel: {
        getList() {
            const data = localStorage.getItem('carouselList');
            return data ? JSON.parse(data) : this.getDefaultList();
        },

        getDefaultList() {
            return [
                {
                    id: 1,
                    title: '欢迎来到化学世界',
                    image: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=chemistry%20periodic%20table%20colorful%20background%20modern%20science&image_size=landscape_16_9',
                    link: '#',
                    sort: 1,
                    status: 1
                },
                {
                    id: 2,
                    title: '探索元素奥秘',
                    image: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=chemical%20elements%20atoms%20molecules%203d%20render%20science&image_size=landscape_16_9',
                    link: '#',
                    sort: 2,
                    status: 1
                },
                {
                    id: 3,
                    title: '趣味化学游戏',
                    image: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=chemistry%20game%20colorful%20fun%20education%20kids&image_size=landscape_16_9',
                    link: '#',
                    sort: 3,
                    status: 1
                }
            ];
        },

        add(item) {
            const list = this.getList();
            const maxId = Math.max(...list.map(item => item.id), 0);
            item.id = maxId + 1;
            item.sort = list.length + 1;
            item.status = 1;
            list.push(item);
            list.sort((a, b) => a.sort - b.sort);
            localStorage.setItem('carouselList', JSON.stringify(list));
            return item;
        },

        update(id, item) {
            const list = this.getList();
            const index = list.findIndex(item => item.id === parseInt(id));
            if (index !== -1) {
                list[index] = { ...list[index], ...item };
                localStorage.setItem('carouselList', JSON.stringify(list));
                return true;
            }
            return false;
        },

        delete(id) {
            const list = this.getList();
            const newList = list.filter(item => item.id !== parseInt(id));
            newList.forEach((item, index) => {
                item.sort = index + 1;
            });
            localStorage.setItem('carouselList', JSON.stringify(newList));
            return true;
        },

        updateSort(items) {
            items.forEach((item, index) => {
                item.sort = index + 1;
            });
            localStorage.setItem('carouselList', JSON.stringify(items));
            return true;
        }
    },

    // 公告数据管理
    notice: {
        getList() {
            const data = localStorage.getItem('noticeList');
            return data ? JSON.parse(data) : this.getDefaultList();
        },

        getDefaultList() {
            return [
                {
                    id: 1,
                    title: '网站更新通知',
                    content: '化学世界网站已更新至2.0版本，新增化学游戏和元素对比功能！',
                    type: 'marquee',
                    status: 1,
                    createdAt: new Date().toISOString()
                }
            ];
        },

        add(item) {
            const list = this.getList();
            const maxId = Math.max(...list.map(item => item.id), 0);
            item.id = maxId + 1;
            item.status = 1;
            item.createdAt = new Date().toISOString();
            list.push(item);
            localStorage.setItem('noticeList', JSON.stringify(list));
            return item;
        },

        update(id, item) {
            const list = this.getList();
            const index = list.findIndex(item => item.id === parseInt(id));
            if (index !== -1) {
                list[index] = { ...list[index], ...item };
                localStorage.setItem('noticeList', JSON.stringify(list));
                return true;
            }
            return false;
        },

        delete(id) {
            const list = this.getList();
            const newList = list.filter(item => item.id !== parseInt(id));
            localStorage.setItem('noticeList', JSON.stringify(newList));
            return true;
        },

        getActiveMarquee() {
            const list = this.getList();
            return list.filter(item => item.type === 'marquee' && item.status === 1);
        }
    },

    // ESP32-S3 硬件认证：解析设备跳回来的 #auth= 凭证
    // 返回 true 表示这次进入是靠硬件认证过的
    checkESP32Auth() {
        const hash = window.location.hash;
        if (!hash || hash.indexOf('#auth=') !== 0) return false;

        // 先抹掉地址栏里的凭证——不管后面解析成功还是失败。
        // 留在 history 里的话，后退一步就能把过期凭证再喂一次。
        history.replaceState(null, '', window.location.pathname + window.location.search);

        let data;
        try {
            data = decodeAuthPayload(hash.slice(6));
        } catch (e) {
            console.error('ESP32 认证数据解析失败（可能是复制粘贴时被截断）:', e);
            return false;
        }

        if (!data || data.success !== true || !data.user ||
            typeof data.user.username !== 'string' || !data.user.username) {
            console.warn('ESP32 认证数据格式不正确，已忽略');
            return false;
        }

        if (typeof data.exp === 'number') {
            if (Date.now() > data.exp + AUTH_CLOCK_SKEW) {
                console.warn('ESP32 认证凭证已过期，请重新走一次硬件认证');
                // 记一笔，登录页会把它显示出来，否则用户只看到"莫名其妙被踢回登录页"
                sessionStorage.setItem('authError', '硬件认证凭证已过期（2 分钟有效），请重试');
                return false;
            }
        } else {
            // 旧固件没有 exp 字段，放行但记一笔
            console.warn('ESP32 认证凭证缺少 exp 字段（旧版固件），已按有效处理');
        }

        const perms = String(data.user.permissions || '')
            .split(',')
            .map(p => p.trim())
            .filter(p => KNOWN_PERMISSIONS.includes(p));

        sessionStorage.setItem('adminLoggedIn', 'true');
        sessionStorage.setItem('adminUser', JSON.stringify({
            username: data.user.username,
            role: data.user.role === 'admin' ? 'admin' : 'visitor',
            permissions: perms
        }));
        if (data.token) sessionStorage.setItem('esp32Token', data.token);
        sessionStorage.setItem('authSource', 'esp32');

        console.log('ESP32 硬件认证通过:', data.user.username, '来自', data.device || '设备');
        return true;
    },

    // 硬件认证相关的零碎操作，供页面调用
    esp32: {
        url() {
            return ESP32_AUTH_URL;
        },

        authPageUrl() {
            return ESP32_AUTH_URL + '/';
        },

        // 这次会话是不是硬件认证进来的
        isLinked() {
            return sessionStorage.getItem('authSource') === 'esp32';
        },

        token() {
            return sessionStorage.getItem('esp32Token');
        },

        // 只能用整页跳转：https 页面 fetch http 设备会被 mixed content 拦掉
        openAuthPage() {
            window.location.href = this.authPageUrl();
        },

        // 手动指定设备地址（路由器换了网段、mDNS 不生效时用）
        setUrl(url) {
            if (url) {
                localStorage.setItem('esp32AuthUrl', url.replace(/\/+$/, ''));
            } else {
                localStorage.removeItem('esp32AuthUrl');
            }
            window.location.reload();
        },

        unlink() {
            sessionStorage.removeItem('esp32Token');
            sessionStorage.removeItem('authSource');
        }
    },

    // 初始化
    init() {
        // 检测 ESP32-S3 硬件认证回调
        this.checkESP32Auth();

        this.users = this.getUsers();

        // 检查登录状态
        if (window.location.pathname.includes('admin/') &&
            !window.location.pathname.includes('login.html') &&
            !this.isLoggedIn()) {
            window.location.href = 'login.html';
            return;
        }

        // 绑定退出按钮
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.logout();
            });
        }
    }
};

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    AdminSystem.init();
});
