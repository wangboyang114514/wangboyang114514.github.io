const fs = require('fs');
const path = require('path');

// 要添加的 JavaScript 代码
const scriptToAdd = `
<script>
    fetch('../head.html')
       .then(response => response.text())
       .then(data => {
            const head = document.getElementsByTagName('head')[0];
            head.innerHTML += data;
        })
       .catch(error => console.error('Error loading head.html:', error));
</script>
`;

// 定义 english 文件夹的路径
const englishFolder = 'D:\\06-Git\\wangboyang114514.github.io\\english';

// 读取 english 文件夹下的所有文件
fs.readdir(englishFolder, (err, files) => {
    if (err) {
        console.error('Error reading directory:', err);
        return;
    }

    // 过滤出 HTML 文件
    const htmlFiles = files.filter(file => path.extname(file) === '.html');

    // 遍历每个 HTML 文件
    htmlFiles.forEach(file => {
        const filePath = path.join(englishFolder, file);

        // 读取文件内容
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error(`Error reading file ${file}:`, err);
                return;
            }

            // 在 <head> 标签中添加 JavaScript 代码
            const newData = data.replace(/<head>/i, `<head>${scriptToAdd}`);

            // 将修改后的内容写回文件
            fs.writeFile(filePath, newData, 'utf8', err => {
                if (err) {
                    console.error(`Error writing file ${file}:`, err);
                } else {
                    console.log(`Script added to ${file}`);
                }
            });
        });
    });
});