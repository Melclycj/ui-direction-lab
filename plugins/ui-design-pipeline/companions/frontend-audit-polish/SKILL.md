---
name: frontend-audit-polish
description: >
  Apply the findings in an audit document as batched patches across a directory of frontend
  files. Works on any HTML/CSS/JSX directory where you have the files plus one or more audit
  docs listing per-file or cross-cutting fixes: patches files in parallel, re-validates with
  whatever validators the project has, and writes a closeout. This is the fix half of the
  audit loop, not the audit itself. Triggers: "apply this audit to the wave", "polish round on
  these files", "batch-fix this pattern across these surfaces", "按审计意见批量修这批页面", "打磨这批页面".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# frontend-audit-polish

Standalone skill. Applies audit-driven batched patches to any frontend directory and re-validates. Closes the audit → fix → re-audit loop.

## What it does

Takes (a) a directory of frontend files and (b) one or more audit documents listing fixes. Groups fixes by pattern (cross-cutting) and by file (unique). Spawns one patch subagent per affected file. Re-validates with whatever validators the project has. Writes a closeout.

## Inputs (ask once, never invent)

1. **Target dir**: where the files to patch live.
2. **Contract** (required — `<path-to-_context.md>` OR explicit `--no-contract`): the project's binding contract. For anchor-wave outputs this is `<target>/audits/_context.md` (auto-detect this default; offer it to the user). The polish round inlines the contract's `## Contract Amendments` section into every patch subagent's prompt as a hard rule — no patch may violate a ratified amendment. For greenfield directories with no contract, pass `--no-contract` explicitly. **The skill refuses to run silently without one.**
3. **Audit doc paths**: one or more markdown files listing fixes (e.g., `audits/2026-05-19-*-usability-audit.md`).
4. **Pilot subset** (optional): list of file slugs to patch first as a validation pilot. On pilot success, prompt user before applying to the rest.
5. **Re-validators** (optional, auto-detected): commands or skill paths to run after patching. Auto-detect:
   - `${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/validate_surface.py` → run if `<target>/audits/contracts/<slug>.contract.json` exists.
   - `${CLAUDE_PLUGIN_ROOT}/authoring/taste-skill/SKILL.md` → Read + apply (light pass) if present.
   - `<target>/verify/` → run `frontend-visual-regression` in `run` mode if present.

## Expected audit doc structure

Each audit doc should follow this template (or recognizably close):

```markdown
---
title: <surface or pattern> · Audit
date: YYYY-MM-DD
surface: <relative path or "cross-cutting">
status: draft | resolved
verdict: <Apply listed fixes | Pass | Escalate>
---

# <title>

## Finding 1: <short title> [BLOCKER | MAJOR | MINOR — <heuristic>]

**Where:** <file or selector>
**Where in code:** `<file>:<line>`
```snippet```
**Heuristic:** <principle name>
**Fix:**
```code
<replacement code>
```
```

Cross-cutting audits use `surface: cross-cutting` and list a master table of files affected by each pattern, with a canonical resolution.

If the audit doc doesn't fit this template → parse what you can, report unparseable findings to the user, don't invent.

## Workflow

### 1. Parse audit docs
Read each audit doc. Extract:
- **Per-file findings**: surface slug + finding title + severity + fix code block.
- **Cross-cutting patterns**: pattern name + master list of files affected + canonical resolution.
- **ESCALATE findings**: report and skip — don't auto-patch.

Output of this step: a list of `(file, finding-id, severity, fix-instruction)` tuples, plus a separate list of cross-cutting patterns with their file-lists.

### 2. Group and dedupe
- Files appearing in cross-cutting patterns get those patterns' canonical resolution applied first.
- Files appearing only in per-file audits get their unique fixes applied.
- If a file appears in both: cross-cutting pattern fix runs first, per-file fixes layer on top.
- If two patterns target the same line in the same file: report the conflict, ask user to resolve.

### 3. Pilot subset (if specified)
Apply patches to the pilot subset only. Run re-validators on patched pilot files. Report:
- Pilot files patched + verdicts.
- Any pilot patch that failed re-validation → STOP, surface evidence, ask user whether to revise fix instructions or skip the pattern.

If pilot passes, proceed to full subset (or, if user prefers, stop and let them review the pilot diff).

### 4. Spawn patch subagents (parallel, ≤10 per batch)
One subagent per affected file. Each subagent's prompt includes:
- The current file content (or path to read).
- The list of fixes to apply to this file (cross-cutting + per-file), each with: finding title, severity, exact fix code from the audit.
- **Contract Amendments** — inlined verbatim from the contract path's `## Contract Amendments` section (empty block if `--no-contract` was passed). These are HARD RULES the patch MUST NOT violate. If a fix as instructed would violate an amendment (e.g. the audit says "use `warn` token" but Amendment #7 ratifies `--status-blocked-*` as the canonical name), the subagent does NOT silently revise the fix and does NOT apply it. It returns `blocked(amendment-conflict: <amendment-id>)` for that finding and the parent surfaces the conflict to the user.
- **Hard write-scope**: ONLY the file in question.
- A `re_validate_cmd` to run after patching (the parent provides this; subagent runs it and reports the result).

