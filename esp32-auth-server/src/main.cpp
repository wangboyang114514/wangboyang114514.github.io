#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <ArduinoJson.h>
#include <esp_timer.h>
#include "config.h"
#include "auth.h"
#include "pages.h"

WebServer server(80);

// ============================================================
//  状态灯：蓝=连接中，绿=就绪，红=WiFi 断开
//  板子没灯就把 config.h 里的 STATUS_LED_PIN 改成 -1
// ============================================================
static void setLed(uint8_t r, uint8_t g, uint8_t b) {
#if STATUS_LED_PIN >= 0
    neopixelWrite(STATUS_LED_PIN, r, g, b);
#endif
}

// ============================================================
//  跨域
//  原来一律回 Access-Control-Allow-Origin: *，意味着用户随便打开
//  哪个网页，那个网页都能对着 http://<esp32>/api/login 试密码并读到
//  "成功/失败"的差别——等于把设备变成密码爆破预言机。
//  现在只对白名单来源回显 Origin，其余不回 ACAO，浏览器自己会拦。
// ============================================================
static bool isAllowedOrigin(const String& origin) {
    if (origin == ALLOWED_ORIGIN) return true;
    // 本地起 http 服务调试（python -m http.server 等）
    if (origin.startsWith("http://localhost")) return true;
    if (origin.startsWith("http://127.0.0.1")) return true;
    return false;
}

static void applyCors() {
    String origin = server.header("Origin");
    if (origin.length() > 0 && isAllowedOrigin(origin)) {
        server.sendHeader("Access-Control-Allow-Origin", origin);
        server.sendHeader("Vary", "Origin");
    }
    server.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
    server.sendHeader("Access-Control-Max-Age", "600");
}

static void sendJson(int code, const String& json) {
    applyCors();
    server.send(code, "application/json; charset=utf-8", json);
}

static String docToString(const JsonDocument& doc) {
    String out;
    serializeJson(doc, out);
    return out;
}

// ============================================================
//  登录频率限制
//  按来源 IP 记失败次数，连续 5 次后锁 30 秒，之后每次翻倍、上限 10 分钟。
//  实现在 loop 里非阻塞推进，不用 delay() 卡住整个服务。
// ============================================================
struct Attempt {
    String ip;
    uint8_t fails;
    uint32_t lockUntil;
};

static Attempt attempts[MAX_ATTEMPTS];
static int attemptCount = 0;

static Attempt* findAttempt(const String& ip, bool create) {
    for (int i = 0; i < attemptCount; i++) {
        if (attempts[i].ip == ip) return &attempts[i];
    }
    if (!create) return nullptr;

    int slot;
    if (attemptCount < MAX_ATTEMPTS) {
        slot = attemptCount++;
    } else {
        // 表满了：挤掉失败次数最少的那条（最不可能是正在爆破的来源）
        slot = 0;
        for (int i = 1; i < attemptCount; i++) {
            if (attempts[i].fails < attempts[slot].fails) slot = i;
        }
    }
    attempts[slot].ip = ip;
    attempts[slot].fails = 0;
    attempts[slot].lockUntil = 0;
    return &attempts[slot];
}

static uint32_t lockRemainingMs(const String& ip) {
    Attempt* a = findAttempt(ip, false);
    if (!a || a->lockUntil == 0) return 0;

    int32_t left = (int32_t)(a->lockUntil - millis());
    if (left > 0) return (uint32_t)left;

    a->lockUntil = 0;
    return 0;
}

static void noteFailure(const String& ip) {
    Attempt* a = findAttempt(ip, true);
    if (!a) return;

    if (a->fails < 250) a->fails++;

    if (a->fails >= LOGIN_MAX_FAILS) {
        int over = a->fails - LOGIN_MAX_FAILS;
        if (over > 5) over = 5;
        uint32_t lock = LOGIN_LOCK_BASE_MS << over;
        if (lock > LOGIN_LOCK_MAX_MS) lock = LOGIN_LOCK_MAX_MS;
        a->lockUntil = millis() + lock;
        Serial.printf("[auth] %s 连续失败 %d 次，锁定 %lu 秒\n", ip.c_str(), a->fails, (unsigned long)(lock / 1000));
    }
}

static void noteSuccess(const String& ip) {
    Attempt* a = findAttempt(ip, false);
    if (a) {
        a->fails = 0;
        a->lockUntil = 0;
    }
}

// ============================================================
//  请求体大小闸门
//  登录请求只有几十字节，超过 512 字节一定是异常流量
// ============================================================
static bool guardBodySize() {
    if ((size_t)server.clientContentLength() > MAX_BODY_BYTES) {
        sendJson(413, "{\"success\":false,\"error\":\"请求体过大\"}");
        return false;
    }
    return true;
}

