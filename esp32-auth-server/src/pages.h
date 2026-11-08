#ifndef PAGES_H
#define PAGES_H

#include <Arduino.h>
#include <WiFi.h>
#include "config.h"
#include "auth.h"

// ============================================================
//  设备端页面
//  都是纯 HTML 字符串，直接由 ESP32 吐出。为了省 flash，
//  CSS 走统一的一段，模板变量用 %XXX% 占位再替换。
// ============================================================

static String tplReplace(String s, const char* key, const String& value) {
    s.replace(key, value);
    return s;
}

// 共用样式：和站点的深色玻璃风格保持一致
static const char* PAGES_CSS = R"css(
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
background:linear-gradient(135deg,#1a1a2e,#16213e 55%,#0f3460);min-height:100vh;color:#fff;
display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:rgba(255,255,255,0.08);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.16);
border-radius:20px;padding:32px;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,0.4)}
.wide{max-width:640px}
h1{font-size:1.35rem;margin-bottom:6px;text-align:center}
.sub{font-size:.82rem;opacity:.55;text-align:center;margin-bottom:24px}
label{display:block;font-size:.82rem;margin-bottom:6px;opacity:.75}
input,select{width:100%;padding:12px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.18);
background:rgba(255,255,255,0.06);color:#fff;font-size:.95rem;margin-bottom:16px}
input:focus,select:focus{outline:none;border-color:#4fc3f7;background:rgba(79,195,247,0.08)}
.btn{width:100%;padding:13px;border:none;border-radius:10px;font-size:.95rem;font-weight:600;cursor:pointer;
background:linear-gradient(135deg,#4fc3f7,#0288d1);color:#fff;transition:transform .15s,opacity .15s}
.btn:hover{transform:translateY(-1px)}
.btn:active{transform:scale(.99)}
.btn:disabled{opacity:.5;cursor:not-allowed;transform:none}
.btn.ghost{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);font-weight:500}
.btn.danger{background:linear-gradient(135deg,#ef5350,#c62828)}
.alert{background:rgba(239,83,80,0.15);border:1px solid rgba(239,83,80,0.4);color:#ff8a80;
border-radius:12px;padding:12px 14px;font-size:.8rem;line-height:1.5;margin-bottom:18px}
.err{color:#ff8a80;font-size:.83rem;text-align:center;margin-top:12px;min-height:1.2em}
.hint{margin-top:18px;font-size:.75rem;opacity:.4;text-align:center;line-height:1.6}
.meta{margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.1);
font-size:.72rem;opacity:.45;text-align:center;line-height:1.7;word-break:break-all}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:20px}
.kv{background:rgba(255,255,255,0.05);border-radius:12px;padding:12px 14px}
.kv .k{font-size:.7rem;opacity:.5;margin-bottom:4px}
.kv .v{font-size:.95rem;font-weight:600;word-break:break-all}
.row{display:flex;gap:10px;flex-wrap:wrap}
.row>*{flex:1;min-width:140px}
a{color:#4fc3f7;text-decoration:none}
a:hover{text-decoration:underline}
)css";

// ============================================================
//  登录页
// ============================================================
inline String getLoginPage(bool defaultAdminPassword) {
    String html = R"rawliteral(<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>硬件认证 - Chemistry World</title>
<style>)rawliteral";
    html += PAGES_CSS;
    html += R"rawliteral(</style>
</head>
<body>
<div class="card">
  <h1>Chemistry World</h1>
  <p class="sub">%MODEL% 硬件认证</p>
  %BANNER%
  <form id="f">
    <label for="u">用户名</label>
    <input type="text" id="u" autocomplete="username" required>
    <label for="p">密码</label>
    <input type="password" id="p" autocomplete="current-password" required>
    <button class="btn" type="submit" id="btn">登录</button>
  </form>
  <div class="err" id="err"></div>
  <div class="meta">
    设备：%HOST%<br>
    验证通过后跳转到管理后台
  </div>
</div>
<script>
const SITE_URL = "%SITE_URL%";
const PAYLOAD_TTL = 120000;   // 回跳凭证 2 分钟有效，过期作废

// 中文用户名要按 UTF-8 编码再 base64，直接 btoa 会抛异常
function b64url(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = '';
  bytes.forEach(b => bin += String.fromCharCode(b));
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

const err = document.getElementById('err');
const btn = document.getElementById('btn');

document.getElementById('f').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('u').value;
  const password = document.getElementById('p').value;

  btn.disabled = true;
  btn.textContent = '验证中…';
  err.textContent = '';

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({username, password})
    });
    const data = await res.json();

    if (data.success) {
      const payload = {
        success: true,
        token: data.token,
        user: data.user,
        device: '%MODEL%',
        exp: Date.now() + PAYLOAD_TTL
      };
      window.location.href = SITE_URL + '#auth=' + b64url(JSON.stringify(payload));
      return;
    }

    if (res.status === 429) {
      const sec = Math.ceil((data.retryAfterMs || 30000) / 1000);
      err.textContent = '尝试次数过多，请 ' + sec + ' 秒后再试';
    } else {
      err.textContent = data.error || '用户名或密码错误';
    }
  } catch (e) {
    err.textContent = '网络错误：' + e.message;
  }

  btn.disabled = false;
  btn.textContent = '登录';
});
</script>
</body>
</html>)rawliteral";

    String banner;
    if (defaultAdminPassword) {
        banner = "<div class=\"alert\">管理员仍是默认密码。登录后请立即到「设备状态」页修改，"
                 "否则任何知道默认密码的人都能进后台。</div>";
    }

    String host = WiFi.localIP().toString() + " / " + String(DEVICE_NAME) + ".local";
    html = tplReplace(html, "%MODEL%", DEVICE_MODEL);
    html = tplReplace(html, "%SITE_URL%", SITE_URL);
    html = tplReplace(html, "%BANNER%", banner);
    html = tplReplace(html, "%HOST%", host);
    return html;
}