Subagent returns:
```
<file>: patched(N fixes) | re-validated(PASS|FAIL) | blocked(M fixes: amendment-conflict) | <one-phrase note if anomaly>
```

### 5. Re-validate at parent level
After all patch subagents complete, the parent runs the auto-detected validators across all patched files (not just the per-subagent self-checks):
- Run `validate_surface.py` against each patched surface that has a contract.
- Read `${CLAUDE_PLUGIN_ROOT}/authoring/taste-skill/SKILL.md` and apply a light red-team pass over the patched files (catches drift the audit didn't anticipate).
- If `frontend-visual-regression` is set up against this target, run `mode=run` to detect unintended visual regressions.

### 6. Write closeout
Write `<target>/audits/<YYYY-MM-DD>-polish-closeout.md`:

```markdown
---
title: Polish round closeout
date: YYYY-MM-DD
source_audits:
  - <audit-doc-path>
  - ...
status: resolved
---

# Polish closeout

## Files patched (N)
| File | Findings applied | Severity highest | Re-validation |
|---|---|---|---|
| <slug> | 3 (1 cross-cutting + 2 per-file) | MAJOR | PASS |
| ... | ... | ... | ... |

## Cross-cutting patterns resolved
- **Pattern A** (<name>): N files now use canonical X. Evidence: file:line per affected file.
- ...

## Per-file fixes
For each file, list the unique findings addressed.

## Re-validation summary
- validate_surface.py: PASS=N FAIL=N (list)
- taste-skill light pass: NEW_FINDINGS=N (list)
- visual regression: PASS=N FAIL=N (list, with diff magnitude)

## Contract amendments proposed
- Patches blocked by amendment-conflict (each: file + finding-id + amendment-id + reason).
- New amendments suggested (to feed into the next `anchor-prototype-wave` Stage 8 promotion step — one bullet per proposed rule, with cited evidence across N files).

## Followups
- Findings NOT resolved this round (reason: ESCALATE, ambiguous, etc.).
- NEW findings surfaced during patching (taste-skill caught, regression caught, etc.).
- Suggested next polish round: <description>.
```

### 7. Optional: snapshot before & after
If `anchor-prototype-wave-versions` is available AND the target is an anchor-wave output dir:
- Before patching: suggest invoking `anchor-prototype-wave-versions` to snapshot the pre-polish state.
- After patching: optionally re-snapshot with label `post-polish-<date>`.
This gives the user safe rollback via the version switcher.

## Hard boundaries

- Each patch subagent writes ONLY its assigned file. No cross-file edits within a subagent.
- Do NOT auto-resolve ESCALATE findings — surface them, skip.
- Do NOT silently lower severity. If a BLOCKER can't be patched, list it in followups.
- Re-validation failures do NOT auto-revert — record in closeout. User decides.
- Do NOT modify the audit docs themselves — they're inputs.
- Do NOT modify the contract (`_context.md`). Amendments are written only by `anchor-prototype-wave` Stage 8 (promotion step). If a polish round surfaces a finding that requires amending the contract, list it under "Contract amendments proposed" in the closeout and stop on that finding — do NOT amend silently.
- Do NOT commit changes — that's the user's call.

## When to stop and ask

1. **No contract path provided AND no `--no-contract` override.** Ask: "Where does the project's `_context.md` live? (Or pass `--no-contract` if this is a greenfield directory with no binding contract.)" Auto-suggest `<target>/audits/_context.md` if it exists. Do NOT default to `--no-contract`.
2. Contract path provided but the file has no `## Contract Amendments` section. Ask the user whether (a) the contract has no amendments yet (proceed with empty amendments block) or (b) the contract path is wrong.
3. Audit docs missing, unparseable, or empty.
4. Pilot subset fails — show evidence, ask before applying to rest.
5. >50% of patches fail re-validation — fix instructions likely wrong; surface to user.
6. Audit doc contains ESCALATE_HUMAN findings — surface before any patching.
7. Two patterns conflict on same file:line — ask user to resolve precedence.
8. ≥1 patch returned `blocked(amendment-conflict)` — surface the conflict and the proposed amendment-change to the user; do NOT patch around it.

## Pairs well with

- `anchor-prototype-wave` outputs (apply audits to wave surfaces).
- `anchor-prototype-wave-versions` (snapshot before polish for safe rollback).
- `frontend-visual-regression` (run `capture` before polish, `run` after to detect unintended regressions).
- `taste-skill` (used as a re-validator pass after patching).

## Reference — expected audit-doc shapes

This skill consumes four audit-doc shapes (all following the template in §Expected audit doc structure):
- **Per-surface contract audit** — findings tied to one surface's contract.
- **Per-surface usability audit** — HCI-lens findings for one surface.
- **Cross-cutting summary** — one pattern × the list of surfaces it hits + a canonical resolution.
- **Polish closeout** — the post-patch record this skill itself writes.

No external sample directory is required — the templates above are self-contained.
