#!/usr/bin/env node
/**
 * pipeline-gate.js — project-local PreToolUse[Agent] hook (ui skills lab).
 *
 * PURPOSE
 *   Hard-block the `anchor-prototype-wave` surface fan-out unless the USER has
 *   explicitly approved the pipeline-step transition (lock chassis -> wave).
 *   The model may PROPOSE skipping a step (e.g. Batch-2 motion); it may NOT
 *   act on that skip until the user answers. This hook is the deterministic
 *   teeth behind that rule (instruction alone proved insufficient).
 *
 * ENFORCEMENT (honest scope + limits)
 *   - Only gates Agent spawns that AUTHOR a wave surface (precise marker/path match).
 *     Batch-1 exploration, reviews, and every non-wave agent pass through untouched.
 *   - Requires BOTH:
 *       (a) a fresh, gate-specific approval sentinel  .goals/pipeline-gate.json
 *       (b) a recent USER message (in the transcript) containing an approval word.
 *     (b) is the anti-self-approval backstop: the model writes the sentinel, so on
 *     its own the sentinel is self-approvable; (b) makes it impossible to wave-through
 *     in a turn sequence where the user never actually approved anything.
 *   - Fail-OPEN on the hook's own infrastructure errors (never brick a session);
 *     fail-CLOSED on the definite "gated action + no valid approval" case (the point).
 *   - Detection is heuristic (prompt markers / output path), NOT a formal proof.
 *   - Does NOT gate Workflow launches (this lab uses Agent fan-out) or the chassis
 *     write itself — the wave fan-out is the high-value choke point. Extendable later.
 *
 * MOTION-ARCHITECTURE EXTENSION (2026-07-10, motion-score plan step 10)
 *   When the spawn prompt reveals a run root (testbed/runs/<run>) whose
 *   motion/pipeline-state.json exists, the wave fan-out ADDITIONALLY requires
 *   state SECTIONAL_LOCKED|BASE_WAVE_READY + composition_ready +
 *   sectional_status selected|skipped + a verbatim chassis approval.
 *   An `atomic-patch subagent` fan-out requires state ATOMIC_OPEN + a verbatim
 *   atomic_policy approval. Runs WITHOUT a state file are legacy: unchanged.
 *   Same philosophy: fail-OPEN on infra errors (unreadable state), fail-CLOSED
 *   on a definite gated action without its evidence. The portable teeth are
 *   anchor-prototype-wave/scripts/preflight_wave.py; this hook is the
 *   deterministic in-session backstop.
 */
'use strict';
const fs = require('fs');
const path = require('path');

function readStdin() { try { return fs.readFileSync(0, 'utf8'); } catch { return ''; } }

function findRepoRoot(startDir) {
  let d = startDir;
  for (let i = 0; i < 10 && d; i++) {
    try { if (fs.existsSync(path.join(d, '.git'))) return d; } catch {}
    const parent = path.dirname(d);
    if (parent === d) break;
    d = parent;
  }
  return startDir;
}

// Broad on purpose — this is only the anti-self-approval BACKSTOP (the sentinel is
// the gate-specific artifact). Matches short EN/ZH approvals the user actually types.
const APPROVAL_RE = /\b(ok|okay|approve[d]?|yes|yep|go|run it|ship it|do it)\b|批准|同意|确认|通过|跑|开跑|可以|行了?|做(吧|hook)/i;

