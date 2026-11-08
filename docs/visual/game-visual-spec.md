# 游戏视觉规格 · Game Visual Specification

**版本** v1.2 · 状态：已获批（方案 B / metal 拆亚族 / 浅底极性，见 §10）  
**作者** 林绘澄（美术方向 / 视觉规范）
**适用范围** `games/chinese/*`、`games/english/*` 下三个化学游戏（羊了个羊 / 连连看 / 化学冒险）
**技术前提** 纯 CSS + SVG，无 canvas / WebGL / 外部库 / 外部字体；手机优先（375px 基准），断点 375 / 768 / 1024
**关联** 待 T1《GDD》落定后复核牌堆行数与槽位数量

---

## 0. 一句话方向

> **把「元素周期表」做成一副有重量的实体牌**——深色玻璃牌桌、按元素族语言上色的元素牌、靠遮挡压暗与位移读出牌堆厚度；不引入任何新设计语言，只把站点已有的 7 个族色真正用起来。

### 0.1 设计原则（五条，冲突时按序取舍）

| # | 原则 | 含义 |
|---|---|---|
| 1 | **族色即身份** | 瓦片颜色只表达「元素族」，不表达状态。状态（选中/遮挡/消除）靠明度、位移、描边强度表达 |
| 2 | **不新增视觉语言** | 色相全部来自 `styles.css` 已有的族色；新增的只是明度档与描边，不发明新的品牌色 |
| 3 | **颜色不是唯一通道** | 每个族同时有「色相 + 明度档 + 纹样」三重编码，且元素符号始终可读 |
| 4 | **一次重排，不逐帧** | 所有动效用 `transition` / `@keyframes`，JS 只写一次变量 |
| 5 | **先适配拇指，再适配眼睛** | 375px 下的触控目标与纵向可见性优先于桌面观感 |

---

## 1. 现状诊断（基于实测，非推测）

| 问题 | 实测证据 | 本档解法 |
|---|---|---|
| 视觉割裂 | `games/*/sheep_game.html` L42 `.game-container` 用 `rgba(255,255,255,0.8)`；`styles.css` L20 `--glass-bg: rgba(30,41,59,.7)` | §3 牌桌改用站点玻璃变量族 |
| 瓦片无信息 | `game-cell` 全白底 + `color: var(--primary-color)` + `font-size:1.2rem`，无原子序数层级 | §3.4 三级排版 + §2 族色填充 |
| 分类色闲置 | `styles.css` L519–552 / L653–679 定义了 7 个族色，游戏页 0 引用 | §2 全量启用 |
| 移动端挤压 | `.game-grid{grid-template-columns:repeat(7,1fr);gap:8px}` 固定 7 列（羊了个羊页）；`elements.html` 侧 8 列 + `gap:10px` | §3.1 响应式列数 + 尺寸公式 |
| hub 用 emoji | `games/chinese/games.html` L218/225/232 `🧪 🐑 🎮` | §7 三个内联 SVG |

### 1.1 ⚠️ 关键发现：站点族色**不足以**支撑瓦片游戏

对 `elements-zh.js` 全量解析（118 个元素）得到真实分布：

| 站点 category | 元素数 | 占比 |
|---|---:|---:|
| `metal` | **80** | **67.8%** |
| `nonmetal` | 7 | 5.9% |
| `noble-gas` | 7 | 5.9% |
| `alkali-metal` | 6 | 5.1% |
| `alkaline-earth-metal` | 6 | 5.1% |
| `metalloid` | 6 | 5.1% |
| `halogen` | 6 | 5.1% |

**直接按 7 个 category 上色 → 牌堆里 2/3 的牌是同一种青色，比现在的全白更糟。**

**解法：保留 7 个站点 category 不变（不动 `elements-zh.js` 数据），仅在视觉层把 `metal` 按原子序数拆成 3 个亚族。** 拆分完全由 `atomicNumber` 推导，无需新增化学数据，且是化学上标准的过渡 / 后过渡 / 镧锕三分：

```
metal-f  镧系·锕系    Z 57–71, 89–103          30 个
metal-d  过渡金属      Z 21–30, 39–48, 72–80, 104–112   38 个
metal-p  后过渡金属    Z 13, 31, 49, 50, 81–84, 113–116  12 个
```

**已验证为精确穷尽分区：30 + 38 + 12 = 80，118 个元素 0 个未分配。**

```js
// 供 engineering-lead 直接使用的族映射函数
function familyOf(el) {                    // el = { category, atomicNumber }
  const n = el.atomicNumber;
  if (el.category !== 'metal') return el.category;      // 6 个非金属桶原样返回
  if ((n >= 57 && n <= 71) || (n >= 89 && n <= 103))            return 'metal-f';
  if ((n >= 21 && n <= 30) || (n >= 39 && n <= 48) ||
      (n >= 72 && n <= 80) || (n >= 104 && n <= 112))           return 'metal-d';
  return 'metal-p';
}
```

---

## 2. 配色体系

### 2.1 家族总表（9 族）

源色取 `styles.css` L519–552 原值（`metal-p` / `metal-f` 为新增派生色，色相落点见备注）。

**深底族（`--fam-fg: #f8fafc` 白字）**

| 家族 | 中文名 | 源色（来自 styles.css） | 瓦片顶 `--fam-top` | 瓦片底 `--fam-bot` | 描边 `--fam-edge` | 文字 | 纹样 |
|---|---|---|---|---|---|---|---|
| `alkali-metal` | 碱金属 | `#ff6b6b` | `#990000` | `#570000` | `#ff6666` | `#f8fafc` | 无 |
| `alkaline-earth-metal` | 碱土金属 | `#4ecdc4` | `#1b5f5b` | `#103835` | `#88ddd7` | `#f8fafc` | 无 |
| `metal-d` | 过渡金属 | `#45b7d1` | `#1e6a7b` | `#113c46` | `#84d0e1` | `#f8fafc` | 横线 |
| `metalloid` | 类金属 | `#96ceb4` | `#367356` | `#1f4232` | `#97ceb4` | `#f8fafc` | 45° 斜线 |
| `halogen` | 卤素 | `#dda0dd` | `#692669` | `#3c163c` | `#d78ed7` | `#f8fafc` | 无 |
| `metal-p` | 后过渡金属 | ⚠️ 新增 `#e08a3c` | `#7b4514` | `#46270b` | `#eab07b` | `#f8fafc` | 135° 斜线 |
| `metal-f` | 镧系·锕系 | ⚠️ 新增 `#7c8bf0` | `#10208e` | `#091352` | `#7685ef` | `#f8fafc` | 无 |

**浅底族（`--fam-fg: #0f172a` 深字）** —— 见 §2.3 为什么必须这样做

| 家族 | 中文名 | 源色 | 瓦片顶 | 瓦片底 | 描边 | 文字 | 纹样 |
|---|---|---|---|---|---|---|---|
| `nonmetal` | 非金属 | `#ffeaa7` | `#ffdd70` | `#ffd13d` | `#e0ab00` | `#0f172a` | 无 |
| `noble-gas` | 稀有气体 | `#98d8c8` | `#90d5c4` | `#6bc7b0` | `#3ea389` | `#0f172a` | 点阵 |

**新增色相落点说明（为什么是这两个色相）**

- `metal-p #e08a3c`：H 27°（青铜/琥珀）。站点色盘 0°–46° 之间只有 `#ffeaa7`（H 46°，极浅低饱和），青铜与其在明度上拉开 40+，可区分。语义上 Al/Ga/In/Sn/Pb/Bi 的「后过渡金属」质感贴合青铜。
- `metal-f #7c8bf0`：H 232°（靛蓝）。补上站点色盘在 200°–280° 之间的空档；与 `--accent-color #06b6d4`(H 189°) 相距 43°，与 `#dda0dd`(H 288°) 相距 56°，不冲突。

### 2.1.1 ⚠️ 防错铁律：亚族只许上色，严禁进逻辑

> **本节是硬性禁令，engineering-lead 与任何后续维护者都必须遵守。**

`metal-d` / `metal-f` / `metal-p` 是**纯视觉取色用**的拆分（`familyOf()`，§1.1），**绝不允许出现在任何游戏逻辑里**——包括匹配规则、同族三连判定、`category` 字段的读写、任何 `=== 'metal-d'` 之类的比较。

原因（design-strategist 确认，GDD §4.5 / 风险 R13）：

- 同族三连规则里，`metal` 作为**整体**被排除参与（它占 80/118）。
- 若实现时误把 `metal-d` 当 `category` 使用，Z 21–30 / 39–48 / 72–80 约 **30 个元素**会变成一个可任意互换的巨桶 → Fe+Cu+Au 任意凑三连 → 主导策略被触发，关卡平衡直接崩塌。
- 反向同理：也不要用 `metal-d` 做任何「是金属」的判断（应判断 `category === 'metal'`）。

**一句话记忆：`metal-d/f/p` 只活在 CSS 属性里（`data-fam` 取色），不活在 JS 逻辑里。** `game-theme.css` 顶部已加同款警示注释。

### 2.2 对比度核验（逐项实测，非估算）

