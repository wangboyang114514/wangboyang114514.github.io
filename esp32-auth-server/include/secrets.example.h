#ifndef SECRETS_H
#define SECRETS_H

// ============================================================
//  WiFi 凭据模板
//
//  使用方法：
//     cp include/secrets.example.h include/secrets.h
//  然后填写下面两项。secrets.h 已被 .gitignore 排除，
//  写进去的账号密码不会被提交到仓库。
// ============================================================

#define WIFI_SSID     "你的WiFi名称"
#define WIFI_PASSWORD "你的WiFi密码"

// ------------------------------------------------------------
//  可选：固定 IP
//  不定义 USE_STATIC_IP 时走 DHCP（推荐，省心）。
//  定义了则路由器每次分配同一个地址，前端就不用改地址了。
// ------------------------------------------------------------
// #define USE_STATIC_IP
#ifdef USE_STATIC_IP
  #define STATIC_IP      "192.168.1.100"
  #define STATIC_GATEWAY "192.168.1.1"
  #define STATIC_SUBNET  "255.255.255.0"
  #define STATIC_DNS     "192.168.1.1"
#endif

#endif // SECRETS_H
