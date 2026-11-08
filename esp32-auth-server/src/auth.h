#ifndef AUTH_H
#define AUTH_H

#include <Arduino.h>
#include <ArduinoJson.h>

struct User {
    String username;
    String passwordHash;
    String role;
    String permissions;
};

struct TokenInfo {
    String token;
    String username;
    uint64_t expiresAt;   // esp_timer 毫秒，64 位，不会像 millis() 那样 49 天回绕
};

// ----- 哈希 -----
String sha256Hex(const String& text);
String hashPassword(const String& password);
bool verifyPassword(const String& password, const String& hash);

// ----- NVS 用户存储 -----
void initUsers();
JsonDocument getUsersJson();
bool findUser(const String& username, User& outUser);
bool addUser(const String& username, const String& password, const String& role, const String& permissions);
bool deleteUser(const String& username);
bool changeUserPassword(const String& username, const String& newPassword);
int  countUsers();
bool isDefaultAdminPassword();
void factoryResetUsers();

// ----- Token -----
String createToken(const String& username);
bool verifyToken(const String& token, String& outUsername);
bool isTokenAdmin(const String& token);
void revokeToken(const String& token);
void revokeUserTokens(const String& username);
void cleanupTokens();
int  activeTokenCount();

#endif // AUTH_H
