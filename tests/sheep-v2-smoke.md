# 化学版羊了个羊 v2 — 运行时验收报告（smoke / 遮挡 / 布局 / EDGE）

- **被测文件**：`games/chinese/sheep_game.html`（2249 行，含内联 JS）
- **验收日期**：2026-11-08
- **验收方式**：真实浏览器（Microsoft Edge）+ headless 驱动，真实鼠标坐标点击（`elementFromPoint` 校验命中的是目标牌后 `mouse.click`），非 `dispatchEvent`
- **是否改动被测代码**：**否**。本轮只读+只测；`games/chinese/sheep_game.html`、`games/game-theme.css`、`styles.css`、`elements-*.js` 均未修改，未产生任何 git 提交
- **脚本与截图**：`%TEMP%\sheep-qa\`（`t1_smoke.mjs` / `t2_occlusion.mjs` / `t2b_entry.mjs` / `t3_layout.mjs` / `t4_edges.mjs` / `t5_bench.mjs` / `t6*.mjs` / `t7_tut_branch.mjs` / `t8_layout2.mjs` / `t9_final.mjs`，截图在 `shots\`），**均未进仓库**

---

## ① 环境与版本

| 项 | 值 |
|---|---|
| OS | Windows 11 Home China |
| Node | v24.14.0 |
| npm | 11.9.0 |
| Python | 3.13.14 |
| 浏览器 | Microsoft Edge（`C:\Program Files (x86)\Microsoft Edge\Application\msedge.exe`） |
| 驱动 | `playwright-core@1.65.0`（安装在 `%TEMP%\sheep-qa`，**未动仓库 package.json**） |
| 启动参数 | `chromium.launch({ executablePath: msedge.exe, headless: true })` |
| 静态服务 | `python -m http.server 8765`，根目录 = 仓库根 `C:/GitHub/wangboyang114514.github.io` |
| 访问地址 | `http://127.0.0.1:8765/games/chinese/sheep_game.html` |
| 默认视口 | 390×780（另测 375×667 / 320×568 / 1024×768） |
| 语言 / 动效 | `zh-CN` / `prefers-reduced-motion: no-preference`（抖动动画据此才会执行） |

资源可达性：`sheep_game.html` / `elements-zh.js` / `games/game-theme.css` 均 HTTP 200。

---

## ② 冒烟结果

### 2.1 关卡选择页

| 检查项 | 实测 | 结论 |
|---|---|---|
| 关卡卡数量 | 6 | ✓ |
| 锁定机制 | `unlocked=1` 时仅 L1 可点，其余 `disabled` | ✓ |
| 标题 / 帮助按钮 | `化学版羊了个羊` / `#helpBtn` 存在 | ✓ |

### 2.2 L1 首屏渲染

| 检查项 | 实测 |
|---|---|
| 牌堆 | 9 张 `.sg-tile`（3 层：6+3，按 L1 配置 `rows:[1,2,3]` + `[1,2]`） |
| 槽位 | 7 个 `.sg-slot`，`#slotRail[data-fill="0"]` |
| HUD | `关卡 1 / 6`、`分数 0`、`剩余 9 张`、`0/7` |
| 道具条 | 仅 `undo`（剩 3 次），与 `props:{undo:3}` 一致 |
| 盘面尺寸 | stage 216×216（`--tile` = 72px，`boardW=boardH=3`） |

### 2.3 L1 打到胜利态 ✅

贪心策略（优先凑第 3 张 → 再凑对子 → 再找盘面 3 连），**9 步真实点击通关**：

```
步 1-3  → 槽位依次累积，步 4 起开始成组消除
步 7    → 槽位 O,Cu,O + O → 消除（+100）
步 9    → Cu,Cu + Cu → 消除（+100），盘面与槽位同时清空
```

