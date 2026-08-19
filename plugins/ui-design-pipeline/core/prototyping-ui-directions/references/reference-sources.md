# 参考源登记表 + reference-first 工作流(reference-sources)

> 用在 `prototyping-ui-directions` 的 **Stage 1(reference acquisition)**:用户说要某个具名复杂效果 / 找灵感时,
> **先来这查"去哪看"**,而不是凭一段文字硬写。配 `style-pool.md`(风格)/ `font-pool.md`(字体)/ `motion-pool.md`(动效:文字 #1–#10 + 整页滚动编排 #11–#20)。
> 与 skill 一起部署(随 `references/` 走)。

## 0 · 能力诚实(crux —— 决定一切分层)
**我读代码强,但我"看不见"运行中的动画。** 所以每个源按**两根独立的轴**打分,不是一条直梯:

- **VISUAL 视觉保真**:这个"长相"可不可构建?(真 token / type / layout / 组件规格 = 高;只截图 = 低)
- **MOTION 动效保真**:有没有**真动画代码**,**什么引擎**?
  - `gsap`/原生 → **能直接进我们的 HTML 产物**(最高,我的强项)
  - Framer/React → 只进 **TSX** variant;HTML variant 只能**借手法转 GSAP**(`interpret-to-gsap`,绝不冒充能直接抄)
  - WebGL/canvas → 我能读代码但**看不见输出**、且重 → `webgl-readonly-heavy`,标注
  - 闭源大站(Hermès/Linear 级,minified/bundled)→ **拿不到真实现** → 只产"**神似**逆向版",**标"诠释非复制"**

一个源可以"视觉高 / 动效零"(DESIGN.md 就是),所以两轴分开看。
`WebFetch` 只回 text/HTML(无 JS 执行、无动效);Playwright 能拿渲染后 DOM + (压缩的)脚本 + 状态采样。

### 第三轴 · 谁看(consumer)—— 正交于 fidelity,定**分工**
源还分"该谁去看",这条轴决定调用契约:
- 🤖 **AI 读**:我 fetch+抽取(token/代码/结构),**你只审结果**(如桶 A、Ant/Carbon 代码)。
- 👁 **人看**:价值在视觉/动效,我看不了/看了低效 → **你看你挑**,再把截图/选择丢我(如桶 E 画廊、动效灵感墙)。
- 🤝 **分工**:你看 live demo **挑**哪个,我读代码 **建**(如桶 B/C —— 动效你看效率高,我读 GSAP 源)。

铁律:👁 的源我**只给你 URL 让你看**,绝不假装能 fetch 出视觉/动效。

---

## 1 · 桶(buckets)—— 用户点名的源 = bucket #1(公共资源,非私有 skill)

> 每桶按"我到底能拿到什么"组织;`engine` / `provenance` / `do-not-copy` / `cap` 标在桶上。
> **cap = 每类封顶 ≈3-5 条**(防 `awesome-design` 那 400 条洪水)——靠 promotion-loop + 人工策展慢慢长。

### 桶 A · DESIGN.md corpus —— ★ 视觉最高价值(静态)
- **源**:`voltagent/awesome-design-md`(73+ 大厂)· `VoltAgent/awesome-claude-design`(68)· `zephyrwang6/brand-design-md`(62)· `bergside/awesome-design-skills`。
- **VISUAL 高 / MOTION 无**:每个 brand 一个 `DESIGN.md` = 可直接构建的静态 token(role-tagged hex + type scale + spacing/radius/shadow + 组件规格)。**没有动效代码**。
- **拿法**:fetch `raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<brand>/DESIGN.md` → 把 9 段映射进我们的 pool(色板→style/palette;typography→`font-pool`;guardrails→taste 校验)。
- **provenance** `web-verified` + `community-reverse-eng`(社区逆向,可能与真 brand 漂移→标置信度)+ **`do-not-copy`**(只逆向系统,不抄资产)。
- **已坐实(SaaS 样板)**:`stripe`(Söhne/商用,轻量大标题)· `vercel`(Geist/免费)→ 见 `font-pool.md §1`。SaaS/dev 还有 linear*/supabase/sentry/raycast/warp/cursor/notion 等(*linear 走 Inter,taste 禁,不推荐)。
- **cap**:不全收;按需 parse 单个 brand 当"参考卡"。
- **第一方官方设计系统**(也收入本桶,比社区 DESIGN.md 更权威 = 源头):**Ant Design**(ant.design)/ **IBM Carbon**(carbondesignsystem.com)= **真组件代码 T1,我能直接读**;**Material Design**(m3.material.io)/ **Apple HIG**(developer.apple.com/design)= spec/token 锚。
- **交互细节 spec 锚(2026-08-05 入)**:**detail.design** —— 策展式"小设计决策"参考,**6 类目**(Design / Copywriting / Accessibility / Motion / Optimization / Feedback),每条 = 标题 + **一句话做法** + 类目 + 截图/视频演示(**不是长文分析**)。**服务端渲染 ⇒ 文字层我能直接读**;实例逐字:*"Clicking the Input Label Focuses the Input Field"* [Accessibility] · *"Screen Shaking Feedback — Feedback for the dead end."* [Motion] · *"'Follow Us' Text Trick — You don't have to say Follow us on X."* [Copywriting]。
  ⚠️ **按 §0 双轴打分它两轴都低**(无 token、无动画代码)——**别按分数把它踢了**:它的价值在"**可执行的交互规则**"这条**双轴测不到的第三维**,是本表唯一能直接喂校验清单的源(taste-skill 只讲"该用哪类微交互"的品味方针,**没有做法清单**,不重叠)。
  **谁看** 🤝 分工:**文字层我读,视频演示你看**。`web-verified` · ⚠ **社区策展、非第一方**(比 Ant/Carbon 低一档) · 演示素材 `do-not-copy`。
- **谁看** 🤖 AI 读 —— 我 fetch+parse token,人不必访问(第一方系统同 🤖,Ant/Carbon 连组件代码都能读;**detail.design 例外 = 🤝**,见其条)。

### 桶 B · 代码组件库(React + Framer)
- **源**:Aceternity UI · Magic UI · 21st.dev(有 Magic MCP;⚠ **`21st.com` 是它的笔误,不是独立产品** —— 403 且搜不到任何独立产品证据,**别再当新源收**)· React Bits · motion-primitives · Hover.dev。
- ⚠️ **本桶已 6 条 / cap ≤3-5 = 超载**,且 **2026-08-05 查实至今零调用**(6 个库名全仓只命中登记表自己 + 计划文档,`testbed/` 下 0 命中,57 件素材无一出自它们)。**新增一律先解决「外部素材库到底怎么利用」那个悬案**(桶 B ↔ 桶 C 的定位与优先级 / 直接装 vs 读了重写 / `tsx-direct` 走多深),否则只是把洪水阀焊死。
  **候选挂起**:`eldoraui.site`(150+ React/TS/Tailwind/Motion 组件,shadcn 兼容 registry + 官方 MCP,**LICENSE 坐实 MIT** —— 本表极罕见的**可直接复制**源)= **🔒 BLOCKED,等上述裁决**,不是"不收"。
- **VISUAL 高 / MOTION 高 但 engine = Framer Motion(只 React)**。
- **engine 标记**:`tsx-direct`(TSX variant 直接用)/ `interpret-to-gsap`(HTML variant 只借手法转 GSAP,**绝不**当能直接抄的列出)。
- **拿法**:多为 shadcn-compatible registry → 复用本 harness 的 `shadcn-registry` skill 走安装路径(reuse,别重造)。
- **provenance** `web-verified`(站点在维护)。**cap ≤ 3-5**(别收 5 个 Framer 库)。
- **谁看** 🤝 分工 —— 你看 live demo 挑,我读代码 port。
- **按工作流类别的入口** → `component-pattern-pool.md`(把本桶 + shadcn/Radix/Ant/Carbon 按 Actions/Input/Nav/Containment/Data-Display/Feedback 重切成"某类交互去哪拿代码"的指针表;结构 ≠ 动效,动效仍走 `motion-pool.md`)。

### 桶 C · 教程/demo 代码(vanilla + GSAP/WebGL)—— ★ 动效最高价值
- **源**:**Codrops / tympanus** · GSAP Showcase + CodePen GreenSock · GitHub demo repos。
- **VISUAL 中 / MOTION 高 且 engine = GSAP/原生 → 直接进我们 HTML**。WebGL/canvas demo = `webgl-readonly-heavy`。
- **拿法**:每 demo → name + effect + 源 repo URL + 库(GSAP/Three)+ 1 行手法 + 可移植性。**复杂动效优先来这**(我读真 `gsap.to(...{duration,ease,stagger})`、timeline、ScrollTrigger 参数)。
- **provenance** `web-verified`。喂 `motion-pool.md`。
- **谁看** 🤝 分工(动效)—— **你看 demo 效率高**,我读 GSAP 源建。

### 桶 D · meta 索引(source-of-sources)—— 当矿不当料
- **源**:**`gztchan/awesome-design`**(400+ 链接,两大类 "Get things done" / "Concepts":Color/Typography/Toolkit/Prototyping/Styleguide…)· **bentogrids.com**(bento 版式专题,详见下)· github topic 列表。
- **不 wholesale ingest**:走 §2 选取流程,每类挑一小撮高信号、逐条 fetch-verify、只把**核实过的叶子**收进对应桶。索引本身只记**一条**"周期性来挖"。
- **谁看** 🤝 —— 名单你我都能扫;核实按类型分(🤖 的我读、👁 的你看)。
- **bentogrids.com(2026-08-05 入,单一版式专题矿)**:**它自己一行源码都没有**,价值全在**每条链回的出处网址** —— 这正是"矿不是料",故归本桶而**非桶 E**(灵感画廊是终点,本桶是入口)。
  **实测索引**(解析其 `__NEXT_DATA__`,非估算):**285 条,`sourceLink` 缺失 0**;其中 **226 条链回真实上线产品站**(trychroma / neon.tech / dovetail / tuple.app / huly.io / pixelmator / june.so / novu.co / useparagon / kentcdodds / taipy.io …**本行 10 个 2026-08-05 全部 curl 复核 live**)⇒ **这些站的生产 CSS 可下载拆解**
  ⚠ 索引里也有**这台机器连不上的站**(如 `alfabank.ru`,curl 超时/区域不可达)——**挖之前先探活**,别把连不上当"站没了";另 50 条 Dribbble 图 + 7 条 Framer 模板站 + 2 条 Behance ⇒ **无 CSS 可拆,永远只能人看**。分类 `ui` 203 / `graphic` 82(后者是平面 + Figma 社区模板,**非网页**);带 `isDark` 字段(深 156 / 浅 129)可直接按明暗筛;558 素材中 59 个是视频。
  **挖法四步**:①我读索引(已读全)按关键词 / `ui` vs `graphic` / 明暗筛 → ②挑(图我看不见 ⇒ 你翻着挑,或我按站的档次先粗筛)→ ③挑中的**出处站**走 `vendor/competitive-teardown` **Visual Mode** 拆**生产 CSS**(下载样式表 + SHA-256 逐字节核对 + 数出真 hex / 字体 / grid 参数,同 2026-08-04 游戏 IP 站那批的方法,**产硬证据不产"看起来像"**)→ ④落 `style-pool.md`「Bento 卡片风」范本锚;要做可跑件则 bento 机制 = CSS Grid `grid-template-areas`/span,**我自写不依赖它给码**。
  **谁看** 🤝 分工(**图你看 / 索引与 226 个出处链接我读**)。`web-verified` · 收录他人站 → `do-not-copy`。
  ⚠️ **诚实边界**:50 条 Dribbble + 82 条 `graphic` **拆不动**(图 / Figma 模板,无线上 CSS);真正可挖的是 203 条 `ui` 里链向真站的那部分。

### 桶 E · 灵感画廊(静态 look + 动效灵感特例)
- **源**:Awwwards · Godly · SiteInspire · Land-book · Mobbin(登录墙)· Savee · Cosmos · **Typewolf** · Fonts In Use · **Design Spells**(designspells.com,动效特例见下)。
- **VISUAL 低-中(静态)/ MOTION 无**(动效源见桶 C;本桶只 Design Spells 一个动效**灵感**特例):只给 layout/color/type。
- ⚠️ **本桶 10 条 / cap ≈3-5 = 长期超载**(2026-08-05 盘点)。**新增必须净零顶替**,不许只加不减;出库和入库一样是**人的决定**(§5 红线 2 的对称面),我不自行删。
- **拿法**:URL + 提取点 + 登录墙标记。Mobbin 这种登录墙 → 让用户给截图 → 走 `image-to-code-skill`。Typewolf / Fonts In Use → `font-pool` 的范本锚。
- **谁看** 👁 人看 —— 纯视觉,我 fetch 拿不到;**你看你挑** → 截图丢我走 image-to-code。
- **Design Spells 特例(designspells.com,2026-08-05 入,👁 你看你挑)**:微交互/彩蛋收集站——收**真实商业产品**里的隐藏动画与趣味反馈(Monzo 解锁动画 · GitHub Copilot 藏的跳跃小游戏 · Claude Code 的 effort 选择动效 …)。
  **实测形态**(解析其 `sitemap.xml`):**322 条 `/spells/` 条目,每条一个 `<video:video>` 块**(`video:content_loc` → `.mp4`、`video:thumbnail_loc` → 首帧 jpg),**`<video:description>` 零条** ⇒ **每条 = 一段屏幕录像 + 一个标题,无说明文字、无实现代码**。另有 155 个按产品聚合的 `/apps/` 页。
  ⚠️ **我一帧都看不见**:唯一能拿到的是**标题清单**("Unlock animation in Monzo")。写"我看了 Design Spells 觉得…"**就是违规**(§0 铁律)。**你浏览挑手感 → 我在 taste 下诠释成 GSAP(绝不抄)**。
  **❌ 不进 `motion-pool`** —— §5 红线:那池只收**读到真源码**的候选,录像不是源码。cross-ref `motion-pool.md`。
  `web-verified`(322 条 + newsletter 更新到 #73) · 全部是**他人商业产品**录像 → **`do-not-copy` 铁定**。
  > ⚠ **注意 UA**:默认 WebFetch 会吃 **403**(Cloudflare 拦),换浏览器 UA 的 curl 即 200。`/rss.xml` 是 404,真 feed 在 **`/feed`**(仅 newsletter 汇总,不含条目)。
- **🗑 已出库:MotionSites(motionsites.ai)** —— 2026-08-05 被 Design Spells **净零顶替**(桶 E 超载,新增须顶替)。两者同型(👁 动效灵感墙、不可 port、不进 motion-pool),但 MotionSites 是 **AI-prompt 模板**(面向 Lovable/Cursor 生成)而非真实产品实现,且招牌 Neon Pulse / Crystal Wave / Cosmic Ripple / 大渐变 hero **撞 `taste-skill` 硬规则**(无霓虹 · 无渐变大标题 · 单一 accent);另有其创作者自己的提醒作**外部佐证**——"直接用原 prompt 出来的网页几乎和原站一模一样、还共用素材"(**同质化风险**,与本表既有裁定同向)。
  **⇒ 它没被丢掉,转入维护者私有账本的「📌 常设 · 培养审美」清单**(用户个人观看清单:不过 6 闸、不占 cap、不随 skill 部署)。**别再当新源收回本桶。**

### ⚠️ 域名纠正记录(2026-08-05 实测,踩过的坑别再踩)

写错的域名会**静默失败**(DNS 不存在 / 跳转 / 停放页 / 403),不留痕迹 ⇒ 记在这防重踩。

| 常见写法 | 实况 | 正确的 |
|---|---|---|
| `bestdesignonx.com` | **DNS 不存在**(少一个 s) | `bestdesignsonx.com` |
| `bentogrid.com` | 308 永久跳转(少一个 s) | **`bentogrids.com`** |
| `designeverywhere.com` | **GoDaddy 停放待售页**(不是本站) | `designeverywhere.co` |
| `21st.com` | 403,无任何独立产品证据 | **`21st.dev`** 的笔误,**不是新源** |

### 🚫 已判不收(跑过 §2 6 闸,别再重复评估)

| 源 | 不过哪闸 | 理由 |
|---|---|---|
| **variant.com** | ①保真度 + ③不重叠 + §5 第一性原理 | **它是 AI 设计生成器,不是参考源**。`meta description` 逐字:*"Enter an idea for an app or site and see endless design options just by scrolling."* ⇒ 吐的是**机器现生成的设计**,不是"外部已存在且被认可的范本"。本库价值 = 指向**外部可信标准**;收它 = 把回声室入口焊在库上(只不过回声的是别人的模型)。**不属 A–E 任何一桶。** ⚠ "一键导入 Figma" 是转述、站上无证据、**未核实**——但即便为真,它仍是生成器,判定不变 |
| **bestdesignsonx.com** | ③不重叠 + ⑥封顶 | 每小时策展 X/Twitter 设计帖。与桶 E 已有的 **Savee / Cosmos 同型**(泛视觉 moodboard)且**更弱** —— 纯二手转发,无策展站自己的判断;版权归原发帖作者。桶 E 已 10/5,**连顶替资格都没有** |
| **designeverywhere.co** | ①保真度 | 实测条目 = `WK-编号 + 作品名 by 工作室`(Nudo Noodle by Workbyworks …),标签 Typography / Logo Design / Identity ⇒ **平面 / 品牌识别 / 包装设计,不是 web UI**,本仓做不出它;部分内容需 Log In。**⇒ 转维护者私有账本的「培养审美」清单**(用户 2026-08-05:"可以作为人的审美修养,定期去看")——**不入库 ≠ 没价值**,正因它跨出网页,补得上只看网页养不出的审美 |

---

## 2 · 选取流程(怎么选取 —— 用户丢"很多个"时跑这个,operational)

> 这是把"我能推荐很多,怎么选"变成可执行的坎。**不是描述,是流程。**

```
用户丢一批源
   │
   ▼
① 分桶(按桶 A-E 判型)
   │
   ▼
② 逐条过 6 闸 rubric(下) ── 不过 → 丢弃/降级
   │
   ▼
③ 出候选短名单:封顶 + 去重 + 带 tier(视觉/动效)+ engine + provenance 标签
   │
   ▼
④ 给用户看 → 用户批(Stage-1 铁律:fetch/clone 前先和用户锁定 reference 列表)
   │
   ▼
⑤ 批了才 fetch/parse → 收进对应桶 / 喂 pool
```

### 6 闸 rubric(全过才收)
1. **保真度闸** — 两轴诚实打分;优先能产出可构建物的(A/B/C);纯静态(D/E)只在它是**公认品味锚**时收。
2. **引擎匹配闸** — GSAP/原生 = 直接进 HTML;Framer/React = 进 TSX、HTML `interpret-only` **且必须标出**,绝不假装能直接抄。
3. **不重叠闸** — 加的是登记表/已有桶没有的能力(别收 5 个 Framer 库);若用户日后点名私有收藏 skill,先对它跑这一闸再加。
4. **来源/新鲜度闸** — 有人维护、canonical(star/最近提交);社区逆向(DESIGN.md)标置信度。
5. **版权/do-not-copy 闸** — 大厂资产只逆向系统 → 标 `do-not-copy`。
6. **每类封顶闸** — ≈3-5 条/类。让它是**跳板不是垃圾场**。这是洪水阀。

> **默认处置(短名单已经过上面 6 闸 + 你审阅后)**:你**没明确说淘汰的 = promote**(默认收),不必逐条再点头;只有你明说"弃"的才弃。即洪水阀在"进短名单"那关把,**进了短名单的默认留**。

---

## 3 · 调用契约(用户怎么开口 → 我去哪 → 我还什么)

| 用户说 | 我去 | 我还 |
|---|---|---|
| **"灵感/参考: \<vibe/手感\>"**(taste) | 桶 E 灵感画廊 + 桶 A 范本锚 + Typewolf | curated **URL 短名单** + 每条 1 行"为什么 + 提取啥"(逆向,非复制) |
| **"找个能做 X 的代码"**(实现,尤其复杂动效) | 桶 C(GSAP/原生,首选)→ 桶 B(React/Framer) | **可移植源码 + port 到我们 chassis+GSAP+taste 的计划**(代码 + 源 URL + engine 标记) |
| **"做成像 \<brand\> 那样"**(brand 风格) | 桶 A:拉该 brand 的 `DESIGN.md` 当参考卡 | 真 token(视觉高)+ 诚实提醒"**只给 look 不给 motion**,且 `do-not-copy` 资产" |

- 灵感 → URL;实现 → 可移植代码 + URL。**live/核实过的 URL 需要 WebSearch/WebFetch 或用户给**;纯记忆只能给 canonical 名字(无新鲜度保证)。
- **谁看映射**:第 1 行"灵感"= 👁 **你看**(我只给 URL,不假装能读);第 2 行"找代码"= 🤝/🤖 **我读**;第 3 行 brand = 🤖 **我 parse**。consumer 轴(§0)就是这张契约的底层逻辑。

## 4 · 复用既有 skill(别重造)
**都在本仓 `vendor/` 里**(从 global vendored,clone 即完整;上游仍在 `~/.claude/skills/`):
`vendor/competitive-teardown`(拆参考站——lab 版**只有** Design-Reference Visual Mode,出视觉提取卡;商业记分卡那半边没拷)·
`vendor/image-to-code-skill`(截图→代码,服务桶 E / 登录墙画廊)· `vendor/shadcn-registry`(桶 B 安装)·
`vendor/imagegen-frontend-web`(生成参考图)。
动效品味不外借:lab 内 canonical = `authoring/taste-skill` §8。
另有全局 `development-workflow.md §0 Research & Reuse`(harness 层,不随本仓走)。

## 5 · 成长治理(库怎么长大 —— human-gated,防自产回声室)

> **第一性原理:本库的价值 = 指向"外部可信标准"(external credible standards)。** 一旦它被自产货填满,就退化成
> 自我引用的回声室,失去"可信范本"的意义。所以成长有红线。

**红线 1 · 自产输出绝不当 standard 自动入库。** 跑出来好看的页、被用户选中的 LEAD、打分过线的 surface ——
都只代表"**这个项目合适**",**不代表"行业范本"**。它们不因"赢了"就进库。

**红线 2 · 能回流的只有 run 里发现的"外部"料**,且必须**人为把关**:
- 我**不自行加**;我把候选 **surface 给用户**(范本锚 + URL/源 + 1 行为什么 + provenance + 走 §2 6 闸的结果),
  **用户决定加不加**(Stage-1 铁律的延伸:入库 = 人的决定)。

**按 pool 分,我能帮多少(能力诚实):**
| pool | 我能做 | 必须靠人 |
|---|---|---|
| **style-pool** | 遇到池里没有的风格 → 报你:名 + URL + 为什么 | **你亲自去那站看视觉再定**(品味是人的活,我看静态≠会判好坏) |
| **font / palette** | 从真 DESIGN.md / 官网**抄真 family/hex 提候选**(可数据化) | 是否够"外部可信" + 入库,你点头 |
| **motion** | **只在读到真源码**(桶 C GSAP/原生)时提候选 | 我**没法靠"看"判动效好坏** → 由人 / 打分器 `interaction_quality` 判;**我不能自动更新 motion-pool** |

**provenance 分层(库的体质)**:`web-verified` / canonical = **主干**(库应以这档为主);`your-skill` = **内部验证记号,
比 standard 弱一档**,不应主导任何 pool(`Northway`/`Grove` 行只作"自家用过、可参照"留底,不是行业范本)。
