// Chemistry World 后端服务
// 安全特性：环境变量管理凭据、bcrypt 密码哈希、helmet 安全头、速率限制
//
// 使用前：
// 1. npm install
// 2. 复制 .env.example 为 .env，填入真实的用户名和 bcrypt 密码哈希
// 3. 用 node hash-password.js <密码> 生成 bcrypt 哈希
// 4. node server.js

require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const bcrypt = require('bcrypt');

const app = express();
const PORT = process.env.PORT || 3000;

// 从环境变量读取用户凭据（密码为 bcrypt 哈希）
// 格式：ADMIN_USER=admin,ADMIN_PASSWORD_HASH=$2b$10$xxxxx
function loadUsers() {
    const users = {};
    const envKeys = Object.keys(process.env).filter(k => k.endsWith('_USER'));
    envKeys.forEach(userKey => {
        const prefix = userKey.replace('_USER', '');
        const username = process.env[userKey];
        const hashKey = `${prefix}_PASSWORD_HASH`;
        const passwordHash = process.env[hashKey];
        if (username && passwordHash) {
            users[username] = passwordHash;
        }
    });
    return users;
}

const users = loadUsers();

// 安全中间件
app.use(helmet());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// 静态文件（排除敏感文件）
app.use(express.static('public', {
    setHeaders: (res, path) => {
        if (path.includes('.env') || path.includes('package')) {
            res.setHeader('Content-Disposition', 'attachment');
        }
    }
}));

// 登录接口速率限制（防暴力破解）
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 分钟窗口
    max: 10,                     // 最多 10 次尝试
    message: { error: '请求过于频繁，请稍后再试' },
    standardHeaders: true,
    legacyHeaders: false
});

// 登录处理
app.post('/login', loginLimiter, async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: '用户名或密码错误' });
    }

    const storedHash = users[username];
    if (!storedHash) {
        // 统一错误信息，不泄露用户是否存在
        return res.status(401).json({ error: '用户名或密码错误' });
    }

    try {
        const match = await bcrypt.compare(password, storedHash);
        if (match) {
            res.json({ success: true, message: '登录成功' });
        } else {
            res.status(401).json({ error: '用户名或密码错误' });
        }
    } catch (err) {
        console.error('登录验证错误:', err.message);
        res.status(500).json({ error: '服务器内部错误' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`已加载 ${Object.keys(users).length} 个用户账号`);
});
