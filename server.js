const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// 创建一个简单的用户数据库
const users = {
    "admin": "password123",
    "user1": "mypassword"
};

// 配置 bodyParser 中间件
app.use(bodyParser.urlencoded({ extended: true }));

// 配置静态文件路径
app.use(express.static('public'));

// 登录处理
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (users[username] && users[username] === password) {
        res.send("登录成功!");
    } else {
        res.send("登录失败: 用户名或密码错误");
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
