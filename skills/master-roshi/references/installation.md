# Installation workflow

Install only after an explicit persistence request. The operation is instruction-only and transactional.

## Targets

| Target | Type | Managed payload |
| --- | --- | --- |
| `AGENTS.md` | shared | canonical marked contract |
| `CLAUDE.md` | shared | marked adapter containing `@AGENTS.md` |
| `GEMINI.md` | shared | marked adapter containing `@./AGENTS.md` |
| `.clinerules/master-roshi.md` | dedicated | unmarked canonical contract body |

`AGENTS.md` is the recommended default. Claude Code selection resolves to `AGENTS.md` plus `CLAUDE.md`; Gemini CLI resolves to `AGENTS.md` plus `GEMINI.md`. Cline already supports `AGENTS.md`; its dedicated target is optional.

## 1. Inspect and select

Locate the project root read-only. Detect every target plus relevant docs and configuration. Establish the learning outcome only when it is not already confirmed.

When no target exists, ask one question offering Shared `AGENTS.md` (recommended), Claude Code, Gemini CLI, optional dedicated Cline, or any combination. Do not infer a platform.

## 2. Preflight every resolved target

Use `<!-- master-roshi:start -->` and `<!-- master-roshi:end -->` for shared files. A shared target is valid only with no markers or exactly one ordered, non-nested pair. A dedicated target has no markers and is wholly owned by Master Roshi.

Preflight all selected files before changing any. Unmatched, reversed, duplicated, or nested markers in any shared target abort the entire transactional update. Explain the malformed state; do not guess or skip that target.

## 3. Write by target type

For a shared file with a valid block, replace only that block. With no block, append the managed payload. Preserve all outside content byte-for-byte. Retain the newline convention; if a nonempty file lacks a final newline, preserve its bytes and insert one newline separator before the block. Adapt only managed payload line endings and compare content after line-ending normalization.

For `.clinerules/master-roshi.md`, create parent directories when selected and replace the whole file with the canonical contract body without the start/end markers. Do not apply shared-file marker logic.

## 4. Verify

Re-read every selected target. Verify payload equality, adapter text, marker counts for shared files, absence of markers for the dedicated file, preservation of outside bytes, and that no unselected file changed. Report a mismatch plainly and do not claim success.

