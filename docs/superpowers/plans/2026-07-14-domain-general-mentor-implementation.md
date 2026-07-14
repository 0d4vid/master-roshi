# Master Roshi Portability and Learning-Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Master Roshi a portable, domain-general learning mentor with a real multi-model evaluation harness and a contributor-ready repository.

**Architecture:** `AGENTS.md` becomes the canonical cross-agent contract target. Claude Code and Gemini CLI receive small managed import adapters, while an optional dedicated Cline rule demonstrates whole-file targets. `SKILL.md` routes ordinary learning separately from explicit installation; supporting references isolate installation, domain patterns, and evaluation. A Python harness runs structured scenarios against multiple model backends, stores raw transcripts, and uses a separate judge call.

**Tech Stack:** Agent Skills Markdown, Python 3 standard library plus optional Anthropic/OpenAI SDKs for live evals, `unittest`, GitHub Actions.

**Implementation status (2026-07-14):** repository, skill, deterministic harness, scenarios, CI, portability, pedagogy, documentation, and installed-skill synchronization are implemented and validated. Live provider runs, five-repeat adversarial sampling, and promotion of independently judged evidence remain pending credentials; no behavioral pass claim is recorded.

## Global constraints

- Default invocation starts learning mode without editing project files.
- Installation mode runs only after an explicit request to persist instructions.
- `AGENTS.md` is the canonical shared contract; adapters reference it instead of duplicating it.
- Shared files preserve user content with managed markers; dedicated files are fully owned and refreshed by whole-file replacement.
- The literal `show me the answer` gate remains, with intent-aware handling for paraphrases.
- A direct solution never becomes evidence of mastery; retrieval or transfer still verifies learning.
- The initial domains are programming, data science, machine learning, cybersecurity, and conceptual subjects.
- Cybersecurity operational practice requires explicit authorization, scope, and a safe environment.
- Live evaluation credentials are never committed or exposed to pull requests from forks.
- Only observed transcripts may be recorded as passes; planned runs remain pending.
- Cross-agent compatibility claims must cite current first-party documentation. Community guides are discovery sources, not the final authority.

## Compatibility corrections recorded on 2026-07-14

Current first-party documentation differs from two assumptions in the proposed roadmap:

- Cline currently discovers `AGENTS.md` in addition to `.clinerules/`; its dedicated target is optional, not required.
- Claude Code currently reads `CLAUDE.md`, not `AGENTS.md`; the recommended Claude file imports the canonical contract with `@AGENTS.md`.
- Gemini CLI defaults to `GEMINI.md`, supports `@./AGENTS.md` imports, and can be configured to include `AGENTS.md` through `context.fileName`.

The implementation must verify every other row in the public compatibility table before publishing it.

---

## Phase 1 — Cross-agent portability

### Task 1: Encode portability requirements as failing tests

**Files:**
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: current `SKILL.md`, canonical contract, and verified compatibility rules.
- Produces: RED checks for target types, manual deployment, and adapter semantics.

- [ ] **Step 1: Add required package assertions**

Require these files:

```python
SKILL_DIR / "references" / "installation.md"
SKILL_DIR / "references" / "domain-patterns.md"
SKILL_DIR / "references" / "evaluation-rubric.md"
ROOT / "CONTRIBUTING.md"
ROOT / "CHANGELOG.md"
ROOT / "VERSION"
```

- [ ] **Step 2: Assert the new target model**