// ============================================================
//  未授权 / token 过期
// ============================================================
inline String getUnauthorizedPage() {
    String html = R"rawliteral(<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>令牌失效</title>
<style>)rawliteral";
    html += PAGES_CSS;
    html += R"rawliteral(</style>
</head>
<body>
<div class="card">
  <h1>令牌无效或已过期</h1>
  <p class="sub">设备重启或超过 2 小时都会让旧令牌失效</p>
  <a class="btn ghost" href="/" style="display:block;text-align:center;line-height:1.6">重新登录</a>
</div>
</body>
</html>)rawliteral";
    return html;
}

// ============================================================
//  设备状态页
// ============================================================
inline String getStatusPage(const String& token, const User& user) {
    String html = R"rawliteral(<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>设备状态 - Chemistry World</title>
<style>)rawliteral";
    html += PAGES_CSS;
    html += R"rawliteral(</style>
</head>
<body>
<div class="card wide">
  <h1>设备状态</h1>
  <p class="sub">%MODEL% · %HOST%</p>

  <div class="grid" id="grid"></div>

  <h1 style="font-size:1rem;text-align:left;margin-bottom:12px">修改我的密码</h1>
  <div class="row">
    <input type="password" id="np" placeholder="新密码（至少 6 位）" autocomplete="new-password">
    <button class="btn" style="max-width:120px" onclick="changePwd()">修改</button>
  </div>

  <div class="row" style="margin-top:8px">
    <a class="btn ghost" id="usersLink" style="text-align:center;line-height:1.7">用户管理</a>
    <button class="btn ghost" onclick="logout()">退出登录</button>
  </div>

  %RESET%

  <div class="err" id="err"></div>
  <div class="meta">
    当前账号：%USERNAME%（%ROLE%）<br>
    令牌 2 小时后过期，设备重启后全部失效
  </div>
</div>
<script>
const TOKEN = "%TOKEN%";
document.getElementById('usersLink').href = '/users?token=' + encodeURIComponent(TOKEN);

function fmtUptime(ms) {
  const s = Math.floor(ms / 1000);
  const d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600),
        m = Math.floor(s % 3600 / 60), sec = s % 60;
  if (d) return d + ' 天 ' + h + ' 小时';
  if (h) return h + ' 小时 ' + m + ' 分';
  if (m) return m + ' 分 ' + sec + ' 秒';
  return sec + ' 秒';
}