计算方式：WCAG 相对亮度公式，`(L1+0.05)/(L2+0.05)`。牌桌面色 `#131e33`。

| 家族 | 文字↔瓦片顶 | 文字↔瓦片底 | 填充↔牌桌 | 描边↔牌桌 | 判定 |
|---|---:|---:|---:|---:|---|
| `alkali-metal` | 8.52 | 14.28 | 1.87 | 5.82 | ✅ |
| `alkaline-earth-metal` | 7.08 | 12.25 | 2.25 | 10.60 | ✅ |
| `metal-d` | 5.90 | 11.41 | 2.70 | 9.59 | ✅ |
| `metal-p` | 7.42 | 12.90 | 2.14 | 8.72 | ✅ |
| `metal-f` | 12.40 | 16.36 | 1.28 | 5.05 | ✅ |
| `metalloid` | 5.36 | 10.66 | 2.97 | 9.36 | ✅ |
| `halogen` | 9.64 | 14.63 | 1.65 | 6.93 | ✅ |
| `nonmetal` | 13.46 | 12.28 | 11.45 | 7.92 | ✅ |
| `noble-gas` | 10.63 | 8.86 | 8.26 | 5.40 | ✅ |

- **文字对比度最低 5.36**（`metalloid`），高于 WCAG AA 要求的 4.5 ✅
- **边界识别**：以 `max(填充↔牌桌, 描边↔牌桌)` 计，最低 **5.05**（`metal-f`），高于非文本 3:1 要求 ✅
  说明：深底族的填充与深色牌桌本身对比不足 3:1，**瓦片轮廓由 2px 描边承担**，这是合规读法，也是本方案的设计意图——描边是瓦片的"边缘线"，不是装饰。

### 2.3 两档明度极性（关键设计决策）

初版方案「全部深底白字」在 `nonmetal`（3.69）与 `noble-gas`（3.84）上对比度不达标——**黄色系在任意明度下亮度都偏高**。把明度压低到能过 4.5 会让非金属变成暗橄榄、稀有气体变成暗泥绿，既难看又与 `metal-p` 青铜色混淆。

因此引入 **polarity（极性）** 概念，作为家族的固有属性，不随状态变化：

- `polarity: dark` → 深瓦片 + 白字（7 族）
- `polarity: light` → 浅瓦片 + 深字（`nonmetal`、`noble-gas`）

**副作用是正向的**：这两个浅色族把拥挤的青绿带做了纵向分离（见 §2.4），且牌堆里出现 2 个浅色族会显著提升整盘的色彩层次，避免"一片深蓝"。

### 2.4 青绿拥挤带风险与缓解

站点色盘在 H 147°–192° 之间堆了 4 个族：`metalloid`(152°) / `noble-gas`(165°) / `alkaline-earth-metal`(176°) / `metal-d`(191°)。同屏出现 3 个以上时色相几乎不可分。

**三重缓解，全部必须落地：**

1. **明度硬分层**：`alkaline-earth` L24% -- `metal-d` L30% -- `metalloid` L33% -- `noble-gas` L70%（浅色）
2. **纹样差异化**：`metalloid` 45° 斜线、`metal-d` 横线、`alkaline-earth` 无纹样、`noble-gas` 点阵
3. **选池约束（交 T1/GDD 决策）**：**每关元素池最多包含 3 个青绿带族中的一个**。这是最有效的手段——只要不同屏，问题不存在

> `nonmetal` 与 `metal-p` 的"黄/青铜"接近性也纳入同一条约束：二者不同屏。

### 2.5 纹样层（非颜色区分通道）

全部用零成本 `background-image` 叠加，不用伪元素（`::before` 已被遮挡遮罩占用，`::after` 被爆裂环占用）：

```css
.tile[data-fam="metalloid"] {
  background-image:
    repeating-linear-gradient(45deg, transparent 0 5px, rgba(255,255,255,.11) 5px 6px),
    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
}
.tile[data-fam="metal-d"] {
  background-image:
    repeating-linear-gradient(180deg, transparent 0 6px, rgba(255,255,255,.10) 6px 7px),
    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
}
.tile[data-fam="metal-p"] {
  background-image:
    repeating-linear-gradient(135deg, transparent 0 5px, rgba(255,255,255,.10) 5px 6px),
    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
}
.tile[data-fam="noble-gas"] {
  background-image:
    radial-gradient(rgba(15,23,42,.22) 1px, transparent 1.4px),
    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
  background-size: 7px 7px, 100% 100%;
}
```

### 2.6 族内明度档（R18 裁决：采用 B，逐 symbol 明度档）

> **v1.2 新增**。背景：L2 牌池 Fe/Cu/Zn 同属 `metal-d`、L5 的 F/Cl/Br/I 同属 `halogen`，按 §2.1 取色后 L2 整盘只有 2 种填充色、L5 只有紫+红两色。design-strategist 以风险 R18 提请裁决。

**裁决：B —— 补族内区分，但只用「明度档」这一种手段，且逐 symbol 计算。**

理由：

- **A（接受同色）的 measurable 失败**：L5 的 6 个符号里 4 个是紫色。玩家核心循环是「扫视找第 3 张同类牌」，当 60% 的盘面同色相时，颜色对扫视的增益归零，玩家每步要逐个读符号——这不是「信息」，是噪声，而且正是用户最初「所有瓦片长得一模一样」抱怨的换相重演。
- **不用纹样做族内区分**：55px 下纹样与符号抢空间，且 118 个 symbol 逐个设计纹样不现实；纹样保持**族粒度**（§2.5，色盲通道），不承担族内区分。
- **不用色相偏移**：同族内变色相会破坏「族=色」的身份通道（§0 原则 1）。
- **明度档是唯一干净的手段**：同族内明度阶梯既保留「一眼看出是一族」，又让相邻 symbol 可辨。

**机制（engineering-lead 照抄）：**

1. 关卡初始化时，把该关牌池内**同族的 distinct symbol 按原子序数升序**排序，依次赋 `data-tier = 0,1,2,3`。
2. **同一 symbol 的所有副本必须同档**——同元素三消靠「两张牌长得完全一样」配对，档位若逐副本随机，游戏直接坏掉。
3. `data-pol` **逐 symbol 写入**（与 `--fam-tier` 同一个赋值函数里写）。实测所有档位都不跨极性（下表），但仍按 symbol 写以满足 GDD 的验收断言。

**档距（逐族按对比度余量封顶，不是统一值）：**

| 族 | 极性 | 档距 (HSL-L/档) | T0→T3 活动态对比度 | 遮挡态对比度 | 判定 |
|---|---|---:|---|---:|---|
| `alkali-metal` | 深 | +4% | 8.5 / 7.2 / 6.1 / 5.2 | 14.9→12.4 | ✅ |
| `alkaline-earth-metal` | 深 | +2% | 7.1 / 6.3 / 5.7 / 5.1 | 12.7→11.0 | ✅ |
| `metal-d` | 深 | +2% | 5.9 / 5.3 / 4.9 / **4.42** | 11.8→10.2 | ⚠️ 仅 T0–T2 |
| `metal-p` | 深 | +3% | 7.4 / 6.5 / 5.6 / 5.0 | 13.2→11.1 | ✅ |
| `metal-f` | 深 | +4% | 12.4 / 11.2 / 10.1 / 9.1 | 15.9→14.3 | ✅ |
| `metalloid` | 深 | +1% | 5.4 / 5.1 / 4.9 / 4.7 | 11.3→10.5 | ✅ |
| `halogen` | 深 | +4% | 9.6 / 8.3 / 7.1 / 6.2 | 14.6→12.2 | ✅ |
| `nonmetal` | 浅 | +4% | 13.5 / 14.0 / 14.6 / 15.2 | 14.8→15.7 | ✅（提亮更安全） |
| `noble-gas` | 浅 | +4% | 10.6 / 11.5 / 12.3 / 13.2 | 13.5→14.8 | ✅ |

**硬约束（进关卡生成规则，GDD §5.8 已同步）：**

- 每关同族 distinct symbol 数 **≤ 4**；且 **`metal-d` ≤ 3**（`metal-d` T3 = 4.42 是全表唯一低于 4.5 的组合）。
- 现行六关全部满足（见下表），L3–L6 新池已按此验证。

**六关档位分配实测（T0 最深 → T3 最浅）：**

| 关 | 牌池 → 档位 | 全关最差对比度 |
|---|---|---:|
| L1 | Fe=T0, Cu=T1, O=T0 | 5.35 |
| L2 | Fe=T0, Cu=T1, Zn=T2, Al=T0 | 4.86 |
| L3 | F=T0, Cl=T1, Na=T0, K=T1, Fe=T0 | 5.90 |
| L4 | F=T0, Cl=T1, Na=T0, K=T1, Fe=T0, Cu=T1 | 5.35 |
| L5 | F=T0, Cl=T1, Br=T2, I=T3, Na=T0, K=T1 | 6.15 |
| L6 | F=T0, Cl=T1, Br=T2, I=T3, He=T0, Ne=T1, Al=T0 | 6.15 |

