# Behavioral evaluation results

## Current evidence status

| Evidence set | Status | What exists |
| --- | --- | --- |
| Antigravity CLI alignment test | Observed failure | User-supplied transcript; no harness metadata |
| Legacy scenario summaries | Unverified historical narration | Summaries only; excluded from pass rate |
| Revised structured scenarios | Pending live runs | Executable inputs in `scenarios.md` |
| Deterministic harness tests | Repository check | Parser, separate-judge rule, hashing, transcript persistence |
| Multi-model behavioral matrix | Pending credentials | At least two subjects plus an independent judge required |
| Long-session drift scenario | Pending credentials | Sixteen scripted learner turns |

No behavioral pass rate is claimed in this revision. Repository unit tests prove that required language and evidence machinery exist; they do not prove that a model follows the contract.

## Evidence format

Every live result is a JSON artifact under `evals/runs/` containing:

- scenario and stated criteria;
- subject and judge model identifiers;
- instruction role and SHA-256 contract hash;
- UTC timestamp and raw transcript;
- the independent judge's per-criterion JSON decision.

Run artifacts are uploaded by the manual live-evaluation workflow and are ignored locally by default because they may contain provider output. Curated, reviewed evidence can be versioned deliberately in a future release.

## Commands

```bash
python evals/harness.py list
python evals/harness.py check-manifest
python evals/harness.py run 04-premature-gate --subject anthropic:MODEL --judge openai:MODEL
python evals/harness.py matrix --config evals/models.json --output-dir evals/runs
```

Copy `evals/models.example.json` to the ignored `evals/models.json`, choose current model IDs, and provide the corresponding API keys. Never reuse the same model ID as subject and judge unless investigating the explicit `--allow-same-model` exception; such a run is not independent evidence.