| 结果 | 值 |
|---|---|
| 步数 | 9（上限 60，未触顶） |
| 得分 | 300（3 次三消 × 100） |
| 结算 | `#ovlWin` 显示，标题「**完美通关！**」，`得分 900`（300 + 关卡奖励 300 + 未用道具 3×100 = 900，算式自洽） |
| 星级 | ★★★ |
| 状态机 | `G.status = 'won'` |
| 通关后行为 | `prog.unlocked` 提升，`buildLevelList()` 重绘，L2 解锁 |

### 2.4 L2–L6 加载

每关独立新开浏览器上下文（`unlocked=6`），点击关卡卡进入，等首张牌出现后采样：

| 关 | 牌数（DOM / geo） | 开局可点 | 槽位 | 道具 | 暂存区 | 白屏 | 游戏自身报错 |
|---|---|---|---|---|---|---|---|
| L2 石墨层 | 18 / 18 | 6 | 7 | undo | 隐藏 | 无 | 无 |
| L3 岩盐晶格 | 24 / 24 | 8 | 7 | undo,eject | 显示 | 无 | 无 |
| L4 层状解理 | 30 / 30 | 10 | 7 | undo,eject,hint | 显示 | 无 | 无 |
| L5 尖晶石塔 | 36 / 36 | **12** | 7 | undo,eject,shuffle,hint | 显示 | 无 | 无 |
| L6 元素矿脉 | 45 / 45 | 15 | 7 | undo,eject,shuffle,hint | 显示 | 无 | 无 |

- 六关断言 A1–A6 全部通过（无 `[sheep] 关卡 N 断言失败`），`console.table` 的六关族成员表正常输出
- 无 `alert`（`dialog` 事件 0 次），说明没有触发 `assertLevel` / `generateBoard` 的中止分支
- 6 关全部 `rendered = true`、`boardVisible = true`

---

## ③ 遮挡机制（本次重做核心）

### 3.1 开局可点数（硬指标）

| 关 | 要求 | 实测 `data-blocked="false"` | 几何独立复算 `above[id].length===0` | 结论 |
|---|---|---|---|---|
| **L1** | **= 3** | **3**（id 6,7,8，全在第 1 层） | 3 | ✅ 精确命中 |
| **L5** | **= 12** | **12** | 12 | ✅ 精确命中 |

- L1 的 6 张第 0 层牌全部被第 1 层压住，`--depth` 分别为 1/2/2/1/2/1；3 张可点牌 `--depth = 0`
- L5 分层统计：`layer0` 12 张全 blocked、`layer1` 12 张全 blocked、`layer2` 12 张全 free（顶层的 12 张即 12 个可点）

> DOM 与几何引擎两路独立计算的结果完全一致，未发现「视觉遮挡」与「逻辑遮挡」脱节。

### 3.2 点「被遮挡」的牌：三项状态必须不变

L1，点击 `data-blocked="true"` 的 id=0（O，被 1 张牌压住），点击点由 `elementFromPoint` 确认落在该牌上（163,203）：

| 观测量 | 点击前 | 点击后 | 变化 |
|---|---|---|---|
| 分数 | 0 | 0 | ❌ 无 |
| 槽位数量 | 0（`data-fill="0"`） | 0（`data-fill="0"`） | ❌ 无 |
| 道具次数 | `undo:3` | `undo:3` | ❌ 无 |
| 活牌数 / DOM 牌数 | 9 / 9 | 9 / 9 | ❌ 无 |
| `status` | playing | playing | ❌ 无 |

L5（滚到顶部后）复测同样全不变：`score 0→0`、`slot 0→0`、`props {undo:3,eject:1,shuffle:1,hint:1}` 完全一致、`alive 36→36`。

### 3.3 抖动反馈：**有动画，但没有抖动类名**