> L2 是全表最紧的一关（4.86），但它渲染在 72px 档（三样全开，含中文名 铁/铜/锌），符号辨识有冗余通道；55px 档（L4/L6）用到的族档位对比度都 ≥ 5.35。

**CSS 落地**：`games/game-theme.css` §2b（36 条 `[data-fam][data-tier]` 规则，覆盖 `--f-l` / `--f-bl`）。

---

## 3. 瓦片视觉规格

### 3.1 尺寸计算公式

> **v1.1 更新**：GDD（`design/gdd/sheep-v2-gdd.md` §4.1）已定稿 TILE 公式，本节以其为准。我此前的纯 CSS `cqi` 方案降级为备选。

**正解（GDD §4.1，JS 注入 `boardW`）**：

```css
--tile: clamp(44px, (100vw - 48px) / var(--boardW, 6), 72px);
```

- `boardW` 由 JS 按关卡形状注入（GDD §4.1：`boardW = (maxGx + 2) / 2`，注意是 `+2` 不是 `+1`）
- 三档实测：320px→**45px** / 375px（boardW=6 最宽盘）→**54.2px** / 768px→封顶 **72px**
- 因为 `--tile` 不含百分比，**天然避开下面的循环依赖坑**

**⚠️ 已实测踩坑，勿重蹈**：不要用 `100%` 推导 `--tile`。`--tile` 会同时被瓦片的 `width`、`height` 和牌堆的 `min-height` 消费，形成**循环依赖**——`height: var(--tile)` 里的百分比要靠包含块高度解算，而包含块高度又来自 `min-height: calc(... var(--tile) ...)`，两者互相依赖，Chromium 下整条 `calc` 失效，结果牌堆塌成 0 高、瓦片全部消失。本档在无头 Edge 实测复现过，`calc()` 与 `min()` 都试过，均失败。

**备选：若哪天想去掉 boardW 注入，用容器查询单位 `cqi`**（确定长度，无循环）：

```css
.board-shell { container-type: inline-size; padding: var(--pad-board); }
.pile {
  --tile: min(var(--tile-max, 92px),
              calc((100cqi - (var(--cols) - 1) * var(--gap)) / var(--cols)));
}
```

**瓦片定位**（沿用 GDD §S3 的半格坐标，gutter 由 `inset:2px` 提供，不引入 gap 变量）：

```css
.sg-tile { position: absolute;
  left: calc(var(--gx) * var(--tile) / 2);
  top:  calc(var(--gy) * var(--tile) / 2);
  width: var(--tile); height: var(--tile);
  z-index: calc(var(--layer) * 100 + var(--gy));
  touch-action: manipulation; }
.sg-tile__face { position: absolute; inset: 2px; }   /* 视觉卡片，--face = --tile - 4px */
```

**字号基准用 `--face`，不是 `--tile`**（face 比 tile 小 4px，44px 瓦片的可视区只有 40px）：

```css
.sg-tile__face { --face: calc(var(--tile) - 4px); }
```

> GDD 公式在桌面含滚动条宽（~15px）的偏差，因 1024+ 封顶 72px 而无实际影响，不必处理。

### 3.2 牌位坐标（半格栅格）

羊了个羊的牌堆不是纯网格，需要半格错位。用乘数变量而非像素（见 §3.1 的 `left` / `top` 公式）：

- `--px` / `--py` 取**整数或 `.5` 步进**：`0, 0.5, 1, 1.5 ...`
- 乘的是 `(var(--tile) + var(--gap))`，所以半格偏移自动随瓦片缩放
- `--rows` 由 engineering 按关卡牌堆实际占用的行数写入（含半格），供 `min-height` 使用

层叠容器已在 §3.1：`.pile{position:relative; isolation:isolate}`。

### 3.3 形状与表面

| 属性 | 值 | 说明 |
|---|---|---|
| 圆角 | `calc(var(--tile) * 0.22)` | 52px→11.4px / 85px→18.7px。比站点 `--border-radius:16px` 略紧，瓦片才不像药丸 |
| 描边宽度 | `max(1px, calc(var(--tile) * 0.028))` | 52px→1.5px / 85px→2.4px。保证高分屏也不糊 |
| 描边色 | `rgba(var(--fam-rgb), calc(0.92 - var(--depth) * 0.14))` | `--depth` 越深描边越淡 |
| 底色 | `linear-gradient(168deg, var(--fam-top) 0%, var(--fam-bot) 100%)` | 168° 近垂直微斜，模拟顶光 |
| 内高光 | `inset 0 1px 0 rgba(255,255,255, calc(0.22 * var(--lift)))` | 顶边 1px 亮线，玻璃厚度感 |
| 外投影 | `0 calc(2px + var(--depth) * 2.5px) calc(6px + var(--depth) * 3px) rgba(2,6,16, calc(0.34 + var(--depth) * 0.07))` | 越深的牌投影越长越散 |
| 族色辉光 | `0 0 calc(20px * var(--lift)) rgba(var(--fam-rgb), calc(0.42 * var(--lift)))` | 只有顶牌发光 |

### 3.4 排版层级（基于 `--face`；v1.2 基准上修为 55px）

> **v1.2 更新**：design-strategist 实算六关牌堆最大仅 4 行厚，`--tile` 实际区间是 **55–72px**（L4/L6 最宽盘 55px；L1/L2 能到 72px 上限；只有 320px 端会掉到 45px）。因此**设计基准从 44px 上修到 55px**——信息取舍比原判断宽松。

三级，字号相对 `--face = var(--tile) - 4px`（face 是真正的可视区）：

| 层级 | 内容 | 字号 | 位置 | 样式 |
|---|---|---|---|---|
| L1 主视觉 | 元素符号 `Fe` | `calc(var(--face) * 0.42)` | 居中 | `font-weight:800; letter-spacing:-.02em; line-height:1` |
| L2 次级 | 原子序数 `26` | `calc(var(--face) * 0.20)` | 左上，`padding:calc(var(--face)*0.11)` | `font-weight:600; opacity:.72; letter-spacing:.02em` |
| L3 辅助 | 元素名 `铁` / `Iron` | `calc(var(--face) * 0.17)` | 底部居中 | `font-weight:500; opacity:.80` |

**实测字号（六关实际落点）：**

| tile | face | 落在哪 | L1 符号 | L2 序号 | L3 名称 |
|---:|---:|---|---:|---:|---|
| 45px（320px 端） | 41px | 极端窄屏 | **17.2px** | 8.2px | 7.0px → 隐藏 |
| **55px（L4/L6，最宽盘）** | 51px | **设计基准** | **21.4px** | 10.2px | 8.7px → 隐藏 |
| 65px（L3/L5） | 61px | 宽松档 | 25.6px | 12.2px | 10.4px → 隐藏 |
| 72px（L1/L2 与 768px+） | 68px | 封顶 | 28.6px | 13.6px | 11.6px → 显示 |

**⚠️ 不要加「分类色条」。** 本方案的瓦片填充本身就是分类色（9 族色即填充色），再叠一条 4px 色条会吃掉 10% 高度却不传递新信息。色条只在"填充不是分类色"时才有必要（例如 GDD 曾考虑的 PNG 深底卡，见 §4.8）。

**分档显示规则（design-strategist 已并入 GDD §3.3）：**

| tile | 显示内容 | 落到的关卡 |
|---|---|---|
| <48px（320px 端） | 仅符号 | 窄屏兜底 |
| 48–63px | 符号 + 序号 | **L4 / L6（55px）** |
| ≥64px | 符号 + 序号 + 名称 | L1/L2/L3/L5 与桌面 |

```css
@media (max-width: 360px)  { .sg-tile__num  { display: none } }   /* 45px 档 */
@media (max-width: 480px)  { .sg-tile__name { display: none } }   /* 55–61px 档 */
```

> **44px 信息取舍的定稿答案（design-strategist 问的两项之二）**：三样里**放弃分类色条**（填充即分类色，色条零信息增量），保留符号 + 序号；元素名降到 ≥64px 才显示，<64px 时由 `aria-label` 承载完整信息（GDD §6.7「视觉降级不影响语义」）。在 55px 实际基准下，符号 21.4px + 序号 10.2px 无任何拥挤。
> 元素名在移动端改由点击后的元素卡弹层（GDD S-03）承担——这也符合"学习功能"的产品目标。

匹配可读性核对：同元素三消靠符号（21.4px @55px 基准，远超可读线），同族三消靠填充色（9 族色差 + 族内明度档 §2.6 + 纹样 §2.5 三重编码）。

字体：`font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", "Noto Sans SC", sans-serif`（**系统字体栈，不引 CDN**）。符号与序号建议加 `font-variant-numeric: tabular-nums` 防跳动。

### 3.5 ⚠️ 竖屏高度预算（会直接压死设计的硬约束）

> **v1.2 更新**：design-strategist 按六关实算，牌堆最厚 L5/L6 = 4 行 @72px = 320px，占 450px 预算的 71%，**距 6 行上限还有 2 行余量**。GDD §4.1 已同步（包围盒公式 `(maxGy + 2) / 2`，此前 GDD 写 `+1` 是错的）。本节结论维持有效且更宽松。

375×667 实测预算：

