# Multi-Agent Compatibility Design

## Goal

Extend Master Roshi so the same skill package can install durable Socratic mentoring instructions for Codex, Claude Code, Google Antigravity IDE, Antigravity CLI, Hermes Agent, and OpenCode without duplicating the canonical mentoring contract unnecessarily or overwriting user-authored rules.

## Compatibility model

The package remains an Agent Skill with `skills/master-roshi/SKILL.md` as its entry point and `references/mentoring-contract.md` as the single canonical contract. Its existing frontmatter (`name` and `description`) is accepted by the additional agents; agent-specific metadata stays optional and non-blocking.

Project-local installation paths are documented by surface:

| Surface | Skill location |
| --- | --- |
| Codex | `$CODEX_HOME/skills/master-roshi/` or `~/.codex/skills/master-roshi/` |
| Claude Code | `.claude/skills/master-roshi/` or `~/.claude/skills/master-roshi/` |
| Antigravity IDE and CLI | `.agents/skills/master-roshi/` |
| OpenCode | `.agents/skills/master-roshi/` or `.opencode/skills/master-roshi/` |
| Hermes Agent | `~/.hermes/skills/master-roshi/` or `hermes skills install` |

The shared `.agents/skills/master-roshi/` path is the recommended project-local installation when Antigravity and OpenCode must use the same copy.

## Platform selection and target resolution

After directory classification and learning-context discovery, the skill asks which agent surfaces the project should support. It may recommend detected agents, but it never infers a write target solely from an unrelated file. Selected platforms are resolved into effective instruction targets, then duplicate paths are collapsed before preflight.

| Selected platform | Effective instruction target |
| --- | --- |
| Codex | Root `AGENTS.md` |
| Claude Code | Root `CLAUDE.md` |
| Antigravity IDE + CLI | One canonical root file plus `.agents/rules/master-roshi.md` adapter |
| Hermes Agent | First effective file in `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`; create `AGENTS.md` if none exists |
| OpenCode | First effective file in `AGENTS.md`, `CLAUDE.md`, deprecated `CONTEXT.md`; create `AGENTS.md` if none exists |

For the combined Antigravity target, choose the canonical root file in this order:

1. A selected or already-planned `AGENTS.md`.
2. An existing `AGENTS.md`.
3. An existing `GEMINI.md`.
4. Otherwise create `AGENTS.md`.

The Antigravity IDE adapter contains a managed reference to that canonical file, such as `@../../AGENTS.md`. Antigravity CLI reads the canonical root file directly. This provides one contract for both surfaces while following the IDE's workspace-rule convention.

When several selected platforms resolve to the same path, write one managed contract block. If Hermes has an existing higher-priority `.hermes.md`, update it even when another selected platform also requires `AGENTS.md`, because Hermes would otherwise ignore the shared file.

## Precedence-impact safeguard

Before writing, calculate each selected agent's effective instruction source after the proposed changes. If creating a higher-priority file would cause an existing lower-priority file with user-authored content to stop loading, explain the exact shadowing change and require confirmation. Never copy, merge, or delete user instructions automatically.

Examples include creating `AGENTS.md` for Codex while an OpenCode project currently relies on `CLAUDE.md`, or while Hermes currently relies on its lower-priority `CLAUDE.md` fallback.

## Transactional managed updates

Contract targets retain the canonical markers:

```text
<!-- master-roshi:start -->
<!-- master-roshi:end -->
```

The Antigravity adapter uses the same markers around its single `@` reference, but its expected payload is the resolved reference rather than the mentoring contract.

Preflight every resolved contract target and adapter before changing any file. Unmatched, reversed, duplicated, or nested markers in any target abort the entire transaction. Preserve all bytes outside each managed block, retain newline conventions, and verify every target after writing. Create `.agents/rules/` only when Antigravity IDE is selected.

## Documentation changes

The README will add:

- a supported-agent table separating skill installation from generated instruction targets;
- a shared Antigravity/OpenCode installation example using `.agents/skills/`;
- a Hermes installation example;
- precedence notes for Hermes and OpenCode;
- an Antigravity IDE/CLI explanation showing the canonical file and adapter.

The support claim remains limited to the documented Agent Skill and instruction discovery behavior. Plugin packaging, global instruction mutation, and automatic migration of unrelated rule content remain out of scope.

## Testing strategy

Static validation will fail first for the new platform names, target files, shared installation path, adapter behavior, precedence ordering, deduplication language, and documentation links. The implementation then updates the skill and README until the suite passes.

Fresh-agent pressure scenarios will cover:

1. Empty project selecting combined Antigravity creates one canonical contract and one adapter.
2. Existing `GEMINI.md` becomes the Antigravity canonical file when no `AGENTS.md` is selected or present.
3. Antigravity plus OpenCode deduplicates their shared `AGENTS.md` contract.
4. Hermes chooses `.hermes.md` over `AGENTS.md` and does not edit a lower-priority file unnecessarily.
5. OpenCode uses existing `CLAUDE.md` when no `AGENTS.md` exists.
6. Selecting Codex plus OpenCode detects that a new `AGENTS.md` would shadow OpenCode's existing `CLAUDE.md`.
7. A malformed Antigravity adapter aborts all selected writes.
8. Existing content remains byte-for-byte unchanged across nested and root targets.

The official skill validator, repository unit suite, SVG parser, staged diff check, and GitHub Actions validation remain release gates.

## Documentation sources

- [Antigravity Agent Skills](https://antigravity.google/docs/skills)
- [Antigravity IDE rules](https://antigravity.google/docs/ide-rules)
- [Antigravity CLI migration and context files](https://antigravity.google/docs/gcli-migration)
- [Hermes Agent context files](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/context-files.md)
- [Hermes Agent skills](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)
- [OpenCode rules](https://opencode.ai/docs/rules/)
- [OpenCode skills](https://opencode.ai/docs/skills/)
