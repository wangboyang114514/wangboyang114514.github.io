#!/usr/bin/env node
// ESP32-S3 认证服务自检脚本
//
// 用法（刷完固件、串口看到 IP 之后）：
//   node esp32-auth-server/test/api-smoke.mjs http://192.168.1.100
//
// 想连登录相关的用例再加账号密码（不传就只跑不需要凭据的用例）：
//   ESP32_USER=admin ESP32_PASS='你的密码' node esp32-auth-server/test/api-smoke.mjs http://chemworld.local
//
// 注意：最后一步会故意用错密码试几次，正常情况不触发限流；
// 如果你的 LOGIN_MAX_FAILS 调过，这一步可能把本机 IP 锁住。

const base = (process.argv[2] || process.env.ESP32_URL || 'http://chemworld.local').replace(/\/+$/, '');
const user = process.env.ESP32_USER || '';
const pass = process.env.ESP32_PASS || '';

let pass_ = 0;
let fail_ = 0;

function ok(name, extra = '') {
    pass_++;
    console.log(`  ✅ ${name}${extra ? '  ' + extra : ''}`);
}

function bad(name, detail) {
    fail_++;
    console.log(`  ❌ ${name}  ${detail}`);
}

async function req(path, { method = 'GET', body, timeout = 5000 } = {}) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeout);
    try {
        const res = await fetch(base + path, {
            method,
            headers: body ? { 'Content-Type': 'application/json' } : undefined,
            body: body ? JSON.stringify(body) : undefined,
            signal: ctrl.signal
        });
        let json = null;
        try { json = await res.json(); } catch (e) { /* 有些响应没有 body */ }
        return { status: res.status, json, headers: res.headers };
    } finally {
        clearTimeout(timer);
    }
}

function summary(title) {
    console.log(`\n${title}`);
}

(async () => {
    console.log(`目标设备：${base}\n`);

    // ---------- 1. 探活 ----------
    summary('[1] 探活 /api/ping');
    let ping;
    try {
        ping = await req('/api/ping', { timeout: 3000 });
    } catch (e) {
        bad('设备无响应', e.name === 'AbortError' ? '3 秒超时（设备不在线？IP 不对？）' : e.message);
        console.log('\n设备连不上，后面的用例跳过。');
        process.exit(1);
    }

    if (ping.status === 200 && ping.json?.success) {
        ok('HTTP 200，返回 success=true');
        ok('设备信息', `${ping.json.device || '?'} v${ping.json.version || '?'} / ${ping.json.ip || '?'} / ${ping.json.rssi ?? '?'} dBm`);
        if (typeof ping.json.users === 'number') ok('账号数', String(ping.json.users));
    } else {
        bad('探活失败', `status=${ping.status} body=${JSON.stringify(ping.json)}`);
    }

    // ---------- 2. 跨域头 ----------
    summary('[2] 跨域白名单');
    {
        const allowed = await fetch(base + '/api/ping', { headers: { Origin: 'https://wangboyang114514.github.io' } })
            .then(r => r.headers.get('access-control-allow-origin')).catch(() => null);
        const denied = await fetch(base + '/api/ping', { headers: { Origin: 'https://evil.example.com' } })
            .then(r => r.headers.get('access-control-allow-origin')).catch(() => null);

        if (allowed === 'https://wangboyang114514.github.io') ok('站点来源被放行');
        else bad('站点来源没拿到 ACAO', String(allowed));

        if (denied === null) ok('陌生来源被拒绝（没有回 ACAO）');
        else bad('陌生来源竟然也拿到了 ACAO', String(denied));
    }

    // ---------- 3. 错误密码必须被拒 ----------
    summary('[3] 错误凭据');
    {
        const r = await req('/api/login', { method: 'POST', body: { username: 'admin', password: 'definitely-wrong-' + Date.now() } });
        if (r.status === 401) ok('错误密码返回 401');
        else if (r.status === 429) ok('已处于限流状态（说明限流生效）', JSON.stringify(r.json));
        else bad('错误密码没被拒', `status=${r.status}`);
    }

    // ---------- 4. 未带 token 不能读用户列表 ----------
    summary('[4] 未授权访问');
    {
        const r = await req('/api/users/list');
        if (r.status === 403 || r.status === 401) ok('无 token 读取用户列表被拒', `status=${r.status}`);
        else bad('无 token 竟然能读用户列表', `status=${r.status}`);
    }

    // ---------- 5. 正常登录链路 ----------
    if (!user || !pass) {
        summary('[5] 登录链路');
        console.log('  ⏭  跳过（未提供 ESP32_USER / ESP32_PASS）');
    } else {
        summary('[5] 登录链路');
        const login = await req('/api/login', { method: 'POST', body: { username: user, password: pass } });

        if (login.status !== 200 || !login.json?.token) {
            bad('登录失败', `status=${login.status} ${JSON.stringify(login.json)}`);
        } else {
            const token = login.json.token;
            ok('登录成功', `token ${token.length} 位`);
            ok('返回用户信息', `${login.json.user?.username} / ${login.json.user?.role}`);
            ok('返回有效期', `${login.json.expiresIn} 秒`);

            const ver = await req('/api/verify', { method: 'POST', body: { token } });
            if (ver.status === 200 && ver.json?.success) ok('/api/verify 令牌有效');
            else bad('/api/verify 判定异常', `status=${ver.status}`);

            const list = await req('/api/users/list?token=' + encodeURIComponent(token));
            if (list.status === 200 && Array.isArray(list.json?.users)) ok('用户列表可读', `${list.json.users.length} 个账号`);
            else bad('用户列表读取失败', `status=${list.status}`);

            const out = await req('/api/logout', { method: 'POST', body: { token } });
            if (out.status === 200 && out.json?.success) ok('/api/logout 正常返回');
            else bad('/api/logout 异常', `status=${out.status}`);

            const after = await req('/api/verify', { method: 'POST', body: { token } });
            if (after.status === 401) ok('登出后令牌立即失效');
            else bad('登出后令牌居然还能用', `status=${after.status}`);
        }
    }

    // ---------- 6. 请求体上限 ----------
    summary('[6] 请求体上限');
    {
        const big = 'x'.repeat(2000);
        const r = await req('/api/login', { method: 'POST', body: { username: big, password: big } });
        if (r.status === 413) ok('2KB 请求体被拒（413）');
        else bad('超大请求体没有被拦', `status=${r.status}`);
    }

    console.log(`\n结果：${pass_} 通过，${fail_} 失败`);
    process.exit(fail_ === 0 ? 0 : 1);
})();
