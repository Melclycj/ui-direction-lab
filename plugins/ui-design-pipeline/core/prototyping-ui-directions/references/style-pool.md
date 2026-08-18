# 视觉风格池(Batch 1 视觉参考)— 可选 base-case

> ⚠️ **这是兜底,不是菜单。** 仅在想不出更好方向时拿来当起点或参照,**不要求**从里面选;
> 优先提原创方向,把这些当"push past 的跳板"。用在 `prototyping-ui-directions` 的
> **Batch 1(视觉方向)**——决定 palette / 字体 / 布局 / 密度那一轴。

| 大类 | 风格 | 一句话 | 适合 / 倾向 | 范本锚 |
|---|---|---|---|---|
| 经典高级 | 极简高级风 | 大留白、克制、少即是多 | 高端品牌、咨询、奢侈品;浅色为主、低密度 | Vercel · ElevenLabs · Apple · Aesop |
| 经典高级 | Apple 式产品官网风 | 居中大图 + 短句 + 渐进揭示 | 产品发布页;明暗皆可、强 hero | Apple |
| 经典高级 | 瑞士国际主义风 | 严格网格、无衬线、左对齐、红黑 | 编辑/机构/作品集;高秩序、低装饰 | — |
| 产品工具 | Bento 卡片风 | 不规则方格拼贴(Apple 控制中心) | SaaS 功能区、dashboard;中密度 | Apple 控制中心 |
| 产品工具 | 深色科技 SaaS 风 | 深底 + 单一霓虹 accent + mono 数字 | 开发者工具、AI 产品;暗色、中高密度 | Linear · Raycast · Sentry · xAI · Warp · **e2b**(dev-infra;**营销页浅色 / app 控制台深色**[截图坐实]、橙 `#ff8800`=active·绿=LIVE 状态、IBM Plex Mono 大数字非霓虹——拓宽本行,非典型 dark-neon;控制台**构图**范本已移交 `ia-companion.plan.md` 种子) |
| 产品工具 | 设计系统风 | token 化、组件齐整、可复用感 | 平台/B2B;中性、强一致 | Stripe · Supabase · Vercel |
| 产品工具 | 现场工程风 | 浅底工业仪表:分区舞台、长引导线、校准刻度轨、大型编号 | 建设/物流/数据工具/工业产品;米白+炭黑、中高密度、单一信号黄 | 👁 **终末地**(https://endfield.hypergryph.com/ · 生产 CSS 坐实:`#191919`/`#fff`/信号黄 `#fffa00`,Novecento Sans Wide + clip-path 分区 · 闭源游戏 IP,**诠释非复制**) |
| 未来科技 | 玻璃拟态风 | 毛玻璃、内发光边、层叠透明 | 科技/金融科技;深色背景配 | — |
| 未来科技 | 3D 沉浸风 | WebGL/3D 场景、空间纵深 | 发布会、概念站;重资源、需 perf 控 | 👁 igloo.inc(https://igloo.inc · Awwwards SOTY 2024 · 全 WebGL:Three.js+GSAP) · Bruno Simon portfolio(https://bruno-simon.com · Awwwards SOTD · Three.js 可驾驶开放世界) · landonorris.com(https://landonorris.com) · Shopify Editions Winter'26(https://www.shopify.com/au/editions/winter2026 · 季节页 URL 会过期,失效即换当期 Editions)——后两个用户 2026-07-07 亲选并判:"非常优秀的向下翻滚式作品,超前 3D 效果"(替换 Seamora;curl 200 核实)。HOW 层见 `three/`(threejs-scroll-stage) |
| 未来科技 | 宇宙档案风 | 午夜底 + 衬线叙事标题 + 圆形轨道仪表、星图节点 | 叙事档案、文化编辑、天文工具、角色资料;暗色、低密度、大留白 | 👁 **来自星尘**(https://exa.hypergryph.com/ · 生产 CSS 坐实:白/近黑 + 水青 `#46f6e6` 极克制,思源宋 + Sumerhan,44 处 mask + 轨道 keyframe · 闭源游戏 IP,**诠释非复制**) |
| 未来科技 | 数据可视化风 | 图表即主角、信息密集 | 分析/监控产品;高密度、mono | — |
| 排版表达 | 杂志编辑风 | 大标题衬线、栏宽、引文 | 内容站、品牌叙事;editorial | Claude · Mistral(编辑衬线 AI) · Hermès·Aesop(编辑奢侈,诠释非复制) |
| 排版表达 | 动态排版风 | 文字本身在动/变形(kinetic type) | 创意站、活动页;强 motion(接 Batch 2) | — |
| 排版表达 | 全屏视觉风 | 整屏大图/大字,一屏一观点 | 营销落地、作品集 | Runway(照片/视频驱动) · Ferrari·Lamborghini·Bugatti(奢侈汽车,黑底全屏+单金属 accent,诠释非复制) |
| 个性潮流 | 新野兽派 | 粗边、硬阴影、原始 HTML 感、高对比 | 个性品牌、潮牌;不怕"丑" | 本 lab Northway(lab) |
| 个性潮流 | 复古未来主义 | 80s/90s 科幻、网格地平线、霓虹 | 音乐/游戏/活动 | — |
| 个性潮流 | Y2K 数字风 | 千禧金属、气泡、像素、亮色 | 年轻向、潮流电商 | — |
| 情感品牌 | 插画品牌风 | 自定义插画主导、暖、人格化 | 消费品牌、教育、儿童 | — |
| 情感品牌 | 手写涂鸦风 | 手绘笔触、随性、不规则 | 创意工作室、个人站 | — |
| 情感品牌 | 有机自然风 | 柔色、圆角、自然纹理、慢节奏 | 健康、食品、可持续品牌 | 本 lab Grove(lab) |
| 情感品牌 | 明快协作风 | 圆角胶囊、粗描边、错位硬阴影、漂浮层与弹跳反馈 | 协作工具、趣味引导、家庭向、活动页;亮底、中密度 | 👁 **POPUCOM**(https://popucom.hypergryph.com/ · 生产 CSS 坐实:蓝 `#3994ff` 撑主结构、黄橙只当动作信号 · ⚠ 原站三色并用,进产品 UI 须先收成**单一 accent**(见 `palette-pool.md` §2)· 闭源游戏 IP,**诠释非复制**) |

> **范本锚 provenance**:具名 brand = `web-verified`(从其 DESIGN.md 坐实,含奢侈汽车 Ferrari/Lamborghini/Bugatti);`本 lab X(lab)` = `your-skill`;Apple = canonical memory;**闭源大站(Hermès/Aesop 等)= 逆向 `memory-candidate` + `do-not-copy`,标"诠释非复制"**(视觉 👁 你看,只给 URL);`—` = 留待人工 surface(看视觉是人的活,见 §成长)。
>
> **游戏 IP 站(终末地/来自星尘/POPUCOM,2026-08-04 入池)= 证据 `web-verified` + 权利 `do-not-copy`,标"诠释非复制"。**
> 证据档次比 DESIGN.md 更硬:直接下载其**公开生产样式表**并 **SHA-256 逐字节核对**通过(4 份共 353KB,与上游 2026-07 快照完全一致),色值/字体是数出来的不是记的。
> **但证据强度 ≠ 可复制性** —— 这三家是商业游戏 IP,logo/角色美术/自有字体一律不取,只借构图、层级、几何与配色**语法**。
> 二手来源 `ark-ui-skill`(github.com/Brandon030722/ark-ui-skill,clean-room 蒸馏)**不当锚**,只作"已有人蒸馏过一遍"的旁证。

**用法提示**:Batch 1 的 3-4 个 variant 应在**这一轴的多个 facet**上拉开差距(如「瑞士国际主义(浅/高秩序) vs 深色科技 SaaS(暗/中密) vs 杂志编辑(衬线/叙事)」),而不是同一风格换三个 accent 色。motion 这批先压成朴素默认(只 load-in 或不动),留给 Batch 2。

> 守 `taste-skill` 的硬规则不受本池影响:无紫 LILA、单一 accent、数字 mono、禁 Inter、禁 3 等宽卡片栏等——风格池只决定"往哪个方向走",不豁免品味门。

## 成长(human-gated,见 `reference-sources.md` §5)
看视觉风格好坏是**人的活**(我看静态≠会判品味)。所以遇到池里没有的风格时,我**不自行加**——我把它 **surface 给你**(风格名 + URL + 为什么),**你亲自去那站看了再决定加不加**。自产页面跑得再好也不当 standard 入池。
