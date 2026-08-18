---
name: threejs-scroll-stage
description: Lab-authored Three.js patterns for scroll-driven brand-site 3D stages - particle formation morphing (Points/BufferGeometry), ScrollTrigger-to-canvas progress bridge, mouse-parallax camera, full disposal chain, reduced-motion, chassis-token color derivation, and shard-constructed objects with pointer repulsion. Use when a page needs a signature 3D/particle scene choreographed by the page's GSAP scroll timeline.
---

# Three.js Scroll Stage (LAB-AUTHORED)

> ⚠️ **Provenance: this skill is authored by this lab. It is NOT part of the vendored
> [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) set** (see `three/README.md`
> distinction table). It fills the gap none of the audited upstream skill packs cover: particle
> formation morphing, the scroll→canvas bridge, and mouse parallax. Every pattern cites its
> external learning sources (three.js official examples / GreenSock official docs / Codrops).

## What this covers

The "signature scene" tier of high-end brand sites: a full-viewport (or hero) `<canvas>` whose
content — a lit 3D object with mouse parallax, or a few thousand particles morphing between
formations — is driven by the page's scroll position. This is the effect class that makes
visitors remember a site (Seamora-class scrollytelling).

Prerequisites: `threejs-fundamentals` (scene/camera/renderer), `threejs-geometry`
(BufferGeometry), `threejs-lighting` + `threejs-materials` for lit-object stages.

Formerly a known gap, now covered: *shard-constructed objects with per-piece pointer
repulsion* is **Pattern 7** below (built + live-verified in the 2026-07-08 rebuild wave).

## Ground rules — 3D obeys the 2D pipeline

These are lab law, not suggestions (they mirror the GSAP discipline in `animation/`):

1. **ScrollTrigger drives; the canvas only receives progress.** Page choreography stays in GSAP.
   The Three stage exposes `setProgress(p)` (p ∈ [0,1]) and never listens to scroll itself —
   no `window.scrollY`, no wheel listeners, no IntersectionObserver-as-scroll-driver.
2. **One loop.** The Three render loop joins `gsap.ticker`. Never run a second
   `requestAnimationFrame` loop next to GSAP's.
3. **Colors derive from chassis tokens** (`--token-*` CSS custom properties), never invented
   in JS. Fallbacks allowed for standalone testing only.
4. **Full cleanup or it didn't happen**: geometry/material/texture/renderer `.dispose()`,
   ScrollTrigger `.kill()`, ticker removal, event unbinding. SPA route change must leave zero
   WebGL contexts and zero listeners behind.
5. **`prefers-reduced-motion: reduce` gets a static frame**, not a slower animation.
6. 🔴 Never mix GSAP/Three and Framer Motion in the same component tree (taste-skill red line).

## Quick Start — minimal complete stage

A ~3000-particle formation morph, scroll-scrubbed, with mouse parallax and full teardown:

