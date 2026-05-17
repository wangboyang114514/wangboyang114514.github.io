// 后台管理系统核心脚本 (混淆版)
// 此文件已做混淆处理，请勿直接修改

const _0x2a1b = {
    'k': atob('YWRtaW4='),
    'p': atob('YWRtaW4xMjM='),
    'r': atob('YWRtaW4='),
    'x': ['Y2Fyb3VzZWw=', 'bm90aWNl', 'dXNlcnM=', 'ZWRpdA==', 'ZGVsZXRl']
};
const _0x3c4d = {
    'k': atob('dmlzaXRvcg=='),
    'p': atob('dmlzaXRvcjEyMw=='),
    'r': atob('dmlzaXRvcg=='),
    'x': ['Y2Fyb3VzZWw=', 'bm90aWNl']
};
const _0x5e7f = function(_0x1a2b) {
    return atob(_0x1a2b);
};

const AdminSystem = {
    getUsers() {
        const _0x8c9d = localStorage.getItem('adminUsers');
        if (_0x8c9d) {
            return JSON.parse(_0x8c9d);
        }
        return {
            [_0x2a1b['k']]: {
                username: _0x2a1b['k'],
                password: _0x2a1b['p'],
                role: _0x2a1b['r'],
                permissions: _0x2a1b['x'].map(_0x5e7f)
            },
            [_0x3c4d['k']]: {
                username: _0x3c4d['k'],
                password: _0x3c4d['p'],
                role: _0x3c4d['r'],
                permissions: _0x3c4d['x'].map(_0x5e7f)
            }
        };
    },

    saveUsers(_0x2b3c) {
        localStorage.setItem('adminUsers', JSON.stringify(_0x2b3c));
        this.users = _0x2b3c;
    },

    users: null,

    login(_0x4d5e, _0x6e7f) {
        if (!this.users) {
            this.users = this.getUsers();
        }
        const _0xa1b2 = this.users[_0x4d5e];
        if (_0xa1b2 && _0xa1b2.password === _0x6e7f) {
            sessionStorage.setItem('adminLoggedIn', 'true');
            sessionStorage.setItem('adminUser', JSON.stringify({
                username: _0xa1b2.username,
                role: _0xa1b2.role,
                permissions: _0xa1b2.permissions
            }));
            return true;
        }
        return false;
    },

    isLoggedIn() {
        return sessionStorage.getItem('adminLoggedIn') === 'true';
    },

    // 获取当前用户
    getCurrentUser() {
        const userStr = sessionStorage.getItem('adminUser');
        return userStr ? JSON.parse(userStr) : null;
    },

    // 获取当前权限
    getRole() {
        const user = this.getCurrentUser();
        return user ? user.role : 'guest';
    },

    // 检查是否为管理员
    isAdmin() {
        return this.getRole() === 'admin';
    },

    // 检查是否有编辑权限
    hasEditPermission() {
        return this.getRole() === 'admin';
    },

    // 检查是否有指定权限
    hasPermission(permission) {
        const user = this.getCurrentUser();
        return user && user.permissions && user.permissions.includes(permission);
    },

    // 用户管理
    userManagement: {
        // 获取所有用户
        getAllUsers() {
            return AdminSystem.getUsers();
        },

        // 修改用户密码
        changePassword(username, newPassword) {
            const users = AdminSystem.getUsers();
            if (users[username]) {
                users[username].password = newPassword;
                AdminSystem.saveUsers(users);
                return true;
            }
            return false;
        },

        // 修改用户名
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

        // 设置用户权限
        setPermissions(username, permissions) {
            const users = AdminSystem.getUsers();
            if (users[username]) {
                users[username].permissions = permissions;
                AdminSystem.saveUsers(users);
                return true;
            }
            return false;
        },

        // 获取用户权限
        getPermissions(username) {
            const users = AdminSystem.getUsers();
            return users[username] ? users[username].permissions : [];
        },

        // 获取所有可用权限列表
        getAvailablePermissions() {
            return [
                { key: 'carousel', name: '轮播图管理' },
                { key: 'notice', name: '公告管理' },
                { key: 'users', name: '用户管理' },
                { key: 'edit', name: '编辑权限' },
                { key: 'delete', name: '删除权限' }
            ];
        },

        // 创建访客用户
        createUser(username, password) {
            const users = AdminSystem.getUsers();
            if (users[username]) {
                return false;
            }
            users[username] = {
                username: username,
                password: password,
                role: 'visitor',
                permissions: ['carousel', 'notice']
            };
            AdminSystem.saveUsers(users);
            return true;
        },

        // 删除用户
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

    // 退出登录
    logout() {
        sessionStorage.removeItem('adminLoggedIn');
        sessionStorage.removeItem('adminUser');
        window.location.href = 'login.html';
    },

    // 轮播图数据管理
    carousel: {
        // 获取轮播图列表
        getList() {
            const data = localStorage.getItem('carouselList');
            return data ? JSON.parse(data) : this.getDefaultList();
        },

        // 默认轮播图数据
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

        // 添加轮播图
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

        // 更新轮播图
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

        // 删除轮播图
        delete(id) {
            const list = this.getList();
            const newList = list.filter(item => item.id !== parseInt(id));
            // 重新排序
            newList.forEach((item, index) => {
                item.sort = index + 1;
            });
            localStorage.setItem('carouselList', JSON.stringify(newList));
            return true;
        },

        // 更新排序
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
        // 获取公告列表
        getList() {
            const data = localStorage.getItem('noticeList');
            return data ? JSON.parse(data) : this.getDefaultList();
        },

        // 默认公告数据
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

        // 添加公告
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

        // 更新公告
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

        // 删除公告
        delete(id) {
            const list = this.getList();
            const newList = list.filter(item => item.id !== parseInt(id));
            localStorage.setItem('noticeList', JSON.stringify(newList));
            return true;
        },

        // 获取启用的跑马灯公告
        getActiveMarquee() {
            const list = this.getList();
            return list.filter(item => item.type === 'marquee' && item.status === 1);
        }
    },

    // 初始化
    init() {
        // 加载用户数据
        this.users = this.getUsers();

        // 检查登录状态
        if (window.location.pathname.includes('admin/') && 
            !window.location.pathname.includes('login.html') && 
            !this.isLoggedIn()) {
            window.location.href = 'login.html';
            return;
        }

        // 绑定登录表单
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const role = document.getElementById('role').value;
                
                if (this.login(username, password, role)) {
                    window.location.href = 'index.html';
                } else {
                    alert('用户名、密码或身份选择错误！');
                }
            });
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