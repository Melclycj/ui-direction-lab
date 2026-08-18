# 配色池(Batch 1 视觉参考 · token-level palettes)— 可选 base-case

> ⚠️ **这是兜底,不是菜单。** 仅在想不出更好配色时拿来当起点或参照,**不要求**从里面选。
> 用在 `prototyping-ui-directions` 的 **Batch 1(视觉方向)**——决定 palette 那一轴(配 `style-pool.md` 风格 / `font-pool.md` 字体)。
> 与 font-pool 同源:SaaS 行的 hex 是**真的从 brand `DESIGN.md` 抄下来的**(见 `reference-sources.md` 桶 A),不是编的。

## Schema(每条配色带什么)
`vibe` · **bg / ink(分层) / 单一 accent / border-rule** 四件套(token 级,可直接进 `--token-color-*`)· **范本锚** · **provenance** · `notes`。

**provenance 三标**(同 font-pool)
- `web-verified` — 从真实 fetch 的 DESIGN.md / 官网坐实(库的**主干**应是这一档:外部可信标准)。
- `your-skill` — 本 lab 跑过、锁进 `testbed/chassis/` 的真配色(**内部验证记号,不等于"外部行业标准"**,见 §成长)。
- `memory-candidate` — 记忆里的 canonical 名字,落地前再核。

## Taste 守则(不被本池豁免)
- **单一 accent**(`taste-skill` 硬规则):产品 UI 一套配色只挂 **一个** accent,不堆多彩。
- **无紫 LILA**:避免 lilac/violet 当 accent。⚠️ 见 §1 Stripe 的注意。
- **bg/ink 走分层**(ink / ink-mid / ink-soft),靠明度阶建层级,不靠多色。
- **从 chassis 的 color token 取值**,页面只引用 `var(--token-color-*)`。

---

## §1 · SaaS / developer-tool —— ★ SEEDED FROM REAL `DESIGN.md`(sample vibe)

**颗粒度:10 个 brand 收敛成 2 个 sub-vibe,brand 作行内锚(真 hex)。**

| sub-vibe | bg / canvas | ink(分层) | 单一 accent(择一) | 范本锚(真 hex) | provenance |
|---|---|---|---|---|---|
| **Light SaaS** | `#ffffff` / soft `#fafafa`·`#f6f9fc` | 近黑 `#171717`–`#0d253d` · body `#4d4d4d` | 蓝 `#0070f3` / 翡翠 `#3ecf8e` / 薄荷 `#00d4a4` / 橙 `#ff8800`(e2b,+ 黑 CTA `#000`) | Vercel(蓝)· Supabase(翡翠)· Mintlify(薄荷)· e2b(橙/dev-infra,亮默认 bg `#fafafa`·ink `#000`/`#333`/`#666`/`#999`;暗变体 `#000`·`#141414`·`#1a1a1a`) | `web-verified`(e2b=Playwright 实测 token) |
| **Dark dev-tool** | 近黑 `#07080a`–`#010102` · surface 抬一档 | 浅 `#f4f4f6`–`#f7f8f8` | lime `#c2ef4e` / 白胶囊 / 暖白 `#f7f5f0` | Sentry(lime)· Raycast(白)· Warp(暖白 on `#2b2622`) | `web-verified` |

- **taste tension(紫)**:Stripe `#533afd` / Notion `#5645d4` / Linear `#5e6ad2` 都偏紫 → 撞"无紫 LILA",**逆向其结构、换非紫 accent**(蓝/绿/lime)再用。
- Vercel 的 mesh 渐变(cyan `#50e3c2`/violet `#7928ca`/pink `#ff0080`)= **营销专用**,不当产品 accent。

---

## §2 · 其余 vibe —— 部分已被本 lab 坐实(`your-skill`,真 chassis 配色)

