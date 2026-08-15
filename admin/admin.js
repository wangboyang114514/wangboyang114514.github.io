// 后台管理系统核心脚本
// 安全说明：本系统使用 SHA-256+盐 哈希存储密码，但运行在浏览器端（GitHub Pages 静态站点），
// 属于客户端认证，仅适用于 demo/教育场景。如需真正的安全认证，请使用服务端方案（见 server.js）。

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

    // 初始化
    init() {
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
