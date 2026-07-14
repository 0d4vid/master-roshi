<p align="center">
  <img src="assets/turtle-terminal.svg" alt="A turtle shell shaped like a terminal window" width="220">
</p>

<h1 align="center">Master Roshi</h1>

<p align="center"><strong>Train your reasoning. Ship your own code.</strong></p>

Master Roshi is a small, fan-inspired agent skill that turns coding assistants into
Socratic mentors. Instead of dropping a complete solution at the first sign of
friction, it gives you one useful next step, asks one focused reasoning question,
and reviews what you try. Think less answer vending machine, more calm dojo
session—with your hands still on the keyboard.

## Installation

### With `$skill-installer`

Ask Codex to install the skill directly from its repository path:

```text
$skill-installer Install https://github.com/0d4vid/master-roshi/tree/main/skills/master-roshi
```

Restart or reload your agent session after installation so the new skill is
discovered.

### Manual copy

Clone the repository, then copy `skills/master-roshi` into a recognized skills
directory. For a personal Codex install, the default is
`~/.codex/skills/master-roshi` (or `$CODEX_HOME/skills/master-roshi` when
`CODEX_HOME` is set):

```sh
git clone https://github.com/0d4vid/master-roshi.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R master-roshi/skills/master-roshi "${CODEX_HOME:-$HOME/.codex}/skills/master-roshi"
```

For Claude Code, install it personally at `~/.claude/skills/master-roshi` or
inside one project at `.claude/skills/master-roshi`:

```sh
mkdir -p "$HOME/.claude/skills"
cp -R master-roshi/skills/master-roshi "$HOME/.claude/skills/master-roshi"
```

Keep one installed copy per location so updates stay predictable.

## Usage

Invoke the skill when you want coaching rather than an instant implementation:

```text
$master-roshi Help me build a small URL shortener from an empty project.
```

In an existing project, give the agent a concrete task and let it inspect the
current code before the lesson begins:

```text
$master-roshi Help me add pagination to this API without breaking its current tests.
```

The training loop is intentionally simple:

1. Inspect the project and identify the current task.
2. Offer one actionable step and one reasoning question.
3. Let you make a meaningful attempt.
4. Review the attempt with hints, then tighten the next step.
5. Reveal a direct solution only when the answer gate has been earned.

Safety-critical issues involving security, privacy, or data loss do not wait for
the ceremony. The mentor calls those out directly.

## Agent support

Master Roshi can install or refresh its mentoring contract in either convention:

| Agent | Project instruction file | Documentation |
| --- | --- | --- |
| Codex | `AGENTS.md` | [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Claude Code | `CLAUDE.md` | [Claude Code memory](https://code.claude.com/docs/en/memory) |

If one or both files already exist, the skill refreshes every recognized file
it finds. If neither exists, it asks whether to create the Codex file, the
Claude file, or both.

## The answer gate

The exact phrase `show me the answer` requests a direct solution. It is not a
shortcut around the learning loop: the request is honored after you have made a
meaningful attempt, explained your reasoning, and engaged with hint-based
review for the current task. That earned gating keeps the session useful while
still giving you a clear way forward when you are genuinely stuck.

## Safe project updates

The managed mentoring contract is delimited by these markers:

```html
<!-- master-roshi:start -->
<!-- master-roshi:end -->
```

On update, only the content inside that managed block may be replaced. Text
before and after it—including unmatched project instructions—must be preserved.
If the markers are missing, duplicated, reversed, or otherwise ambiguous, the
skill stops and asks for manual repair instead of guessing. This makes repeated
installs safe and keeps your repository's own rules in charge.

## Contributing

Issues and focused pull requests are welcome. Please keep the mentoring contract
portable, preserve user-authored instruction text, and add or update tests for
behavior changes. Run the repository suite before opening a pull request:

```sh
python -m unittest discover -s tests -v
```

## License and disclaimer

Released under the [MIT License](LICENSE).

Master Roshi is an unofficial, fan-inspired developer tool. It is not affiliated
with, endorsed by, or sponsored by any franchise owner. The project uses original
text and artwork; it includes no copied franchise art or character likeness.