async function load() {
  try {
    const d = await (await fetch('/api/ping')).json();
    document.getElementById('grid').innerHTML = [
      ['固件版本', d.version],
      ['IP 地址', d.ip],
      ['信号强度', d.rssi + ' dBm'],
      ['已运行', fmtUptime(d.uptimeMs)],
      ['账号数', d.users],
      ['mDNS', '%DEVICE%.local']
    ].map(([k, v]) => `<div class="kv"><div class="k">${k}</div><div class="v">${v}</div></div>`).join('');
  } catch (e) {
    document.getElementById('err').textContent = '读取设备信息失败：' + e.message;
  }
}

async function changePwd() {
  const np = document.getElementById('np').value;
  const err = document.getElementById('err');
  if (np.length < 6) { err.textContent = '密码至少 6 位'; return; }

  const res = await fetch('/api/users/password', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token: TOKEN, username: '%USERNAME%', newPassword: np})
  });
  const data = await res.json();

  if (data.success) {
    // 改自己的密码会让当前令牌立即失效，必须重新登录
    alert('密码已修改，请重新登录');
    location.href = '/';
  } else {
    err.textContent = data.error || '修改失败';
  }
}

async function logout() {
  await fetch('/api/logout', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token: TOKEN})
  }).catch(() => {});
  location.href = '/';
}

async function factoryReset() {
  if (!confirm('确定恢复出厂设置？所有账号会被清除，设备将重启并回到默认账号。')) return;
  if (!confirm('再确认一次：这个操作不可撤销。')) return;
  await fetch('/api/factory-reset', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token: TOKEN})
  }).catch(() => {});
  document.body.innerHTML = '<div class="card"><h1>已恢复出厂设置</h1><p class="sub">设备重启中，约 10 秒后重新访问</p></div>';
}

load();
</script>
</body>
</html>)rawliteral";

    String resetBlock;
    if (user.role == "admin") {
        resetBlock = "<button class=\"btn danger\" style=\"margin-top:8px\" onclick=\"factoryReset()\">"
                     "恢复出厂设置（清除全部账号）</button>";
    }

    String host = WiFi.localIP().toString();
    html = tplReplace(html, "%MODEL%", DEVICE_MODEL);
    html = tplReplace(html, "%HOST%", host);
    html = tplReplace(html, "%DEVICE%", DEVICE_NAME);
    html = tplReplace(html, "%TOKEN%", token);
    html = tplReplace(html, "%USERNAME%", user.username);
    html = tplReplace(html, "%ROLE%", user.role == "admin" ? "管理员" : "访客");
    html = tplReplace(html, "%RESET%", resetBlock);
    return html;
}

// ============================================================
//  用户管理页
// ============================================================
inline String getUsersPage(const String& token) {
    String html = R"rawliteral(<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>用户管理 - Chemistry World</title>
<style>)rawliteral";
    html += PAGES_CSS;
    html += R"rawliteral(