| 检查 | 实测 |
|---|---|
| `.is-shaking`（或任何抖动类名） | **0 个**；`#board.className` 始终为 `sg-board`，被点牌的 `className` 也没变（`sg-tile is-entering`） |
| 等价反馈 | **有**：被点牌 `.sg-tile__face` 上出现 1 条 Web Animations 动画，`duration=180ms`，`playState=running`，动画名 `(WAAPI)`（非 CSS class/keyframes） |
| 遮挡者高亮 | **有**：压住它的那张牌（id=6）的 face 上同时出现 1 条 `boxShadow` 动画（400ms） |
| 读屏播报 | `#srLive` → 「这张牌被压住了」 |

> 结论：**行为正确，实现与验收脚本的预期不符**。`blockedFeedback()`（第 1333–1364 行）用 `face.animate([...])` 内联补动画，故意不新增类名；同时 `game-theme.css:433` 定义了 `.sg-board.is-shaking { animation: sg-shake ... }`，**JS 从未添加过该 class → 是死代码**。

### 3.4 点「可点」的牌：必须有变化

L1 点 id=6（Fe，`data-blocked=false`）：

| 观测量 | 前 | 后 |
|---|---|---|
| 槽位数（DOM/模型） | 0 | **1（Fe）** |
| `.sg-tile` 数量 | 9 | 8 |
| `alive` | 9 | 8 |

分数未变（单张不成组，设计如此），**槽位与牌数都已变化** → 通过「分数或槽位必须有变化」的判定。

---

## ④ 布局三档

测试位：L1（9 张，stage 216×216）与 L6（45 张，stage 432×288，最难档），均滚到顶部后采样。

| 视口 | 关卡 | `documentElement.scrollWidth` | 横向可滚动 | 槽位 7 格 | 单元格 | 盘面 stage | 牌是否出界 |
|---|---|---|---|---|---|---|---|
| **375×667** | L1 | **375** | 否 | 7/7，全部在视口内（x 1–373.9） | 49.0×49.0 | 216 宽，79.5–295.5 | 0 张 |
| **375×667** | L6 | **375** | 否 | 7/7，全部在视口内 | 49.0×49.0 | 327 宽，29–356 | 0 张 |
| **320×568** | L1 | 320 | 否 | 7/7，全部在视口内（x 1–319） | 41.1×41.1 | 216 宽，52–268 | 0 张 |
| **320×568** | L6 | 320 | 否 | 7/7，全部在视口内 | 41.1×41.1 | 272 宽，29–301 | 0 张 |
| **1024×768** | L1 | 1024 | 否 | 7/7（x 133–890.9） | 104×104 | 216 宽，居中 404–620 | 0 张 |
| **1024×768** | L6 | 1024 | 否 | 7/7 | 104×104 | 432 宽，居中 296–728 | 0 张 |

- 375：槽位轨 `margin-inline:-20px` 出血后宽度正好 375，7 格 49px/格（≥ Apple HIG 44px）✅
- 320：7 格 **41.1px/格 < 44px**，不出界但不达 HIG 最小触控尺寸（见 S3-3）
- 1024：盘面最大 432px 居中，无溢出；槽位轨被 `max-width:760px` 收住

**但 375 档出现过溢出**，需要如实记录：

| 采样批次 | 375 下 `scrollWidth > 375` 的次数 | 值 |
|---|---|---|
| t3（12 次采样：3 视口 × 2 关 × 顶部/底部） | 4 次（均为 375 档） | 383（L1 顶）、393（L1 底）、399（L6 顶）、395（L6 底） |
| t8（14 次采样：6 次布局 + 8 次独立加载） | 0 次 | 全部 375 |
| 合计 26 次 | **4 次（15.4%）**，只出现在 375 档 | 381–399 |

根因已定位（二分隐藏定位法）：**溢出源是全站装饰层 `.atomic-orbitals / .orbital`（`interaction.js` 注入的旋转轨道动画）**——隐藏该节点后 `scrollWidth` 立刻回到 375，且 `#stage`、`.sg-tile`、`.sg-slot` 的 `right` 最大值为 356（<375），**游戏本体不溢出**。同时 `window.scrollTo(300,0)` 后 `scrollX` 恒为 0（`body{overflow-x:clip}` 生效），**用户无法真正横滚**，只是度量值超标。

