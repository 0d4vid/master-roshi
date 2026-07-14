from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "master-roshi"
SKILL = SKILL_DIR / "SKILL.md"
CONTRACT = SKILL_DIR / "references" / "mentoring-contract.md"
INSTALLATION = SKILL_DIR / "references" / "installation.md"
DOMAINS = SKILL_DIR / "references" / "domain-patterns.md"
RUBRIC = SKILL_DIR / "references" / "evaluation-rubric.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class RepositoryContractTests(unittest.TestCase):
    def test_required_repository_files_exist(self) -> None:
        required = [
            ROOT / "README.md",
            ROOT / "LICENSE",
            ROOT / "assets" / "turtle-terminal.svg",
            ROOT / ".github" / "workflows" / "validate.yml",
            ROOT / ".github" / "workflows" / "live-evals.yml",
            ROOT / "evals" / "baseline.md",
            ROOT / "evals" / "harness.py",
            ROOT / "evals" / "manifest.json",
            ROOT / "evals" / "scenarios.md",
            ROOT / "evals" / "results.md",
            SKILL,
            CONTRACT,
            INSTALLATION,
            DOMAINS,
            RUBRIC,
            OPENAI_YAML,
            ROOT / "CONTRIBUTING.md",
            ROOT / "CHANGELOG.md",
            ROOT / "VERSION",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [], f"Missing files: {missing}")

    def test_skill_frontmatter_and_size(self) -> None:
        content = read(SKILL)
        match = re.match(r"^---\n(.*?)\n---\n", content, flags=re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md needs YAML frontmatter")
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, r"(?m)^name: master-roshi$")
        description = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
        self.assertIsNotNone(description)
        self.assertTrue(description.group(1).startswith("Use when "))
        self.assertLessEqual(len(content.splitlines()), 500)
        self.assertNotRegex(content, r"\b(?:TODO|TBD)\b")

    def test_skill_routes_to_documented_instruction_files(self) -> None:
        content = read(SKILL)
        self.assertIn("AGENTS.md", content)
        self.assertIn("CLAUDE.md", content)
        self.assertIn("references/mentoring-contract.md", content)
        self.assertIn("references/installation.md", content)
        self.assertIn("transactional", content.lower())
        self.assertIn("line-ending normalization", content)

    def test_skill_routes_learning_and_install_modes(self) -> None:
        content = read(SKILL)
        self.assertIn("Learning mode", content)
        self.assertIn("Install mode", content)
        self.assertIn("installation.md", content)
        self.assertIn("domain-patterns.md", content)
        self.assertIn("evaluation-rubric.md", content)
        for target in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".clinerules/master-roshi.md"]:
            self.assertIn(target, content)
        self.assertNotIn("learner wants coding help", content.lower())

    def test_installation_defines_shared_and_dedicated_targets(self) -> None:
        content = read(INSTALLATION)
        for phrase in ["shared", "dedicated", "@AGENTS.md", "@./AGENTS.md", "byte-for-byte", "transactional"]:
            self.assertIn(phrase, content)
        self.assertIn("AGENTS.md", content)
        self.assertIn("CLAUDE.md", content)
        self.assertIn("GEMINI.md", content)
        self.assertIn(".clinerules/master-roshi.md", content)

    def test_contract_has_adaptive_loop_and_hardened_gate(self) -> None:
        content = read(CONTRACT)
        for stage in ["Diagnose", "Frame", "Scaffold", "Elicit", "Respond", "Fade", "Verify"]:
            self.assertIn(stage, content)
        required = [
            "Task: <x> | Attempt: y/n | Reasoning: y/n | Hint review: y/n",
            "tests, build, linter",
            "misconception",
            "show me the answer",
            "specific behavior",
            "mitigation",
            "retrieval",
            "transfer",
            "`done`",
        ]
        for phrase in required:
            self.assertIn(phrase, content)

    def test_domain_patterns_cover_initial_domains_and_safety(self) -> None:
        content = read(DOMAINS).lower()
        for phrase in ["programming", "data science", "machine learning", "cybersecurity", "conceptual", "authorization", "scope", "safe environment"]:
            self.assertIn(phrase, content)

    def test_evaluation_rubric_requires_real_independent_evidence(self) -> None:
        content = read(RUBRIC).lower()
        for phrase in ["fresh context", "critical failure", "subject", "judge", "five", "contract hash", "raw transcript"]:
            self.assertIn(phrase, content)

    def test_adversarial_and_domain_scenarios_are_executable(self) -> None:
        content = read(ROOT / "evals" / "scenarios.md")
        for scenario_id in [
            "06-iterative-dictation",
            "07-pseudocode-laundering",
            "08-false-earned-claim",
            "09-authority-reframe",
            "10-analogous-laundering",
            "11-data-science",
            "12-cyber-safety",
            "14-long-session-drift",
            "18-reinvocation",
        ]:
            self.assertIn(f'"id":"{scenario_id}"', content)
        self.assertGreaterEqual(content.count("```json eval"), 15)

    def test_skill_defines_both_planning_paths_and_safe_append(self) -> None:
        content = read(SKILL)
        self.assertIn("Learner-led plan", content)
        self.assertIn("Agent-proposed plan", content)
        self.assertIn("one planning decision at a time", content)
        self.assertIn("insert one newline separator", read(INSTALLATION))

        contract = read(CONTRACT)
        self.assertIn("learner-led plan", contract.lower())
        self.assertIn("agent-proposed plan", contract.lower())
        self.assertIn("one planning decision at a time", contract.lower())

    def test_reveal_is_text_only_and_requires_all_three_conditions(self) -> None:
        content = read(CONTRACT)
        self.assertIn("Never create or edit project files in Learning mode", content)
        self.assertIn("Attempt:", content)
        self.assertIn("Reasoning:", content)
        self.assertIn("Hint review:", content)
        self.assertIn("A new task resets every field", content)

    def test_contract_defines_ordered_turn_and_hint_progression(self) -> None:
        content = read(CONTRACT)
        concept = content.index("**Concept:**")
        action = content.index("**Action:**")
        question = content.index("**Reasoning question:**")
        self.assertLess(concept, action)
        self.assertLess(action, question)
        for level in range(1, 5):
            self.assertRegex(content, rf"(?m)^{level}\. ")

    def test_mentoring_contract_contains_required_guardrails(self) -> None:
        content = read(CONTRACT)
        self.assertEqual(content.count("<!-- master-roshi:start -->"), 1)
        self.assertEqual(content.count("<!-- master-roshi:end -->"), 1)
        required_phrases = [
            "show me the answer",
            "attempt",
            "reasoning",
            "hint-based feedback",
            "current task",
            "one learner action",
            "one question whose answer changes the next turn",
            "security",
            "privacy",
            "data loss",
            "retrieval or transfer",
        ]
        lowered = content.lower()
        for phrase in required_phrases:
            self.assertIn(phrase.lower(), lowered)

        fabricated_attributions = [
            "confucius says",
            "lao tzu says",
            "japanese proverb",
            "chinese proverb",
            "asian proverb",
            "zen proverb",
        ]
        for phrase in fabricated_attributions:
            self.assertNotIn(phrase, lowered)

    def test_openai_metadata_matches_the_skill(self) -> None:
        content = read(OPENAI_YAML)
        self.assertIn('display_name: "Master Roshi"', content)
        self.assertIn('short_description: "Learn technical subjects without outsourcing the thinking"', content)
        self.assertIn("$master-roshi", content)

    def test_readme_has_public_project_information(self) -> None:
        content = read(ROOT / "README.md")
        required = [
            "Learn with AI without outsourcing the thinking.",
            "Installation",
            "AGENTS.md",
            "CLAUDE.md",
            "show me the answer",
            "Contributing",
            "MIT",
            "unofficial",
        ]
        for phrase in required:
            self.assertIn(phrase, content)
        self.assertIn("https://docs.github.com/en/copilot/reference/custom-instructions-support", content)
        self.assertIn("https://code.claude.com/docs/en/memory", content)
        self.assertIn("Works everywhere, even without a skill system", content)
        self.assertIn("Compatibility", content)
        self.assertIn("Learning mode", content)
        self.assertIn("Install mode", content)
        self.assertIn("CONTRIBUTING.md", content)

    def test_readme_embeds_the_canonical_manual_contract(self) -> None:
        content = read(ROOT / "README.md")
        match = re.search(r"<summary>Raw portable contract block</summary>\s*```markdown\n(.*?)```", content, re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1).rstrip() + "\n", read(CONTRACT))

    def test_contributor_docs_explain_validation_and_evidence(self) -> None:
        content = read(ROOT / "CONTRIBUTING.md")
        for phrase in ["evals/baseline.md", "evals/scenarios.md", "evals/results.md", "python -m unittest", "quick_validate.py", "raw transcript"]:
            self.assertIn(phrase, content)

    def test_svg_is_self_contained(self) -> None:
        content = read(ROOT / "assets" / "turtle-terminal.svg")
        self.assertIn("<svg", content)
        self.assertIn("Turtle terminal", content)
        external_content = content.replace('xmlns="http://www.w3.org/2000/svg"', "")
        self.assertNotRegex(external_content, r"https?://")
        self.assertNotIn("<image", content)


if __name__ == "__main__":
    unittest.main()
