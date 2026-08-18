# Slop Gates — 出稿前负面清单 + 六轴 pre-emit 自评（hallmark 适配版）

> 源：[Nutlope/hallmark](https://github.com/Nutlope/hallmark) `slop-test.md`（58 门，MIT）；verbatim 存档见 [`_vendor/hallmark-slop-test.md`](_vendor/hallmark-slop-test.md)（含 commit hash / 拉取日期）。
> 本文=**本仓适配版**：(a) 桶 = lab core 门（选门标准：本仓真实翻过车 / 最常见 AI 默认）；(b) 桶 = conditional 门；(c) 桶 = 不收门。58 门（1-57 + 38a）全覆盖，被裁的可对回 vendor 原文。
> **用法**：PUD Batch 出稿 = **每批一次** gate sweep（对本批共性）+ per-variant 六轴 stamp；APW Base Wave = **每 wave 扫一次** (a) 桶 + per-surface stamp。instruction-layer 自查，**非机器 gate**（不进 registry / sync / hook）。

## (a) Lab core 门 — 每门答案必须是 no（24 门）

门号沿用 hallmark 原编号，方便对回原文。

1. display 字体是 Inter / Roboto / Open Sans / Poppins / Lato / 系统默认？（font-pool「禁 Inter 主字」的扩面）
2. 任何地方出现紫→蓝（或 cyan→magenta）渐变——包括 `background-clip: text` 渐变标题？
3. 3 等宽卡片格 + icon-above-heading 瓦片？
4. 卡片套卡片？
6. hero 全居中 auto-fail：`min-height:100vh` 全居中，或 eyebrow / 标题 / lede / CTA 全在同一居中竖轴？（至多两个居中元素；eyebrow 或 CTA 必须离轴）
8. 复用不该复用的结构——generic AI 模板（Hero→3 features→CTA→footer），或与本项目上一个产出同一结构指纹？
9. 分节只靠等距空白，无 rule / 无 ornament / 无色变，节节同节奏？
10. 任何地方用 `transition: all`？（必须点名属性）
11. `hover:scale-105`（或任何统一 hover-scale）铺在多个不相关元素上？
13. 任一元素同时挂多于一个 hover 效果（translate + scale + shadow + color + rotate）？
14. 动画 `width` / `height` / `top` / `left` / `margin` / `padding`？（只动 transform / opacity）
15. focus ring 渐显？（必须瞬时出现——键盘用户要立即指示）
19. 占位名（Jane Doe / John Smith）或 startup 陈词（Acme / Nexus / Seamless / Unleash）？
24. 任何 padding / gap / margin 脱离命名 spacing 刻度（4px 倍数）？`padding: 17px` 就是 tell。
26. 交互元素缺 `:focus-visible` / `:active` / `:disabled` 任一态？
30. 混用两套以上 icon 库，或 emoji（✨🚀⚡🔥🎯✅）当 feature / step / pricing 图标？
37. 页面超过 3 个 `font-family` 家族？（display + body + 至多 1 outlier；同族不同字重算 1）
38a. 任何标题 / display 用斜体？（斜体只许做正文段内 emphasis；标题强调走字重 / accent 色 / 画线）
40. 任一 (color, background) 对不过对比阈值？body 4.5:1（APCA Lc≥60）；大字 / icon / focus ring 3:1（Lc≥45）
41. 最常翻车对比三连：按钮文字≈填充色（黑上黑）；accent 面上缺 `--color-accent-ink`；暗底分节没翻文字色（ink-on-ink）？
42. nav 是 AI 默认指纹（左 wordmark + 4-5 行内链接 + 右按钮 + 1px hairline + 白底）？
45. hero 装饰无语义锚点（漂浮 cursor / 无来由数字角标 / 随机 ornament）？装饰必须有动机。
46. 编造数据（"10× faster" / "trusted by 50,000+"）填 stat 位？用户没给的数字一律 `—` 占位或问回；裸数字不得独扛 hero。
54. eyebrow / 编号与标题同横排（tag-left, header-right）？auto-fail——eyebrow 只许竖排叠在标题正上方同列。

## (b) Conditional 门 — 命中条件才查（28 门，紧凑表）

| 门 | 条件 / 本仓重标定 |
|---|---|
| 5 | 用卡片列表时：禁粗色左右侧条 border |
| 7 | 纯 `#000` / `#fff` 作基色——**brutalist chassis 豁免**；纯白纸底对 modern-minimal 派亦允；其余风格禁 |
| 12 | overshoot / bouncy easing——仅物理隐喻交互允许；按钮 / modal / tooltip 等 UI 状态变化禁 |
| 16·17·18 | 含 toast / tooltip / 轮播时：可见效果不弹成功 toast；tooltip hover 800-1000ms、focus 0ms；轮播必须 hover+focus 暂停（WCAG 2.2.2） |
| 22 | 零 chroma 中性色——**Editorial Monochrome / Stripe 派豁免**；其余中性色最少 0.005 chroma 偏 anchor 色相 |
| 23 | accent 面积 >~5% viewport——**acid / atmospheric 类风格重标定**（bloom 即设计本体时可到 ~20%） |
| 25 | 有成段正文时：prose measure 45-75ch |
| 28·29·31 | hero 富化出现时：视频禁自动带声、必须 poster + `fetchpriority="high"`；抽象背景单 accent ≤5% 不动画；插画 hand SVG / 纯 CSS 优先于 Lottie |
| 33 | 有手绘装饰 SVG / canvas 时：必须 `aria-hidden="true"` 或 `aria-label` |
| 34·44·49 | 浏览器验证轮查（需真渲染）：320-1920 无横滚（fix = html+body `overflow-x: clip`）；hero 1280×800 折内完整；可点击文案任何宽度不折两行 |
| 35 | 用文字装饰（highlighter / underline）时视检位置：highlighter 压 x-height 不压 baseline；underline 1-2px、offset 1-2px |
| 36 | 混高 flex 行（按钮+文字 / icon+文字）必须 `align-items: center` + 内件 `line-height: 1` |
| 38 | 用 outlier 第三字体时：≤2 个 slot（wordmark + hero stat 是正典对） |
| 39 | 含表单时查 input 五态：border-width 恒 1px / focus 走 outline 非 border / input 高 = 按钮高（44px 底）/ helper 位 `min-height:1lh` / disabled 三通道 |
| 43 | 带真实 footer 时：禁 AI 默认指纹（4 列链接 + social 排 + 底部小版权 + 灰底） |
| 47 | 要展示产品截图 / 设备框时：禁手绘假 chrome（浏览器条 / 手机框 / 终端框）——用真截图或裸内容 |
| 48 | variant 用 `:root` token 体系时：颜色 / 字体不得中途脱 token 即兴（inline hex / 一次性 font-family = fail） |
| 50·51·53·55·56 | 命中对应 pattern 时：图像 grid track 用 `minmax(0,1fr)`；display 长词 `overflow-wrap:anywhere`；CSS radio tab 防 scroll-jump；全大写 display `line-height ≥1.0`；双 sticky top:0 错位 `--banner-height` |

## (c) 不收门 — 理由一词（6 门，紧凑表）

| 门 | 理由 |
|---|---|
| 20 | hallmark 专有（macrostructure stamp 机制）——本仓 stamp = 六轴 stamp（见文尾） |
| 21 | hallmark 专有（Specimen 主题目录 fall-through） |
| 27 | 重复 → 指针 [motion-pool 三纪律](motion-pool.md)（reduced-motion 分支已是本仓硬纪律） |
| 32 | hallmark 专有（component-cookbook variation knobs）——概念由 Variety 轴接管 |
| 52 | hallmark 专有（主题 section-head 覆盖体系） |
| 57 | hallmark 专有（study 动词 / studied-DNA，不在本次吸收范围） |

## 六轴 pre-emit 自评（出稿前跑，不是出稿后）

出稿**前**对计划中的产出逐轴打 1-5 分。**任一轴 <3 → 强制返工一轮再交人评**——别把已知弱点带进 gate sweep。
原话保留："Two passes is normal. Three is a sign the brief is wrong, not the design — re-read the brief."（两轮正常，三轮说明 brief 错了——回读 brief。）

| 轴 | 打什么分 | 本仓语境注 |
|---|---|---|
| **P** Philosophy | 页面有没有清晰的 *why*——一个立场？还是只是个 layout？ | 对应 variant 的一句 thesis |
| **H** Hierarchy | 2 秒内能否分出 primary / secondary / tertiary？ | |
| **E** Execution | 细节全在 spec 内吗（rule 粗细 / accent 足迹 / text-wrap / focus ring / 对比度）？ | 对应 (a) 桶实现类门 |
| **S** Specificity | 像*这个 brief*，还是"谁家都能用的页"？ | |
| **R** Restraint | 没挣到位置的装饰 / 冗余 / 凑数 padding 都删了吗？ | |
| **V** Variety | 与本项目此前产出共享结构指纹吗？**按结构距离打分，非视觉距离——换色不算 variety**（"colour-swaps don't count as variety"） | 直击 batched exploration「换皮」翻车：同批 variants 结构指纹必须互异 |

**Stamp 格式**（variant / surface 文件头注一行，随件走）：`/* pre-emit critique: P5 H4 E5 S4 R5 V5 */`
后续 run 应能找到这行、避免重复同一弱点。gate sweep 结果记 run-notes（每批 / 每 wave 一行：`slop sweep: pass` 或 `FAIL: 门号`）。