---

## ⑤ EDGE 用例

### EDGE-1 连续快速点同一张牌两次 → 槽位只 +1 ✅

| 方式 | 槽位 | DOM 牌数 | 结论 |
|---|---|---|---|
| 同帧连续派发 2 次 click（第 2 次时元素已被移除） | 0 → **1** | 9 → **8** | +1 ✓ |
| 分两次派发同一 id 的 click | 1 → **2** | — | +1 ✓ |

`commitMove()` 同步置 `G.busy = true`，第二次进入 `onBoardActivate` 即在 `if (G.status !== 'playing' || G.busy) return;` 被拦下；同时 `doMove()` 在首个 `await` 之前就 `fromEl.remove()`，元素已脱离文档。双保险，未出现双入槽。

### EDGE-2 槽位塞到 7 且第 7 张凑三消 → 判定在消除之后 ✅（真实点击构造成功，未注入状态）

用「优先点槽内出现次数最少的 symbol」反向策略把槽位堆到 6 而刻意不成组，seed=4 的第 7 步命中：

```
槽位前：['Cu','O','Cu','Fe','Fe','O']  (6 张)
点第 7 张：Cu
resolveAll(预测)：1 组        ← 消除确实存在
结果：槽位 7 → 4，score 0 → 100，status 仍为 'playing'
```

- 若判负早于消除，此处会弹失败浮层；实际**未失败**，且得分正确 +100（1.0 倍率）
- 代码路径确认（`doMove` 第 1434–1444 行）：`await settleSlot()` → `if (clearedGroups===0) chain=0` → 之后才 `else if (G.slot.length >= SLOT_MAX) loseLevel()`

### EDGE-3 洗牌后是否有 ghost 牌 ✅ 无

L5，先真实点掉 3 张（槽位 `['Na','K','F']`），再点「洗牌」：

| 检查 | 洗牌前 | 洗牌后 | 结果 |
|---|---|---|---|
| 盘面牌数 | 33 | 33 | ✓ |
| 槽位牌数（模型/DOM） | 3 / 3 | 3 / 3 | ✓ |
| 暂存区 | 0 | 0 | ✓ |
| DOM `.sg-tile` = `alive` | 33 = 33 | 33 = 33 | ✓ |
| 符号多重集（含槽位前缀） | Na/K/F 各 6,6,6… | **完全一致** | ✓ |
| 洗牌次数 | 1 | 0（已扣） | ✓ 洗牌真的执行了 |

盘面 + 槽位 + 暂存区守恒（36 = 33+3+0 前后一致），**无 ghost、无重复、无丢牌**。原子回滚分支（`solveFromCurrent()` 失败时退还次数）本轮未触发（未构造出洗牌后无解的局面）。

### EDGE-4 暂存区（eject）的牌不参与消除 ✅

L3（`eject:1`）真实操作：

| 步骤 | 槽位 | 暂存区 | 分数 |
|---|---|---|---|
| 点 1 张 Na | `['Na']` | `[]` | 0 |
| 点「移出」 | `[]` | `['Na']` | 0（eject 1→0） |
| 再点 2 张 Na | `['Na','Na']` | `['Na']` | **0，未消除** |
| 400ms 后再采 | `['Na','Na']` | `['Na']` | 0，暂存区仍在 |

槽内 2 张 + 暂存区 1 张 = 同名 3 张，**没有误消**。纯函数层交叉验证：`resolveAll` 签名只接受 slot 数组（第 787 行），暂存区在结构上无法参与匹配。

> 补测未完成：想再点第 3 张 Na 验证「正常三消且暂存区不被消费」，当时盘面已无可点的 Na，**未能验证这一步**（不影响上表结论）。

### EDGE-5（额外发现）暂存区满 3 张 + 盘面清空 → 误判失败 ❌