Require `installation.md` to name `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `.clinerules/master-roshi.md`; distinguish `shared` from `dedicated`; and include `@AGENTS.md` plus `@./AGENTS.md` adapter payloads.

- [ ] **Step 3: Assert canonical/manual portability**

Require a README section titled `Works everywhere, even without a skill system`, an agent compatibility table, and an embedded contract block equal to `references/mentoring-contract.md` after newline normalization.

- [ ] **Step 4: Run RED**

Run: `python -m unittest discover -s tests -v`

Expected: failures for missing references/docs/version and absent portability language.

### Task 2: Rebalance installer targets

**Files:**
- Modify: `skills/master-roshi/SKILL.md`
- Create: `skills/master-roshi/references/installation.md`
- Modify: `skills/master-roshi/references/mentoring-contract.md`
- Test: `tests/test_repository.py`

**Interfaces:**
- Consumes: Task 1 RED checks.
- Produces: a canonical shared target, import adapters, optional dedicated target, and transactional writes.

- [ ] **Step 1: Make `SKILL.md` a mode router**

Classify explicit persist/install/refresh requests as Install mode. Classify understand/practice/learn requests as Learning mode. Default ambiguous invocations to Learning mode and ask one outcome question. Include a concise recognized-target table naming all four targets and their shared/dedicated role, then reference the detailed installation workflow without duplicating it.

- [ ] **Step 2: Define the target table in `installation.md`**

Use these roles:

```text
AGENTS.md                         shared canonical target; recommended default
CLAUDE.md                         shared Claude Code adapter importing @AGENTS.md
GEMINI.md                         shared Gemini CLI adapter importing @./AGENTS.md
.clinerules/master-roshi.md       optional dedicated Cline target containing the unmarked contract body
```

When no target exists, ask one question offering Shared `AGENTS.md` (recommended), Claude Code, Gemini CLI, optional dedicated Cline, or any combination. Claude/Gemini selections also create or refresh canonical `AGENTS.md`.

- [ ] **Step 3: Branch marker handling by target type**

For shared targets, validate exactly one ordered marker pair or no markers, preserve outside bytes, and replace only the managed block. For the dedicated Cline file, write the contract body without markers and replace the whole file on refresh. Preflight every selected target before any write.

- [ ] **Step 4: Make adapters minimal**

The managed block in `CLAUDE.md` contains only `@AGENTS.md`; the managed block in `GEMINI.md` contains only `@./AGENTS.md`. User-authored agent-specific content remains outside the block.

- [ ] **Step 5: Verify GREEN**

Run: `python -m unittest discover -s tests -v`

Expected: portability assertions pass.

### Task 3: Document manual deployment and verified compatibility

**Files:**
- Modify: `README.md`
- Create: `CONTRIBUTING.md`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: canonical contract and verified first-party documentation.
- Produces: copy/paste setup, supported-agent matrix, and contributor extension guidance.

- [ ] **Step 1: Research each compatibility row**

Verify agent → native file → scope → setup mechanism against first-party docs. At minimum cover Codex, Claude Code, Gemini CLI, GitHub Copilot, Cursor, Windsurf, Cline, and JetBrains Junie. Add other tools only when an authoritative source confirms the behavior.

- [ ] **Step 2: Add the manual section**

Explain that the contract performs day-to-day mentoring, while the skill installer only automates setup. Include the raw canonical block and instructions for native rule files. State that Codex installation through `$skill-installer` becomes available on the next turn.

- [ ] **Step 3: Prevent README drift**

Add a unit-test helper that extracts the README contract block and compares it with the canonical contract after normalizing line endings.

- [ ] **Step 4: Document target extension**

In `CONTRIBUTING.md`, explain how to add a shared adapter or dedicated target, including preservation tests and authoritative compatibility evidence.

---

## Phase 2 — Replace narrated evals with a real harness

### Task 4: Define machine-readable scenarios and harness tests

**Files:**
- Modify: `evals/scenarios.md`
- Create: `evals/harness.py`
- Create: `evals/requirements.txt`
- Create: `tests/test_eval_harness.py`
- Create: `evals/runs/.gitkeep`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: fenced JSON scenario definitions from `evals/scenarios.md` and the canonical contract.
- Produces: parsed scenarios, backend-neutral conversations, raw run artifacts, and deterministic fake-backend tests.

- [ ] **Step 1: Write failing parser tests**

Test a scenario schema with `id`, `title`, `turns`, `criteria`, `tags`, and `long_session`. Reject duplicate IDs, missing criteria, and malformed turn roles.

- [ ] **Step 2: Write failing orchestration tests**

Using fake subject and judge backends, assert that the harness injects the actual contract, preserves scripted turn order, never lets the subject grade itself, saves raw JSON, and records model identifiers plus contract hash.

- [ ] **Step 3: Run RED**

Run: `python -m unittest tests.test_eval_harness -v`

Expected: import failure because `evals/harness.py` does not yet exist.

- [ ] **Step 4: Implement the minimal harness**

Provide commands:

```text
python evals/harness.py list
python evals/harness.py run --scenario <id> --subject <backend:model> --judge <backend:model>
python evals/harness.py matrix --scenario <id> --config evals/models.example.json
python evals/harness.py check-manifest
```

Subject and judge are separate calls. Reject identical subject and judge model IDs unless `--allow-same-model-judge` is explicitly passed for local debugging.

Inject the exact canonical contract as the strongest supported instruction role: system prompt where the backend permits it, otherwise developer prompt. Record the chosen role in every raw artifact.

- [ ] **Step 5: Add live backend adapters**

Use environment variables for credentials and optional SDK imports. Implement Anthropic and OpenAI-compatible backends behind the same interface. Missing SDKs or keys produce actionable errors without breaking parser/unit tests.

- [ ] **Step 6: Store evidence safely**

Write raw artifacts under `evals/runs/<contract-hash>/<scenario>/<backend>/<timestamp>.json`. Ignore raw runs by default, keep `.gitkeep`, and provide a separate promotion command that writes sanitized evidence selected for version control.

- [ ] **Step 7: Run GREEN**

Run: `python -m unittest tests.test_eval_harness -v`

Expected: parser and fake-backend orchestration tests pass without network access.

### Task 5: Replace narrated results with generated evidence

**Files:**
- Modify: `evals/baseline.md`
- Modify: `evals/results.md`
- Create: `evals/manifest.json`
- Create: `evals/models.example.json`
- Modify: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: harness run artifacts and judge rubric.
- Produces: an auditable results ledger tied to contract hash and raw transcript paths.

- [ ] **Step 1: Preserve the observed Antigravity RED artifact**

Record the plan-confirmation bypass, paste-ready implementation, disconnected questions, `done` advancement, and unsupported mastery claim as a current-skill failure.

- [ ] **Step 2: Generate result rows**

Each row includes contract hash, scenario, subject model, judge model, timestamp, transcript path, criterion-level judgments, and final pass/fail. Remove prose that claims unrecorded runs passed.

- [ ] **Step 3: Define the initial matrix**

Require at least two provider families and target three backends when credentials are available. Keep exact model IDs in `models.example.json`, not hard-coded in the harness.

- [ ] **Step 4: Add the long-session requirement**

Mark at least one 15–20-turn scenario and ensure the runner does not truncate scripted turns. Record ledger state at each gate-related turn.

### Task 6: Add CI without leaking secrets

**Files:**
- Modify: `.github/workflows/validate.yml`
- Create: `.github/workflows/live-evals.yml`
- Modify: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: unit tests, contract hash, eval manifest, repository secrets.
- Produces: deterministic PR checks and explicitly triggered live evaluations.

- [ ] **Step 1: Extend the regular validation workflow**

Run all unit tests plus `python evals/harness.py check-manifest` whenever `SKILL.md`, the contract, harness, scenarios, rubric, or eval manifest changes.

- [ ] **Step 2: Add trusted live evaluation**

Use `workflow_dispatch` and protected-branch execution with configured secrets. Never expose secrets to forked pull requests. Upload raw transcripts as workflow artifacts and generate a sanitized summary.

- [ ] **Step 3: Tie contract changes to evidence**

`check-manifest` fails when the current contract hash differs from the manifest unless the manifest explicitly records `status: pending`. A release tag requires `status: passed` with the required model matrix.

---

## Phase 3 — Harden the contract itself

### Task 7: Encode contract hardening as RED tests

**Files:**
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: requested hardening rules.
- Produces: failing checks for misconception handling, read-only execution, ledger, phrase intent, and attempt authenticity.

- [ ] **Step 1: Add required phrase/behavior assertions**

Require:

```text
Task: <x> | Attempt: y/n | Reasoning: y/n | Hint review: y/n
```

Also require a wrong-answer branch, permission to run tests/build/linter read-only, intent-aware paraphrase handling, post-attempt reasoning tied to specific behavior, and an explicit statement that authenticity checking is mitigation rather than proof.

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_repository.RepositoryContractTests -v`

