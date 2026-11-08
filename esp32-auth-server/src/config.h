#ifndef CONFIG_H
#define CONFIG_H

// ============================================================
//  WiFi 凭据不在这里，在 include/secrets.h
//  该文件被 .gitignore 排除，仓库里只有 secrets.example.h 模板。
//  缺文件时这里会直接 #error，而不是带着空 SSID 烧进去
//  然后对着串口猜为什么连不上。
// ============================================================
#if __has_include("secrets.h")
  #include "secrets.h"
#else
  #error "缺少 include/secrets.h：请先执行 cp include/secrets.example.h include/secrets.h 并填写 WiFi 账号密码"
#endif

// ===== 设备身份 =====
// mDNS 主机名 → 浏览器直接访问 http://chemworld.local，不用记 IP
#define DEVICE_NAME   "chemworld"
#define DEVICE_MODEL  "ESP32-S3"
#define FIRMWARE_VER  "1.1.0"

// 板载 RGB 灯（ESP32-S3-DevKitC-1 是 GPIO48 的 WS2812）
// 板子没有灯就改成 -1，编译期自动去掉点灯代码
#define STATUS_LED_PIN 48

// ===== 站点 =====
// 认证成功后跳回的地址。必须和 admin.js 所在位置一致
#define SITE_URL "https://wangboyang114514.github.io/admin/index.html"

// ===== 跨域白名单 =====
// 登录请求里带的是明文密码，Access-Control-Allow-Origin 绝不能是 *
// 否则任意网页都能把本机当成密码爆破预言机
#define ALLOWED_ORIGIN "https://wangboyang114514.github.io"

// ===== 密码哈希 =====
// 盐值必须与 admin.js 里的 PASSWORD_SALT 完全一致，否则两边算出的哈希不同
#define PASSWORD_SALT "cw_salt_2024_a1b2c3d4e5f6"

// ===== Token =====
#define TOKEN_EXPIRE_MS 7200000ULL  // 2 小时
#define MAX_TOKENS      10          // 最多同时存在的有效 token
#define TOKEN_BYTES     16          // token 随机字节数 → 32 位十六进制

// ===== 防爆破 =====
#define MAX_ATTEMPTS       8        // 最多跟踪多少个来源 IP
#define LOGIN_MAX_FAILS    5        // 连续失败几次开始锁
#define LOGIN_LOCK_BASE_MS 30000UL  // 首次锁定 30 秒，之后翻倍
#define LOGIN_LOCK_MAX_MS  600000UL // 锁最长 10 分钟

// ===== 请求限制 =====
#define MAX_BODY_BYTES 512          // 登录/改密这类请求体都很小，超了直接拒

// ===== 默认用户 =====
// 密码哈希(SHA-256(salt + password))：
//   admin   "ChemWorld@Admin2024" -> ba51a903b8da1740864e713fc04fd3b65cbb3a5597f657f05b853a2f6b5bf5c9
//   visitor "ChemWorld@Guest2024" -> bcc144d4913a0f2f3780a734fec3230f05b432306c18abd466b21a218bd19b84
// 这两个密码是公开写在 admin.js 注释里的，只用于首次启动。
// 烧录后请立刻在 /status 页面改掉，登录页会一直红字提醒直到改完。
#define DEFAULT_ADMIN_HASH    "ba51a903b8da1740864e713fc04fd3b65cbb3a5597f657f05b853a2f6b5bf5c9"
#define DEFAULT_VISITOR_HASH  "bcc144d4913a0f2f3780a734fec3230f05b432306c18abd466b21a218bd19b84"

#endif // CONFIG_H