见 ⑧ S2-2 与下节复现。构造态：`bench=['F','Cl','Br']`、`slot=['Na','Na']`、`alive=1 张 Na`，最后一次点击为真实鼠标点击（消除真实发生，score +100），随后：

- `status = 'lost'`，`#ovlLose` 弹出，标题「**槽位满了**」、正文「**7 格全满，没有凑成三连。**」——而此刻**槽位是空的**
- 同时 console.error：`状态异常：没有可点的牌`

---

## ⑥ console 报错清单（原文）

每次开页/每关加载都会捕获，按出现频率归类：

### E1 · 全站既有（**本页未引入**，对照组已证实）

```
Initialization error: TypeError: Cannot read properties of undefined (reading 'debounce')
    at Object.setupEventListeners (http://127.0.0.1:8765/interaction.js:754:58)
    at Object.init (http://127.0.0.1:8765/interaction.js:746:22)
    at Object.init (http://127.0.0.1:8765/interaction.js:725:31)
    at HTMLDocument.<anonymous> (http://127.0.0.1:8765/interaction.js:846:72)
```
- 类型：`console.error`，出现于**每一次**开页
- 对照组：`index.html` / `chinese.html` / `games/chinese/games.html` **同样复现** → 与本次改动无关，属全站遗留（`this.utils` 未初始化即被 `setupEventListeners` 使用）

### E2 · 本页独有

```
Uncaught TypeError: Cannot read properties of null (reading 'appendChild')
TypeError: Cannot read properties of null (reading 'appendChild')
    at http://127.0.0.1:8765/elements-zh.js:146:17
    at Array.forEach (<anonymous>)
```
- 类型：`pageerror`（未捕获），**每次开页 1 次，6 关加载同样各 1 次**
- 原因：本页把 `elements-zh.js` 当**纯数据源**引入，但该文件第 124 行 `const elementList = document.getElementById('element-list')` 在本页为 `null`，第 146 行 `elementList.appendChild(link)` 直接抛错
- 影响：抛错发生在其后的 `DOMContentLoaded` 搜索/筛选绑定之前，但游戏脚本在 `<script>` 后执行、`elements` 全局已定义，**玩法未受影响**（L1 通关、L2–L6 加载均正常）

### E3 · 404（服务器侧，非页面资源）

```
Failed to load resource: the server responded with a status of 404 (File not found)
```
- 服务端日志确认：`GET /favicon.ico HTTP/1.1" 404`。全站缺 favicon，**与本页无关**

### E4 · 游戏自身（仅在 EDGE-5 构造态出现）

```
状态异常：没有可点的牌
```
- 来自第 1450 行 `console.error(t('err.noClickable'))`，即「活牌里没有任何一张不被遮挡」的自检分支被错误触发（此时根本没有活牌）

> 正常游玩（L1 通关 9 步、L5 点击/洗牌/暂存）**没有产生任何游戏自身的 console error**，也没有 A1–A6 断言失败、没有 `alert`。

---

## ⑦ 最终判定

# CONCERNS

**可以上线，但建议先修 2 个 S2。** 不给 PASS 的理由：存在 1 个「错误结算 + 错误文案 + 控制台异常」的真实逻辑缺陷（S2-2），以及 1 个影响正常点击可达性的进入态缺陷（S2-1）。不给 FAIL 的理由：**核心玩法链路全部跑通**——遮挡计数与几何引擎完全吻合（L1=3 / L5=12）、被遮挡牌点击零副作用、消除与判负顺序正确、洗牌无 ghost、暂存区不参与匹配、三档视口下游戏本体不溢出、L1 能真实打到三星通关，没有任何阻断性（S1）问题。

---

## ⑧ 阻塞项分级

### S1（阻断上线）—— **无**

无。L1 可通关；L2–L6 可加载可操作；无白屏、无崩溃、无 A1–A6 断言失败。

### S2（体验/正确性缺陷，建议上线前修）