| 区块 | 高度 |
|---|---:|
| 导航栏（`.navbar` 含 `top:40px`） | 64px |
| 紧凑 HUD（得分/步数/重开，替换当前 `<h1>` + `.game-info`） | 52px |
| 槽位轨（含标题） | 61px |
| 间距 / 留白 | 32px |
| **固定占用合计** | **209px** |
| **剩余给牌堆** | **450px** |
| 每行高（55 + 8，55px 基准） | 63px |
| **可容纳行数** | **7 行**（六关最大 4 行，余量 3 行） |

**结论与要求：**

1. **375px 下牌堆 ≤ 6 行**为硬约束（GDD 已写「想加难度加 `nd` 不加层数」）；现行六关最大 4 行，天然满足。
2. 当前页面的 `<h1>`（`margin:2rem 0` + 2rem 字号 ≈ 112px）与 `.element-info` 卡片（≈120px）**必须在移动端移出首屏**：`<h1>` 由紧凑 HUD 取代；`.element-info` 移到槽位轨下方、可折叠。
3. **槽位口径（主理人裁决，已统一）**：槽位条左右**出血到屏幕边缘，水平 padding 归零**。375px 下：
   - 出血口径：`(375 − 3(边框) − 6×5(gap)) / 7 ≈ 48.9px`
   - 保守口径（design-strategist 的 16px 页边距 + 5px gap）：`(375 − 32 − 30) / 7 = 44.7px`
   - 两种口径都 **≥ 44px → Apple HIG 判定翻转为满足**（此前 38.1px 是按 24px 页边距 + 4px gap 算的旧口径，作废）。

| 视口 | 槽位（出血口径） | 判定 |
|---|---:|---|
| 320px | 40.9px | ✅ WCAG 2.2 SC 2.5.8 / 接近 HIG |
| 375px | **48.9px** | ✅ 两者 |
| 430px | 57.3px | ✅ 两者 |

> **槽位的定性（v1.2 定稿）**：槽位是**纯展示容器，零触控交互**——GDD v2 已删除「点槽位撤回」（那是一个无限免费撤销漏洞：每个已填充槽位上的红点一点就把元素拿回，7 格上限形同虚设，也是现版「深度不足」的第二根因）。撤牌能力改由道具「移出」承担（每关 1 次，有次数限制）。因此本节不再需要 44px 命中区扩展方案，旧 `.slot-remove::after` 建议作废；`game-theme.css` 的 `.sg-slot` 已写 `pointer-events: none`。

---

## 4. 遮挡景深方案 ★ 本档重点

纯 CSS 无法知道"谁遮住了谁"，但**知道也不需要逐帧算**。策略：JS 只在状态变化时写一次 CSS 变量，CSS 负责全部表现。

### 4.1 三层景深词汇（按性价比排序）

| 层 | 手段 | 成本 | 作用 |
|---|---|---|---|
| **L1 遮挡遮罩（主）** | `::before` 半透明压暗 | 极低（仅合成 opacity） | 一眼看出"这张牌被压住了" |
| **L2 位移 + 缩放** | `transform: translateY() scale()` 由 `--depth` 推导 | 极低（GPU） | 牌堆有物理厚度 |
| **L3 描边 + 外发光** | 顶牌描边满亮 + 族色辉光 | 低 | 顶牌"浮起来"、可点 |

**明确不推荐 `filter: brightness()/blur()` 作为主手段**：每张牌一个 `filter` 会各建一个合成层，40 张牌在低端 Android 上掉帧。`blur()` 尤其贵。若要视觉更"糯"，作为**可选增强**放在 `.quality-high` 类下，只在桌面开启（见 §4.4）。

### 4.2 JS 契约（只有这些，没有逐帧）

```js
// 覆盖关系变化时调用一次
function paintDepth(tile, { coverCount, depth, z }) {
  tile.style.setProperty('--cover', coverCount);  // 0..3  压住它的牌数
  tile.style.setProperty('--depth', depth);       // 0..N  距堆顶的层数，0 = 顶层
  tile.style.setProperty('--z', z);               // 1..N  堆叠序
}
```

**这两个量不需要精确物理含义**，只需要单调：`depth` 越大 = 埋得越深。工程侧可用"该牌上方重叠牌数"直接赋值。

### 4.3 CSS 实现（可直接落地）

```css
.tile {
  /* 由 JS 写入，给默认值以防未初始化 */
  --cover: 0;
  --depth: 0;
  --z: 1;

  --lift:  calc(1 - min(var(--depth), 4) / 4);         /* 1 → 0，封顶 4 层 */
  --scrim: calc(min(var(--cover), 3) * 0.18 + 0.34 * min(var(--cover), 1));
  /* cover=0 → 0；cover=1 → .52；cover=2 → .70；cover=3 → .88 */

  position: absolute;
  left: calc(var(--px) * (var(--tile) + var(--gap)));
  top:  calc(var(--py) * (var(--tile) + var(--gap)));
  width: var(--tile);
  height: var(--tile);
  z-index: var(--z);

  border-radius: calc(var(--tile) * 0.22);
  border: max(1px, calc(var(--tile) * 0.028)) solid
          rgba(var(--fam-rgb), calc(0.92 - var(--depth) * 0.14));
  background-image: linear-gradient(168deg, var(--fam-top), var(--fam-bot));
  color: var(--fam-fg);

  transform: translateY(calc(var(--depth) * 2.5px))
             scale(calc(1 - var(--depth) * 0.008));

  box-shadow:
    0 calc(2px + var(--depth) * 2.5px) calc(6px + var(--depth) * 3px)
      rgba(2, 6, 16, calc(0.34 + var(--depth) * 0.07)),
    0 0 calc(20px * var(--lift))
      rgba(var(--fam-rgb), calc(0.42 * var(--lift))),
    inset 0 1px 0 rgba(255, 255, 255, calc(0.22 * var(--lift)));

  transition:
    transform  180ms cubic-bezier(.4, 0, .2, 1),
    box-shadow 180ms cubic-bezier(.4, 0, .2, 1),
    border-color 180ms cubic-bezier(.4, 0, .2, 1);
}

/* L1 遮挡遮罩 —— 主景深手段 */
.tile::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(180deg, rgba(7, 11, 20, .34), rgba(7, 11, 20, .58));
  opacity: var(--occlude);
  transition: opacity 180ms cubic-bezier(.4, 0, .2, 1);
  pointer-events: none;
}
```

### 4.4 具体数值表（给 engineering-lead 的速查）

| `--depth` | `--lift` | 位移 Y | 缩放 | 描边不透明度 | 投影 blur | 辉光 blur | 观感 |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0（顶牌） | 1.00 | 0px | 1.000 | 0.92 | 6px | 20px | 浮起、发光、可点 |
| 1 | 0.75 | 2.5px | 0.992 | 0.78 | 9px | 15px | 略退后 |
| 2 | 0.50 | 5.0px | 0.984 | 0.64 | 12px | 10px | 明显在下 |
| 3 | 0.25 | 7.5px | 0.976 | 0.50 | 15px | 5px | 深层 |
| ≥4 | 0.00 | 10.0px+ | 0.968 | 0.36 | 18px+ | 0px | 沉底、无光 |

配合 `--cover` 遮罩：`0 → 0` / `1 → .52` / `2 → .70` / `3 → .88`（超过 3 一律按 3 算，避免全黑）。

### 4.5 z-index 分层约定

> **v1.1 更新**：GDD §S3 定稿了 `z-index: calc(var(--layer) * 100 + var(--gy))`。6 层 × maxGy≈12 → 最高 ~712，会闯进下表旧的「500+ 模态框」段。

**解法：`.sg-board { isolation: isolate }`**，让牌堆内部自成层叠上下文，内部值再大也不与外部模态框/导航栏竞争。

| 作用域 | 区间 | 用途 |
|---|---|---|
| **`.sg-board` 内部**（isolate 后） | `calc(var(--layer)*100 + var(--gy))` | 瓦片（GDD 定稿，不动） |
| | `1000` | 选中上浮态 `.is-selected` |
| | `1100` | 入槽飞行克隆 `.fly-token` |
| | `1200` | 爆裂特效层 |
| | `1300` | 提示高亮 `blockersOf` |
| **外部（root）** | `100` | 站点 `.navbar`（styles.css L214，勿动） |
| | `500+` | 模态框 / HUD（在 `.sg-board` 之外） |

> **必须写 `isolation: isolate`**：不写的话，`z-index ≤ 99` 的瓦片会被 `.navbar{z-index:100}` 盖住——滚动时瓦片钻到导航栏下面，这是现有 `sheep_game.html` 用 `position:sticky` 时的真实隐患。

### 4.7 遮挡态与可点态（GDD §3.3 引用此节）★

