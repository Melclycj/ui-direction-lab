# three/ — Three.js / WebGL 能力层(vendored + 1 件 lab 自写)

Three.js 是这个 lab 的 **canvas/3D 引擎**。这组 = 10 个 vendored 基础 skill(讲「**怎么把 Three.js 写对**」,
API/cleanup/perf = HOW)+ **1 个 lab 自写件**补真空(粒子阵型 morph / scroll→canvas 桥 / 鼠标视差)。
**什么时候该上 3D / 上哪种(品味 + 政策 = WHEN)由 `authoring/taste-skill` §8 管**——两层不重叠。

## Provenance(出处)

- 来源:[CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) · commit `b1c6230`
  (`b1c623076c661fc9b03dac19292e825a5d106823`, 2026-01-19) · 收录日 2026-07-05
- License:**MIT**——⚠️ 上游**无独立 LICENSE 文件**(GitHub API `license: null`),MIT 仅在其 README
  §License 声明;逐字引用 + provenance 见同目录 `LICENSE-UPSTREAM.md`(不伪造上游没写过的 LICENSE 文件)。
- **verbatim 收录**:10 个 SKILL.md 一字未改(收录时抽查 fundamentals + interaction 与上游逐字 diff 一致)。
  要升级就锁新 SHA 从上游重新拉、覆盖即可——**别手改它们的正文**,否则就成了「上游 vs 我们的 fork」两个真相源。
- 弱信号(收录审查 2026-07-05 记录):上游仅 6 commits、无社区 PR 淬炼——所以收录记 SHA、抽查过真代码
  (对官方 three.js r160+ API 审过、有 disposal 专段)才收。同轮审查:`freshtechbro/claudedesignskills` **弃**
  (重叠 + 停更 + 与官方 gsap 8 件套两真相源冲突);`dgreenheck/webgpu-claude-skill` **browse-later**
  (质量最高但 WebGPU/TSL 栈超前,Chrome/Edge 113+ 门槛)。

## Vendored vs lab-authored(区分表——绝不冒充上游)

| Skill | 出处 | 管什么 |
|---|---|---|
| `threejs-fundamentals` | vendored | scene/camera/renderer 设置、Object3D 层级、坐标系、transforms |
| `threejs-geometry` | vendored | 内置形状、BufferGeometry、自定义几何、instancing |
| `threejs-materials` | vendored | PBR/basic/phong/shader 材质、材质属性与性能 |
| `threejs-lighting` | vendored | 灯光类型、阴影、环境光/IBL、灯光性能 |
| `threejs-textures` | vendored | 纹理类型、UV、环境贴图、纹理设置与优化 |
| `threejs-animation` | vendored | keyframe/骨骼动画、morph targets、AnimationMixer、混合 |
| `threejs-loaders` | vendored | GLTF/纹理/HDR 加载、async 模式、加载进度 |
| `threejs-shaders` | vendored | GLSL、ShaderMaterial、uniforms、自定义效果 |
| `threejs-postprocessing` | vendored | EffectComposer、bloom、DOF、屏幕空间效果 |
| `threejs-interaction` | vendored | raycasting、controls、鼠标/触摸输入、拾取 |
| **`threejs-scroll-stage`** | **lab-authored(非上游!)** | 粒子阵型 morph(Points/BufferGeometry)、scroll→canvas 桥(ScrollTrigger progress)、鼠标视差相机、cleanup 全链、reduced-motion、chassis token derive |

## 诚实缺口声明(为什么要自写 1 件)

vendor 审查(2026-07-05)发现:CloudAI-X / freshtechbro / dgreenheck **三家全都不覆盖**本 lab 真空区的核心三件——
**粒子阵型 morph、scroll→canvas 桥、鼠标视差**(恰是 jesus-site 复刻验证暴露的 2/10 招牌档效果的构件)。
→ `threejs-scroll-stage` 由 lab 自写,学习源=**外部成熟代码**(three.js 官方 examples / Codrops Cinematic 3D
scroll / GreenSock 官方文档,每 pattern 附引用),jesus-site 只当"栈能做"的结构参照、不当学习源。

## 3D 路由 + 与 gsap-* 的分工(3D 服从 2D 既有规矩)

