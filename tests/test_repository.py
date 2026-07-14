from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "master-roshi"
SKILL = SKILL_DIR / "SKILL.md"
CONTRACT = SKILL_DIR / "references" / "mentoring-contract.md"
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
            ROOT / "evals" / "baseline.md",
            ROOT / "evals" / "scenarios.md",
            ROOT / "evals" / "results.md",
            SKILL,
            CONTRACT,
            OPENAI_YAML,
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
        self.assertIn("one question at a time", content.lower())
        self.assertIn("unmatched", content.lower())
        self.assertIn("preserve", content.lower())
        self.assertIn("select every recognized file that exists", content)
        self.assertIn("Preflight all selected files before changing any", content)
        self.assertIn("line-ending normalization", content)

    def test_skill_defines_both_planning_paths_and_safe_append(self) -> None:
        content = read(SKILL)
        self.assertIn("Learner-led plan", content)
        self.assertIn("Agent-proposed plan", content)
        self.assertIn("one planning decision at a time", content)
        self.assertIn("insert one newline separator", content)

        contract = read(CONTRACT)
        self.assertIn("learner-led plan", contract.lower())
        self.assertIn("agent-proposed plan", contract.lower())
        self.assertIn("one planning step at a time", contract.lower())

    def test_reveal_is_text_only_and_requires_all_three_conditions(self) -> None:
        content = read(CONTRACT)
        self.assertIn("Do not create or edit project code at any time", content)
        self.assertIn("the exact phrase does not authorize file mutation", content)
        self.assertIn("the learner made an attempt", content)
        self.assertIn("the learner explained their reasoning", content)
        self.assertIn("at least one hint-based review", content)
        self.assertIn("A new task resets every earned condition", content)

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
            "hint-based review",
            "current task",
            "one actionable step",
            "one reasoning question",
            "security",
            "privacy",
            "data loss",
            "Master Roshi lesson",
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
        self.assertIn('short_description: "Turn coding agents into Socratic mentors"', content)
        self.assertIn("$master-roshi", content)

    def test_readme_has_public_project_information(self) -> None:
        content = read(ROOT / "README.md")
        required = [
            "Train your reasoning. Ship your own code.",
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
        self.assertIn("https://learn.chatgpt.com/docs/agent-configuration/agents-md", content)
        self.assertIn("https://code.claude.com/docs/en/memory", content)

    def test_svg_is_self_contained(self) -> None:
        content = read(ROOT / "assets" / "turtle-terminal.svg")
        self.assertIn("<svg", content)
        self.assertIn("Turtle terminal", content)
        external_content = content.replace('xmlns="http://www.w3.org/2000/svg"', "")
        self.assertNotRegex(external_content, r"https?://")
        self.assertNotIn("<image", content)


if __name__ == "__main__":
    unittest.main()
