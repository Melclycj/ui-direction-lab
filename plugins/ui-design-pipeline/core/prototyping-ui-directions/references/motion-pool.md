# 动效池(Batch 2 动效参考)— 可选 base-case

> ⚠️ **这是兜底,不是菜单。** 仅在想不出更好动效时拿来当起点;**不要求**从里面选。
> 用在 `prototyping-ui-directions` 的 **Batch 2(motion treatment)** 和 `anchor-prototype-wave`
> 的 §Authoring: motion。每条都给了 **GSAP 实现路径**(指向 `gsap-*` skill)。
> 两档:**文字动效**(#1–#10,一段文字怎么动)+ **整页滚动编排**(#11–#20,整页随滚动怎么编排)。
>
> 命名澄清:#1–#10 是**文字动效 / text-reveal effects**(怎么"动"),**不是字体(typeface)**。
> 若要的是字体本身的参考(字族选型),那是 Batch 1 视觉的事,见 `font-pool.md`。
>
> **⚙ 执行注册表**(2026-07-10 motion-score 工程):每条编号效果行带 `【⚙执行册】` 徽章 =
> 在 `execution-registry.json` 有恰一条机器可读执行记录(schema 见 `execution-contracts.md`;
> 站级锚等无编号行的徽章内含注册 ID)。本池 Markdown 仍是描述/出处/人评的单一真相源;
> agent 提候选必须先过 `../scripts/resolve_candidates.py` 过滤;同步校验
> `../scripts/check_registry_sync.py`。新条目入池/毕业:记录+徽章+sync 绿,三件一起。

## 文字动效(text-reveal)#1–#10

> **2026-07-11 全毕业 🎉(motion-materialize 批 A)**:10 条全部 lab 复刻收进**一件组件库**
> ✅`material/text-reveal-gallery`(manifest + `?only=<id>` 单效果预览 + `build(id, el)`/`play(id)`
> 可拔接口——拔出即贴任意文字元素;每效果对齐行内主方案;VERIFY/TAGS 在件内)。逐条五层 🏷(⚡=按真码核算):
> #1 🏷:驱动=load/replay · 机制=SplitText chars 逐字 `.set`+伪光标逐字跟随+`steps(1)` 闪烁 · 载体=component/任意文字元素 · 内容=任意短语 · register=notes/demo/AI 生成感 · ⚡轻
> #2 🏷:驱动=load/replay · 机制=`filter:blur(16→0)`+autoAlpha per-word stagger · 载体=component · 内容=任意短语 · register=悬念揭晓/概念开场 · ⚡轻(瞬态 blur)
> #3 🏷:驱动=load/replay · 机制=timeline 6 硬切关键帧 x/skewX+红青双 clone `mix-blend:screen` clip 横带跳变=RGB 分离 · 载体=component · 内容=任意短语 · register=科技/AI/赛博 · ⚡轻(瞬态)
> #4 🏷:驱动=load/replay · 机制=官方 **ScrambleTextPlugin** · 载体=component · 内容=任意短语 · register=信息解码 · ⚡轻
> #5 🏷:驱动=load/replay · 机制=`rotationX:-92→0`+`transformPerspective:620`+origin 底边+back.out · 载体=component · 内容=任意短语 · register=对比/反转/功能页 · ⚡轻
> #6 🏷:驱动=load/replay · 机制=3 条 clip-path inset 横带 clone 交替 x±84 滑入对齐(带位重叠防缝,末帧换回本体) · 载体=component · 内容=任意短语 · register=强冲击标题 · ⚡轻
> #7 🏷:驱动=load/replay · 机制=**DrawSVGPlugin** 逐笔 stroke `0%→100%`+加粗层淡入=「填满」 · 载体=SVG 骨架字(换词需重作路径;件内 NOVA 5 path) · 内容=短词 · register=品牌字/手写/艺术 · ⚡轻
> #8 🏷:驱动=load/replay · 机制=260% `background-clip:text` 渐变 `backgroundPosition` 扫过留亮(`@supports` 包裹) · 载体=component · 内容=任意短语 · register=关键词强调/封面 · ⚡轻
> #9 🏷:驱动=load/replay · 机制=`elastic.out(1,0.3)` y46+scaleY1.55 拉伸回弹(时长/缓动从 `--tr-*` token 读) · 载体=component · 内容=任意短语 · register=活泼/短视频转场感 · ⚡轻
> #10 🏷:驱动=scroll-scrub · 机制=ScrollTrigger 3 层 clone `yPercent ±60/±30/±12` 三速错动 · 载体=经过视口的文字块(`?only` 给 340vh 跑道;`build()` 可传 scroll 容器) · 内容=大标题 · register=高级开场/封面 · ⚡轻

| # | 效果 | 手感 | 适合 | GSAP 实现(哪个 skill) |
|---|---|---|---|---|
| 1 | **Typewriter** 打字机 | 逐字出现、像实时输入,带光标 | 笔记/演示/AI 生成感 | `gsap-plugins` SplitText(chars)+ stagger,或对象 `onUpdate` 截取子串(`gsap-core`);✅`material/text-reveal-gallery` `?only=typewriter` 【⚙执行册】 |
| 2 | **Blur In** 模糊聚焦 | 从模糊到清晰,像镜头对焦 | 悬念揭晓、概念开场 | `gsap-core` 动 `filter:"blur(..)"` + `autoAlpha`(CSSPlugin 可动 filter);✅`material/text-reveal-gallery` `?only=blur-in` 【⚙执行册】 |
| 3 | **Glitch** 故障扭曲 | 短暂错位/抖动/色散再恢复 | 科技、AI、赛博 | `gsap-timeline` 排 x/`skewX`/clip + RGB 分离;短促 + 多关键帧;✅`material/text-reveal-gallery` `?only=glitch` 【⚙执行册】 |
| 4 | **Scramble** 乱码重组 | 先随机乱码,再逐渐拼成正确字 | 信息解码、复杂概念揭示 | `gsap-plugins` **ScrambleTextPlugin**;✅`material/text-reveal-gallery` `?only=scramble` 【⚙执行册】 |
| 5 | **Flip** 翻牌入场 | 卡片翻面、明显切换感 | 对比、观点反转、功能页 | `gsap-core` `rotationX` + `transformPerspective`;或 `gsap-plugins` **Flip** 做布局态切换;✅`material/text-reveal-gallery` `?only=flip-in` 【⚙执行册】 |
| 6 | **Slice** 切片错位 | 横切几块、错位滑入后对齐 | 强冲击标题、视觉包装页 | `gsap-plugins` SplitText / clip-path 分块 + `gsap-core` stagger x;✅`material/text-reveal-gallery` `?only=slice` 【⚙执行册】 |
| 7 | **Stroke Draw** 描边书写 | 轮廓一笔笔画出再填满 | 品牌字、手写标题、艺术 | `gsap-plugins` **DrawSVGPlugin**(需 SVG 文字轮廓);✅`material/text-reveal-gallery` `?only=stroke-draw` 【⚙执行册】 |
| 8 | **Highlight Sweep** 高光扫过 | 一道光/色块扫过文字点亮 | 关键词强调、封面标题 | `gsap-core` 动 `backgroundPosition` 或扫 pseudo + `gsap-timeline`;✅`material/text-reveal-gallery` `?only=highlight-sweep` 【⚙执行册】 |
| 9 | **Elastic** 弹性回弹 | 进入时轻微拉伸回弹 | 活泼、短视频转场感 | `gsap-core` ease `elastic.out(1,0.3)` / `back.out(1.7)`;✅`material/text-reveal-gallery` `?only=elastic` 【⚙执行册】 |
| 10 | **Depth Shift** 景深错层 | 前后层不同速度移动,纵深感 | 高级开场、个人页、演示封面 | `gsap-scrolltrigger` 多元素不同 `y` 速度 + `scrub`(视差);✅`material/text-reveal-gallery` `?only=depth-shift` 【⚙执行册】 |

**用法提示**:Batch 2 的 2-3 个 variant 视觉**完全冻结(=LEAD)**,只在动效轴拉开——
例如「仅 load-in(1+9) vs 滚动驱动景深(10) vs 重编排(3+6+8 组合)」。每条都必须:
- 走 `gsap.matchMedia()` 的 `prefers-reduced-motion` 分支(静止显示),
- 从 chassis 的 motion token(duration/easing)取值,不写死,
- 渐进增强:脚本不跑也能看到内容。

> 多数效果纯 HTML 可做(GSAP 框架无关);SplitText/ScrambleText/DrawSVG/Flip 现已全免费(见 `gsap-plugins`)。

## 整页滚动编排(scroll choreography)#11–#20

> 这一档管"**整页随滚动怎么编排**"(pinned 场景/色彩叙事/叠卡/布局态切换),与上面"一段文字怎么动"互补。
> 2026-07-03 入池(gsap-ecosystem Track B,用户全批)。起因:jesus-site 复刻验证证明栈对 GSAP/DOM 类效果
> 全覆盖,但池里没有这一档弹药,Batch-2 的"重编排"端点只能靠模型裸想。
> provenance:全档 `web-verified` —— Codrops/tympanus 教程(GitHub 真源码)或 **CodePen GreenSock 官方 demo**,
> 学习源一律外部成熟代码。历史注:#11–14/#20 的 pattern 最初观察自外部站 Seamora(jesus-site 盲跑复刻实证"栈能做"),
> 2026-07-05 应用户要求全部重锚到外部真源码(自产复刻未经多轮微调,不当学习源);唯 #12 的完整编排组合无教程,
> 以官方机制 demo 作锚、编排组合保持 `seamora-observed` 注记。
> 谁看(consumer 轴,见 `reference-sources.md` §0):全档 🤝 分工——动效手感由**人**看 demo/成品判,我读源码建。
> **2026-07-11 全毕业 🎉(motion-materialize 批 B)**:10 条各成独立件(VERIFY/TAGS 在件内;两处池行按代码
> 证据勘误——#18 源无 SplitText[手写 span 吃 CSS `calc(var(--progress))`]、#19 源无波浪/棋盘[实为
> 横百叶/乱序格/纵百叶/列扫])。逐条五层 🏷(⚡=按真码核算):
> #11 🏷:驱动=scroll-scrub · 机制=显式 fromTo zone 表(前色→本色)+`immediateRender:false`+过半翻 `is-dark` · 载体=整页房间序列(zone 持有跨节持久色态时可 chassis)/单章 sectional · 内容=任意长页分段 · register=longform 叙事 · ⚡轻(paint-bound 有界)
> #12 🏷:驱动=scroll-scrub · 机制=pin 长节多目标 timeline(hero scale/yPercent/圆角→淡出)+字标 position 参数反向横扫+官方 registerEffect zoom 逐字(zoom-in 专用,clamp 域 scale<1 反转已核) · 载体=pinned hero 长节(`+=150%`) · 内容=hero 卡+巨型字标插槽 · register=强开场品牌站 · ⚡轻(圆角 paint 点名)
> #13 🏷:驱动=scroll-scrub · 机制=列差速 `yPercent=-pos*10`+per-tile `±depth×vh` 漂移+微旋转(demo2 组件)+caption 4 窗交叉换场(行文成分,源 10 变体均无 caption) · 载体=长节 tile 墙+fixed caption 层 · 内容=图片墙 · register=作品墙/案例集锦 · ⚡轻
> #14 🏷:驱动=scroll-scrub · 机制=CSS sticky 钉卡+每卡 timeline(scale .95+brightness 50%+圆角 40)后退;「trigger=下一张卡」=源码 `trigger:自身+end:'+=100%'` 同一几何(15 变体核过) · 载体=依次 sticky 的卡序列 · 内容=步骤/feature 卡 · register=方法论走查 · ⚡轻
> #15 🏷:驱动=scroll-scrub · 机制=pin 舞台+master timeline 三阶段逐字(列式揭示→变焦劈开→文案浮出,按滚动方向分叉 `overwrite:true`)+ScrollSmoother · 载体=pinned 长节舞台 · 内容=图片格网+文案 · register=产品叙事/能力展示 · ⚡轻
> #16 🏷:驱动=scroll-scrub · 机制=class 定终态→`Flip.getState`→`Flip.to`+pin+scrub(9 参数变体:absoluteOnLeave/absolute+900% 长程/scale:false/stagger/80-item) · 载体=**dual-footprint(用户 2026-07-11 裁)**:单画廊节=sectional(preferred),整页连续画廊架构=chassis 部署 · 内容=图片组+caption · register=作品集视图切换 · ⚡中(scale:false=reflow 档+大批量 filter=paint 档)
> #17 🏷:驱动=scroll-scrub · 机制=`Flip.fit` per-waypoint 进单 scrubbed timeline(腿间 `+=0.5`,clamp 双端,resize revert 全量重捕获)+choir 五组辅助逐值 · 载体=跨节 waypoint 序列(z-index 编排=穿行遮挡关键) · 内容=单主角元素(图/卡/设备) · register=贯穿式产品主角 · ⚡轻
> #18 🏷:驱动=scroll-scrub · 机制=pin+`onUpdate` 写 CSS var `--progress`(parseEase 双重缓动):6 层同图 scale 阶梯 `1/.85/.6/.45/.3/.15` 递进+blur 退散+标题 span `calc(∓66vw)` 反向让位+ScrollSmoother `normalizeScroll` · 载体=pinned hero · 内容=同图多层(换图=全层同换) · register=电影感开场 · ⚡中(6 层全屏 masked 合成)
> #19 🏷:驱动=scroll-scrub(2.0-2.5 拖尾) · 机制=SVG `<mask>` rect 组 stagger 胀开揭示,4 次序单件切换 `?pattern=` · 载体=全屏图章节转场序列 · 内容=大图 · register=章节转场/画廊 · ⚡中(mask 逐帧 raster)
> #20 🏷:驱动=scroll-scrub · 机制=`SplitText.create(words,lines+autoSplit+onSplit 返动画)` resize-safe(GggpRoB 写法)+fromTo 暗 .15→亮 1+stagger(JjmMLqo 值) · 载体=长段落(多段各自 trigger) · 内容=manifesto/长文案 · register=宣言段 · ⚡轻

