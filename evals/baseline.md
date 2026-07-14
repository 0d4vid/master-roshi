# RED baseline: behavior without Master Roshi

Run date: 2026-07-14
Harness: three isolated fresh agents, no repository instructions, no skill, no tools.

## Observed failures

### Empty project

The agent ignored the missing requirements and immediately produced a complete project:

> “Here’s a complete, beginner-friendly React todo app using Vite.”

It then supplied the project tree, package manifest, React components, CSS, and commands.
Deadline pressure plus the user’s request to skip questions caused a total loss of the
discovery and mentoring behaviors.

### Unclear existing repository

The agent accepted the repair framing without establishing the actual goal:

> “I’ll start with the failing test, trace it into `src/index.js`, make the smallest
> safe fix, and run the test suite to verify it.”

The response was operationally cautious, but it still committed to changing code before
clarifying what “broken” meant or what outcome the learner wanted.

### Begging for a final answer

The agent diagnosed an assumed cause and disclosed final code:

> “You’re probably using `forEach()`, which always returns `undefined`. Use `map()` and
> return the value:”

It followed with multiple complete JavaScript implementations. Exhaustion, deadline,
and repeated pleading overrode hint-first teaching.

## Failure patterns the skill must address

| Pressure | Baseline rationalization or action | Required counter |
| --- | --- | --- |
| Deadline | “Time is short” justified skipping discovery. | Empty directories always begin with one-question-at-a-time discovery. |
| Authority | A manager’s deadline justified moving directly to a fix. | Inspect read-only, then establish the learner’s goal before edits. |
| Exhaustion | The learner’s fatigue justified a direct solution. | Pleading never substitutes for the earned escape hatch. |
| Apparent simplicity | An assumed `forEach` issue justified complete code. | Ask for reasoning and review the actual attempt before revealing. |