// --- motion-architecture state discovery + checks (fail-open on infra) ---
function findMotionState(prompt, repo) {
  const rx = /(?:[A-Za-z]:)?[^\s"'`]*testbed[\/\\]runs[\/\\][^\s"'`\/\\]+/g;
  const seen = new Set();
  let m;
  while ((m = rx.exec(prompt))) {
    const hit = m[0].replace(/[\/\\]+$/, '');
    const rel = hit.replace(/^.*?(testbed[\/\\]runs[\/\\])/, '$1');
    for (const cand of [hit, path.join(repo, rel)]) {
      const sp = path.join(cand, 'motion', 'pipeline-state.json');
      if (seen.has(sp)) continue;
      seen.add(sp);
      try {
        if (fs.existsSync(sp)) return { path: sp, doc: JSON.parse(fs.readFileSync(sp, 'utf8')) };
      } catch (e) {
        return { path: sp, error: String(e) }; // exists but unreadable -> infra
      }
    }
  }
  return null; // no motion pipeline discovered -> legacy run
}

function waveMotionProblem(motion) {
  if (!motion) return null;            // legacy run: no extra requirement
  if (motion.error || !motion.doc) return null; // infra fail-open
  const d = motion.doc;
  const appr = d.user_approvals || {};
  if (!/^(SECTIONAL_LOCKED|BASE_WAVE_READY)$/.test(String(d.state || '')))
    return `motion pipeline-state is "${d.state}" — Base Wave spawns only at SECTIONAL_LOCKED (or BASE_WAVE_READY for fix-loop respawns)`;
  if (d.composition_ready !== true)
    return 'motion pipeline-state: composition_ready is not true';
  if (!/^(selected|skipped)$/.test(String(d.sectional_status || '')))
    return `motion pipeline-state: sectional_status "${d.sectional_status}" — Sectional Score not settled (selected|skipped)`;
  if (!String(appr.chassis || '').trim())
    return 'motion pipeline-state: user_approvals.chassis is empty (never self-approve the lock)';
  return null;
}

function atomicGateProblem(motion) {
  if (!motion)
    return 'no motion/pipeline-state.json discoverable from the prompt — an Atomic Pass exists only inside a motion-pipeline run; include the run path (testbed/runs/<run>/...) in the spawn prompt';
  if (motion.error || !motion.doc) return null; // infra fail-open
  const d = motion.doc;
  if (String(d.state || '') !== 'ATOMIC_OPEN')
    return `motion pipeline-state is "${d.state}" — Atomic Pass starts only at ATOMIC_OPEN (BASE_WAVE_READY + approved policy + transition first)`;
  if (!String((d.user_approvals || {}).atomic_policy || '').trim())
    return 'motion pipeline-state: user_approvals.atomic_policy is empty (the user approves the POLICY before any atomic patching)';
  return null;
}

function extractUserText(ev) {
  const m = (ev && ev.message) || ev || {};
  if (typeof m.content === 'string') return m.content;
  if (Array.isArray(m.content)) {
    return m.content
      .filter(c => c && (c.type === 'text' || typeof c.text === 'string'))
      .map(c => c.text || '')
      .join(' ');
  }
  if (typeof ev.text === 'string') return ev.text;
  return '';
}

function main() {
  let input;
  try { input = JSON.parse(readStdin() || '{}'); } catch { process.exit(0); } // infra fail-open

  const toolName = input.tool_name || input.toolName || '';
  if (!/^(Agent|Task)$/i.test(String(toolName))) process.exit(0);

  const ti = input.tool_input || input.toolInput || {};
  const prompt = String(ti.prompt || '') + '\n' + String(ti.description || '');

  // --- detectors: wave surface-authoring fan-out + atomic-patch fan-out ---
  const isWaveSurface =
    /surface[-\s]?authoring subagent/i.test(prompt) ||
    /anchor-wave[\/\\][^\/\\"'\s]+[\/\\]index\.html/i.test(prompt);
  const isAtomicPatch = /atomic[-\s]?patch subagent/i.test(prompt);
  if (!isWaveSurface && !isAtomicPatch) process.exit(0); // not a gated action -> allow

  const repo = process.env.CLAUDE_PROJECT_DIR || findRepoRoot(process.cwd());
  const motion = findMotionState(prompt, repo);

  // --- atomic-patch fan-out: gated purely by the motion state machine ---
  if (isAtomicPatch && !isWaveSurface) {
    const problem = atomicGateProblem(motion);
    if (!problem) process.exit(0); // ALLOW
    process.stderr.write([
      'PIPELINE-GATE (project hook) — BLOCKED an Atomic Pass fan-out.',
      `Reason: ${problem}.`,
      '',
      'To proceed correctly: finish the Base Wave (BASE_WAVE_READY), have the USER approve',
      'the atomic policy (pipeline_state.py approve --gate atomic_policy — verbatim words),',
      'set atomic_status policy-approved, transition --to ATOMIC_OPEN, and re-run',
      'preflight_wave.py --stage atomic. Never self-approve; never hand-edit the state file.',
    ].join('\n') + '\n');
    process.exit(2);
  }

  // --- check (a): fresh, gate-specific approval sentinel ---
  let sentinelOK = false, sentinelWhy = 'no .goals/pipeline-gate.json sentinel found';
  try {
    const sp = path.join(repo, '.goals', 'pipeline-gate.json');
    if (fs.existsSync(sp)) {
      const s = JSON.parse(fs.readFileSync(sp, 'utf8'));
      const gateOK = /wave/i.test(String(s.gate || ''));
      const appr = String(s.user_approval || '').trim();
      const at = Date.parse(s.approved_at || '');
      const ttl = (Number(s.ttl_seconds) > 0 ? Number(s.ttl_seconds) : 14400) * 1000;
      const fresh = at && (Date.now() - at) < ttl;
      if (!gateOK) sentinelWhy = `sentinel.gate="${s.gate}" is not a wave gate`;
      else if (!appr) sentinelWhy = 'sentinel.user_approval is empty';
      else if (!fresh) sentinelWhy = 'sentinel expired (approved_at + ttl_seconds elapsed)';
      else sentinelOK = true;
    }
  } catch { sentinelWhy = 'sentinel unreadable / invalid JSON'; }

  // --- check (b): a recent USER approval in the transcript (anti self-approval) ---
  let userApprovedRecently = false, transcriptSeen = false;
  try {
    const tp = input.transcript_path || input.transcriptPath;
    if (tp && fs.existsSync(tp)) {
      transcriptSeen = true;
      const lines = fs.readFileSync(tp, 'utf8').split(/\r?\n/).filter(Boolean).slice(-40);
      for (const ln of lines) {
        let ev; try { ev = JSON.parse(ln); } catch { continue; }
        const role = String(ev.role || (ev.message && ev.message.role) || ev.type || '').toLowerCase();
        if (role !== 'user') continue;
        if (APPROVAL_RE.test(extractUserText(ev))) { userApprovedRecently = true; break; }
      }
    } else {
      userApprovedRecently = true; // transcript unavailable -> infra fail-open on THIS check only
    }
  } catch { userApprovedRecently = true; }

  // --- check (c): motion-architecture state (only when a state file exists for the run) ---
  const motionProblem = waveMotionProblem(motion);

  if (sentinelOK && userApprovedRecently && !motionProblem) process.exit(0); // ALLOW

  // --- BLOCK ---
  const why = !sentinelOK
    ? sentinelWhy
    : (!userApprovedRecently
        ? (transcriptSeen ? 'no recent user approval found in the transcript' : 'approval unverifiable')
        : motionProblem);
  const msg = [
    'PIPELINE-GATE (project hook) — BLOCKED an anchor-prototype-wave surface fan-out.',
    'A pipeline-step transition (lock chassis -> wave) is the USER\'s decision, not the model\'s.',
    `Reason: ${why}.`,
    '',
    'To proceed correctly:',
    '  1) Present the transition — and any proposed SKIP (e.g. skipping Batch-2 motion) — as an',
    '     explicit either/or, then WAIT for the user to answer. Do NOT fold a skip into a',
    '     recommendation you then act on.',
    '  2) After the user approves, write .goals/pipeline-gate.json:',
    '     {"gate":"anchor-wave","run":"<run-id>","proposed":"<what you proposed>",',
    '      "user_approval":"<the user\'s approving words, verbatim>","approved_at":"<ISO-now>","ttl_seconds":14400}',
    '  3) Re-spawn the wave. Never self-approve.',
    '  (Motion-pipeline runs: if the reason above is the motion pipeline-state, fix it via the',
    '   prototyping-ui-directions Sectional Score ceremony + pipeline_state.py, then re-run',
    '   anchor-prototype-wave/scripts/preflight_wave.py --stage base-wave until it exits 0.)',
  ].join('\n');
  process.stderr.write(msg + '\n');
  process.exit(2); // exit 2 = block; stderr is fed back to the model
}

main();
