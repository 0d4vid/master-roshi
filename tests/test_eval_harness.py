from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evals.harness import FakeBackend, Scenario, extract_scenarios, run_scenario


class HarnessTests(unittest.TestCase):
    def test_extracts_fenced_json_scenario(self) -> None:
        text = '''## Example\n```json eval\n{"id":"x","title":"X","turns":[{"role":"user","content":"hi"}],"criteria":["asks"],"tags":["smoke"],"long_session":false}\n```'''
        scenarios = extract_scenarios(text)
        self.assertEqual([s.id for s in scenarios], ["x"])

    def test_rejects_duplicate_ids(self) -> None:
        block = '```json eval\n{"id":"x","title":"X","turns":[{"role":"user","content":"hi"}],"criteria":["asks"],"tags":[],"long_session":false}\n```'
        with self.assertRaisesRegex(ValueError, "duplicate"):
            extract_scenarios(block + "\n" + block)

    def test_run_uses_separate_subject_and_judge_and_saves_evidence(self) -> None:
        scenario = Scenario("x", "X", [{"role": "user", "content": "hi"}], ["asks"], [], False)
        subject = FakeBackend("subject-model", ["mentor response"])
        judge = FakeBackend("judge-model", [json.dumps({"pass": True, "criteria": [{"criterion": "asks", "pass": True}]})])
        with tempfile.TemporaryDirectory() as directory:
            artifact = run_scenario(scenario, "contract", subject, judge, Path(directory))
            saved = json.loads(artifact.read_text(encoding="utf-8"))
        self.assertEqual(saved["subject_model"], "subject-model")
        self.assertEqual(saved["judge_model"], "judge-model")
        self.assertEqual(saved["instruction_role"], "system")
        self.assertIn("contract_hash", saved)
        self.assertEqual(saved["transcript"][-1]["content"], "mentor response")

    def test_rejects_same_subject_and_judge_model_by_default(self) -> None:
        scenario = Scenario("x", "X", [{"role": "user", "content": "hi"}], ["asks"], [], False)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "different models"):
                run_scenario(
                    scenario,
                    "contract",
                    FakeBackend("same", ["reply"]),
                    FakeBackend("same", ["{}"]),
                    Path(directory),
                )


if __name__ == "__main__":
    unittest.main()
