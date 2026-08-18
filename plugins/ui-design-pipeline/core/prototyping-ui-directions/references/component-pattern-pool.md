# 组件模式池(component-pattern-pool)— 指针,不是清单

> ⚠️ **这是"去哪找组件代码"的指针表,不是组件清单,也不是菜单。** 用在 `prototyping-ui-directions` Stage 1 /
> `anchor-prototype-wave` 授权 surface 时:知道某类交互(动作/输入/导航…)的**可复用代码在哪个 registry**,
> 而不是从零手搓。组织轴 = **工作流类别**(借 `design-system`(companions) skill 的组件分类当结构,**不 fork 它**)。
> 与 `reference-sources.md` 桶 B(代码组件库)+ `shadcn-registry` skill 同源;此表是按"工作流类别"重切的入口。

## Schema / 约定
- **组织轴 = 6 工作流类别**(不是按 registry):Actions / Input / Navigation / Containment / Data-Display / Feedback。
- 每类给:**典型组件** · **去哪拿(registry 指针)** · **engine / consumer**。**不列穷举组件**,只给入口。
- **engine 三标**(同 `reference-sources.md` §0):
  - `readable-code` 🤖 — 我能直接读源码(shadcn / Radix / Ant / Carbon),port 进 chassis+taste。
  - `tsx-direct` — Framer Motion registry(桶 B),只进 **TSX** variant。
  - `interpret-to-gsap` — **HTML** variant 只借手法、动效转 GSAP(见 `motion-pool.md`),**绝不冒充直接抄**。
- **cap ≈ 2-4 指针/类**(防洪水;这是入口不是仓库)。

## ⚠️ 铁律 · 结构 ≠ 动效(honesty)
静态 registry / DESIGN.md 给的是**组件结构 + token 用法**(**无动效**)。组件"怎么动"是另一回事 →
一律去 **`motion-pool.md`**(GSAP recipes)。本池只指"结构去哪拿",**不描述动效**;别把 registry 的
Framer demo 当"能直接抄的 HTML 动效"(它是 React,HTML variant 只能 `interpret-to-gsap`)。

## 6 类 × registry 指针

| 类别 | 典型组件(示例,非穷举) | 去哪拿(registry 指针) | engine / consumer |
|---|---|---|---|
| **Actions** | button · icon-button · button-group · dropdown-menu · FAB | shadcn(button / dropdown-menu)· Radix Primitives · Ant / Carbon | `readable-code` 🤖 |
| **Input** | input · textarea · select · combobox · checkbox · radio · switch · slider · date-picker · form | shadcn(form / input / select …)· Radix · React Hook Form(校验逻辑)· Ant / Carbon | `readable-code` 🤖 |
| **Navigation** | navbar · tabs · breadcrumb · pagination · sidebar · command palette · menubar | shadcn(tabs / navigation-menu / command)· Radix · 桶 B(Aceternity/Magic UI 的动效 navbar) | `readable-code` 🤖 / 桶 B `interpret-to-gsap` 🤝 |
| **Containment** | card · dialog · drawer · sheet · accordion · collapsible · popover · tooltip | shadcn(dialog / drawer / accordion / popover)· Radix · Vaul(drawer) | `readable-code` 🤖 |
| **Data-Display** | table · data-table · list · badge · avatar · stat · chart · tree · calendar | shadcn(table)· TanStack Table(表格逻辑)· Tremor(charts)· Ant / Carbon | `readable-code` 🤖 |
| **Feedback** | toast · alert · progress · spinner · skeleton · empty-state · confirm-modal | shadcn(sonner / alert / progress / skeleton)· Radix | `readable-code` 🤖 |

> **动效来源(所有类共用)**:上表给的是**结构**。要"这个 card/toast/tab **怎么进场 / 怎么切换**" →
> `motion-pool.md`(#1–#20 GSAP recipes:文字动效 + 整页滚动编排)。桶 B(Aceternity / Magic UI / React Bits)有炫动效但 = **Framer/React**:
> TSX variant 可 `tsx-direct`,HTML variant 只 `interpret-to-gsap`(读手法 → GSAP 重写),**标出,绝不冒充直接抄**。

## 用法提示
- Stage 1 / 授权 surface 时,先按**要做的交互属于哪一类**查本表 → 拿 registry 指针 → 走 `shadcn-registry`(**本包不随发 = 提名**;lab checkout 在 `vendor/shadcn-registry`,装不到就记 `companion_skipped: shadcn-registry` 并手动走 registry 页)装(桶 B 走同 skill 的 registry 安装路径),别手搓。
- 拿到的是**结构**;套上 chassis 的 token(color/type/space via `--token-*`)+ 过 `taste-skill` 门 + 动效走 `motion-pool`。
- **不 fork `design-system` skill**(它与 prototyping 重叠):本表只借它的**工作流分类结构**当组织轴,组件代码仍去 registry 现拿。
- 第一方系统(Ant Design / IBM Carbon)组件代码 T1 可读(🤖),比社区 registry 更权威——需真 token 值时 WebFetch 其 docs 逐一坐实(别凭记忆写 hex/px)。

## 成长(human-gated,见 `reference-sources.md` §5)
- **能数据化提候选**:registry 是外部可信标准(维护中 + canonical),我能从真站/真 repo **抄出真 registry 指针**提议(`web-verified`)。
- **但入库仍人为把关**:我 surface 候选(类别 + registry + URL + engine 标),**你定加不加**;cap(≈2-4/类)是洪水阀。
- **自产组件不当 standard**:wave 里跑出的好组件 ≠ 行业范本,不自动回填本池(同 `reference-sources.md` §5 红线)。
