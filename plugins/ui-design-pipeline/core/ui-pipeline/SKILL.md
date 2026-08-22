---
name: ui-pipeline
version: 1.0.0
description: >
  Front door for the UI design pipeline — start a new run, or resume one that was interrupted.
  Routes by screen count: one screen goes straight to variant exploration, two or more start
  with information architecture, so layout is settled once rather than re-invented per page.
  Owns the run root and the resume pointer that survives a cleared session. Enter here rather
  than naming a downstream skill. Triggers: "design this product", "give me a few UI
  directions", "explore UI directions", "build the pages for X", "continue the UI run", "where
  did the design run stop", "做几版 UI 方向", "设计这个产品", "接着上次的 UI 流程".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# ui-pipeline

The front door. Two jobs, both small:

1. **Never let a multi-screen product skip IA round 1.** Asking for "a few UI directions"
   used to land straight on `prototyping-ui-directions`, which explores one screen. On a
   product with a second screen that silently discards the step that makes every later page
   inherit one layout instead of inventing its own.
2. **Make an interrupted run resumable.** A run spans several sessions. Context gets
   compacted, sessions get cleared. Without a durable pointer the next session cannot tell
   what was decided, what was approved, or what comes next — and re-asking a human for
   decisions they already made is the most expensive failure this pipeline has.

This skill does no design work of its own. It routes, and it keeps the pointer.

## Run root

One run, one directory. Establish it before anything is generated:

```
<run-root>/                       default: ui-run/<date>-<nickname>/
  RUN.md                          the resume pointer (this skill owns it)
  ia/                             information-architecture out-dir (rounds 1 and 2)
  directions/                     prototyping-ui-directions out-dir
  directions/motion/              pipeline-state.json — the MACHINE state
  surfaces/                       anchor-prototype-wave out-dir
```

Both downstream skills accept an explicit output dir as an input (`information-architecture`
§Inputs "Output dir", `prototyping-ui-directions` §Inputs 6). **Pass those paths explicitly**
rather than letting each take its own default — their defaults land in two unrelated
directories, which is what makes a run hard to find later.

## Step 1 — resume, or start

Before asking the user anything, look for an existing run:

```bash
ls -d ui-run/*/ 2>/dev/null; ls */RUN.md 2>/dev/null; ls RUN.md 2>/dev/null
```

**A run exists** → read its `RUN.md`, then cross-check against the machine state if one has
been initialised:

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/prototyping-ui-directions/scripts/pipeline_state.py \
  show --state-file <run-root>/directions/motion/pipeline-state.json
```

Report the position in one short paragraph — stage reached, what the human already decided,
what the next action is — then continue from there. Do **not** re-ask a decision `RUN.md`
already records; quote it back instead.

If `RUN.md` and the machine state disagree, **the machine state wins** and you say so out
loud. `RUN.md` is a convenience, and a stale convenience must never move a gate (see
§Hard rules).

**No run exists** → Step 2.

## Step 2 — route

Ask exactly one question before routing:

> How many screens does this product have — one, or more than one?

- **One screen** → `Read ${CLAUDE_PLUGIN_ROOT}/core/prototyping-ui-directions/SKILL.md` and
  run it, output dir `<run-root>/directions/`. IA is skippable only here.
- **Two or more** → `Read ${CLAUDE_PLUGIN_ROOT}/companions/information-architecture/SKILL.md`
  and run **round 1** first, output dir `<run-root>/ia/`. Its approved hero-screen spec is
  the intake for `prototyping-ui-directions` (§Inputs 7), which runs next.

Do not ask anything else here. Every other input belongs to the skill that needs it, and
those skills ask in their own order — asking early means guessing at questions you have not
earned yet.

After the chassis locks, `information-architecture` **round 2** runs before the wave. That
handoff is already specified in the two skills; this skill's only job is to make sure round 2
is not forgotten because a session boundary fell in the wrong place. `RUN.md` is what
remembers.

## RUN.md — generated, never maintained

`RUN.md` is **not a ledger anyone updates**. It is regenerated from two sources that cannot
drift, and the only way to "update" it is to re-run one command:

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/ui-pipeline/scripts/render_run.py --run-root <run-root>
```

That was a deliberate correction. The first version of this skill said "update RUN.md at every
stage boundary", which is an instruction — and one missed update leaves a pointer that says the
run is somewhere it is not. **A pointer that lies is worse than no pointer**, because the next
session believes it. So nothing here is remembered; it is recomputed:

| What lands in RUN.md | Where it comes from |
|---|---|
| stage status, gate flags | `directions/motion/pipeline-state.json` — the append-audited machine state |
| the human decisions, verbatim | `user_approvals` + `state_log` in that same file. `pipeline_state.py approve` refuses an empty approval-text and is write-once, so the quote in RUN.md is the quote the user actually gave |
| IA / directions / wave progress | what is on disk in the run root — `ia/info-spec.json`, `ia/wireframes/`, `directions/variant-*/`, `directions/CHASSIS.md`, `surfaces/` |
| **Current pointer** | computed: the first stage that is not done, and which skill owns it |

Every render stamps the sha256 of the state it was rendered from, so staleness is detectable
rather than assumed:

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/ui-pipeline/scripts/render_run.py --run-root <run-root> --check
```

`preflight_wave.py` runs that check before the surface wave — the most expensive step in the
pipeline — and BLOCKs on a stale or hand-written pointer, naming the re-render command. A run
with no `RUN.md` at all (a skill invoked directly, or a legacy layout) is noted and allowed:
this gate defends against forgetting, not against deliberate removal.

**Render it when you create the run root, and again whenever you report a position to the user.**
Re-rendering is idempotent and costs nothing.

**Honest limit.** This guarantees `RUN.md` never lies, because it is computed. It does not
guarantee `RUN.md` is always current — only the wave preflight forces a re-render. A run
interrupted between the two IA rounds still depends on someone running the command. Those are
different promises and only the first one is enforced.

## Hard rules

- **`RUN.md` is a pointer, not a gate.** Gate decisions read `pipeline-state.json` through
  `pipeline_state.py`, which is append-audited and refuses illegal transitions. Nothing in
  this skill may write that file, and no gate may be satisfied by what `RUN.md` claims. A
  second writable source of truth is how state drifts, and drifted state approves things a
  human never approved.
- **Never hand-edit `RUN.md`.** It is a build artifact. An edit is silently overwritten by the
  next render, and a hand-edited pointer is exactly the lying pointer the generator exists to
  prevent — the wave preflight rejects one that carries no render stamp.
- **Never invent an input to keep moving.** If a downstream skill needs something and the
  user has not said it, stop and ask — `RUN.md` records the question as `Blocked on`.
- **Never re-ask a recorded decision.** Quote it and move on.
- **Never route around IA on a multi-screen product** because the user asked for "directions".
  Say what the extra step buys and let them decline explicitly; record the decline.

## Anti-patterns

- Creating a run root per skill instead of one per run — the thing this skill exists to stop.
- Writing anything into `RUN.md` by hand — including "just fixing" a status. Change the run,
  then re-render; if a status is wrong, the derivation is wrong and that is the bug to fix.
- Reporting a position to the user from memory instead of from a fresh render.
- Treating a resumed run as a fresh one because `RUN.md` was hard to find. Search first; ask
  the user for the path second; start over only if they confirm there is nothing to resume.