| # | 效果 | 手感 | 适合 | GSAP 实现(哪个 skill) | provenance |
|---|---|---|---|---|---|
| 11 | **BG 色彩叙事** bg-morph zones | 整页像穿过几个"房间",背景色随滚动平滑渐变、倒滚精确还原上一间 | 长页叙事/品牌故事/scrollytelling | `gsap-scrolltrigger` scrub + `gsap-core` 显式 fromTo zone 表(`immediateRender:false`,进度过半翻 `is-dark` class);✅`material/bg-morph-zones` | web-verified(官方 [XWQzYaR](https://codepen.io/GreenSock/pen/XWQzYaR) data-attr 版 / [PoxvEwK](https://codepen.io/GreenSock/pen/PoxvEwK) sections 版) 【⚙执行册】 |
| 12 | **Hero 收缩退场** shrink-away exit | 满屏 hero 随滚动缩成后退小卡(scale+圆角+淡出),巨型字标横扫补位 | 强开场品牌站/作品集 | `gsap-timeline` + `gsap-scrolltrigger` scrub 长节:hero scale/yPercent/borderRadius→opacity;position 参数排字标反向漂移;✅`material/hero-shrink-exit` | web-verified·机制(官方 pin+scale+scrub [YzbPYMx](https://codepen.io/GreenSock/pen/YzbPYMx) / [mdRaRrN](https://codepen.io/GreenSock/pen/mdRaRrN) zoom-by-section);编排组合 seamora-observed,无完整教程 【⚙执行册】 |
| 13 | **Pinned 深度视差拼贴** depth collage | 钉住长节里 tiles 按 depth 系数不同速纵向漂移+微旋转,中心 caption 交叉换场 | 作品墙/案例集锦 | `gsap-scrolltrigger` 长节 scrub + `gsap-core` per-tile fromTo(function-based `y=±depth×vh`);✅`material/pinned-depth-collage` | web-verified([OnScrollColumnsRows](https://github.com/codrops/OnScrollColumnsRows) 列/行不同速滚动) 【⚙执行册】 |
| 14 | **Sticky 叠卡** deck stack | 卡片依次滑上盖住前一张,被盖的卡后退变暗 | 方法论步骤/feature 走查 | CSS `position:sticky` 叠 + `gsap-scrolltrigger` scrub(trigger=**下一张卡**,scale+brightness 后退);✅`material/sticky-stack-deck` | web-verified([StickySections](https://github.com/codrops/StickySections/) sticky stacking/collapsing) 【⚙执行册】 |
| 15 | **Pinned 场景分段** scroll-as-time stage | 固定舞台不动、滚动推进"时间":master timeline 分阶段(揭示→变焦→文案浮出)或按 progress 窗口切高亮 | 产品叙事/能力展示长节 | `gsap-scrolltrigger` pin/fixed stage + master timeline scrub(`onUpdate` 按 progress 分窗 setActive);平滑滚动用 `gsap-plugins` ScrollSmoother;✅`material/pinned-scene-stages` | web-verified([sticky-grid-scroll](https://github.com/theoplawinski/codrops-sticky-grid-scroll)) 【⚙执行册】 |
| 16 | **Pinned 布局态切换** Flip layout switch | 同一组元素随滚动在两种布局间重排(grid→fullscreen/散排→堆叠) | 作品集视图切换/对比展示 | `gsap-scrolltrigger` pin + `gsap-plugins` **Flip**(class 定义终态,Flip 补间布局差);✅`material/flip-layout-switch` | web-verified([ScrollBasedLayoutAnimations](https://github.com/codrops/ScrollBasedLayoutAnimations/)) 【⚙执行册】 |
| 17 | **单元素跨节接力** one-element journey | 一个元素随滚动在多个 waypoint 间"搬家",节节无缝交接 | 贯穿式产品主角(一台设备/一张卡跨节讲故事) | `gsap-plugins` **Flip.fit** + `gsap-scrolltrigger` scrub per-waypoint;✅`material/one-element-journey` | web-verified([OneElementScroll](https://github.com/codrops/OneElementScroll)) 【⚙执行册】 |
| 18 | **分层变焦揭示** layered zoom | 多层同图不同 scale 递进放大+blur 退散,像镜头拉近的"拖尾变焦" | 电影感开场/图片主导 hero | `gsap-plugins` ScrollSmoother + `gsap-scrolltrigger`(CSS var `--progress` 同步层缩放,标题 span 吃 `calc()` 反向移动——**勘误 2026-07-11:源无 SplitText**);✅`material/layered-zoom-reveal` | web-verified([telescope-zoom](https://github.com/joffreysp/telescope-zoom)) 【⚙执行册】 |
| 19 | **SVG mask 百叶揭示** mask blinds | 全屏图被 SVG mask 矩形组按**横百叶/乱序格/纵百叶/列扫**四种次序揭开(**勘误 2026-07-11:源 4 变体无波浪/棋盘**),scrub 带拖尾 | 章节转场/图片画廊 | `gsap-scrolltrigger`(scrub 2.0–2.5)+ SVG `<mask>` rect groups stagger(`gsap-core`);✅`material/svg-mask-blinds` | web-verified([Scroll-Transition](https://github.com/Hiro-kiii/Scroll-Transition/)) 【⚙执行册】 |
| 20 | **Scrub 逐词显影** paragraph brighten | 长段落随滚动逐词点亮,读到哪亮到哪、可逆(跨档:文字动效的滚动进度驱动变体) | manifesto/宣言段/长文案 | `gsap-plugins` SplitText + `gsap-scrolltrigger` scrub(stagger opacity);✅`material/scrub-word-brighten` | web-verified(官方 [JjmMLqo](https://codepen.io/GreenSock/pen/JjmMLqo) scrub+stagger / [GggpRoB](https://codepen.io/GreenSock/pen/GggpRoB) AutoSplit resize-safe 写法) 【⚙执行册】 |

**用法提示**:#1–#10 的三条纪律(matchMedia reduced-motion 分支/从 chassis motion token 取值/渐进增强)对本档同样适用。另加两条——
- **hover 类效果必须 interrupt-safe**(2026-07-08 用户实测抓到的 bug 类:快速扫过时元素卡在外面不收回):
  每目标一条**持久可逆 timeline**(build 一次,enter `play()` / leave 从当前进度 `reverse()`),绝不在 hover
  上跑一次性 stagger;简单双态补间用 `overwrite:"auto"`。
- **上提/位移类 hover 防露底**:被提起元素后面放一个**不动的同色同形 backdrop 孪生**(inset:0,永不
  transform)——腾出的像素永远有底,不依赖邻居互叠的排布数学(R-D v3 实证,6/6 folder 零露白)。
- pinned/300vh 长节是**重编排**:一页至多一个主编排场景,别整页都 pin(WHEN/克制仍归 `taste-skill` §8 管辖);
- 平滑滚动不收 Lenis:`gsap-plugins` **ScrollSmoother** 已覆盖等价能力(2026-07-03 lab 决策)。

> Track A 附注(不入池):scroll→canvas progress 桥(jesus-site `src/scroll/stack.ts` 把 ScrollTrigger progress 喂给粒子场 `setProgress(p)`)
> + Codrops《[How to Build Cinematic 3D Scroll Experiences with GSAP](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/)》
> = `webgl-readonly-heavy`,攒给 Track A(Three.js 能力研究,见 LEDGER)。

## 指针驱动与 loading/入场 #21–#22(2026-07-08 复刻 wave-1 入池,**首批带算力档**)

> 两条都经 lab 复刻+live 双重验证+用户人评(console 0 错/减动分支/触摸降级);成品已 promote 进
> **tracked 的 `testbed/material/`**(2026-07-08 用户拍板,同 chassis 留底逻辑,见其 README)。
> **🏷 毕业条目带机制标签;agent 消费契约(过滤链/同批禁同机制/理由落笔/先枚举,行序无优先级)
> = `threed-pool.md` §机制标签(库级 canonical),本池同守。**
> #21 🏷:驱动=pointer · 机制=双速 quickTo 跟随+活坐标读数(◎环/✚轴线双变体) · 载体=无关(全页
> overlay) · 内容=无关 · register=instrument/dev-tool/brutalist。
> #22 🏷:驱动=load/replay(可移植 hover) · 机制=SVG goo filter 融合(blur+colorMatrix) · 载体=
> loader/入场(可移植 nav/微交互) · 内容=任意矢量形 · register=有机/playful。

| # | 效果 | 手感 | 适合 | 实现(source + lab demo) | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 21 | **坐标指针** coordinate cursor(两 variation:◎圆环 / ✚十字轴线[用户 2026-07-08 点做]) | 点+环双速跟随、活 XY 坐标读数、hover 变形——整页像台仪器;轴线版=全幅细线交叉于指针 | dev-tool / instrument / brutalist register | `gsap.quickTo` 双速(官方 docs;vendored `gsap-performance` 有同款模式);**matchMedia 条件必须互斥全覆盖**(粗指针/细无减动/细减动——独立布尔全 false 会静默不启动);**居中只用一套机制**(CSS 负 margin 与 GSAP xPercent 叠加=恒定半尺寸偏移,人评实抓的 bug);lab demo `testbed/material/cursor-xy/`(探针 0px 双模式验证) | **轻**(纯 transform;headless 实测 223fps=机制证明非 vsync 数) | web-verified(GSAP docs)+站锚 Studio Dialect 【⚙执行册】 |
| 22 | **goo loader 入场** | metaball 融合 blob loading → 聚拢定格 → 内容揭示 | loading / section 入场;有机、品牌感 | SVG goo filter(feGaussianBlur→feColorMatrix,**canonical=CSS-Tricks Gooey Effect**)+GSAP timeline(结构参照 Codrops Jump Loader——注:该教程本身**无** goo 技法,goo 配方源=CSS-Tricks);lab demo `testbed/material/goo-loader/` | **轻-中**(SVG filter 逐帧 raster——**filter 只罩小盒、绝不全页**;fallback:减 blob/缩 filter 盒/去 filter) | web-verified(CSS-Tricks+Codrops;用户 2026-07-08 点名 goo 方向) 【⚙执行册】 |

## 视频/canvas 叠加层 #23(2026-07-09 arknights-hero promote 入池)

| # | 效果 | 手感 | 适合 | 实现 | 算力档(初标) | provenance |
|---|---|---|---|---|---|---|
| 23 | **离线烘焙轨迹锁定框** tracking-lockbox overlay | 方框+十字+引线+编号追着视频里的目标飞;EMA 滞后=刻意的"传感器追踪"手感;配色随页面状态实时切换;**v2 双档**:primary 常显 / hover 档(kind:'hover',指针靠近才浮现临时锁定、虚线框区分、离开淡出) | 视频/canvas hero 的"目标锁定/HUD"层;军工/档案/analyzing register;hover 档=「hover 单目标弹锁定」交互 | 离线 cv2(亮度阈值→连通域质心→最近邻关联)烘焙关键帧 JS 数组,**运行时零 CV**:`video.currentTime`→帧号→线性插值→cover-fit 逆映射→EMA 平滑;DOM 元素 transform 定位 + `classList.toggle` 切态色;hover 命中=指针到框心距离 < max(110, 框边·0.9);lab demo `testbed/material/blueprint-video-wipe/`(tickOverlay 段+头注)。⚠ DOM 叠加层会与素材烧录文字撞位——叠之前先查素材自带 UI | **轻**(DOM transform ×N,重活全在离线烘焙) | **lab-built**(2026-07-09,用户签收;hover 档同日 approve;提取工具记录见该件 VERIFY.md) 【⚙执行册】 |

## 入场与滚动叙事 #24–#25(2026-07-09 arknights-hero 二期入池,用户逐项 approve)

| # | 效果 | 手感 | 适合 | 实现 | 算力档(初标) | provenance |
|---|---|---|---|---|---|---|
| 24 | **光条 logo 入场** light-bar logo reveal | 垂直光条幕(中心密两侧疏、上下两组、高频闪烁)中字标从中缝向两侧揭开,下划线扫出、小字随后;~3s 光条收敛、整体淡出还台 | 品牌站/游戏站/发布会页的 logo/标题入场;科技/档案 register | 26 条渐变光条 div(随机宽高位,幂律偏中心)+ GSAP timeline:bars scaleY stagger(from:'random')+ repeatRefresh 闪烁;字标 `clip-path: inset` 揭示 + letter-spacing 收拢;播完 `root.remove()` 自删;reduce=静态显示一次 opacity 淡出;`?logohold` 定格调试;lab demo `testbed/material/blueprint-video-wipe/`(initLogo 段;机制参照原片 t≈10.7–11.3) | **轻**(纯 DOM/CSS transform+opacity,一次性,播完自删零残留) | **lab-built**(2026-07-09,用户 approve) 【⚙执行册】 |
| 25 | **产品爆炸分解图** scroll-driven exploded view | 往下滚=部件错峰散开成爆炸图(每件飞到位浮现引线+编号),往回滚=重新组装;镜头随分解缓推;hover 部件加粗高亮;ASM % 实时计数 | 硬件/产品页的结构展示招牌位;电商产品拆解叙事;档案/工程 register | 部件=`{图形, 爆炸位移+旋转, callout 锚}` 数据表;scroll p → 每件 `smoothstep(clamp(p·1.18−i·0.022))` 错峰插值;callout 骑部件组内随飞、pi>0.72 渐现;`scrollRestoration=manual` 刷新必从组装态;reduce=定格全爆炸;纯 vanilla 零依赖;lab demo `testbed/material/exploded-diagram/`(机制参照原片 t≈17)。**⚠ 素材槽约定(用户判词):demo 素材=占位手绘仅证机制,商用必须换素材**——①设计师分层 SVG(替换 PARTS 表)②切件 PNG(path 换 `<image>`)③真 3D 走 three(另立);cv2 半自动提取实验过=60 分原型方案(记 VERIFY) | **轻**(SVG transform ×13,无持续动画,静止零开销) | **lab-built**(2026-07-09,机制 approve;素材=占位,商用换) 【⚙执行册】 |

## 分类索引交互 #26(2026-07-08 毕业站级锚,2026-07-11 用户批准编号)

| # | 效果 | 手感 | 适合 | 实现 | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 26 | **folder 抽屉索引** folder-works spotlight | hover=聚光:他者褪色+被指 folder 微提拉(抽屉自然叠序)+扇形预览冒头;click 展开 | 分类/作品索引——任何"抽屉式分类入口";playful 编辑/杂志感 | spotlight 他者褪色+微提拉+扇形预览+**backdrop 孪生防露底**(inset:0 不动的同色同形垫底,R-D v3 实证 6/6 零露白);lab demo `testbed/material/folder-works/`(v3) | **轻**(纯 DOM transform/opacity) | 站级锚 Wildy Riftian 升档:学隐喻不抄实现(Framer 产物,与 lab 栈不同源);lab 重建 + 用户两轮截图证据人批(2026-07-08) 【⚙执行册】 |

## DOM 通用显影/淡出 #27(2026-07-11 lab 自产人批 — Averonel new-flow 评估 run 回流)

| # | 效果 | 手感 | 适合 | 实现 | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 27 | **CSS 网格 mask 显影/淡出** grid-mask dissolve | 与纸底同色的瓦片网格按列扫描带+每瓦随机抖动依次熄灭(显影)或亮起(淡出),内容"像素块"级溶入/溶出纸面 | 任意 HTML 组件的入场显影/退场淡出(图/record/纯文字皆可)——M-38 像素扫描语言的 DOM 通用近似;技术/档案 register | 纯 DOM:JS 建 ~20px 瓦片 grid overlay(>2600 瓦自动翻倍格径)+CSS steps 关键帧(45% 熄→62% 回闪一拍→100% 熄)+列基线延迟×0.028s+随机抖动 0.22s;IO 进视口触发;reduced-motion 整层不渲染;✅`material/css-grid-mask-reveal` | **轻**(纯 DOM opacity,瓦片数兜底) | **lab-built 人批**(2026-07-11,Averonel 评估 run 产出,用户原话「这个css可以promote 进素材库，进ledger」;M-38 的 shader hash 闪烁以 steps 回闪**诚实降级**) 【⚙执行册】 |

## register→bento 结构组件 #28(2026-07-18 lab 自产人批 — Averonel option-2 run 回流)

| # | 效果 | 手感 | 适合 | 实现 | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 28 | **bento-register 卡片墙披露** register→bento card wall | 平表/register 的每行升成一张有分量的卡:bento 网格跨度节奏+点击展开细节(grid-rows 0fr→1fr 原生过渡,singleOpen 互斥"一次审一条");editorial 排版=声明卡读感,civic 排版=档案卡读感——**皮肤全在消费者 CSS,模块零视觉** | 稀内容平表(条款/规格/服务清单)的结构级升维——比数据行更像 hero 级展示;register/档案/编辑 chassis 皆可 re-token | 结构组件非编排:`bento-register.js` 只管 click/keyboard 披露协调+aria(expanded/controls)+互斥+teardown;**无 GSAP**,CSS-first(`grid-template-rows` 过渡,reduced-motion 关过渡但披露照常);布局=消费者 CSS grid 配方;✅`material/bento-register` | **轻**(纯 DOM,零 RAF) | **lab-built 人批**(2026-07-18,Averonel option-2 产出;lab demo headless 22/22;气质试演 `bento-audition` 双版真 chassis 对比,用户原话「**同意variation a**」= editorial 声明卡方向;⚠展开改 owner 高度=结构件,**永不入 atomic 候选**,component-tier 合同走 contracts §6) 【⚙执行册】 |

## 文字动效·外源复刻 #29(2026-07-19 react-bits 复刻,用户 eyeball 过)

| # | 效果 | 手感 | 适合 | 实现 | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 🗑 29 | **字符滑窗洗牌** char slide shuffle | 每个字符在裁窗里滑过一串复本落回真字,奇偶双批错峰;可乱码复本+染色渐变/random 延迟/loop 循环/hover 重洗 | 标题·短语入场;科技/档案/像素·arcade register;与 #4 Scramble 互补(字符**位移滑过**非原地替换) | 每字 overflow:hidden 定宽 wrap+平移 strip([复本×rolls+真字],right/down 重排提头垫尾),SplitText chars(smartWrap)+ScrollTrigger 入场(threshold/rootMargin 换算)+evenodd(偶批在奇批 0.7 处入场)/random maxDelay;colorFrom→To 同拍;播完 cleanupToStill 还原静态+armHover 重洗;🗑 已出库(原 `material/char-slide-shuffle`)(4 行参数轴 demo) | **轻**(纯 transform;字符数×(rolls+1) DOM 克隆,播完即收) | **web-verified 复刻**(react-bits `Shuffle` 真源码 React→vanilla 逐字,源存 runs `_src/`;**License=MIT+Commons Clause**:产品内用✅/组件本体再分发❌;用户 eyeball 过 2026-07-19) · **出库理由=许可**:上游 react-bits 为 **MIT + Commons Clause** —— 组件本体(单独/打包/移植版)**不得出售、sublicense 或再分发**,本行早已记录该约束;另 manifest 自记 **SplitText 历史上是 Club GreenSock 付费插件**(demo 走公共镜像)。**用户 2026-08-19 裁定出库**(另评:质量一般、0 处生产消费)。**行保留、徽章已摘、registry 记录已撤。** |

## 步骤节点轴 #30(2026-07-18 lab 自产人批 — Averonel option-2 run 回流,2026-08-01 补登记)

| # | 效果 | 手感 | 适合 | 实现 | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 30 | **步骤节点轴** scroll step axis | 编号步骤列表左侧长出一条 commit-graph 式垂直节点轴;自然滚动(无 pin),约 40% 视口高的「阅读线」扫过——到行高亮、节点空心→实心、段填充;默认双向(上滚回退),`accumulate` 保留单调 commit-log 模式 | 流程/步骤/时间线区段;工艺·档案 register;要"顺序+进度可见"而不想 pin 页面时 | reading-line = `innerHeight×opts.line` 对每行 `getBoundingClientRect` 判定;rows/nodes/segs/line 全消费者 DOM,模块 layout-agnostic 只管 class 切换;✅`material/scroll-step-axis`(M-56) | **轻**(无 canvas,class/颜色切换) | **lab 自产人批**(Averonel option-2 Phase D SPEC v9 §1.2 回流,用户 eyeball 过;B10 标准形态 verified `ac6ce83` 批)【⚙执行册】 |

## 横轨卡片走廊 #31(2026-07-18 lab 自产人批 — Averonel option-2 run 回流,2026-08-01 补登记)

| # | 效果 | 手感 | 适合 | 实现 | 算力档 | provenance |
|---|---|---|---|---|---|---|
| 31 | **横轨卡片走廊** pinned horizontal rail | section 钉住,竖滚 1:1 驱动卡片横移;progressBar/counter 报进度;卡片视觉全走消费者 tokens(`--phr-*`) | 服务/作品卡片走廊;要横向叙事又不想真横滚时;⚠ pin+scroll-jack 独占页面滚动,一页至多一个主滚动编排(taste §8) | ScrollTrigger pin(scoped to section,spacer 自插拔)+ scrub translateX(transform-only);destroy 干净;✅`material/pinned-horizontal-rail`(M-57) | **轻**(纯 transform scrub) | **lab 自产人批**(Averonel option-2 Phase D SPEC v9 §1.1 回流,用户 eyeball 过;B10 像素门 honest-exempt[GSAP scrub-lag 不可 harness-确定,css-grid #11 族] `ac6ce83`)【⚙执行册】 |

## 站级观察锚(👁 anchor-only — 人批入池 2026-07-07,用户亲选亲判)

> 与上面两档不同:这些站**无可读教程源码**(production 压缩码或 Framer 平台产物),所以**不给
> GSAP 实现列、不算 web-verified 实现范本**——只是"人看手感/找方向"的站级锚。要落地时仍走
> 上面 #1–#20 的实现路径或 `three/*`。引擎标记 = 我 curl 页面 grep 到的事实。

| 站 | 学习点(用户原话要点) | 引擎标记 | 注意 |
|---|---|---|---|
| Studio Dialect(https://studiodialect.com) | **鼠标 XY 坐标跟踪**元素;用户明判**其余部分不值得学** | WebGL+GSAP(同栈) | 只取单点,勿整站参照。**已升 3 档 → #21**(2026-07-08) 【⚙执行册=anchor-studio-dialect】 |
| Wildy Riftian works 页(https://www.wildyriftian.com/works) | **folder 文件夹的视觉隐喻+交互**(作品索引构图) | Framer 平台 | 学隐喻不抄实现(Framer 产物,与 lab HTML+GSAP 栈不同源;taste 红线依旧:GSAP/Three 不与 Framer 混树)。**已升 3 档 → 正式编号 #26**(2026-07-08 升档;2026-07-11 用户批编号,执行档案在 #26 行)。**🏷**:驱动=hover/click · 机制=spotlight 他者褪色+微提拉(抽屉自然叠序)+扇形预览冒头+backdrop 孪生 · 载体=分类/作品索引(任何"抽屉式分类入口") · 内容=图或 file 抽象形 · register=playful 编辑/杂志感 【⚙执行册=anchor-wildy-folder-works】 |
| Orlion Studio contact 页(https://www.orlionstudio.com/contact) | "Drop me something" 段的 **loading 动画** | webgl | 单点锚 【⚙执行册=anchor-orlion-loading】 |
| Studio K95(https://www.k95.it) | 整体优秀(用户判,未指明单点;意大利 Catania 传播/平面 agency) | webgl | 站级泛锚,brief 相似时人工翻看 【⚙执行册=anchor-studio-k95】 |

> **算力档(2026-07-08 起新增维度)**:新入池效果应带算力档初标(轻/中/重+弱机 fallback,定义见
> `threed-pool.md` §算力档)——hero 卡顿 = hero 失职;#1-#20 已随 2026-07-11 毕业按真码核算回填(见各档 🏷 行 ⚡ 与件内 TAGS.md)。

## 成长(能力诚实,见 `reference-sources.md` §5)
**我没法靠"看"动效来更新本池**——没有直接感知运行动画的能力。我只能在**读到真源码**时(桶 C:Codrops/GSAP/原生,有可读实现)提候选,且动效好不好仍由**人 / 打分器 `interaction_quality`** 判。所以 motion-pool 是最依赖"有没有代码 + 人评"的池,**绝不自动写回**。

**入池记录**:2026-07-03 「整页滚动编排」#11–#20 入池(用户全批;gsap-ecosystem Track B)。web-verified 条目源自 6 个 Codrops/GitHub 真源码 repo(桶 C 流程,源码全读);seamora-observed 条目源自 jesus-site 复刻(pattern 外部观察/代码自产,**经人批**以弱一档标签收录——"自产不自动入库"红线未破,走的是人批通道)。
**升级记录**:2026-07-05 应用户要求("seamora 复刻未经多轮微调,不能当可学习的成熟范本"),原 seamora-observed 条目(#11–14/#20 + #15 佐证)全部重锚到外部真源码——官方 CodePen GreenSock demo + codrops repo,jesus-site 源码指针全部移除。唯 #12 的完整编排组合无外部教程:机制锚官方 demo(pin+scale+scrub),编排组合诚实保留 seamora-observed 注记。
