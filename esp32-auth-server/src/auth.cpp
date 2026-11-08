#include "auth.h"
#include "config.h"
#include <Preferences.h>
#include <esp_system.h>
#include <esp_timer.h>
#include <mbedtls/sha256.h>
#include <string.h>

static Preferences prefs;
static TokenInfo tokens[MAX_TOKENS];
static int tokenCount = 0;

// 64 位毫秒时基。原来用 millis()（32 位）计算过期时间，49 天左右会回绕，
// 回绕后所有 token 会被当成"还没过期"，保险起见换成 esp_timer。
static inline uint64_t nowMs() {
    return (uint64_t)(esp_timer_get_time() / 1000ULL);
}

// ===== SHA-256 =====

String sha256Hex(const String& text) {
    uint8_t hash[32];
    // 用一次性接口而不是 start/update/finish：后者在 mbedTLS 2.x 和 3.x 之间
    // 返回值类型变过（void → int），一次性接口两边签名一致。
    mbedtls_sha256((const unsigned char*)text.c_str(), text.length(), hash, 0);

    char hex[65];
    for (int i = 0; i < 32; i++) {
        sprintf(hex + i * 2, "%02x", hash[i]);
    }
    hex[64] = '\0';
    return String(hex);
}

String hashPassword(const String& password) {
    return sha256Hex(String(PASSWORD_SALT) + password);
}

// 定长比较，避免逐字节短路泄露前缀信息。
// 局域网内的攻击者本来就能测时延，聊胜于无，但没成本。
static bool constantTimeEquals(const String& a, const String& b) {
    if (a.length() != b.length()) return false;
    uint8_t diff = 0;
    for (size_t i = 0; i < a.length(); i++) {
        diff |= (uint8_t)(a[i] ^ b[i]);
    }
    return diff == 0;
}

bool verifyPassword(const String& password, const String& hash) {
    return constantTimeEquals(hashPassword(password), hash);
}

// ===== NVS 用户存储 =====

static void seedDefaults() {
    JsonDocument doc;
    JsonArray arr = doc.to<JsonArray>();

    JsonObject admin = arr.add<JsonObject>();
    admin["username"] = "admin";
    admin["passwordHash"] = DEFAULT_ADMIN_HASH;
    admin["role"] = "admin";
    admin["permissions"] = "carousel,notice,users,edit,delete";

    JsonObject visitor = arr.add<JsonObject>();
    visitor["username"] = "visitor";
    visitor["passwordHash"] = DEFAULT_VISITOR_HASH;
    visitor["role"] = "visitor";
    visitor["permissions"] = "carousel,notice";

    String jsonStr;
    serializeJson(doc, jsonStr);
    prefs.putString("users", jsonStr);
    prefs.putBool("seeded", true);

    Serial.println("[auth] 已播种默认用户 admin / visitor");
    Serial.println("[auth] 警告：这两个是公开的默认密码，请立刻在 /status 页面修改");
}

void initUsers() {
    prefs.begin("auth", false);

    if (!prefs.getBool("seeded", false)) {
        seedDefaults();
    } else {
        // 数据区被写坏时（断电、擦写异常）getString 会拿到空串，
        // 这里兜一把，别让设备变成"谁都登不进"的砖头。
        String users = prefs.getString("users", "");
        if (users.length() < 2) {
            Serial.println("[auth] NVS 用户数据异常，重新播种");
            seedDefaults();
        }
    }

    prefs.end();
}

JsonDocument getUsersJson() {
    prefs.begin("auth", true);
    String jsonStr = prefs.getString("users", "[]");
    prefs.end();

    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, jsonStr);
    if (err) {
        Serial.printf("[auth] 用户 JSON 解析失败: %s\n", err.c_str());
        doc.to<JsonArray>();
    }
    return doc;
}

static void saveUsersJson(const JsonDocument& doc) {
    String jsonStr;
    serializeJson(doc, jsonStr);
    prefs.begin("auth", false);
    prefs.putString("users", jsonStr);
    prefs.end();
}

bool findUser(const String& username, User& outUser) {
    JsonDocument doc = getUsersJson();
    JsonArray arr = doc.as<JsonArray>();

    for (JsonObject obj : arr) {
        if (obj["username"] == username) {
            outUser.username = obj["username"].as<String>();
            outUser.passwordHash = obj["passwordHash"].as<String>();
            outUser.role = obj["role"].as<String>();
            outUser.permissions = obj["permissions"].as<String>();
            return true;
        }
    }
    return false;
}

