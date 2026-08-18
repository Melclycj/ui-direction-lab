# 字体配对池(Batch 1 视觉参考 · typeface pairings)— 可选 base-case

> ⚠️ **这是兜底,不是菜单。** 仅在想不出更好字体方向时拿来当起点或参照,**不要求**从里面选。
> 用在 `prototyping-ui-directions` 的 **Batch 1(视觉方向)**——决定 typography 那一轴(配 `style-pool.md` 的 palette/布局)。
> 命名澄清:这是**字体(typeface)** 配对池;**文字怎么"动"** 是另一回事,见 `motion-pool.md`。

## Schema(每条配对带什么)
`vibe` · **display + body + mono** 三件套 · 每件 `family` + `来源(source)` + `免费/商用(free/commercial)` ·
**exemplar anchor**(谁用得最好,品味锚)· **provenance**(这条哪来的,诚实)· `notes`(含 taste 守则)。

**provenance 三标(诚实来源)**
- `web-verified` — 从真实 fetch 的文件/页面坐实(如 DESIGN.md corpus、字体官网)。
- `your-skill` — 本 lab 自己跑出来、已 live 验证、锁进 `testbed/chassis/` 的真实选择(最高可信)。
- `memory-candidate` — 模型记忆里的 canonical 名字,可靠但 URL/细节未逐一新搜;落地前应 verify。

## Taste 守则(不被本池豁免)
- **禁 Inter 作主字**(`taste-skill` 硬规则)。Vercel 等的 stack 里把 Inter 当 fallback——我们**不沿用**,主字用 Geist 等非 Inter grotesk,fallback 走 `system-ui`。
- **数字用 mono**(tabular/等宽),所以每条都给 mono 件。
- **从 chassis 的 type token 取值**(family/size/weight/tracking),不在页面里写死。
- **免费优先**:能用免费字达到效果就不上商用字;商用字只作"范本锚"标注,不要求购买。

---

## §1 · SaaS / developer-tool —— ★ SEEDED FROM REAL `DESIGN.md`(sample vibe,坐实非记忆)

这一档是这次的**样板**,数据来自真实 fetch 的 10 个 brand DESIGN.md(见 `reference-sources.md` 桶 A)。
**颗粒度:10 个 SaaS/dev brand 收敛成 3 档,brand 只作行内 exemplar 锚,不一厂一行。**

| 配对档 | family | 范本锚(真) | 来源 / 免费·商用 | 真实 token / 备注 | provenance |
|---|---|---|---|---|---|
| **免费首选** | **Geist** + **Geist Mono** | Vercel | Google Fonts · Fontshare · npm `geist` · **免费 OFL** | stack `Geist, system-ui`;Display XL 48/600/-2.4px;Body 16/400 | `web-verified` |
| **高级 grotesk(商用)** | Söhne / Circular / Linear 自有 | Stripe · Supabase · Linear | 商用/proprietary ↔ 免费替身 **General Sans**(Fontshare)/ **Hanken Grotesk**(Google) | Stripe 轻量大标题 weight 300 + `ss01`;Linear 仅暗色 | `web-verified` |
| **配角字(可选)** | Rubik / Instrument Serif | Sentry(Rubik)· Warp(Instrument Serif) | Google · **免费** | Rubik=友好圆润;Instrument Serif=dev 里加一点编辑感 | `web-verified` |

**推荐落地(免费优先,taste-clean)**:Display+Body = **Geist**(Vercel 同款,一族吃下)· Mono = **Geist Mono / JetBrains Mono**。
- ⚠️ **Inter 陷阱**:SaaS/dev 半数(Raycast / Notion=Notion Sans / Warp / Resend-UI / Mintlify / Supabase 替身)主字走 **Inter → taste 禁**。**只借它们的结构,不采字**;主字用 Geist,fallback `system-ui`。
- **IBM Plex 配对(e2b 同款,免费 OFL,taste-clean 的另一条 dev-tool 路子)**:body **IBM Plex Sans** + **IBM Plex Mono 作展示字**(等宽当标题 = 技术终端感,不只用于数字)+ mono 亦 IBM Plex Mono。Geist 之外的免费选择,非 Inter;accent 见 `palette-pool` 橙 `#ff8800`。`web-verified`(e2b=Playwright 实测)。

---

## §2 · 其余 vibe —— 种子行(部分已被本 lab 坐实 = `your-skill`)

