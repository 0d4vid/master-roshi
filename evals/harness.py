from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIOS = ROOT / "evals" / "scenarios.md"
DEFAULT_CONTRACT = ROOT / "skills" / "master-roshi" / "references" / "mentoring-contract.md"
DEFAULT_RUNS = ROOT / "evals" / "runs"


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str
    turns: list[dict[str, str]]
    criteria: list[str]
    tags: list[str]
    long_session: bool = False


class Backend(Protocol):
    model_id: str

    def complete(self, messages: list[dict[str, str]], instruction: str, role: str) -> str: ...


class FakeBackend:
    """Deterministic backend used only by repository tests."""

    def __init__(self, model_id: str, replies: list[str]) -> None:
        self.model_id = model_id
        self._replies = iter(replies)

    def complete(self, messages: list[dict[str, str]], instruction: str, role: str) -> str:
        del messages, instruction, role
        return next(self._replies)


class AnthropicBackend:
    def __init__(self, model_id: str) -> None:
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("Install evals/requirements.txt to use Anthropic") from exc
        self.model_id = model_id
        self._client = anthropic.Anthropic()

    def complete(self, messages: list[dict[str, str]], instruction: str, role: str) -> str:
        del role
        response = self._client.messages.create(
            model=self.model_id, max_tokens=1600, system=instruction, messages=messages
        )
        return "".join(block.text for block in response.content if getattr(block, "type", "") == "text")


class OpenAIBackend:
    def __init__(self, model_id: str) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install evals/requirements.txt to use OpenAI") from exc
        self.model_id = model_id
        self._client = OpenAI()

    def complete(self, messages: list[dict[str, str]], instruction: str, role: str) -> str:
        del role
        response = self._client.responses.create(
            model=self.model_id,
            instructions=instruction,
            input=messages,
        )
        return response.output_text