// ============================================================
//  页面路由
// ============================================================
void handleLoginPage() {
    applyCors();
    server.send(200, "text/html; charset=utf-8", getLoginPage(isDefaultAdminPassword()));
}

void handleStatusPage() {
    String token = server.arg("token");
    String username;
    if (!verifyToken(token, username)) {
        applyCors();
        server.send(401, "text/html; charset=utf-8", getUnauthorizedPage());
        return;
    }
    User user;
    if (!findUser(username, user)) {
        // 令牌还在但账号已被删：给个最低权限的占位，别让页面拿到空字符串
        user.username = username;
        user.role = "visitor";
        user.permissions = "";
    }
    applyCors();
    server.send(200, "text/html; charset=utf-8", getStatusPage(token, user));
}

void handleUsersPage() {
    String token = server.arg("token");
    String username;
    if (!verifyToken(token, username)) {
        applyCors();
        server.send(401, "text/html; charset=utf-8", getUnauthorizedPage());
        return;
    }
    applyCors();
    server.send(200, "text/html; charset=utf-8", getUsersPage(token));
}

// ============================================================
//  API
// ============================================================

// 探活：给前端/脚本判断"设备在不在线"，不需要任何凭据
void handleApiPing() {
    JsonDocument resp;
    resp["success"] = true;
    resp["device"] = DEVICE_MODEL;
    resp["name"] = DEVICE_NAME;
    resp["version"] = FIRMWARE_VER;
    resp["ip"] = WiFi.localIP().toString();
    resp["uptimeMs"] = (uint64_t)(esp_timer_get_time() / 1000ULL);
    resp["rssi"] = WiFi.RSSI();
    resp["users"] = countUsers();
    sendJson(200, docToString(resp));
}

void handleApiLogin() {
    if (!guardBodySize()) return;

    String ip = server.client().remoteIP().toString();

    uint32_t wait = lockRemainingMs(ip);
    if (wait > 0) {
        server.sendHeader("Retry-After", String((wait + 999) / 1000));
        JsonDocument resp;
        resp["success"] = false;
        resp["error"] = "尝试过于频繁，请稍后再试";
        resp["retryAfterMs"] = wait;
        sendJson(429, docToString(resp));
        return;
    }

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String username = doc["username"].as<String>();
    String password = doc["password"].as<String>();

    if (username.length() == 0 || password.length() == 0) {
        sendJson(400, "{\"success\":false,\"error\":\"用户名和密码不能为空\"}");
        return;
    }

    User user;
    // 用户不存在和密码错误返回同一句话，不给枚举用户名留口子
    bool ok = findUser(username, user) && verifyPassword(password, user.passwordHash);

    if (!ok) {
        noteFailure(ip);
        Serial.printf("[auth] 登录失败 user=%s from=%s\n", username.c_str(), ip.c_str());
        sendJson(401, "{\"success\":false,\"error\":\"用户名或密码错误\"}");
        return;
    }

    noteSuccess(ip);
    String token = createToken(username);

    JsonDocument resp;
    resp["success"] = true;
    resp["token"] = token;
    resp["expiresIn"] = (uint32_t)(TOKEN_EXPIRE_MS / 1000ULL);
    resp["user"]["username"] = user.username;
    resp["user"]["role"] = user.role;
    resp["user"]["permissions"] = user.permissions;

    sendJson(200, docToString(resp));
    Serial.printf("[auth] 登录成功 %s from %s\n", username.c_str(), ip.c_str());
}

// 校验 token 是否还有效（前端刷新页面时用，避免拿着过期 token 继续操作）
void handleApiVerify() {
    if (!guardBodySize()) return;

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String token = doc["token"].as<String>();
    String username;
    if (!verifyToken(token, username)) {
        sendJson(401, "{\"success\":false,\"error\":\"令牌无效或已过期\"}");
        return;
    }

    User user;
    findUser(username, user);

    JsonDocument resp;
    resp["success"] = true;
    resp["user"]["username"] = user.username;
    resp["user"]["role"] = user.role;
    resp["user"]["permissions"] = user.permissions;
    sendJson(200, docToString(resp));
}

void handleApiLogout() {
    if (!guardBodySize()) return;

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String token = doc["token"].as<String>();
    String username;
    if (verifyToken(token, username)) {
        revokeToken(token);
        Serial.printf("[auth] 登出 %s\n", username.c_str());
    }
    // 无论 token 是否存在都回成功，登出接口不该暴露 token 是否有效
    sendJson(200, "{\"success\":true}");
}