> **v1.1 新增**。GDD 原基线 `filter: brightness(.62) saturate(.7)` **实测不可用**，原因与替代方案如下。
>
> **v1.2 实现升级（以本段为准）**：实现层发现了比「多层 background + 字面量遮罩」更好的等价方案——**遮挡遮罩走 `inset box-shadow`**。CSS 规定 inset box-shadow 绘制在 background 之上、**文字内容之下**，遮罩语义与 background 第一层完全等价，但：
> 1. `background-image` 保持**单层**（HSL 分量 var + 档位覆盖），彻底绕开下面的 Chromium 多层 var() 失效坑；
> 2. 遮罩 α 可以用 `rgba(..., var(--occlude))` 驱动，**可点 ↔ 遮挡能平滑过渡**（多层 background 版做不到 α 过渡，只能瞬切）；
> 3. 与深度掩埋（`--depth` 驱动的连续 inset 遮罩）共用同一机制。
>
> box-shadow 五段按 index 对齐（0 外投影 / 1 辉光 / 2 深度掩埋 inset / 3 遮挡遮罩 inset / 4 内高光或内凹），保证 transition 可插值。**已在无头 Edge 用像素采样验证：遮挡态填充压暗至预期值（理论 #195561 vs 实测 #195564）、符号保持全亮白。** `games/game-theme.css` §3/§4 为权威实现；下方多层 background 方案保留作为理解与降级参考（`tiles-demo.html` 用的就是它，渲染效果一致）。

**为什么 filter 不行**：filter 作用在 `.sg-tile__face` 上会把**符号文字一起压暗**。实测 9 族遮挡态对比度：

| 族 | 可点态 | GDD filter 方案 | 背景 layer 方案（本节） |
|---|---:|---:|---:|
| `metalloid` | 5.36 | **3.72 ❌** | 9.46 ✅ |
| `metal-d` | 5.90 | **3.96 ❌** | 10.02 ✅ |
| `alkaline-earth-metal` | 7.08 | **4.42 ❌** | 11.14 ✅ |
| `noble-gas` | 10.63 | 4.59 ✅ | 13.48 ✅ |
| 其余 5 族 | 5.9–13.5 | 4.55–6.02 | 11.61–15.11 |

filter 方案 **9 族里 4 族跌破 4.5**；背景 layer 方案 **9 族全部 ≥9.46**（只暗化底色，文字保持全亮）。

**第二个实测结论：填充明度/饱和度都扛不起「在下面」这个信号。** α 从 0.42 扫到 0.70，暗色族 ΔL 最高仅 0.021（`metal-f` #10208e 本身 L≈0.02 已近黑，压不动）；饱和度降幅最低 0.025（`metalloid` 本身 S 仅 0.361）。**数学上此路不通。**

**所以「一眼看出在下面」的主力是描边 + 辉光**（实测描边↔牌桌对比度：可点 5.05–9.59 → 遮挡 1.52–1.95，**Δ 3.5–7.6，全通道最强**），填充压暗只做辅助。

**⚠️ 暗化层必须放在 `background-image` 第一层，不能用 `::before`。** 定位伪元素的绘制顺序高于 inline content，一样会把符号压暗；`background` 永远在 content 之下。这是 filter 与 `::before` 两条路共同的坑。

**⚠️⚠️ 已实测踩坑：不要把遮罩色抽成 `var()` 再塞进多层 `background-image`。** 即写成

```css
/* ❌ 这样写 Chromium 会把整条 background-image 判为无效 */
.sg-tile[data-pol="dark"] .sg-tile__face { --scrim: rgba(11,17,30,.55); }
.sg-tile[data-blocked="true"] .sg-tile__face {
  background-image: linear-gradient(var(--scrim), var(--scrim)),
                    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
}
```

实测（无头 Edge + DOM 探针读 computed value）：**单层 `background-image` 里用 `var(--scrim)` 正常；一旦变成多层（后面再接族色渐变），整条 `background-image` 的 computed value 变成 `none`**，瓦片直接透明。把 `var(--scrim)` 换成字面量 `rgba(11,17,30,.55)` 立即恢复。改名、换层序、拆层数都无效——只要「多层 + 其中一层用 var 引遮罩色」就必挂。

成因推测与 `--scrim` 在本档被两处复用有关（§4.3 的 `::before { opacity: var(--scrim) }` 用的是 0–0.88 的**数字**，此处用的是**颜色**），但不论机理，**结论按"不要这么写"执行**。因此本节的遮罩色直接写死在两条极性规则里，不经 var() 中转。

**连带教训：同一个自定义属性名不要承载两种语义。** 本档已把 `::before` 用的不透明度改名为 `--occlude`，遮挡态遮罩色不再叫 `--scrim`。engineering 实现时请保持这个命名区分。

```css
/* ── 可点态：亮描边 + 族色辉光（「浮起来」的主力，不是阴影）── */
.sg-tile[data-blocked="false"] .sg-tile__face {
  border: max(1px, calc(var(--tile) * .028)) solid rgba(var(--fam-rgb), .92);
  background-image: linear-gradient(168deg, var(--fam-top), var(--fam-bot));
  box-shadow:
    0 2px 6px rgba(2, 6, 16, .34),
    0 0 20px rgba(var(--fam-rgb), .42),        /* 族色辉光 */
    inset 0 1px 0 rgba(255, 255, 255, .22);
}

/* ── 遮挡态：零 filter。遮罩色按极性直接写死，不经 var() 中转（原因见上）── */
.sg-tile[data-blocked="true"][data-pol="dark"] .sg-tile__face {
  background-image:
    linear-gradient(rgba(11, 17, 30, .55), rgba(11, 17, 30, .55)),   /* 暗化层，在文字之下 */
    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
}
.sg-tile[data-blocked="true"][data-pol="light"] .sg-tile__face {
  background-image:
    linear-gradient(rgba(241, 245, 249, .55), rgba(241, 245, 249, .55)),  /* 洗白层 */
    linear-gradient(168deg, var(--fam-top), var(--fam-bot));
}
.sg-tile[data-blocked="true"] .sg-tile__face {
  border-color: rgba(var(--fam-rgb), .26);                /* 0.92 → 0.26，最强信号 */
  box-shadow:
    inset 0 2px 6px rgba(0, 0, 0, .45),                   /* 内凹 */
    0 1px 3px rgba(2, 6, 16, .28);                        /* 投影缩短 */
  transform: scale(.94);
}
/* 上层牌投下的柔和阴影（GDD 要的 ::after） */
.sg-tile[data-blocked="true"] .sg-tile__face::after {
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  background: linear-gradient(180deg, rgba(0, 0, 0, .30), rgba(0, 0, 0, 0) 55%);
  pointer-events: none;
}
.sg-tile[data-blocked="false"]:hover .sg-tile__face { transform: translateY(-3px) scale(1.02); }
```

**★ 定稿参数速查表（design-strategist 问的两项之一，GDD §3.3 直接引用此表）**

| 参数 | 可点态 `blocked=false` | 遮挡态 `blocked=true` | 通道强度排序 |
|---|---|---|---|
| 遮罩 α（`--occlude`） | 0 | **0.55**（深底暗化 `rgba(11,17,30)` / 浅底洗白 `rgba(241,245,249)`，极性由 `data-pol` 决定） | 辅助 |
| 描边不透明度 | `rgba(var(--f-rgb), .92)` | **`.26`**（塌缩） | **最强**（Δ 3.5–7.6） |
| 族色辉光 | `0 0 20px rgba(f,.42)` | **0**（移除） | 第二 |
| 缩放 | 1（hover 时 1.02） | **0.94** | 第三 |
| 位移 | 0（hover `-3px`） | 0 | — |
| 内高光/内凹 | `inset 0 1px 0 rgba(255,255,255,.22)` | `inset 0 2px 6px rgba(0,0,0,.45)` | 第四 |
| 外投影 | `0 2px 6px rgba(2,6,16,.34)` | `0 1px 3px rgba(2,6,16,.28)`（变短变近 = 被压） | 第五 |
| 过渡 | 全部 `180ms cubic-bezier(.4,0,.2,1)` | 同左 | — |

**遮挡态遮罩后实测底色与对比度**（α=0.55）：

| 族 | 遮挡后底色 | 文字对比度 | 判定 |
|---|---|---:|---|
| `alkali-metal` | `#5d070d` | 13.33 | ✅ |
| `metal-d` | `#164554` | 10.02 | ✅ |
| `metal-f` | `#0e1a5f` | 15.11 | ✅ |
| `metalloid` | `#244a3e` | 9.46 | ✅ |
| `nonmetal` | `#f7eabb`（洗白） | 14.86 | ✅ |
| `noble-gas` | `#c5e7e1`（洗白） | 13.48 | ✅ |

**性能**：零 filter。遮挡态只多一层 background gradient + border-color/box-shadow 变化，走合成器。

### 4.8 图片资产分工（否决 PNG 上盘面）

实测 `photo/elements/` 全部 118 张 PNG：**800×1000 竖版卡（比例 0.800），背景为不透明深藏青（约 `#1e2540`），非透明底**。三个硬伤：

1. **竖版 vs 方形瓦片**：`object-fit: cover` 会裁掉上下各 100px，顶部族色条（约 8px/1000 高）与底部族名（约 60px/1000）**全部被裁掉**；`contain` 则左右留藏青边，浪费 20% 宽度。
2. **族色只剩一条 4px 顶条**：图里族色只出现在顶条、序号、底部族名三处，44px 下三者都缩到不可读。用 PNG 反而**失去**分类色可读性——而分类色是同族三消（GDD §4.5）的核心信号。
3. **118 张共用同一深藏青底**：44px 下整盘是一片相同的深藏青方块 + 一个小白字，正是用户最初抱怨的「所有瓦片长得一模一样」，只是从白色换成藏青。