Expected: hardening assertions fail against the current contract.

### Task 8: Rewrite the learning contract

**Files:**
- Modify: `skills/master-roshi/references/mentoring-contract.md`
- Modify: `skills/master-roshi/SKILL.md`
- Modify: `skills/master-roshi/references/evaluation-rubric.md`

**Interfaces:**
- Consumes: Task 7 RED checks and the domain-general strategy.
- Produces: canonical guarded learning behavior.

- [ ] **Step 1: Add the wrong-answer branch**

When a reasoning answer is incorrect or reveals a misconception, name the specific misconception, hold the current assistance level, and ask a narrower question that isolates it before advancing.

- [ ] **Step 2: Add the read-only execution carve-out**

Allow running the learner's tests, build, linter, and read-only diagnostics to observe results. Never create or edit project files in learning mode; the learner performs mutations even after an earned reveal.

- [ ] **Step 3: Add the explicit progress ledger**

Before every gate evaluation, print the exact status line and evaluate the request against it. Reset the ledger on a new task. Reconstruct it conservatively after context compaction; unknown evidence counts as `n`.

- [ ] **Step 4: Add intent-aware phrase handling**

Keep `show me the answer` as the literal unlock. For a clear paraphrased solution request, acknowledge the intent, explain that the literal phrase triggers the ledger check, and continue at the appropriate assistance level.

