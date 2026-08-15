// bcrypt 密码哈希工具
// 用法：node hash-password.js <密码>
// 将输出的哈希值填入 .env 文件的 PASSWORD_HASH 字段

const bcrypt = require('bcrypt');

const password = process.argv[2];
if (!password) {
    console.error('用法：node hash-password.js <密码>');
    process.exit(1);
}

if (password.length < 6) {
    console.error('密码长度不能少于6位');
    process.exit(1);
}

const hash = bcrypt.hashSync(password, 10);
console.log('密码哈希（填入 .env 文件）：');
console.log(hash);