| vibe | display | body | mono | 来源/免费 | 范本锚 | provenance |
|---|---|---|---|---|---|---|
| **新野兽派 / acid** | **Archivo Black** | **Archivo** | **Space Mono** | Google · 全免费 | 本 lab **Northway** fixture(acid·dark,已 live) | `your-skill`(`chassis/northway-brutalist`) |
| **有机/编辑 Didone(quiet-luxury)** | **Playfair Display**(高对比 Didone,可用 italic 作戏剧声) | **Manrope**(安静 grotesk) | **DM Mono** | Google · 全免费 | 本 lab **Grove** fixture(linen,已 live) | `your-skill`(`chassis/grove-linen`) |
| **杂志/奢侈编辑(commercial 高级)** | Canela / Tiempos Headline / GT Sectra | Tiempos Text / 同家 body | (无或 mono 数字) | 商用(Klim/Commercial Type/GT)↔ 免费替身 **Fraunces** / **Playfair** / **Instrument Serif** + body **Newsreader** / **Source Serif 4** | Hermès · Aesop · Vogue 类编辑奢侈(闭源大站→**诠释非复制**,`do-not-copy`) | `memory-candidate`(闭源逆向) |
| **奢侈汽车 / haute(dark dramatic)** | **Saira / Saira Condensed**(refined 窄体 grotesk;Bugatti 自带 fallback)↔ 商用 Bugatti Display / FerrariSans / LamboType | **Saira** / **Cormorant Garamond**(编辑衬线声,Bugatti serif fallback) | **JetBrains Mono** | Google · 全免费(商用字只作锚) | Ferrari · Lamborghini · Bugatti(黑底 + 单金属 accent) | `web-verified`(DESIGN.md)+ reverse-eng + `do-not-copy` |
| **极简/几何** | General Sans / Space Grotesk | General Sans / Hanken Grotesk | IBM Plex Mono | Fontshare / Google · 免费 | 极简产品站 | `memory-candidate` |
| **深色科技 SaaS(neon accent)** | Geist / Space Grotesk | Geist / Hanken Grotesk | Geist Mono / JetBrains Mono | 免费 | 开发者工具站(同 §1) | `memory-candidate`(§1 已坐实部分) |
| **编辑感 AI(AI-product)** | 衬线 display:Fraunces / Newsreader(免费)↔ Tiempos / PP Editorial(商用) | 几何 sans:Geist / General Sans / DM Sans | JetBrains Mono / Geist Mono | Google · Fontshare · 免费 | Claude · Mistral · xAI(暖珊瑚 accent,见 palette);⚠️ 6 个里 5 个用 Inter→只借结构不采字 | `web-verified` |

> **luxury 档(已 seed,2026-07-01)**:用"parse 真源"法坐实——**奢侈汽车/haute** 行 = Ferrari/Lamborghini/Bugatti 从真 DESIGN.md(`web-verified`);**编辑奢侈** 行锚 = Hermès/Aesop/Vogue(闭源大站→逆向,`memory-candidate` + `do-not-copy`,标"诠释非复制")。⚠️ **Ferrari 官方 fallback = Inter**(taste 禁)→ 只借结构不采字,display 用 Saira/Cormorant。dark-luxe 的字是"大 + 克制 + refined 窄体",**不是** Archivo Black 那种粗野。consumer:DESIGN.md token 🤖 我 parse / 闭源大站 live 视觉 👁 你看(只给 URL)。

## 用法提示
- Batch 1 的 variant 在 typography 轴拉开时,应换的是**字族的气质**(grotesk vs Didone vs 几何),不是同一字族换字重。
- 选了某档就把 family 写进 chassis 的 `--token-font-display/body/mono`,页面只引用 token。
- **免费源**:**Fontshare** / **Google Fonts** / **Fontsource(npm)** + **The League of Moveable Type**(theleagueofmoveabletype.com,开源 foundry,🤝)。
- 商用字(Söhne/Canela/Tiempos)只作锚,不要求买;其出处 foundry **Klim**(klim.co.nz,👁 你浏览,**贵 → browse-later** 存着)。
- **想看某字体的真实配对** → **Typ.io 反查**(👁,**带具体字体名去筛**,别逛无限灵感墙——那样低效)。

## 成长(human-gated,见 `reference-sources.md` §5)
字体能**数据化提候选**:我能从真站 / DESIGN.md 抄出真 family 提议(`web-verified`)。但**入库仍人为把关**——我 surface 候选(family + 来源 + 锚 + URL),**你定加不加**。库的主干应是 `web-verified` / canonical 这档**外部可信标准**;`your-skill`(如 `Northway`/`Grove`)是**内部验证记号、比 standard 弱一档**,只作"自家用过、可参照"留底,**不主导本池**。自产输出不因"跑得好"就当范本。