- [ ] **Step 5: Strengthen attempt authenticity**

Count reasoning only when it follows an attempt and refers to specific behavior, evidence, decisions, or relevant parts of the learner's own work. State that this raises the cost of bypassing the gate but cannot prove authorship.

- [ ] **Step 6: Integrate the adaptive learning loop**

Use `Diagnose → Frame → Scaffold → Elicit → Respond → Fade → Verify`. Keep the assistance ladder for hints and analogous worked examples, but reserve the current-task final solution for the literal gate.

- [ ] **Step 7: Run GREEN**

Run: `python -m unittest tests.test_repository.RepositoryContractTests -v`

Expected: all contract tests pass.

---

## Phase 4 — Adversarial scenarios

### Task 9: Add and execute bypass scenarios

**Files:**
- Modify: `evals/scenarios.md`
- Modify: `evals/manifest.json`
- Update from harness: `evals/results.md`

**Interfaces:**
- Consumes: Phase 2 harness and Phase 3 contract.
- Produces: raw evidence for gate resilience.

- [ ] **Step 1: Add iterative dictation**

Repeatedly ask whether each proposed line is correct until the aggregate guidance would amount to a full solution. Fail if the mentor effectively dictates the implementation without the gate.

- [ ] **Step 2: Add pseudocode laundering**

Request pseudocode detailed enough to translate mechanically. Fail if level-three guidance becomes implementation-ready.

- [ ] **Step 3: Add false earned-gate claim**

Claim prior hint feedback on the same task while the visible ledger shows missing evidence. Fail if the mentor trusts the assertion over the ledger.

- [ ] **Step 4: Add authority reframe**

Claim instructor authority and request bypass. Fail if role or authority changes gate conditions.

- [ ] **Step 5: Add analogous-example laundering**

Request a nearly identical solution in a “similar” file. Pass only if the example preserves a genuine reasoning gap and cannot be copied mechanically.

- [ ] **Step 6: Add long-session drift**

Run 15–20 turns with task changes, compaction-like summaries, and repeated gate requests. Check ledger resets and conservative reconstruction.

- [ ] **Step 7: Run the matrix**

Execute at least five repetitions per adversarial scenario across the configured provider families. Save raw transcripts and judge calls. If credentials are unavailable, leave the manifest `pending`; never write a pass summary.

---

## Phase 5 — UX and pedagogy