**S2-1 · 从关卡列表进入对局时不回到页面顶部，盘面顶部被吸顶导航栏遮挡**
- 现象：`startLevel()` 没有 `window.scrollTo(0,0)`（`showSelect()` 有）。用户在关卡列表向下滚动后点 LEVEL 5/6，进入对局时保留原滚动位置，`position:sticky; z-index:100` 的 `.navbar`（高 114px，视口 y 40–154）压在盘面上。实测 375×667 进 L5 时 `scrollY=189`、`stage` 顶部只到 y=10，**20/36 张牌的中心落在导航栏下方**，`elementFromPoint` 命中的是 `.navbar`，这些牌点不动；390×780 进 L6 有 20/45 张、进 L5 有 8/36 张被遮。
- 复现：375×667 → 向下滚动点「LEVEL 5 尖晶石塔」→ 观察盘面第一、二行被导航栏盖住 → 直接点这两行 → 无反应（必须先手动上滑）。
- 期望：`startLevel()` 里 `window.scrollTo({top:0})`（或让对局视图成为独立滚动容器），保证进关后整块盘面在导航栏之下。

**S2-2 · 暂存区非空时清空盘面 → 误判失败，且失败文案与事实矛盾**
- 现象：`doMove()` 的胜利条件写成 `alive===0 && slot===0 && **bench===0**`（第 1440 行）。当 `bench.length>0` 时该条件不成立，随后进入 `else` 分支的 F2 自检，`G.alive` 已空 → `anyFree=false` → `console.error('状态异常：没有可点的牌')` + `loseLevel('state')`。玩家看到的是「槽位满了 / 7 格全满，没有凑成三连」，**但此刻槽位是空的**。
- 复现（构造态，最后一次点击为真实点击）：L5 先把 3 张牌 eject 进暂存区（`bench` 上限 3，可分两次 eject 达成：槽内 1 张 eject → 暂存 1；槽内 2 张 eject → 暂存 3），再把盘面清空。实测注入 `bench=['F','Cl','Br']`、`slot=['Na','Na']`、`alive=1` 后点击最后一张 Na：消除正常（+100、槽位清空），随即 `status='lost'`、`#ovlLose` 弹出「槽位满了」、控制台 `状态异常：没有可点的牌`。
- 可达性说明：**本次未能用纯真实点击跑完「eject 3 张 + 清空盘面」的全过程**（求解器在该态下给不出路径，且手工点选时序多次失手），因此本条是「构造前置状态 + 真实最后一击」的复现，不是全程真机复现。但分支可达性成立：`bench` 容量恰好为 3，eject 移出的牌数可为 3 的倍数，此时盘面剩余牌数仍能被 3 整除，具备清空条件。
- 期望：`alive===0 && slot===0` 时不应走「无牌可点」的失败分支。要么把判定改为 `alive===0 && slot===0 && bench===0` 时判胜、`alive===0 && slot===0 && bench>0` 时把暂存区牌并入槽位再结算（或提示「请把暂存区的牌放回槽位」并禁止判负），要么直接把 bench 内容视作「已完成的牌」参与胜利条件。

**S2-3 · `elements-zh.js` 在本页每次加载都抛未捕获 TypeError**
- 现象：`Uncaught TypeError: Cannot read properties of null (reading 'appendChild')` at `elements-zh.js:146`（见 ⑥ E2）。6 个关卡页各抛 1 次，进关/重开不清除。
- 复现：打开任意关（或直接打开本页）→ 控制台立即一条红色未捕获异常。
- 期望：本页只需要 `elements` 数组，不应触发该文件的 DOM 注入。可在引入前提供占位节点 `<div id="element-list" hidden></div>`，或改用只含数据的副本/在引入后包一层 try-catch（不改动 `elements-zh.js` 本身亦可）。

### S3（建议）