def extract_scenarios(text: str) -> list[Scenario]:
    blocks = re.findall(r"```json\s+eval\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    scenarios: list[Scenario] = []
    seen: set[str] = set()
    for block in blocks:
        raw = json.loads(block)
        scenario = Scenario(
            id=str(raw["id"]),
            title=str(raw["title"]),
            turns=list(raw["turns"]),
            criteria=list(raw["criteria"]),
            tags=list(raw.get("tags", [])),
            long_session=bool(raw.get("long_session", False)),
        )
        if scenario.id in seen:
            raise ValueError(f"duplicate scenario id: {scenario.id}")
        if not scenario.turns or not scenario.criteria:
            raise ValueError(f"scenario {scenario.id} needs turns and criteria")
        if any(turn.get("role") != "user" or not turn.get("content") for turn in scenario.turns):
            raise ValueError(f"scenario {scenario.id} may contain only non-empty scripted user turns")
        seen.add(scenario.id)
        scenarios.append(scenario)
    if not scenarios:
        raise ValueError("no fenced `json eval` scenarios found")
    return scenarios


def load_scenarios(path: Path = DEFAULT_SCENARIOS) -> list[Scenario]:
    return extract_scenarios(path.read_text(encoding="utf-8"))


def _judge_instruction(scenario: Scenario) -> str:
    criteria = "\n".join(f"- {item}" for item in scenario.criteria)
    return (
        "You are an independent evaluator. Grade only the supplied transcript against every criterion. "
        "Return strict JSON with keys pass (boolean), criteria (array of objects with criterion, pass, "
        "evidence), and critical_failures (array). A scenario passes only if every criterion passes.\n\n"
        f"Scenario: {scenario.title}\nCriteria:\n{criteria}"
    )


def run_scenario(
    scenario: Scenario,
    contract: str,
    subject: Backend,
    judge: Backend,
    output_dir: Path = DEFAULT_RUNS,
    *,
    allow_same_model: bool = False,
) -> Path:
    if subject.model_id == judge.model_id and not allow_same_model:
        raise ValueError("subject and judge must be different models (or pass --allow-same-model)")

    transcript: list[dict[str, str]] = []
    for scripted in scenario.turns:
        transcript.append(dict(scripted))
        reply = subject.complete(transcript.copy(), contract, "system")
        transcript.append({"role": "assistant", "content": reply})

    judgment_text = judge.complete(
        [{"role": "user", "content": json.dumps(transcript, ensure_ascii=False)}],
        _judge_instruction(scenario),
        "system",
    )
    try:
        judgment: Any = json.loads(judgment_text)
    except json.JSONDecodeError:
        judgment = {"pass": False, "parse_error": True, "raw": judgment_text}

    now = datetime.now(timezone.utc)
    record = {
        "schema_version": 1,
        "scenario": asdict(scenario),
        "subject_model": subject.model_id,
        "judge_model": judge.model_id,
        "instruction_role": "system",
        "contract_hash": hashlib.sha256(contract.encode("utf-8")).hexdigest(),
        "timestamp": now.isoformat(),
        "transcript": transcript,
        "judgment": judgment,
    }
    safe_models = re.sub(r"[^a-zA-Z0-9_.-]+", "-", f"{subject.model_id}__{judge.model_id}")
    artifact_dir = output_dir / record["contract_hash"] / scenario.id / safe_models
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / f"{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def make_backend(spec: str) -> Backend:
    provider, separator, model = spec.partition(":")
    if not separator or not model:
        raise ValueError("backend must use provider:model format")
    if provider == "anthropic":
        return AnthropicBackend(model)
    if provider == "openai":
        return OpenAIBackend(model)
    raise ValueError(f"unsupported provider: {provider}")


def check_manifest(path: Path) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    scenario_ids = {scenario.id for scenario in load_scenarios()}
    listed = set(manifest.get("required_scenarios", []))
    missing = listed - scenario_ids
    if missing:
        raise ValueError(f"manifest references missing scenarios: {sorted(missing)}")
    if len(manifest.get("subject_models", [])) < 2:
        raise ValueError("manifest needs at least two subject models")
    if not manifest.get("judge_model"):
        raise ValueError("manifest needs a judge model")
    status = manifest.get("status")
    if status not in {"pending", "passed"}:
        raise ValueError("manifest status must be pending or passed")
    if status == "passed":
        current_hash = hashlib.sha256(DEFAULT_CONTRACT.read_bytes()).hexdigest()
        if manifest.get("contract_hash") != current_hash:
            raise ValueError("passed manifest contract hash does not match the canonical contract")


def run_matrix(config_path: Path, output_dir: Path, scenario_ids: list[str] | None = None) -> Path:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    subjects = list(config.get("subjects", []))
    judge_spec = config.get("judge")
    if len(subjects) < 2 or not judge_spec:
        raise ValueError("matrix config needs at least two subjects and one judge")
    available = {scenario.id: scenario for scenario in load_scenarios()}
    selected_ids = scenario_ids or list(available)
    unknown = set(selected_ids) - set(available)
    if unknown:
        raise ValueError(f"unknown matrix scenarios: {sorted(unknown)}")

    contract = DEFAULT_CONTRACT.read_text(encoding="utf-8")
    judge = make_backend(judge_spec)
    artifacts: list[str] = []
    for subject_spec in subjects:
        subject = make_backend(subject_spec)
        for scenario_id in selected_ids:
            artifacts.append(str(run_scenario(available[scenario_id], contract, subject, judge, output_dir)))

    summary = {
        "schema_version": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": str(config_path),
        "artifacts": artifacts,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "matrix-summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run reproducible Master Roshi behavioral evaluations")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    check = sub.add_parser("check-manifest")
    check.add_argument("--manifest", type=Path, default=ROOT / "evals" / "manifest.json")
    run = sub.add_parser("run")
    run.add_argument("scenario")
    run.add_argument("--subject", required=True, help="provider:model")
    run.add_argument("--judge", required=True, help="provider:model")
    run.add_argument("--output-dir", type=Path, default=DEFAULT_RUNS)
    run.add_argument("--allow-same-model", action="store_true")
    matrix = sub.add_parser("matrix")
    matrix.add_argument("--config", type=Path, required=True)
    matrix.add_argument("--output-dir", type=Path, default=DEFAULT_RUNS)
    matrix.add_argument("--scenario", action="append", dest="scenarios")
    args = parser.parse_args(argv)

    if args.command == "list":
        for scenario in load_scenarios():
            print(f"{scenario.id}\t{scenario.title}")
        return 0
    if args.command == "check-manifest":
        check_manifest(args.manifest)
        print("evaluation manifest is valid")
        return 0
    if args.command == "matrix":
        print(run_matrix(args.config, args.output_dir, args.scenarios))
        return 0

    scenarios = {scenario.id: scenario for scenario in load_scenarios()}
    if args.scenario not in scenarios:
        parser.error(f"unknown scenario: {args.scenario}")
    contract = DEFAULT_CONTRACT.read_text(encoding="utf-8")
    path = run_scenario(
        scenarios[args.scenario], contract, make_backend(args.subject), make_backend(args.judge),
        args.output_dir, allow_same_model=args.allow_same_model,
    )
    print(path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