void handleListUsers() {
    String token = server.arg("token");
    String username;
    if (!verifyToken(token, username) || !isTokenAdmin(token)) {
        sendJson(403, "{\"success\":false,\"error\":\"无权限\"}");
        return;
    }

    JsonDocument usersDoc = getUsersJson();
    JsonDocument resp;
    resp["success"] = true;
    resp["users"] = usersDoc.as<JsonArray>();

    sendJson(200, docToString(resp));
}

// 用户名会被拼进 HTML 文本和页面里的 JS 字符串，带引号或尖括号就能把页面结构搞坏，
// 直接禁掉这几个字符。中文、字母、数字、下划线、点、横线、@ 都放行。
static bool isSafeUsername(const String& name) {
    if (name.length() == 0 || name.length() > 32) return false;
    for (size_t i = 0; i < name.length(); i++) {
        char c = name[i];
        if (c == '<' || c == '>' || c == '"' || c == '\'' ||
            c == '\\' || c == '`' || c == '&') return false;
        if ((unsigned char)c < 0x20) return false;
    }
    return true;
}

void handleCreateUser() {
    if (!guardBodySize()) return;

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String token = doc["token"].as<String>();
    String username = doc["username"].as<String>();
    String password = doc["password"].as<String>();
    String role = doc["role"].as<String>();

    if (!isTokenAdmin(token)) {
        sendJson(403, "{\"success\":false,\"error\":\"无权限\"}");
        return;
    }

    if (!isSafeUsername(username)) {
        sendJson(400, "{\"success\":false,\"error\":\"用户名 1-32 字符，不能含引号、尖括号、反斜杠\"}");
        return;
    }
    if (password.length() < 6 || password.length() > 64) {
        sendJson(400, "{\"success\":false,\"error\":\"密码长度需在 6-64 之间\"}");
        return;
    }
    if (role != "admin" && role != "visitor") {
        role = "visitor";
    }

    String permissions = (role == "admin")
        ? "carousel,notice,users,edit,delete"
        : "carousel,notice";

    if (addUser(username, password, role, permissions)) {
        sendJson(200, "{\"success\":true}");
        Serial.printf("[auth] 创建用户 %s (%s)\n", username.c_str(), role.c_str());
    } else {
        sendJson(409, "{\"success\":false,\"error\":\"用户名已存在\"}");
    }
}

void handleChangePassword() {
    if (!guardBodySize()) return;

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String token = doc["token"].as<String>();
    String username = doc["username"].as<String>();
    String newPassword = doc["newPassword"].as<String>();

    String tokenUser;
    if (!verifyToken(token, tokenUser)) {
        sendJson(401, "{\"success\":false,\"error\":\"令牌无效\"}");
        return;
    }

    // 管理员可以改任何人，普通用户只能改自己
    bool admin = isTokenAdmin(token);
    if (!admin && tokenUser != username) {
        sendJson(403, "{\"success\":false,\"error\":\"无权限修改他人密码\"}");
        return;
    }

    if (newPassword.length() < 6 || newPassword.length() > 64) {
        sendJson(400, "{\"success\":false,\"error\":\"密码长度需在 6-64 之间\"}");
        return;
    }

    if (changeUserPassword(username, newPassword)) {
        // 改的是自己 → 当前 token 已被吊销，得重新登录；
        // 改的是别人 → 当前 token 仍然有效
        bool selfChanged = (tokenUser == username);
        JsonDocument resp;
        resp["success"] = true;
        resp["requiresRelogin"] = selfChanged;
        sendJson(200, docToString(resp));
        Serial.printf("[auth] 密码修改 %s by %s\n", username.c_str(), tokenUser.c_str());
    } else {
        sendJson(404, "{\"success\":false,\"error\":\"用户不存在\"}");
    }
}

void handleDeleteUser() {
    if (!guardBodySize()) return;

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String token = doc["token"].as<String>();
    String username = doc["username"].as<String>();

    if (!isTokenAdmin(token)) {
        sendJson(403, "{\"success\":false,\"error\":\"无权限\"}");
        return;
    }

    if (deleteUser(username)) {
        sendJson(200, "{\"success\":true}");
        Serial.printf("[auth] 删除用户 %s\n", username.c_str());
    } else {
        sendJson(404, "{\"success\":false,\"error\":\"用户不存在或是管理员账号\"}");
    }
}

// 清空 NVS 并重启，回到默认账号。只在真忘了所有密码时用
void handleFactoryReset() {
    if (!guardBodySize()) return;

    JsonDocument doc;
    if (deserializeJson(doc, server.arg("plain"))) {
        sendJson(400, "{\"success\":false,\"error\":\"请求格式错误\"}");
        return;
    }

    String token = doc["token"].as<String>();
    if (!isTokenAdmin(token)) {
        sendJson(403, "{\"success\":false,\"error\":\"无权限\"}");
        return;
    }

    sendJson(200, "{\"success\":true,\"message\":\"已恢复出厂设置，设备重启中\"}");
    Serial.println("[auth] 收到恢复出厂请求");
    delay(300);
    factoryResetUsers();
    ESP.restart();
}