```javascript
import * as THREE from "three";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function createScrollStage(container) {
  // ---- tokens (Pattern 6) --------------------------------------------------
  const css = getComputedStyle(document.documentElement);
  const token = (name, fallback) => css.getPropertyValue(name).trim() || fallback;
  const bgColor = new THREE.Color(token("--token-bg", "#14150f"));
  const accent = new THREE.Color(token("--token-accent", "#bfe800"));

  // ---- scene ---------------------------------------------------------------
  const scene = new THREE.Scene();
  scene.background = bgColor;
  const camera = new THREE.PerspectiveCamera(
    50, container.clientWidth / container.clientHeight, 0.1, 100);
  camera.position.set(0, 0, 6);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // ---- particles (Pattern 1) ----------------------------------------------
  const COUNT = 3000;
  const formations = [makeSphere(COUNT, 2), makeGrid(COUNT, 4), makeHelix(COUNT, 2, 4)];
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(formations[0]); // working copy
  const posAttr = new THREE.BufferAttribute(positions, 3);
  posAttr.setUsage(THREE.DynamicDrawUsage); // re-uploaded every scrub frame
  geometry.setAttribute("position", posAttr);

  const material = new THREE.PointsMaterial({
    color: accent, size: 0.025, sizeAttenuation: true,
    transparent: true, opacity: 0.9, depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  const points = new THREE.Points(geometry, material); // ONE draw call for all 3000
  scene.add(points);

  // ---- progress bridge (Pattern 2) ------------------------------------------
  let progress = 0, progressDirty = true;
  function setProgress(p) { progress = p; progressDirty = true; }

  function applyProgress(p) {
    const segs = formations.length - 1;
    const s = Math.min(Math.floor(p * segs), segs - 1);
    const t = p * segs - s;
    const e = t * t * (3 - 2 * t); // smoothstep easing per segment
    const from = formations[s], to = formations[s + 1];
    for (let i = 0; i < positions.length; i++) {
      positions[i] = from[i] + (to[i] - from[i]) * e;
    }
    posAttr.needsUpdate = true;
  }

  // ---- parallax (Pattern 3) --------------------------------------------------
  const pointer = { x: 0, y: 0 };
  function onPointerMove(ev) {
    pointer.x = (ev.clientX / window.innerWidth) * 2 - 1;
    pointer.y = -((ev.clientY / window.innerHeight) * 2 - 1);
  }
  function onResize() {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  }
  window.addEventListener("pointermove", onPointerMove);
  window.addEventListener("resize", onResize);

  // ---- single loop on gsap.ticker (Pattern 2) --------------------------------
  function render(time, deltaMS) {
    const dt = deltaMS / 1000;
    if (progressDirty) { applyProgress(progress); progressDirty = false; }
    const damp = 1 - Math.exp(-4 * dt); // frame-rate-independent lerp factor
    camera.position.x += (pointer.x * 0.6 - camera.position.x) * damp;
    camera.position.y += (pointer.y * 0.4 - camera.position.y) * damp;
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
  }

  // ---- reduced-motion split (Pattern 5) ---------------------------------------
  const mm = gsap.matchMedia();
  mm.add("(prefers-reduced-motion: reduce)", () => {
    applyProgress(1);                    // settle on the final formation
    renderer.render(scene, camera);      // exactly one static frame
    return () => {};
  });
  mm.add("(prefers-reduced-motion: no-preference)", () => {
    const st = ScrollTrigger.create({
      trigger: container, start: "top top", end: "+=300%",
      pin: true, scrub: true,
      onUpdate: (self) => setProgress(self.progress),
    });
    gsap.ticker.add(render);
    return () => { st.kill(); gsap.ticker.remove(render); };
  });

  // ---- teardown (Pattern 4) ----------------------------------------------------
  function destroy() {
    mm.revert(); // kills ScrollTrigger + removes ticker via the cleanup returns
    window.removeEventListener("pointermove", onPointerMove);
    window.removeEventListener("resize", onResize);
    geometry.dispose();
    material.dispose();
    renderer.dispose();
    renderer.domElement.remove();
  }

  return { setProgress, destroy };
}
```

---

## Pattern 1 — Particle formation morph (Points / BufferGeometry)