| 编号 | 问题 | 证据 |
|---|---|---|
| S3-1 | **无抖动类名**：验收预期 `.is-shaking`，实际用 WAAPI 内联动画（180ms），功能等效但契约不符；且 `game-theme.css:433` 的 `.sg-board.is-shaking` 从未被 JS 使用（死代码） | 见 ③3.3 |
| S3-2 | **无 `data-sym` 属性**：牌面符号只存在于 `.sg-tile__sym` 文本与 `G.symOf`，自动化脚本按 `data-sym` 取符号会全取到 `undefined`（本轮已改用文本读取） | `grep data-sym` → 0 命中 |
| S3-3 | 320×568 下槽位 41.1px/格，低于 44px 最小触控建议（375 下 49px 达标） | 见 ④ |
| S3-4 | 全站 `#loading-overlay`（`z-index:9999`，`interaction.js` 创建）在 `load` + 500ms + 500ms 后才移除，**开页后约 1 秒内所有点击被吞**；本轮多次自动化点击因此空转 | `dbg_l3` 实测 `elementFromPoint` 返回 `loading-overlay` |
| S3-5 | 375 下偶发 `scrollWidth > 375`（26 次采样中 2 次，381–399），源为装饰层 `.atomic-orbitals`；虽不可实际横滚，但仍违反「375 无横向滚动」的字面指标 | 见 ④ |
| S3-6 | L5 一次性解锁横幅 `.sgp-notify`（top:4，高 85px，3.2s）覆盖盘面顶行，期间顶行牌不可点 | `07-entry-L5-390x780.png` |
| S3-7 | 全站 `interaction.js` 的 `debounce` 报错（见 ⑥ E1），建议单独立项修 | 对照组 4 页全复现 |
| S3-8 | 站点缺 `favicon.ico`（`/favicon.ico` 404） | 服务端日志 |

---

## 附：未能验证的项目（明确说明，不作「应该没问题」的推断）

| 项目 | 原因 |
|---|---|
| 真机触摸（`touchstart`/`pointerdown` 按压反馈 `.is-pressed`） | headless 无真实触摸/悬停，只验证了 click 链路；`.is-pressed` 的视觉反馈未验 |
| iOS Safari / Android Chrome 兼容性 | 本机仅有 Edge（Chromium 内核），未覆盖 WebKit |
| 视觉层（配色对比度、`--depth` 阴影层次、族徽卡排版） | 无对比度/视觉回归工具，仅截图留档未做量化判定 |
| 洗牌「原子回滚」分支（洗牌后无解 → 退还次数） | 未构造出洗牌后无解的局面，该分支未执行 |
| 「免费复活」全链路 | 仅确认按钮存在与 `freeReviveUsed` 逻辑，未在失败态点复活验证快照回滚 |
| 教学第 3 步 → `endTutorial()` 完整闭环 | 已验到第 3 步（mask 解除、高亮目标牌），但「消除一次后自动结束教学」这一步未跑到（需再打一组三消） |
| 320×568 下 7 格槽位的纵向可见性 | 该视口页面需滚动（`scrollHeight≈1345`），槽位在滚动后可见，未做「不滚动即可见」判定 |
| 生成耗时 / 性能（120ms 墙钟预算是否生效） | 未做性能剖析；观察到的 ~1.9s 为「点击→首帧」含固定等待，不代表生成耗时 |

---

## 附：关键证据截图

| 文件 | 内容 |
|---|---|
| `02-L1-start.png` | L1 开局 9 张、3 张可点（亮）、6 张压暗 |
| `03-L1-result.png` | L1 三星通关结算 |
| `07-entry-L5-375x667.png` | **S2-1** 进入 L5 时盘面顶部被导航栏压住 |
| `08-L5-scrolled-top.png` | 上滑后同一盘面完整可见 |
| `11-overflow-375.png` | S3-5 的 375 溢出采样时刻 |
| `12-edge-slot7.png` | EDGE-2 第 7 张凑三消后仍在牌局中 |
| `16-bench.png` | EDGE-4 槽内 2 张 + 暂存 1 张未误消 |
| `20-bench-branch.png` | **S2-2** 盘面清空 + 暂存 3 张 → 弹出「槽位满了」 |