| vibe | bg / surface | ink(分层) | 单一 accent | border/rule | 范本锚 | provenance |
|---|---|---|---|---|---|---|
| **新野兽派 / acid·dark** | bg `#14150f` · surface `#1e2016` | paper `#f1efe2` · 2nd `#b7b5a4` · 3rd `#82806f` | acid lime **`#bfe800`**(暗用 `#93b300`) | 亮边 `#f1efe2`(硬投影) | 本 lab **Northway** | `your-skill`(`chassis/northway-brutalist`) |
| **有机 / linen(quiet-luxury)** | linen `#f7f5f0` · warm `#f0ede7` | ink `#1a1a17` · mid `#5c5b57` · soft `#9a9890` | terracotta **`#b06a4f`**(交互用 `#8f5133`/hover `#7a4328`) | rule `#d8d5cf` | 本 lab **Grove** | `your-skill`(`chassis/grove-linen`) |
| **深色科技 SaaS(neon)** | 深底(near-black) | 纸字分层 | 单一 neon(青/绿/品红择一) | 暗 hairline | 开发者工具暗色站 | `memory-candidate` |
| **暖 AI(AI-product)** | 奶油 `#faf9f5` / 暖白 `#f5f5f5`(或暗底 `#0a0a0a`) | 暖近黑 `#141413`–`#0c0a09` | 暖珊瑚/橙 `#cc785c`·`#ff7759`·`#fa520f`·`#ff7a17`(择一) | 暖 hairline | Claude · Mistral · xAI · Cohere(Runway=无 accent,照片驱动) | `web-verified` |
| **奢侈汽车 / haute(dark)** | 纯黑 `#000000` / 近黑 `#181818` | 白 `#ffffff` · 2nd `#c9c9c9` | 金属**择一**:金 `#FFC000`(Lambo)/ Rosso 红 `#da291c`(Ferrari)/ 冰蓝 `#c3d9f3`(Bugatti)——**极克制,只点 CTA/mark** | 暗 hairline `#2a2a2a` | Lamborghini(金)· Ferrari(红)· Bugatti(冰蓝) | `web-verified`(DESIGN.md)+ reverse-eng + `do-not-copy` |
| **极简 / 编辑奢侈(light cream)** | 奶油 `#faf9f6` / 象牙 `#f4f1ea`(或纯白 `#ffffff`) | 炭黑 `#1d1d1f` · body `#4d4d4d` · fine `#8a8a8a` | **择一**:冷蓝 `#0066cc`(Apple)/ **无 accent · 纯 mono**(Aesop)/ 暖橙 `#f37021`(Hermès) | 暖 hairline `#e6e2d9` | Apple(蓝)· Aesop(无 accent)· Hermès(橙) | Apple=`web-verified`;Aesop/Hermès=`memory-candidate`(闭源逆向)+ `do-not-copy` |
| **工业信号 / field(light-industrial)** | 米白 `#ffffff` · 反相分区炭 `#191919` | 炭黑 `#191919` · 2nd `#35373c` · soft `#999999` | 信号黄 **`#fffa00`**(站上另有 `#00ffa2` 绿 / `#ff1aac` 品红,**择一不并用**) | 硬边 + clip-path 斜切分区 | 👁 终末地 | `web-verified`(生产 CSS hash 核对)+ `do-not-copy` |
| **宇宙档案 / midnight-serif** | 白 `#ffffff` 为主 · 午夜近黑 `#000000` 反相段 | 近黑 `#000000` · 2nd `#b8b8b8` · soft `#858585` | 水青 **`#46f6e6`**(全站仅 4 处,极克制) | 细 hairline + 圆形轨道描边 | 👁 来自星尘 | `web-verified`(生产 CSS hash 核对)+ `do-not-copy` |
| **明快协作 / playful-blue** | 白 `#ffffff` · 蓝场 `#3994ff` | 深蓝 `#3a5dad` · 更深 `#0050af` · soft `#5a5a5a` | 蓝 **`#3994ff`**(要暖 accent 则黄 `#ffcc1a` / 橙 `#f7a120` **择一**) | 粗描边 + 错位硬阴影 | 👁 POPUCOM | `web-verified`(生产 CSS hash 核对)+ `do-not-copy` |

> luxury 档已 seed(2026-07-01,同 font-pool):**奢侈汽车/haute**(黑+单金属;Ferrari/Lamborghini/Bugatti = `web-verified`)+ **极简/编辑奢侈**(奶油+炭黑;Apple=web-verified / Aesop·Hermès=闭源逆向 `do-not-copy`,标"诠释非复制")。taste:金属色**点到为止**、无紫(冰蓝 `#c3d9f3` 是冷蓝非紫)、冷蓝 `#0066cc` 与暖橙 `#f37021` **择一不并用**。consumer:automotive token 🤖 我 parse / Aesop·Hermès live 视觉 👁 你看(只给 URL)。

> 游戏 IP 档已 seed(2026-08-04,同 style-pool 三行):**工业信号/field** · **宇宙档案/midnight-serif** · **明快协作/playful-blue**。
> 证据 = 直接下载其**公开生产样式表**做 **SHA-256 逐字节核对**(与上游 2026-07 快照完全一致),hex 是数出来的;权利 = `do-not-copy`,标"诠释非复制"。
> **两处 taste tension(本池不豁免)**:① POPUCOM 原站蓝+黄+橙**三色并用**,撞「单一 accent」硬规则 → 照 §1 Stripe 的处理法**逆向其结构、只留一个 accent** 再用。② 来自星尘站上另有紫 `#925dff`,撞「无紫 LILA」→ **不取**,水青 `#46f6e6` 是唯一 accent。
> consumer:三家均为闭源商业游戏 IP,live 视觉 👁 你看(只给 URL);logo / 角色美术 / 自有字体一律不取,只借配色语法。

## 用法提示
- Batch 1 换 palette 时,换的是**明度气质 + accent 色相**(浅 linen vs 暗 acid vs 白 SaaS),不是同一套换 accent。
- 选了就把四件套写进 chassis 的 `--token-color-*`,页面只引用 token。
- **配色工具**:**Coolors**(coolors.co,🤝)生成/微调 → 导出 hex 进 token · **Colorable**(colorable.jxnblk.com,🤖)查对比度/a11y(或我代码直接算)。**灵感优先用本池**,不逛 Color Hunt 那类灵感墙(低效)。

## 成长(human-gated,见 `reference-sources.md` §5)
- **能数据化提议**:配色像字体一样,我能从真 DESIGN.md / 官网**抄出真 hex 提候选**(`web-verified`)。
- **但入库仍人为把关**:库的价值是**外部可信标准**;我 surface 候选(锚 + hex + URL),**你定加不加**。
- **自产配色不当 standard**:跑出来好看的页/选中的 LEAD ≠ 行业范本——`your-skill` 是内部验证记号,不应主导本池(`Northway`/`Grove` 仅作"自家用过、可参照"留底)。