void handleFavicon() {
    server.send(204);
}

void handleNotFound() {
    if (server.method() == HTTP_OPTIONS) {
        applyCors();
        server.send(204);
        return;
    }
    sendJson(404, "{\"success\":false,\"error\":\"Not Found\"}");
}

// ============================================================
//  WiFi
// ============================================================
static void connectWiFi() {
    WiFi.mode(WIFI_STA);
    WiFi.persistent(false);
    WiFi.setAutoReconnect(true);
    WiFi.setSleep(false);   // 关省电，局域网请求响应快很多

#ifdef USE_STATIC_IP
    IPAddress ip, gw, sn, dns;
    ip.fromString(STATIC_IP);
    gw.fromString(STATIC_GATEWAY);
    sn.fromString(STATIC_SUBNET);
    dns.fromString(STATIC_DNS);
    WiFi.config(ip, gw, sn, dns);
    Serial.printf("[wifi] 使用固定 IP %s\n", STATIC_IP);
#endif

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.printf("[wifi] 连接 \"%s\"", WIFI_SSID);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 40) {   // 最多等 20 秒
        delay(500);
        Serial.print(".");
        attempts++;
    }
    Serial.println();

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("[wifi] 已连接");
        Serial.printf("[wifi] IP   : %s\n", WiFi.localIP().toString().c_str());
        Serial.printf("[wifi] RSSI : %d dBm\n", WiFi.RSSI());
        Serial.printf("[wifi] MAC  : %s\n", WiFi.macAddress().c_str());
    } else {
        Serial.println("[wifi] 连接失败 —— 检查 include/secrets.h 里的 SSID / 密码");
        Serial.println("[wifi] 已进入等待重连状态，串口和 USB 仍可用");
    }
}

static void maintainWiFi() {
    static uint32_t lastCheck = 0;
    uint32_t now = millis();
    if (now - lastCheck < 5000) return;
    lastCheck = now;

    if (WiFi.status() == WL_CONNECTED) {
        setLed(0, 12, 0);          // 就绪：暗绿
    } else {
        setLed(40, 0, 0);          // 断开：暗红
        Serial.println("[wifi] 掉线，重连中…");
        WiFi.reconnect();
    }
}

// ============================================================
//  setup / loop
// ============================================================
static void registerRoutes() {
    server.on("/", HTTP_GET, handleLoginPage);
    server.on("/status", HTTP_GET, handleStatusPage);
    server.on("/users", HTTP_GET, handleUsersPage);
    server.on("/favicon.ico", HTTP_GET, handleFavicon);

    server.on("/api/ping", HTTP_GET, handleApiPing);
    server.on("/api/login", HTTP_POST, handleApiLogin);
    server.on("/api/verify", HTTP_POST, handleApiVerify);
    server.on("/api/logout", HTTP_POST, handleApiLogout);

    server.on("/api/users/list", HTTP_GET, handleListUsers);
    server.on("/api/users/create", HTTP_POST, handleCreateUser);
    server.on("/api/users/password", HTTP_POST, handleChangePassword);
    server.on("/api/users/delete", HTTP_POST, handleDeleteUser);
    server.on("/api/factory-reset", HTTP_POST, handleFactoryReset);

    server.onNotFound(handleNotFound);
}

void setup() {
    Serial.begin(115200);
    delay(200);

    Serial.println();
    Serial.println("========================================");
    Serial.printf(" %s 硬件认证服务  v%s\n", DEVICE_MODEL, FIRMWARE_VER);
    Serial.printf(" 设备名: %s\n", DEVICE_NAME);
    Serial.println("========================================");

    setLed(0, 0, 40);        // 蓝：启动中

    connectWiFi();

    if (WiFi.status() == WL_CONNECTED) {
        setLed(0, 20, 0);
        if (MDNS.begin(DEVICE_NAME)) {
            MDNS.addService("http", "tcp", 80);
            Serial.printf("[mdns] http://%s.local\n", DEVICE_NAME);
        } else {
            Serial.println("[mdns] 启动失败，用 IP 访问即可");
        }
    } else {
        setLed(40, 0, 0);
    }

    initUsers();
    registerRoutes();
    server.begin();

    Serial.println("----------------------------------------");
    Serial.printf(" 打开 http://%s/ 登录\n", WiFi.localIP().toString().c_str());
    Serial.println(" 默认账号见 README，登录后请立刻改密码");
    Serial.println("----------------------------------------");
}

void loop() {
    server.handleClient();
    maintainWiFi();
}