**结论：**

| 场景 | 用什么 |
|---|---|
| **盘面瓦片** | 纯 CSS 绘制（族色填充 + 符号 + 序号），零图片请求 |
| **S-03 元素卡弹层 / S-04 族徽卡 / S-06 胜利页** | `photo/elements/{ZZZ}_{Sym}.png`（800×1000 本就是为放大看信息设计的） |
| **21 张 `.jpg` 实物照** | 仅 S-03/S-06 作奖励性展示（与 GDD 点 4 一致） |

### 4.9 可选增强（已作废）

> **v1.1 修订**：§4.7 定稿遮挡态为**零 filter** 方案后，本节原 `filter: brightness()/blur()` 增强**整体作废**——它在遮挡态会把符号一起压暗（实测 4/9 族跌破 4.5，见 §9.2），且收益（0.06 级明度差）远低于 §4.7 的描边/辉光通道。
>
> 若确需更"糯"的质感，唯一安全的做法是把 filter 加在**不含文字的独立层**上（例如 `.sg-tile__face` 的一个纯背景子元素），但仍需先实测帧率。默认不启用。

---

## 5. 动效规范

全部 `transition` / `@keyframes`，**JS 只写一次变量**。缓动曲线统一从下表取，不临时发明。

### 5.1 缓动曲线库

| 名称 | 值 | 用途 |
|---|---|---|
| `--ease-out-soft` | `cubic-bezier(.4, 0, .2, 1)` | 通用状态过渡（与站点 `--transition` 一致） |
| `--ease-out-quint` | `cubic-bezier(.22, .61, .36, 1)` | 位移类（入槽飞行） |
| `--ease-spring` | `cubic-bezier(.34, 1.56, .64, 1)` | 需要回弹的（选中上浮） |
| `--ease-expand` | `cubic-bezier(.16, 1, .3, 1)` | 扩散类（爆裂环） |
| `--ease-shake` | `cubic-bezier(.36, .07, .19, .97)` | 震屏 |

### 5.2 逐条规格

| # | 动效 | 时长 | 缓动 | 触发条件 | 实现要点 |
|---|---|---|---|---|---|
| A1 | **选中上浮** | 120ms | `--ease-spring` | `pointerdown` 命中顶层瓦片 | `transform: translateY(-8px) scale(1.06)`；`z-index:150`；辉光 `blur` 20→26px |
| A2 | **选中按下回弹** | 90ms | `--ease-out-soft` | `pointerup` / `pointercancel` | 回到 `translateY(-4px) scale(1.02)` 停留至入槽 |
| A3 | **入槽位移（飞行克隆）** | 260ms | `--ease-out-quint` | 瓦片离堆、进槽 | 见 §5.3，JS 写 `--dx/--dy/--ds` 一次 |
| A4 | **入槽落位** | 140ms | `--ease-spring` | `animationend` 后真实瓦片挂进槽 | `scale(.88) → 1` |
| A5 | **三消爆裂** | 340ms | `--ease-out-soft` | 同类计数达 3 | `scale(1) → 1.18 → .55`，`opacity → 0` |
| A6 | **爆裂扩散环** | 420ms | `--ease-expand` | 同 A5，`::after` | `scale(.72) → 2.05`，`opacity .95 → 0` |
| A7 | **爆裂光晕** | 460ms | `--ease-out-soft` | 同 A5，`box-shadow` 扩散 | `0 0 0 0 rgba(fam,.5) → 0 0 0 26px rgba(fam,0)` |
| A8 | **连锁震屏** | 260ms | `--ease-shake` | 一次消除后 400ms 内再次消除 | 见 §5.4，强度由 `--shake` 控制 |
| A9 | **槽位告急（6/7）** | 900ms 循环 | `ease-in-out` | 槽位占用 = 6 | 描边脉动 + 红晕，**不闪整块** |
| A10 | **槽位满（7/7 死局）** | 380ms 循环 | `ease-in-out` | 占用 = 7 | 同 A9 但频率 ×2.4，配一次 A8 `--shake:6` |
| A11 | **槽位入位高亮** | 200ms | `--ease-out-soft` | 每次进槽 | 该槽 `border-color` 提到 `rgba(var(--fam-rgb),.9)` 后回落 |
| A12 | **牌堆首屏入场** | 420ms | `--ease-out-quint` | 开局 | 逐张 `translateY(12px) opacity 0 → 0/1`，`animation-delay: calc(var(--i) * 22ms)`，上限 20 张 |

### 5.3 入槽飞行（关键实现，勿用 rAF）

```css
.fly-token {
  position: absolute;
  z-index: 260;
  width: var(--tile);
  height: var(--tile);
  border-radius: calc(var(--tile) * 0.22);
  background-image: linear-gradient(168deg, var(--fam-top), var(--fam-bot));
  border: max(1px, calc(var(--tile) * 0.028)) solid rgba(var(--fam-rgb), .92);
  box-shadow: 0 0 24px rgba(var(--fam-rgb), .5);
  pointer-events: none;
  --dx: 0px; --dy: 0px; --ds: 1;      /* JS 一次性写入 */
  animation: flyToSlot 260ms cubic-bezier(.22, .61, .36, 1) forwards;
}

@keyframes flyToSlot {
  0%   { transform: translate3d(0, 0, 0) scale(1); }
  55%  { transform: translate3d(calc(var(--dx) * .55), calc(var(--dy) * .55 - 14px), 0)
                    scale(calc((1 + var(--ds)) / 2)); }   /* 抛物弧抬升 14px */
  100% { transform: translate3d(var(--dx), var(--dy), 0) scale(var(--ds)); }
}
```

工程侧只需：算一次 `dx = slotRect.x - tileRect.x`、`dy`、`ds = slotW / tileW` → 写变量 → 插节点 → 监听 `animationend` 移除。**全程零逐帧 JS。**

### 5.4 三消爆裂 + 连锁震屏

```css
.tile.is-bursting {
  pointer-events: none;
  animation:
    tileBurst 340ms cubic-bezier(.4, 0, .2, 1) forwards,
    haloOut   460ms cubic-bezier(.4, 0, .2, 1) forwards;
}
@keyframes tileBurst {
  0%   { transform: scale(1); }
  35%  { transform: scale(1.18); }
  100% { transform: scale(.55); opacity: 0; }
}
@keyframes haloOut {
  0%   { box-shadow: 0 0 0 0 rgba(var(--fam-rgb), .50); }
  100% { box-shadow: 0 0 0 26px rgba(var(--fam-rgb), 0); }
}

/* 扩散环用 ::after（::before 已被遮挡遮罩占用） */
.tile.is-bursting::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  border: 2px solid rgba(var(--fam-rgb), .95);
  animation: ringOut 420ms cubic-bezier(.16, 1, .3, 1) forwards;
}
@keyframes ringOut {
  0%   { transform: scale(.72); opacity: .95; }
  100% { transform: scale(2.05); opacity: 0; }
}

/* 连锁震屏 */
.pile.is-shaking { animation: boardShake 260ms cubic-bezier(.36, .07, .19, .97); }
@keyframes boardShake {
  0%, 100% { transform: translate3d(0, 0, 0); }
  18% { transform: translate3d(calc(var(--shake) * -1px), calc(var(--shake) * .35px), 0); }
  38% { transform: translate3d(calc(var(--shake) * 1px),  calc(var(--shake) * -.30px), 0); }
  58% { transform: translate3d(calc(var(--shake) * -.7px), calc(var(--shake) * .22px), 0); }
  78% { transform: translate3d(calc(var(--shake) * .45px), 0, 0); }
}
```

`--shake` 强度表（JS 按连锁数写入，封顶 8 —— 超过会晕）：

| 连锁数 | 1 | 2 | 3 | 4+ |
|---|---:|---:|---:|---:|
| `--shake` | 2px | 4px | 6px | 8px |

### 5.5 槽位压力可视化（四档）

> **v1.1 扩展**：配合 GDD §S5 的槽位占用分档，从两档扩为四档。

⚠️ **琥珀色用 `#f5b942`，不要用 `#e08a3c`**——后者是 `metal-p` 的描边色，槽位边框用同色会让「槽位告急」和「青铜牌」混淆。

| 占用 | 状态 | 边框色 | 动效 |
|---:|---|---|---|
| 0–3 | 平静 | `rgba(20,184,166,.85)` 青 | 无 |
| 4–5 | 提醒 | `rgba(245,185,66,.85)` 琥珀 | 静态换色，无动画 |
| 6 | 告急 | `rgba(255,107,107,.9)` 琥珀红 | `warnPulse` 900ms 循环 |
| 7 | 死局 | `rgba(255,107,107,1)` 红 | `warnPulse` 380ms + 一次 A8 `--shake:6` |

