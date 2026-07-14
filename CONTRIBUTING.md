# Contributing

Master Roshi treats skill changes like code changes: preserve a failing behavior, change the smallest binding guidance, and verify it in fresh contexts.

## Repository map

- `skills/master-roshi/SKILL.md`: mode router and discovery surface.
- `skills/master-roshi/references/`: canonical contract, installation, domains, and evaluation rubric.
- `evals/baseline.md`: observed failures.
- `evals/scenarios.md`: scripted behavioral cases and criteria.
- `evals/results.md`: only observed results linked to a raw transcript.
- `evals/harness.py`: scenario runner and independent judging.
- `tests/`: deterministic repository and harness checks.

## Workflow

1. Add or update a pressure scenario and capture RED behavior.
2. Add a deterministic test for structure or invariant changes.
3. Run `python -m unittest discover -s tests -v` and confirm the intended failure.
4. Update the skill or reference.
5. Re-run deterministic tests, then fresh behavioral runs.
6. Add a pass to `evals/results.md` only when its raw transcript, subject model, judge model, criteria, and contract hash exist.

Never rewrite `evals/baseline.md` to hide a regression. Pending evaluations stay pending.

## Behavioral evaluations

Scenarios are fenced `json eval` objects with `id`, `title`, scripted user `turns`, explicit `criteria`, `tags`, and a `long_session` flag. Keep criteria observable in a transcript. Do not encode the expected answer in a scripted learner turn.

For live runs, install `evals/requirements.txt`, copy `evals/models.example.json` to the ignored `evals/models.json`, select at least two subject models across provider families and a different judge model, then set provider API keys in the environment. `evals/harness.py matrix --config evals/models.json` writes raw artifacts under a contract-hash directory. Never commit credentials or paste them into a scenario.

The manifest stays `pending` until the required matrix has real artifacts. Mark it `passed` only with the exact canonical contract hash and independently judged evidence. The manual GitHub workflow reads model configuration from the protected `EVAL_MODELS_JSON` secret and uploads run artifacts; it is not triggered for untrusted pull requests.

## Adding targets or domains

For an installation target, cite current first-party documentation, classify it as shared or dedicated, and test preservation/overwrite behavior. For a domain pattern, define learner output, progress evidence, and safety constraints; do not add an encyclopedia.

Shared adapters need marker validation, transactional preflight, and byte-preservation tests. Dedicated targets must be demonstrably single-owner and should use whole-file refresh. A new domain must add at least one pressure scenario covering its evidence model and safety boundary.

## Validation

```sh
python -m unittest discover -s tests -v
python C:/Users/JnoDavid/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/master-roshi
python evals/harness.py check-manifest
```

The `quick_validate.py` path may differ by installation. Use the copy bundled with your skill-creator runtime.