| 层 | 谁管 |
|---|---|
| **DOM 动效** | `gsap-*`(canonical) |
| **canvas/3D 内容** | **本组 `three/*`(canonical)** |
| **页面编排/驱动端** | GSAP ScrollTrigger(canvas 只收 progress,不自己听 scroll) |

- 页面编排仍由 **GSAP ScrollTrigger** 驱动;canvas 通过 `setProgress(p)` 之类接口**只收 progress**。
- 3D 颜色(灯光/材质/粒子)从 **chassis token 取**(derive-not-invent),不自发明色。
- **单一 RAF**:Three 渲染循环与 GSAP 合流(gsap.ticker 或单 RAF),**禁双循环**。
- reduced-motion:`prefers-reduced-motion` → 静态帧分支。
- 🔴 **红线(沿用 taste-skill)**:同一组件树里**绝不**混用 GSAP/ThreeJS 和 Framer Motion;
  Three 对象一律走严格 cleanup(geometry/material/renderer.dispose + 事件解绑)。

## SSOT 边界

| 层 | 谁管 |
|---|---|
| 上不上 3D、什么风格(WHEN / 品味) | `authoring/taste-skill` §8(路由行「3D/Canvas → ThreeJS/WebGL」在此落地) |
| Three.js 怎么写对(HOW / API) | **本组 `three/*`(canonical)** |
| 招牌 scroll-driven 3D stage 怎么搭(pattern) | `threejs-scroll-stage`(纯实现:Quick Start + Pattern 1-7 + 其 pattern 相关 anti-pattern) |
| **跨切面陷阱 + 3D 验证纪律**(任意 three+GSAP+GLSL demo 通用,非某一 pattern 专属) | **`three/GOTCHAS.md`**(2026-07-09 从 scroll-stage 拆出,保持后者聚焦) |
| DOM 动效 HOW | `gsap-*`(见其 README SSOT 表) |

## Vendored 件外挂标注(annotate-not-edit——正文一字不改,缺口记这里)

- **`threejs-lighting`(2026-07-07 rematch 消费实测)**:skill 示例的 intensity 值(~1-2)在
  `MeshStandardMaterial` 下渲染结果**明显偏暗**——diffuse 贡献有隐式 `1/π` Lambert 归一化
  (r155+ 物理灯光语义),需要按实际渲染回调 intensity;且 three-point-lighting 示例里 fill light
  放主体**背面**时只照亮相机看不见的半球。写暖/冷 studio 布光时:intensity 靠 live 截图
  反推标定,fill 位置保证在相机可见半球。(来源:R1 rematch subagent 实测,截图证据在其 run)

## 诚实边界(canvas 验证回路,用户 2026-07-03 已接受)

canvas 的验证回路**结构性断**:DOM 里只有 `<canvas>` 一行——validator 无文本可查、无 transform 可采样、
截图只有静帧。本组 skill 只保证「**写得对**」(API/cleanup/perf);「**好不好看**」永远人眼判(live demo + 人评)。

## 用法

不自动路由(Skill 工具不对 project-local skill 自动触发)。需要时由 parent / subagent `Read` 对应
`three/threejs-*/SKILL.md` 照做。入口惯例:fundamentals 起手 → 按需 geometry/materials/lighting →
效果件(shaders/postprocessing)→ 本 lab 招牌场景直接读 `threejs-scroll-stage`。

**谁在消费这套能力**:`core/prototyping-ui-directions`(Stage 3 motion 作图)和
`core/anchor-prototype-wave`(§Authoring: motion)在 brief/contract 要 3D 时读 `three/*`(条件守卫,见各自接缝注记)。

## 部署

这 11 件**随 `ui-design-pipeline` plugin 一起装**,不单独分发:

```
/plugin marketplace add Melclycj/ui-direction-lab
/plugin install ui-design-pipeline@ui-direction-lab
```

装完它们在 `${CLAUDE_PLUGIN_ROOT}/three/<name>/`,主 skill 按这个路径读。

⚠ 这 11 件是**成组**的——3D brief 触发时被主 skill 点名必读,所以刻意整组随包发
(不像 `gsap-*` 那样走提名:GSAP 上游自己就是个 plugin,这套的上游不是,见下)。
