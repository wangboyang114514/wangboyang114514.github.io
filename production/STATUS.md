# 游戏模块升级 · 状态交接

> 最后更新：2026-11-07 23:10
> 本次目标：重做「化学版羊了个羊」（games/chinese/sheep_game.html），解决"太简陋、画质差"
> 团队：chemworld-games（design-strategist / art-director / engineering-lead，当前均为 paused）

---

## 一、用户已拍板的决策（不要重开讨论）

| # | 决策点 | 结论 |
|---|---|---|
| 1 | 技术路线 | **纯 CSS/SVG**，不引 canvas / WebGL / 任何 CDN 库 |
| 2 | 样式落地 | **方案 B**：新增 `games/game-theme.css` 作为 6 页共享主题层 |
| 3 | 金属配色 | 把 `metal`（80/118，67.8%）按原子序数拆 **metal-d / metal-f / metal-p** 三个**视觉**亚族 |
| 4 | 浅底族 | 非金属 / 稀有气体采用**浅底深字**（极性反转），为过 4.5:1 |
| 5 | L6 难度 | `nd: 8 → 7`，实测胜率 44.4%（原 nd=8 为 32.2%） |
| 6 | 设备策略 | 手机优先（375 基准）+ 桌面适配（1024+） |

---

## 二、已完成产物

| 文件 | 行数 | 状态 |
|---|---:|---|
| `design/gdd/sheep-v2-gdd.md` | 1835 | ✅ 设计定稿，A1–A6 断言、六关配置、状态机、i18n 全量 |
| `docs/visual/game-visual-spec.md` | 1039 | ✅ 视觉规范 v1.2，9 族配色、景深、动效、无障碍矩阵 |
| `docs/visual/tiles-demo.html` | 1234 | ✅ 自包含视觉样板，双击可开 |
| `games/game-theme.css` | 581 | ✅ 主题层，选择器全部带前缀，零全局污染 |
| `games/chinese/sheep_game.html` | 2249 | ⚠️ **已重写但未验收**（见第三节） |

所有产物**均未提交 git**。`git status` 显示：
- ` M games/chinese/sheep_game.html`
- `?? design/` `?? docs/` `?? games/game-theme.css`

---

## 三、⚠️ 唯一未闭环项：新版游戏页未经验收

`games/chinese/sheep_game.html` 于 23:07 写入（2249 行 / 100KB），但 engineering-lead 在自验阶段被中断，**没有提交验收报告**。

### 已由主理人独立验过的（可信）

- 内联 JS 单块 69,269 字符，`node --check` **语法通过**（退出码 0）
- 已正确引用 `../game-theme.css` 与 `../../elements-zh.js`
- **旧的内联 `const elements` 数组已删除**（不会与全局冲突白屏）
- `data-blocked` 通过 `dataset.blocked` 赋值（第 1156 行），与主题文件契约一致
- A1–A6 六条断言均已实现（第 649–690 行附近）
- `cw_sheep_v2_progress` 存储键已接入
- `data-tier` 已使用

### 尚未验证（明天必须做）

1. **浏览器实跑**：是否有控制台报错、L1 能否完整通关
2. **点被遮挡牌**是否只抖动、不消耗步数/槽位
3. **375px 下是否横向滚动**，槽位 7 格是否完整可见
4. 六关断言的实跑结果 + 每族成员数的 console.table
5. 生成器在 500 次随机发牌下的 DFS 通过率与平均重掷次数
6. `covers()` 判定算出的起始可点数：L1 应为 3、L5 应为 12

---

## 四、明天第一步（按顺序）

1. **让 engineering-lead 续跑自验**（它上下文还在，见第六节）
   - 重点补：浏览器实跑 + Node 测试脚本的三个数字 + 六关每族成员数打印
2. **派 quality-lead 做烟雾测试**，按 GDD §7.2 的 15 条 EDGE 用例，重点这 5 条：
   - 槽位 6 格时第 7 张恰好凑三消 → 必须判成功，不能判负
   - 一次点击同时两组三消 → 必须 `while` 清完，`chain += 2`
   - 同元素与同族同时满足 → 优先同元素，不重复清除
   - 点被遮挡牌的露出部分 → 只抖动，零消耗
   - 洗牌后不可解 → 原子回滚并退还次数，不留 ghost 牌
3. **中文版通过后才动英文版** `games/english/sheep_game.html`（本轮明确未碰）
4. 全部通过后再考虑 git 提交

---

## 五、必须守住的硬约束（防止明天又踩回去）

- **不用 `filter: brightness()` 做遮挡态**：会把符号文字一起压暗，9 族里 4 族对比度跌破 4.5
- **遮挡态不能用"明度"通道**：明度已被 `data-tier`（族内档位）占用，再用会自相抵消
- **遮挡判定用整数几何**：`A.layer>B.layer && |Δgx|<2 && |Δgy|<2`，不用 `getBoundingClientRect()`
- **被遮挡的牌保持可点击**：点中→抖动+高亮遮挡者，零消耗。`pointer-events:none` 只用于三处（飞出动画 / 教学强制 / 结算遮罩）
- **先消除，后判负**，消除用 `while` 不用 `if`
- **遮罩色不得抽成 CSS 变量放进多层 `background-image`**：Chromium 会把整条 background-image 判无效，瓦片变透明。现方案已改为 `inset box-shadow`
- **`data-fam` 走视觉亚族，匹配逻辑走原始 `category`**：两条通路混用会让 30 个金属元素变成可互换桶，主导策略重现
- **断言 A6（任一白名单族成员数 ≠ 3）**：不报错不崩溃，只让关卡悄悄变成 90–100% 胜率。每条族构成必须人工核对

---

## 六、团队状态

三位成员均为 **paused（alive）**，可继续，不要重建：

| 成员 | agent_id | 已完成 |
|---|---|---|
| design-strategist | `design-strategist@chemworld-games` | T1 全部收口（含 R18 并入） |
| art-director | `art-director@chemworld-games` | T2 全部收口（含 theme.css） |
| engineering-lead | `engineering-lead@chemworld-games` | T3 代码已写，**自验未完成** |

继续方式：对 engineering-lead 发 SendMessage，让它接着补自验即可（它保留着上下文）。