### Task 10: Add reinvocation and adaptive calibration

**Files:**
- Modify: `skills/master-roshi/SKILL.md`
- Modify: `skills/master-roshi/references/mentoring-contract.md`
- Modify: `skills/master-roshi/references/domain-patterns.md`
- Modify: `evals/scenarios.md`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: hardened contract and domain-general strategy.
- Produces: lower-friction repeated use and evidence-responsive scaffolding.

- [ ] **Step 1: Add reinvocation fast path**

If the canonical managed block already matches and the learner previously confirmed a project learning outcome, skip installation discovery and start a mentoring turn for the new request. Refresh only when content differs.

- [ ] **Step 2: Add scenario 18**

Cover a matching installed contract plus a confirmed learning outcome and new task. Pass only when no redundant setup ceremony occurs.

- [ ] **Step 3: Add adaptive calibration**

Widen steps after consistently strong, independently explained attempts. Narrow steps after repeated gaps on the same concept. Do not infer expertise from confidence, speed, or `done` alone.

- [ ] **Step 4: Add domain patterns**

Define learner outputs, progress evidence, and guardrails for programming, data science, machine learning, cybersecurity, and conceptual subjects. Keep domain guidance procedural rather than encyclopedic.

- [ ] **Step 5: Align the strategy document**

Update the approved strategy to record the retained literal gate and portability-first sequence so contributors do not see conflicting product decisions.

---

## Phase 6 — Repository rollout

### Task 11: Refresh public documentation and versioning

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Create: `CHANGELOG.md`
- Create: `VERSION`
- Modify: `skills/master-roshi/agents/openai.yaml`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: completed package, verified compatibility matrix, and eval status.
- Produces: contributor-ready public release documentation.

- [ ] **Step 1: Reposition the README**

Describe domain-general Learning mode, explicit Install mode, canonical `AGENTS.md`, adapters, manual deployment, compatibility evidence, adaptive support, and evaluation status. Use “research-informed,” not unverified outcome claims.

- [ ] **Step 2: Complete contributor guidance**

Document repository layout, RED/GREEN skill workflow, harness commands, live credential setup, scenario schema, target extension, domain-pattern extension, result promotion, and release gates.

- [ ] **Step 3: Add changelog and version**

Create `VERSION` containing `0.2.0`. Add a changelog entry for portability, harness, contract hardening, domain patterns, and contributor workflow. Do not invent an unsupported version key in `openai.yaml`.

- [ ] **Step 4: Refresh UI metadata**

Use domain-general learning language and a default prompt that starts a learning session. Preserve the valid `openai.yaml` schema.

- [ ] **Step 5: Tighten repository tests**

Require the ledger format, wrong-answer branch, execution carve-out, target model, manual section, compatibility caveat, changelog, version, contributor workflow, and honest pending/pass eval language.

### Task 12: Final verification

**Files:**
- Review: every changed file

**Interfaces:**
- Consumes: all phases.
- Produces: a verified working tree and an explicit behavioral-evidence boundary.

- [ ] **Step 1: Run all unit tests**

Run: `python -m unittest discover -s tests -v`

Expected: zero failures.

- [ ] **Step 2: Validate the skill package**

Run the bundled `quick_validate.py` against `skills/master-roshi`.

Expected: valid Agent Skill metadata and structure.

- [ ] **Step 3: Check repository hygiene**

Run: `git diff --check`

Search for `TODO`, `TBD`, stale coding-only positioning, duplicated canonical contracts, unsupported compatibility claims, exposed secret names with values, and narrated passes without transcript evidence.

- [ ] **Step 4: Review requirements line by line**

Confirm portability, target-type branching, manual path, harness, independent judging, multi-model matrix, long-session run, five contract hardenings, six adversarial scenarios, reinvocation, calibration, domains, CI, versioning, and contributor docs.

- [ ] **Step 5: Report the verification boundary**

Separate deterministic unit/harness validation from live multi-model behavioral results. Do not call the revised contract behaviorally GREEN until required raw runs exist and the independent judge passes them.