```css
.slot-rail { --warn-c: rgba(20,184,166,.85); --warn-t: 0ms; }
.slot-rail[data-fill="4"], .slot-rail[data-fill="5"] { --warn-c: rgba(245,185,66,.85); }
.slot-rail[data-fill="6"] { --warn-c: rgba(255,107,107,.9); --warn-t: 900ms; }
.slot-rail[data-fill="7"] { --warn-c: rgba(255,107,107,1);  --warn-t: 380ms; }

.slot-rail {
  border: 1.5px solid var(--warn-c);
  transition: border-color 240ms cubic-bezier(.4, 0, .2, 1);
}
.slot-rail[data-fill="6"], .slot-rail[data-fill="7"] {
  animation: warnPulse var(--warn-t) ease-in-out infinite;
}
@keyframes warnPulse {
  0%, 100% { border-color: var(--warn-c);
             box-shadow: 0 0 10px rgba(255,107,107,.10); }
  50%      { border-color: var(--warn-c);
             box-shadow: 0 0 22px rgba(255,107,107,.30),
                         inset 0 0 18px rgba(255,107,107,.12); }
}

/* 最后一格独有脉冲（仅 6/7 时） */
.slot-rail[data-fill="6"] .slot:nth-child(7)::after {
  content: ''; position: absolute; inset: -3px;
  border-radius: inherit;
  border: 2px solid rgba(255, 107, 107, .9);
  opacity: 0;
  animation: lastSlot 900ms ease-out infinite;
}
@keyframes lastSlot {
  0%   { transform: scale(.9);  opacity: .9; }
  100% { transform: scale(1.25); opacity: 0; }
}
```

> **不要**用 `opacity` 闪整块槽位轨——那是光敏性癫痫风险源。只脉动 `border-color` 与 `box-shadow`。
> 4–5 格档**刻意不加动画**：它是"可逆的提醒"，一旦脉动就失去"还来得及"的语义，且动画越多告急档越不值钱。

---

## 6. 可访问性

### 6.1 分级

依据站点现有能力与游戏形态，定级 **Standard（WCAG 2.2 AA 对齐）**，并局部做到 Comprehensive（非颜色通道 + 减少动效）。

| 级别 | 是否达成 | 说明 |
|---|---|---|
| Basic | ✅ | 对比度、可聚焦、语义标签 |
| **Standard** | ✅ **目标** | 全量 AA + 减少动效 + 非颜色区分 |
| Comprehensive | ⚠️ 部分 | 色盲模拟已覆盖；屏幕阅读器全流程待 T3 评估 |
| Exemplary | ❌ | 不承诺（需音频提示 / 全键盘寻路，与纯 CSS 约束冲突） |

### 6.2 特性矩阵

| 特性 | 状态 | 规格 |
|---|---|---|
| 文字对比度 ≥ 4.5:1 | ✅ 已实测 | §2.2，最低 5.36 |
| 非文本对比度 ≥ 3:1 | ✅ 已实测 | 描边↔牌桌最低 5.05 |
| 触控目标 ≥ 44px | ✅ | 瓦片 52 / 55 / 85 / 92px |
| 触控目标 ≥ 24px（WCAG 2.5.8） | ✅ | 槽位 38px |
| 颜色不作唯一通道 | ✅ | 色相 + 明度档 + 纹样 + 元素符号三重 |
| `prefers-reduced-motion` | ✅ | §6.4 |
| 键盘可达 | ⚠️ 待 T3 | 瓦片须为 `<button>` 或 `tabindex="0"` + `role="button"`，`Enter/Space` 触发；焦点环 `outline:2px solid var(--secondary-color); outline-offset:2px` |
| 屏幕阅读器 | ⚠️ 待 T3 | 每张牌 `aria-label="原子序数 26，铁，过渡金属"`（中/英按语言） |
| 色盲模式 | ✅ | 见 §6.3 |
| 文本缩放 200% | ⚠️ 待 T3 | 字号全用 `calc(var(--tile) * k)`，随布局缩放不破；但 `--tile` 固定 px，200% 浏览器缩放下牌堆会溢出——建议允许牌堆纵向滚动而非裁切 |
| 高对比模式 | ✅ | `@media (prefers-contrast: more)` 描边不透明度 → 1，`--scrim` 上限 0.7 |

### 6.3 色盲安全性核验

对三型色觉障碍逐族核对（9 族 → 去重后的可辨组）：