bool addUser(const String& username, const String& password, const String& role, const String& permissions) {
    JsonDocument doc = getUsersJson();
    JsonArray arr = doc.as<JsonArray>();

    for (JsonObject obj : arr) {
        if (obj["username"] == username) {
            return false;
        }
    }

    JsonObject newUser = arr.add<JsonObject>();
    newUser["username"] = username;
    newUser["passwordHash"] = hashPassword(password);
    newUser["role"] = role;
    newUser["permissions"] = permissions;

    saveUsersJson(doc);
    return true;
}

bool deleteUser(const String& username) {
    JsonDocument doc = getUsersJson();
    JsonArray arr = doc.as<JsonArray>();

    bool found = false;
    // 倒序删，删完不留空洞
    for (int i = (int)arr.size() - 1; i >= 0; i--) {
        if (arr[i]["username"] == username && arr[i]["role"] != "admin") {
            arr.remove(i);
            found = true;
        }
    }

    if (found) {
        saveUsersJson(doc);
        revokeUserTokens(username);   // 删号即下线
    }
    return found;
}

bool changeUserPassword(const String& username, const String& newPassword) {
    JsonDocument doc = getUsersJson();
    JsonArray arr = doc.as<JsonArray>();

    for (JsonObject obj : arr) {
        if (obj["username"] == username) {
            obj["passwordHash"] = hashPassword(newPassword);
            saveUsersJson(doc);
            // 改密码后让该用户已签发的 token 全部失效，
            // 否则"改密码踢掉可疑会话"这件事做不到。
            revokeUserTokens(username);
            return true;
        }
    }
    return false;
}

int countUsers() {
    JsonDocument doc = getUsersJson();
    return (int)doc.as<JsonArray>().size();
}

bool isDefaultAdminPassword() {
    User admin;
    if (!findUser("admin", admin)) return false;
    return constantTimeEquals(admin.passwordHash, String(DEFAULT_ADMIN_HASH));
}

void factoryResetUsers() {
    prefs.begin("auth", false);
    prefs.clear();
    prefs.end();
    tokenCount = 0;
    Serial.println("[auth] NVS 已清空，重启后恢复默认用户");
}

// ===== Token 管理 =====

void cleanupTokens() {
    int j = 0;
    uint64_t now = nowMs();
    for (int i = 0; i < tokenCount; i++) {
        if (now < tokens[i].expiresAt) {
            tokens[j++] = tokens[i];
        }
    }
    tokenCount = j;
}

String createToken(const String& username) {
    cleanupTokens();

    // 原来只有 esp_random() 的 32 位 + millis()，8 位十六进制量级，
    // 局域网内跑一遍枚举是可行的。改成 16 字节 CSPRNG。
    if (tokenCount >= MAX_TOKENS) {
        for (int i = 1; i < tokenCount; i++) {
            tokens[i - 1] = tokens[i];
        }
        tokenCount--;
    }

    uint8_t rnd[TOKEN_BYTES];
    esp_fill_random(rnd, sizeof(rnd));

    char hex[TOKEN_BYTES * 2 + 1];
    for (int i = 0; i < TOKEN_BYTES; i++) {
        sprintf(hex + i * 2, "%02x", rnd[i]);
    }
    hex[TOKEN_BYTES * 2] = '\0';

    tokens[tokenCount].token = String(hex);
    tokens[tokenCount].username = username;
    tokens[tokenCount].expiresAt = nowMs() + TOKEN_EXPIRE_MS;
    tokenCount++;

    return String(hex);
}

bool verifyToken(const String& token, String& outUsername) {
    if (token.length() == 0) return false;

    uint64_t now = nowMs();
    for (int i = 0; i < tokenCount; i++) {
        if (constantTimeEquals(tokens[i].token, token)) {
            if (now < tokens[i].expiresAt) {
                outUsername = tokens[i].username;
                return true;
            }
            return false;   // 命中了但已过期，不用再找
        }
    }
    return false;
}

bool isTokenAdmin(const String& token) {
    String username;
    if (!verifyToken(token, username)) {
        return false;
    }

    User user;
    if (findUser(username, user)) {
        return user.role == "admin";
    }
    return false;
}

void revokeToken(const String& token) {
    int j = 0;
    for (int i = 0; i < tokenCount; i++) {
        if (!constantTimeEquals(tokens[i].token, token)) {
            tokens[j++] = tokens[i];
        }
    }
    tokenCount = j;
}

void revokeUserTokens(const String& username) {
    int j = 0;
    for (int i = 0; i < tokenCount; i++) {
        if (tokens[i].username != username) {
            tokens[j++] = tokens[i];
        }
    }
    tokenCount = j;
}

int activeTokenCount() {
    cleanupTokens();
    return tokenCount;
}
