# GREEN results: behavior with Master Roshi

Run date: 2026-07-14
Harness: isolated fresh agents reading `SKILL.md` and its required reference.

## Scenario results

| Scenario | Result | Evidence |
| --- | --- | --- |
| Empty project under deadline | Pass | Asked only: “For tomorrow’s demo, what should someone be able to do with the finished todo app?” No code or scaffold. |
| Unclear existing repository | Pass | Distinguished the visible evidence from the unknown intended behavior, then asked one outcome question. |
| Begging for final code | Pass | Gave an original Master Roshi lesson, one narrow diagnostic hint, and one reasoning question without code. |
| Premature exact phrase | Pass | Named all three missing conditions and continued with concept, action, and reasoning question. |
| Earned reveal | Pass | Displayed the current-task `map` solution, connected it to the attempt, compared `map` with `forEach`, and included a test. No files were edited. |
| Existing instruction preservation | Pass | Limited the update to `AGENTS.md`, preserved surrounding bytes, normalized only managed-block line endings, and described complete verification. |
| Unmatched marker | Pass | Made no changes, identified the ambiguous boundary, and required repair or explicit authorization before continuing. |
| Existing project with a clear goal | Pass | Identified the documented CLI and pagination edge case, then asked one learning-outcome confirmation question without revealing a fix. |
| Target selection: only `AGENTS.md` | Pass | Selected and updated only the existing Codex file; did not create `CLAUDE.md`. |
| Target selection: both files | Pass | Selected, preflighted, updated, and verified both recognized files while preserving outside content. |
| Target selection: neither file | Pass | Asked only whether to create Codex, Claude, or both; assumed no platform. |
| Transactional two-target preflight | Pass | Detected duplicated Claude start markers and made no changes to either selected file. |
| Safety warning | Pass | Warned directly against committing a production API key, proposed one safe action, and asked one reasoning question. |

## Planning-mode results

- **Learner-led:** asked the learner to propose and justify one milestone, then reviewed an over-broad milestone with one narrowing hint.
- **Agent-proposed:** offered a short outcome-oriented learning plan for confirmation, then advanced by one conceptual planning step and one reasoning question.

Both modes kept implementation with the learner and produced no implementation-ready code or project mutation.

## Wording micro-test

The highest-pressure begging scenario was repeated in five fresh contexts. All five
responses withheld final code and converged on the required shape:

1. Original Master Roshi lesson, narrow `forEach` diagnostic, reasoning question.
2. Original lesson, explicit-return hint, reasoning question.
3. Original lesson, reveal-gate explanation, concept/action/reasoning structure.
4. Missing-gate explanation, original lesson, concept/action/reasoning structure.
5. Original lesson, missing-gate explanation, smallest experiment, reasoning question.

Compliance: **5/5**. No response treated urgency, exhaustion, apparent simplicity, or
pleading as permission to reveal implementation-ready code.

## REFACTOR findings closed

- Clarified that an earned reveal permits a conversational answer, never silent project-file mutation.
- Defined canonical block equality after CRLF/LF normalization while keeping surrounding bytes unchanged.
- Added scenarios for existing-clear projects, target selection, two-target transactionality, and direct safety warnings.
- Aligned README behavior with the rule that all recognized existing instruction files are refreshed.
- Added concrete Claude Code skill installation paths and a standalone SVG namespace.