.user-item{display:flex;align-items:center;justify-content:space-between;gap:12px;
padding:12px 14px;border-radius:12px;background:rgba(255,255,255,0.05);margin-bottom:8px;flex-wrap:wrap}
.avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#4fc3f7,#0288d1);
display:flex;align-items:center;justify-content:center;font-weight:700;flex:0 0 auto}
.uname{font-weight:600;font-size:.92rem}
.urole{font-size:.72rem;opacity:.55;margin-top:2px}
.tag{padding:1px 8px;border-radius:8px;font-size:.68rem;margin-left:6px}
.tag.admin{background:rgba(79,195,247,.2);color:#4fc3f7}
.tag.visitor{background:rgba(255,255,255,.1);opacity:.7}
.act{display:flex;gap:6px}
.act button{padding:6px 12px;font-size:.75rem;border-radius:8px;border:none;cursor:pointer;
background:rgba(255,255,255,.1);color:#fff}
.act button.d{background:rgba(239,83,80,.25);color:#ff8a80}
.empty{text-align:center;opacity:.4;padding:24px;font-size:.85rem}
.toast{position:fixed;top:24px;left:50%;transform:translateX(-50%);padding:11px 22px;border-radius:22px;
background:rgba(0,0,0,.8);font-size:.85rem;opacity:0;transition:opacity .25s;pointer-events:none;z-index:9}
.toast.on{opacity:1}
</style>
</head>
<body>
<div class="card wide">
  <h1>用户管理</h1>
  <p class="sub">%MODEL% · 共 <span id="cnt">0</span> 个账号</p>

  <div id="list"><div class="empty">加载中…</div></div>

  <h1 style="font-size:1rem;text-align:left;margin:22px 0 12px">新建账号</h1>
  <div class="row">
    <input type="text" id="nu" placeholder="用户名" style="min-width:120px">
    <input type="password" id="npp" placeholder="密码（至少 6 位）" style="min-width:140px">
    <select id="nr" style="min-width:100px;max-width:130px">
      <option value="visitor">访客</option>
      <option value="admin">管理员</option>
    </select>
    <button class="btn" style="max-width:100px" onclick="createUser()">创建</button>
  </div>

  <div class="row" style="margin-top:14px">
    <a class="btn ghost" id="backLink" style="text-align:center;line-height:1.7">返回设备状态</a>
  </div>

  <div class="err" id="err"></div>
</div>
<div class="toast" id="toast"></div>
<script>
const TOKEN = "%TOKEN%";
document.getElementById('backLink').href = '/status?token=' + encodeURIComponent(TOKEN);

function toast(t) {
  const el = document.getElementById('toast');
  el.textContent = t;
  el.classList.add('on');
  setTimeout(() => el.classList.remove('on'), 2000);
}

async function loadUsers() {
  const res = await fetch('/api/users/list?token=' + encodeURIComponent(TOKEN));
  const data = await res.json();
  const box = document.getElementById('list');

  if (!data.success) {
    box.innerHTML = '<div class="empty">' + (data.error || '读取失败，请重新登录') + '</div>';
    return;
  }

  document.getElementById('cnt').textContent = data.users.length;
  if (!data.users.length) {
    box.innerHTML = '<div class="empty">暂无账号</div>';
    return;
  }

  box.innerHTML = data.users.map(u => `
    <div class="user-item">
      <div style="display:flex;align-items:center;gap:12px">
        <div class="avatar">${u.username.charAt(0).toUpperCase()}</div>
        <div>
          <div class="uname">${u.username}<span class="tag ${u.role}">${u.role === 'admin' ? '管理员' : '访客'}</span></div>
          <div class="urole">${u.permissions || ''}</div>
        </div>
      </div>
      <div class="act">
        <button onclick="changePwd('${u.username}')">改密码</button>
        ${u.role !== 'admin' ? `<button class="d" onclick="delUser('${u.username}')">删除</button>` : ''}
      </div>
    </div>`).join('');
}

async function createUser() {
  const username = document.getElementById('nu').value.trim();
  const password = document.getElementById('npp').value;
  const role = document.getElementById('nr').value;
  const err = document.getElementById('err');
  err.textContent = '';

  if (!username || password.length < 6) { err.textContent = '用户名不能为空，密码至少 6 位'; return; }

  const res = await fetch('/api/users/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token: TOKEN, username, password, role})
  });
  const data = await res.json();

  if (data.success) {
    document.getElementById('nu').value = '';
    document.getElementById('npp').value = '';
    toast('已创建');
    loadUsers();
  } else {
    err.textContent = data.error || '创建失败';
  }
}

async function changePwd(username) {
  const np = prompt('为 ' + username + ' 设置新密码（至少 6 位）：');
  if (np === null) return;
  if (np.length < 6) { toast('密码至少 6 位'); return; }

  const res = await fetch('/api/users/password', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token: TOKEN, username, newPassword: np})
  });
  const data = await res.json();
  toast(data.success ? '密码已修改' : (data.error || '修改失败'));
}

async function delUser(username) {
  if (!confirm('确定删除账号 ' + username + '？')) return;

  const res = await fetch('/api/users/delete', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token: TOKEN, username})
  });
  const data = await res.json();

  if (data.success) { toast('已删除'); loadUsers(); }
  else { toast(data.error || '删除失败'); }
}

loadUsers();
</script>
</body>
</html>)rawliteral";

    html = tplReplace(html, "%MODEL%", DEVICE_MODEL);
    html = tplReplace(html, "%TOKEN%", token);
    return html;
}

#endif // PAGES_H