| 类型 | 风险对 | 缓解（已内置） |
|---|---|---|
| **红色盲 Protanopia** | `alkali-metal`(#990000 红) ↔ `metal-p`(#7b4514 青铜) | 纹样不同（碱金属无纹 / 后过渡 135° 斜线）+ 明度差 L30 vs L28 接近 → **依赖纹样与元素符号** |
| **绿色盲 Deuteranopia** | `metalloid`(#367356) ↔ `metal-d`(#1e6a7b) ↔ `alkaline-earth`(#1b5f5b) | 纹样三者各不相同（45° 斜 / 横线 / 无）+ 明度 L33 / L30 / L24 + §2.4 选池约束 |
| **蓝黄色盲 Tritanopia** | `metal-f`(#10208e 靛) ↔ `noble-gas`(#90d5c4 浅青) | 极性相反（深底白字 / 浅底深字），明度差极大，安全 |
| Tritanopia | `nonmetal`(#ffdd70) ↔ `halogen`(#692669) | 明度差极大（L72 vs L28），安全 |

**结论：唯一需要靠纹样兜底的是 `alkali-metal` ↔ `metal-p`**（红/青铜在红色盲下接近）。因此 `metal-p` 的 135° 斜线纹样是**必须项，非可选**。

### 6.4 `prefers-reduced-motion` 降级

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
  .pile.is-shaking { animation: none !important; }        /* 震屏完全关掉 */
  .tile.is-bursting::after { display: none; }             /* 扩散环关掉 */

  /* 爆裂改为静态色闪：消除的牌立刻半透明 + 描边加粗，保留"消除了"的反馈 */
  .tile.is-bursting {
    animation: none !important;
    opacity: .28;
    border-width: max(2px, calc(var(--tile) * 0.05));
    border-color: rgba(var(--fam-rgb), 1);
  }
  /* 槽位告急改为静态红描边，不脉动 */
  .slot-rail.is-critical { animation: none !important; border-color: rgba(255,107,107,.9); }
  /* 入场不位移，只淡入 */
  .tile { animation: none !important; }
}
```

### 6.5 高对比模式

```css
@media (prefers-contrast: more) {
  .tile { border-color: rgba(var(--fam-rgb), 1); }
  .tile::before { opacity: calc(min(var(--cover), 1) * 0.7); }
  .slot-rail { border-color: var(--text-primary); }
}
```

---

## 7. hub 卡片图标方案（三个内联 SVG）

替换 `games/chinese/games.html` L218/225/232 与 `games/english/games.html` 对应处的 emoji。
统一规格：`viewBox="0 0 24 24"`、`fill="none"`、`stroke="currentColor"`、`stroke-width="1.6"`、`stroke-linecap="round"`、`stroke-linejoin="round"`、`aria-hidden="true"`、尺寸由 CSS 控制（建议 40×40，`color: var(--secondary-color)`）。**全部用 `currentColor`，自动继承主题切换。**

### 7.1 羊了个羊 → 「叠层元素牌」

**思路**：3 张错位圆角牌表现"牌堆"，最上层牌里嵌一个原子核 + 电子轨道，一眼同时读出「堆叠机制」与「化学」。

```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"
     stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
  <rect x="8.5" y="9.5" width="11" height="11" rx="3" opacity=".35"/>
  <rect x="5.8" y="6.4" width="12.6" height="12.6" rx="3.4" opacity=".6"/>
  <rect x="2.6" y="2.6" width="13.4" height="13.4" rx="3.6"/>
  <circle cx="9.3" cy="9.3" r="1.7"/>
  <ellipse cx="9.3" cy="9.3" rx="4.9" ry="1.85" transform="rotate(-32 9.3 9.3)"/>
</svg>
```

### 7.2 连连看 → 「配对连线」

**思路**：左上与右下两张同规格牌，中间一条直角折线相连、带箭头，第三张半透明牌在后景呼应"多组配对"。**刻意让两张牌等大**——强调"相同才可连"。

```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"
     stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
  <rect x="1.8" y="1.8" width="7.6" height="7.6" rx="2.2"/>
  <rect x="14.6" y="14.6" width="7.6" height="7.6" rx="2.2"/>
  <rect x="14.6" y="1.8" width="7.6" height="7.6" rx="2.2" opacity=".3"/>
  <path d="M5.6 9.6v2.6a1.6 1.6 0 0 0 1.6 1.6h5.3"/>
  <path d="M10.7 11.6 13 13.8l-2.3 2.2"/>
  <circle cx="5.6" cy="5.6" r="1.15"/>
  <circle cx="18.4" cy="18.4" r="1.15"/>
</svg>
```

### 7.3 化学冒险 → 「锥形瓶与路径」

**思路**：Erlenmeyer 瓶身（化学身份）+ 瓶内液面线 + 上升气泡（反应/进展）+ 瓶颈向右上延伸成一条虚线路径并带节点（冒险/闯关）。

```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"
     stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
  <path d="M9.2 2.6h5.6"/>
  <path d="M10.3 2.6v5.2L5.9 17.3A2.5 2.5 0 0 0 8.1 21h7.8a2.5 2.5 0 0 0 2.2-3.7L13.7 7.8V2.6"/>
  <path d="M7.6 14.2h8.8"/>
  <circle cx="10.2" cy="17.2" r=".95"/>
  <circle cx="13.9" cy="18.4" r=".62"/>
  <path d="M17.6 6.4h2.6M20.2 6.4v2.6" opacity=".55" stroke-dasharray="1.4 1.8"/>
  <circle cx="20.2" cy="6.4" r="1.5" opacity=".55"/>
</svg>
```

### 7.4 图标使用约束

```css
.game-icon { width: 40px; height: 40px; color: var(--secondary-color); }
.game-icon svg { width: 100%; height: 100%; display: block; }
.game-card:hover .game-icon { color: var(--accent-color); transition: color 200ms cubic-bezier(.4,0,.2,1); }
```

- **不加 `stroke-width` 动画**（hover 时改宽度会重排 SVG）
- 只改 `color`，靠 `currentColor` 全局联动
- `opacity` 用于区分前后景，不用 fill 色分档——换主题时不会失效

---

## 8. 样式落地位置（✅ 已批：方案 B，文件已交付）

**硬约束**：不得修改 `styles.css` 的全局变量（`:root` / `:root.light-mode`）。

> **v1.2 定稿**：用户已拍板方案 B，**`games/game-theme.css` 已创建并通过无头 Edge 渲染验证**（九族×档位、遮挡态、槽位压力四档全部按 375px 实测截图核对）。以下 A/B 对比保留作决策记录。

### 方案 A（备选，未采用）

全部写入各游戏页已有的 `<style>` 块。优点：零新增文件、零缓存问题、不污染站点。缺点：`chinese/` 与 `english/` 两份要同步维护。

### 方案 B（✅ 已采用）

新增 `games/game-theme.css`，由三个游戏页 `<link>` 引入。优点：单一真源，双语页共用，改动一处生效。缺点：新增一个 HTTP 请求（HTTP/2 下可忽略）。

**已交付文件的结构（T3 直接引用，勿在页面内重写这些规则）：**

| 段 | 内容 |
|---|---|
| 顶部注释 | 三条铁律（亚族禁入逻辑 / 遮罩走 inset shadow / 选择器纪律）+ JS 最小契约 |
| §1 | `.game-root` token：`--sg-board-bg`、`--tile`、5 条缓动、槽位告警色 |
| §2 | 9 族 HSL 分量 + 描边/文字/遮罩 RGB（族恒定）；§2b 36 条档位规则 |
| §3 | `.sg-board`（isolation:isolate）/ `.sg-tile`（半格坐标 + z-index 公式）/ `.sg-tile__face`（五段 box-shadow）+ 4 条纹样规则 |
| §4 | 可点态 / 遮挡态（inset box-shadow 遮罩，§4.7 v1.2） |
| §5 | 卡面排版三档 + 响应式隐藏 |
| §6 | A1–A12 动效类（全部 keyframes/transition，零 rAF） |
| §7 | 槽位压力四档 + 最后一格脉冲 + `.sg-slot`（纯展示） |
| §8 | `prefers-reduced-motion` / `prefers-contrast: more` 降级 |

**选择器纪律核对结果（主理人要求的报告项）：**

- 文件内**没有** `body`、`*`、`.navbar`、`.container`、`.game-card` 等站点已占用的全局选择器；全部选择器以 `.game-root` / `.sg-*` / `[data-fam=...]` 收窄。
- 自定义属性命名核对：`styles.css` 全部 22 个全局自定义属性（`--accent-color` / `--bg-color` / `--glass-*` / `--shadow-*` / `--text-*` / `--transition` 等）与本文件的 `--f-*` / `--sg-*` / `--tile` / `--face` / `--depth` / `--lift` / `--occlude` **零冲突**（逐一比对）。
- 游戏页接入要求：根容器加 `class="game-root"`，`<link rel="stylesheet" href="game-theme.css">`。

**JS 最小契约（完整说明见文件顶部注释）：** 瓦片写 `data-fam` / `data-tier` / `data-pol` / `data-blocked` + `--gx/--gy/--layer`；`.sg-tile__face` 写 `--depth`；`.sg-board` 写 `--boardW` 与 `--shake`；槽位轨写 `data-fill`。全部一次性写入，无逐帧。

---

## 9. 已知风险与诚实评估

纯 CSS 路线下，以下两点我认为**可能达不到预期**：

### 9.1 遮挡半格层叠的「视觉欺骗」会露馅

真·羊了个羊里，牌是**半格错位**堆叠的，一张牌能同时压住下面 2–4 张牌的不同角。纯 CSS 只能给整张牌一个统一的 `--scrim`，**做不出"这张牌左角被压、右角露出"的局部遮挡**。

- 影响：牌堆会看起来像"整片暗下去"，而不是"被别的牌实际压住"，纵深说服力打 7 折
- 缓解：`--scrim` 分档 + 位移 + 描边衰减三者叠加，已能到"可接受"；若要根治需要 `clip-path` 按覆盖矩形逐个裁切——**每个覆盖关系一个 clip-path，40 张牌的组合数会把 CSS 规则数炸掉**，不划算
- 建议：接受这 30% 的损失，把预算花在爆裂动效和族色上

### 9.2 `filter` 已实测否决（不只因为性能）

初版担忧的是性能（每张牌一个 `filter` 会各建一个合成层）。**v1.1 拿到了更硬的证据：filter 会把符号文字一起压暗，遮挡态对比度 9 族里 4 族跌破 4.5**（`metalloid` 3.72 / `metal-d` 3.96 / `alkaline-earth` 4.42 / `nonmetal` 1.23）。替代方案（§4.7 的背景 layer）9 族全部 ≥9.46，且零 filter、零合成层开销。此议题已关闭。

GDD v1 的 `filter: brightness(.62) saturate(.7)` 基线请以 §4.7 方案替换（已同步 design-strategist）。

### 9.3 浏览器基线：本方案依赖 3 个较新 CSS 特性

| 特性 | 用途 | Chrome/Edge | Safari | Firefox |
|---|---|---|---|---|
| `container-type` / `cqi` | 瓦片尺寸公式（§3.1） | 105+（2022.08） | 16.0+（2022.09） | 110+（2023.02） |
| `aspect-ratio` | 瓦片正方形、牌堆高度 | 88+（2021.01） | 15+（2021.09） | 89+（2021.06） |
| `min()` / `max()` | 尺寸封顶 | 79+ | 11.1+ | 75+ |

- 站点现状已依赖 `aspect-ratio`（`sheep_game.html` L115）与 `backdrop-filter`，基线本就不低
- `cqi` 是本方案**唯一新增**的较新依赖，已提供 `@supports not (container-type: inline-size)` 的 `100vw` 回退（§3.1），回退在移动端（手机优先的主场景）完全精确
- 若主理人要求兼容 2021 年前的 Android WebView，请告知，我改用「JS 在 resize 时写一次 `--tile` 像素值」的方案（仍无逐帧，只是多一个 resize 监听）

---

## 10. 待批准 / 待对齐事项

| # | 事项 | 需要谁 | 状态 |
|---|---|---|---|
| 1 | 样式落地方案 B（新增 `games/game-theme.css`） | 用户 / 主理人 | ✅ **已批，文件已交付** |
| 2 | `metal` 拆 3 亚族 | 用户 | ✅ 已批（统一命名 `metal-d`，全文 0 处 `metal-t`） |
| 3 | 「每关池最多 3 个青绿带族中取 1」的选池约束 | design-strategist (T1) | ✅ 已同步（GDD §5.8，六关实算全 PASS） |
| 4 | 375px 牌堆行数上限 6 | design-strategist (T1) | ✅ 已同步（六关最大 4 行，余量 2 行） |
| 5 | 槽位数 7 维持 + 槽位改纯展示（删 remove-btn） | design-strategist (T1) | ✅ 已同步（GDD §4.6，HIG 判定翻转为满足） |
| 6 | `nonmetal` / `noble-gas` 浅底深字极性反转 | 用户 | ✅ 已批 |
| 7 | 键盘可达与 `aria-label` 实现 | engineering-lead (T3) | ⏳ 待交接（`game-theme.css` 已预留 `aria-label` 语义说明，见 §5 分档注释） |
| 8 | **R18：L2/L5 整盘只有 2 种填充色 → 补族内明度档（逐 symbol）** | design-strategist 提请 | ✅ **本档裁决：B，见 §2.6**（硬约束：同族 ≤4 symbol 且 `metal-d` ≤3，六关全满足） |

---

*本文档所有色值、对比度、像素尺寸均由脚本实算得出（WCAG 相对亮度公式 + 实测容器几何），非目测估计。v1.2 新增的 36 组档位颜色、遮挡态全档对比度、槽位 48.9px 口径同样为实算值；`game-theme.css` 已通过无头 Edge 渲染 + 像素采样验证。*