**Learning sources**: three.js official examples
[`webgl_points_waves`](https://threejs.org/examples/#webgl_points_waves) (Points + per-frame
position writes + `needsUpdate`),
[`webgl_buffergeometry_custom_attributes_particles`](https://threejs.org/examples/#webgl_buffergeometry_custom_attributes_particles)
(BufferAttribute discipline),
[`webgl_points_dynamic`](https://threejs.org/examples/#webgl_points_dynamic) (morphing a point
cloud between model targets); docs:
[BufferGeometry](https://threejs.org/docs/#api/en/core/BufferGeometry),
[BufferAttribute](https://threejs.org/docs/#api/en/core/BufferAttribute).

### Formation generators

Precompute every formation ONCE as a `Float32Array(count * 3)`. Generators are pure functions —
they run at init, never in the render loop.

```javascript
// Fibonacci sphere — uniform distribution, no pole clustering.
function makeSphere(count, radius = 2) {
  const a = new Float32Array(count * 3);
  const golden = Math.PI * (Math.sqrt(5) - 1);
  for (let i = 0; i < count; i++) {
    const y = 1 - (i / (count - 1)) * 2;          // 1 → -1
    const r = Math.sqrt(1 - y * y);
    const theta = golden * i;
    a[i * 3] = Math.cos(theta) * r * radius;
    a[i * 3 + 1] = y * radius;
    a[i * 3 + 2] = Math.sin(theta) * r * radius;
  }
  return a;
}

// Flat grid (logo-wall / matrix formation).
function makeGrid(count, size = 4) {
  const a = new Float32Array(count * 3);
  const side = Math.ceil(Math.sqrt(count));
  for (let i = 0; i < count; i++) {
    const x = i % side, y = Math.floor(i / side);
    a[i * 3] = (x / (side - 1) - 0.5) * size;
    a[i * 3 + 1] = (y / (side - 1) - 0.5) * size;
    a[i * 3 + 2] = 0;
  }
  return a;
}

// Helix / DNA ribbon.
function makeHelix(count, radius = 2, height = 4, turns = 3) {
  const a = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const t = i / (count - 1);
    const angle = t * Math.PI * 2 * turns;
    a[i * 3] = Math.cos(angle) * radius;
    a[i * 3 + 1] = (t - 0.5) * height;
    a[i * 3 + 2] = Math.sin(angle) * radius;
  }
  return a;
}
```

Text/logo formations: rasterize text to an offscreen 2D canvas, read `getImageData`, emit one
particle per dark pixel (sample down to your particle budget). Same idea as the official
point-cloud-from-geometry examples — the formation is just another `Float32Array`.

### Morphing

Piecewise-linear across N formations: progress `p ∈ [0,1]` selects a segment, a local `t` lerps
inside it. Ease the local `t` (smoothstep above, or any easing) so each formation "locks in"
instead of drifting past.

```javascript
const segs = formations.length - 1;
const s = Math.min(Math.floor(p * segs), segs - 1);
const t = p * segs - s;
const from = formations[s], to = formations[s + 1];
for (let i = 0; i < positions.length; i++) {
  positions[i] = from[i] + (to[i] - from[i]) * ease(t);
}
posAttr.needsUpdate = true; // flags the attribute for GPU re-upload
```

Organic variant: give each particle a per-particle delay/duration offset (stored in a second
`Float32Array`) so formations dissolve and reassemble instead of moving as one rigid body:

```javascript
// staggered per-particle timing: particle i uses tLocal = clamp((t - delay[i]) / dur[i])
const delay = new Float32Array(COUNT);
for (let i = 0; i < COUNT; i++) delay[i] = Math.random() * 0.3;
// in the loop: const ti = Math.min(Math.max((t - delay[j]) / 0.7, 0), 1);
```

### Performance discipline (~3000 particles)

- **One `THREE.Points`, one geometry, one material = one draw call.** Never one Mesh per
  particle (3000 draw calls kills mobile).
- **Zero allocation in the loop.** All `Float32Array`s (formations, working copy, delays) are
  preallocated at init. The render loop only reads/writes existing arrays.
- `posAttr.setUsage(THREE.DynamicDrawUsage)` — tells WebGL this buffer re-uploads often.
- Only write + `needsUpdate` when progress actually changed (dirty flag) — an idle pinned
  section costs nothing.
- 3000 × 3 floats/frame in JS is fine on 2020+ hardware. Beyond ~50k particles move the lerp
  into a vertex shader (two position attributes + a `uProgress` uniform, mix in GLSL — see
  `threejs-shaders`); don't reach for that complexity at this scale.
- `PointsMaterial` with `depthWrite: false` + `AdditiveBlending` is the standard glow-dust
  look and avoids transparency sort artifacts.

## Pattern 2 — Scroll → canvas bridge (ScrollTrigger owns scroll)

**Learning sources**: GreenSock official
[ScrollTrigger docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) (`scrub`, `pin`,
`onUpdate`, `self.progress`); Codrops
[“How to Build Cinematic 3D Scroll Experiences with GSAP”](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/)
(the exact architecture: GSAP timeline as the single source of truth, 3D scene as a consumer;
demo code is OGL, not three — the architecture transfers).

The stage exposes one write-only entry point; the page's choreography layer decides what feeds it:

```javascript
const stage = createScrollStage(document.querySelector("#stage"));

ScrollTrigger.create({
  trigger: "#stage", start: "top top", end: "+=300%",
  pin: true, scrub: true,
  onUpdate: (self) => stage.setProgress(self.progress),
});
```

Alternative when the scene should sit inside a larger page timeline — scrub a proxy object in
the SAME timeline that runs the DOM beats, so DOM and canvas can never drift apart:

```javascript
const proxy = { p: 0 };
const tl = gsap.timeline({
  scrollTrigger: { trigger: "#chapter", start: "top top", end: "+=400%", pin: true, scrub: true },
});
tl.to(".chapter-title", { yPercent: -40, opacity: 0, duration: 0.4 }, 0)
  .to(proxy, { p: 1, ease: "none", duration: 1, onUpdate: () => stage.setProgress(proxy.p) }, 0);
```

> ⚠️ **Duration trap (found in the 2026-07-05 smoke run):** give the scrub-driving proxy tween
> an **explicit `duration` spanning the timeline's full intended length**. Tweens default to
> 0.5s — if other tweens push the timeline's total duration past the proxy tween's end, the
> proxy reaches `p = 1` partway through the scroll and morph-progress silently decouples from
> scroll-fraction. Silent, looks-fine-in-a-snippet, breaks in a real page.

**Single loop:** the render function joins `gsap.ticker` — GSAP's own heartbeat — instead of a
private `requestAnimationFrame`:

```javascript
function render(time, deltaMS) { /* ... */ renderer.render(scene, camera); }
gsap.ticker.add(render);      // join
gsap.ticker.remove(render);   // leave (teardown)
```

Two loops (RAF + ticker) = double work, jitter from mismatched timing, and two things to leak.
`gsap.ticker` passes `(time, deltaTime, frame)`; `deltaTime` is in **milliseconds**.

**Hold choreography (lock-and-hold, found needed in the 2026-07-07 rematch):** continuous
scrub-morphing (above) reads as a blur through shapes when the narrative wants each formation
to LOCK, HOLD for a scroll window, then transition. Two equivalent builds, both keeping the
"canvas receives progress only" contract:
- keyframe table: `KEYS = [{p:0,f:0},{p:.14,f:1},{p:.36,f:1},...]` — repeated `f` = a hold
  window; locate the segment for `p`, smoothstep the local `t` between its formations; or
- GSAP-native: drive `setProgress` with a timeline whose proxy tweens include explicit hold
  segments (`.to(proxy, {p: 1, duration: .2}) .to(proxy, {}, "+=0.2") ...`), optionally
  widening the progress domain to formation-space (0..N-1) — document the domain if you do.

Rules recap: the canvas never reads `window.scrollY`, never registers wheel/scroll listeners.
If a second scene needs scroll, it gets its own `setProgress` fed by its own ScrollTrigger —
the driver side always lives in the GSAP layer.

## Pattern 3 — Mouse parallax camera (damped lerp)

**Learning source**: three.js official example
[`webgl_points_waves`](https://threejs.org/examples/#webgl_points_waves) — the canonical
`camera.position.x += (mouseX - camera.position.x) * 0.05` damping idiom, upgraded here to a
frame-rate-independent factor.

```javascript
const pointer = { x: 0, y: 0 };           // normalized -1..1
function onPointerMove(ev) {
  pointer.x = (ev.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -((ev.clientY / window.innerHeight) * 2 - 1);
}
window.addEventListener("pointermove", onPointerMove);

// inside render(time, deltaMS):
const dt = deltaMS / 1000;
const damp = 1 - Math.exp(-LAMBDA * dt);  // LAMBDA ≈ 3..6; higher = snappier
camera.position.x += (pointer.x * MAX_X - camera.position.x) * damp;
camera.position.y += (pointer.y * MAX_Y - camera.position.y) * damp;
camera.lookAt(0, 0, 0);                   // keep the subject centered while orbiting
```

- `1 - Math.exp(-λ·dt)` gives identical feel at 30/60/120 fps; a bare `* 0.05` does not.
- Keep offsets small (`MAX_X` ≈ 0.3–0.8 world units) — parallax is a garnish, not a control.
- Parallax the **camera**, not the object, so lighting stays fixed and shadows don't swim.
  (Alternative for multi-layer depth: move 2–3 groups at different factors.)
- Touch devices have no hover: `pointer` just stays at rest (0,0) — the stage must look
  complete without parallax. Do not fake it with device orientation unless asked.
- Parallax composes with scroll: scroll drives formation/progress, pointer drives a small
  camera offset. They touch different variables, so no conflict.

## Pattern 4 — Cleanup chain (dispose everything, unbind everything)

**Learning source**: three.js manual
[“How to dispose of objects”](https://threejs.org/docs/#manual/en/introduction/How-to-dispose-of-objects)
(what `.dispose()` exists on and why the GC can't do it for you).

WebGL resources live on the GPU — JavaScript GC never frees them. A page that mounts/unmounts
the stage (SPA route, gallery tab switch) must run the full chain:

```javascript
function destroy() {
  // 1. drivers first — nothing may render or scrub after this line
  scrollTriggerInstance?.kill();
  gsap.ticker.remove(render);
  // (if using gsap.matchMedia: mm.revert() runs both branches' cleanup returns)

  // 2. listeners
  window.removeEventListener("pointermove", onPointerMove);
  window.removeEventListener("resize", onResize);

  // 3. GPU resources — geometry, material(s), textures ON the materials
  scene.traverse((obj) => {
    obj.geometry?.dispose();
    const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
    mats.forEach((m) => {
      if (!m) return;
      for (const key of Object.keys(m)) {
        if (m[key]?.isTexture) m[key].dispose();  // map, envMap, normalMap, ...
      }
      m.dispose();
    });
  });

  // 4. renderer last, then remove the canvas element
  renderer.dispose();
  renderer.domElement.remove();
}
```

Verification that cleanup actually works (do this in the smoke demo): mount → unmount →
remount several times; `renderer.info.memory` should return to baseline and the console must
stay free of `THREE.WebGLRenderer: Context Lost` / "too many active WebGL contexts" warnings.
Browsers cap live WebGL contexts (~8–16); leaking one per route change kills the site quietly.

## Pattern 5 — Reduced motion (static frame, both branches registered)

**Learning source**: GreenSock official
[`gsap.matchMedia()` docs](https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/) (condition-scoped
setup with automatic cleanup on flip).

```javascript
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: reduce)", () => {
  applyProgress(1);               // most-resolved formation, not mid-morph soup
  renderer.render(scene, camera); // ONE frame; no ticker, no ScrollTrigger, no parallax
  return () => {};
});

mm.add("(prefers-reduced-motion: no-preference)", () => {
  const st = ScrollTrigger.create({ /* ... */ onUpdate: (s) => setProgress(s.progress) });
  gsap.ticker.add(render);
  return () => { st.kill(); gsap.ticker.remove(render); };
});
```

- **Register BOTH branches.** A lone `reduce` handler means the default path never
  initializes (nothing fires for no-preference users) — a real bug class, easy to ship.
- Reduced-motion = a meaningful static frame (final formation, lit object at rest), NOT a
  slowed-down animation and NOT a blank canvas.
- Because each branch returns its own cleanup, a user flipping the OS setting mid-session
  transitions correctly; `mm.revert()` in `destroy()` covers teardown for whichever branch
  is live.
- **Conditions-object trap (found in the 2026-07-08 rebuild wave):** the
  `mm.add({ a: "...", b: "..." }, cb)` conditions-object form only fires while **at least one
  named query matches**. Modeling independent booleans that can be simultaneously false
  (e.g. `isCoarse` + `reduceMotion` on an ordinary desktop) silently no-ops the whole setup.
  Model conditions as **mutually exclusive and exhaustive** (e.g. coarse / fine-no-reduce /
  fine-reduce) so exactly one is always true.
- **Paint-order trap when un-pinning (found in the 2026-07-05 smoke run):** the reduce branch
  often swaps the pinned/absolute layout for static flow. A DOM caption that computes
  `opacity: 1` with correct layout can still render **behind** a sibling absolutely-positioned
  canvas once its own `position` stops creating a stacking context — give overlaid DOM
  `position: relative` (+ `z-index` if needed) so it stays above the canvas in BOTH branches.

## Pattern 6 — Chassis token derive (colors come from CSS, not JS)

**Learning sources**: MDN
[`getComputedStyle`](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle) +
[CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*); three.js manual
[Color management](https://threejs.org/docs/#manual/en/introduction/Color-management)
(hex/CSS strings are read as sRGB and converted under default color management, r152+).

The locked chassis (`tokens.css`) is the single source of truth for color. The stage reads
tokens at init and derives every 3D color from them:

```javascript
const css = getComputedStyle(document.documentElement);
const token = (name, fallback) => css.getPropertyValue(name).trim() || fallback;

const bg     = new THREE.Color(token("--token-bg",     "#14150f"));
const ink    = new THREE.Color(token("--token-ink",    "#e8e6df"));
const accent = new THREE.Color(token("--token-accent", "#bfe800"));

scene.background = bg;
particleMaterial.color.copy(accent);
keyLight.color.copy(ink);                       // lights derive from ink/paper tones
rimLight.color.copy(accent).multiplyScalar(0.6); // derived tint — darker accent, same hue
```

- `new THREE.Color("#bfe800")` / `"rgb(...)"` strings are interpreted as sRGB and converted
  to the working color space automatically under default color management (r152+) — do not
  hand-convert.
- Derivations (darken, desaturate) happen via `THREE.Color` ops on a **token-sourced** base
  (`.multiplyScalar`, `.lerp`, `.offsetHSL`) — that's derive-not-invent. A raw hex that isn't
  a fallback for a token is a violation.
- Fallback values exist so a demo file opened standalone still renders; in pipeline use the
  token always wins. Match fallbacks to the actual chassis you're building against.
- Tokens are read at init. If the page theme can flip at runtime, re-read and `.set()` the
  colors in the theme-change handler (cheap; no rebuild needed).

## Pattern 7 — Shard-constructed object with pointer repulsion (lab-proven 2026-07-08)

**Learning sources**: Codrops
[“Interactive Repulsion Effect with Three.js”](https://tympanus.net/codrops/2018/12/06/interactive-repulsion-effect-with-three-js/)
(distance-falloff push + return mechanic); for true physics-grade fracturing see
[three-pinata](https://github.com/dgreenheck/three-pinata) (real-time mesh fracture library) —
the recipe below needs no library. Reference implementation:
`testbed/material/shard-vessel/` (84 shards, 1 draw call, 624 tris,
console-clean, leak-flat, ~240fps idle / ~131fps active on shared headless hardware).

The Seamora-class hero: an object (vessel, logo, any lathe/mesh form) built from dozens of
fragments that scatter away from the cursor and heal back when it leaves.

### Recipe A — shard partitioning without instancing

Irregular curved surface pieces are NOT uniform, so `InstancedMesh` is the wrong tool.
Instead keep **one non-indexed `BufferGeometry` = one draw call**:

1. Build the base form (e.g. `LatheGeometry(profile, segments)`), call `.toNonIndexed()`.
2. Partition triangles into shard groups by **triangle-centroid binning**: compute each
   triangle's centroid, bin by `(atan2(z,x) angle-band, y height-band)` — e.g. 12 × 7 = 84
   shards; jitter band boundaries for a hand-broken look.
3. Precompute per-shard rest data (member vertex indices, shard centroid) once at init.
4. Per dirty frame, write each shard's translation (+ small quaternion wobble) into the live
   `position`/`normal` arrays from the REST copies, then `needsUpdate = true`. Preallocate
   everything; zero allocation in the loop.

### Recipe B — pointer ray in the object's local space

The group idle-rotates, so intersect in LOCAL space instead of re-transforming every shard
centroid per frame:

```javascript
// once per pointer move:
raycaster.setFromCamera(pointerNDC, camera);
inv.copy(group.matrixWorld).invert();
localRay.copy(raycaster.ray).applyMatrix4(inv);      // ray → group local space
localRay.intersectPlane(localPlane, hitLocal);        // plane through the vessel axis
// per shard: d = shardCentroid.distanceTo(hitLocal); push = max(0, 1 - d/RADIUS)
```

Displacement per shard = radial push vector × falloff, applied with the frame-rate-independent
damping from Pattern 3 — use **asymmetric λ** (fast push ≈ 8-12, slow heal ≈ 2-4) so the
break feels startled and the heal feels deliberate.

### Discipline recap (all inherited)

Single `gsap.ticker` loop; **dirty-flag skips the whole per-vertex rewrite when no shard is
displaced and idle rotation alone doesn't dirty the buffers** (rotation lives on the group
matrix, not the vertices); full Pattern 4 disposal; Pattern 5 reduced-motion = intact static
frame with no pointer listeners; Pattern 6 token-derived colors/lights. Perf tier: **中** at
~100 shards (one draw call); beyond a few hundred shards move displacement into a vertex
shader (`threejs-shaders`).

## Anti-patterns

| ❌ | Why it's wrong |
|---|---|
| One `Mesh` per particle | 3000 draw calls; use ONE `Points` (one draw call) |
| Canvas listens to `scroll`/`wheel` itself | Two scroll sources of truth; ScrollTrigger owns scroll, canvas gets `setProgress(p)` |
| `requestAnimationFrame` loop alongside GSAP | Two heartbeats = jitter + double work; join `gsap.ticker` |
| `new Float32Array`/`new THREE.Color` inside the render loop | Per-frame GC pressure; preallocate at init |
| Hardcoded hex colors in stage code | Breaks chassis SSOT; derive from `--token-*` (fallbacks only for standalone runs) |
| Unmount without `dispose()`/`kill()`/`removeEventListener` | GPU memory + context leak; browsers cap WebGL contexts |
| Only registering the `reduce` matchMedia branch | Default-motion path never initializes — register both |
| Framer Motion in the same tree as the stage | taste-skill red line: never mix engines in one tree |
| Faking parallax with `deviceorientation` on touch | Permission prompts + motion sickness; rest state must look complete |
| Idle Y-rotation on a full-360° `LatheGeometry` (or any perfect solid of revolution) under static camera/lights/untextured material | Rotationally symmetric = the rotation is **pixel-invisible**; break the symmetry (small per-vertex radius wobble via `setXYZ` + `computeVertexNormals`), add a texture, or animate a light instead (found in the 2026-07-05 smoke run) |
| DOM captions parked over the particle formation's center with no legibility treatment | At peak formation density the caption **drowns in particles** (human review finding, 2026-07-07). Offset captions from the formation centroid, add a scrim/text-shadow, or dip particle opacity while a caption is active — choreograph text beats to land where/when the cloud is thin |

> **Cross-cutting gotchas & verification** (traps that hit any three+GSAP+GLSL demo, not just a
> scroll stage — perspective-flip drift, GSAP staggered-`killTweensOf`, GLSL backtick-in-comment,
> `ShaderPass` uniforms-clone, `img.decode` boot hang, transparent z-tie, float-`floor` off-by-one;
> plus verification discipline for 3D work) live in [`three/GOTCHAS.md`](../GOTCHAS.md) so this skill
> stays focused on scroll-stage implementation.

## Related skills

- `threejs-fundamentals` — scene/camera/renderer basics this skill assumes
- `threejs-geometry` — BufferGeometry/BufferAttribute in depth
- `threejs-lighting`, `threejs-materials` — for lit-object stages (vessel-class hero objects)
- `threejs-shaders` — where the morph goes when particle counts outgrow CPU lerp (≥50k)
- `gsap-scrolltrigger` — the driver side of the bridge (pin/scrub/refresh)
- `companions/taste-skill` §8 — WHEN to use 3D at all (this skill is only HOW)

## Consolidated learning sources

- three.js official examples: [`webgl_points_waves`](https://threejs.org/examples/#webgl_points_waves) · [`webgl_buffergeometry_custom_attributes_particles`](https://threejs.org/examples/#webgl_buffergeometry_custom_attributes_particles) · [`webgl_points_dynamic`](https://threejs.org/examples/#webgl_points_dynamic)
- three.js manual: [How to dispose of objects](https://threejs.org/docs/#manual/en/introduction/How-to-dispose-of-objects) · [Color management](https://threejs.org/docs/#manual/en/introduction/Color-management)
- GreenSock official: [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) · [gsap.matchMedia()](https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/) · [gsap.ticker](https://gsap.com/docs/v3/GSAP/gsap.ticker)
- Codrops: [How to Build Cinematic 3D Scroll Experiences with GSAP](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/) (Nov 2025) (demo code is OGL, not three — the architecture transfers)
