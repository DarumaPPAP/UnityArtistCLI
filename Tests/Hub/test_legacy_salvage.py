from __future__ import annotations

from collections import Counter
import csv
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Legacy/MyUnityMCP-1.1.1/Package/Editor"
MATRIX = ROOT / "Design/legacy-capability-salvage.csv"
TOOL = re.compile(r'\\[McpForUnityTool\\(\\s*"([^"]+)"')
EXPECTED = {"graphics": 32, "agent": 10, "world": 3, "profiler": 8, "addressables": 4, "ui": 5, "animation": 5, "audio": 5, "cinematic": 5}
DECISIONS = {"FUTURE_SPEC_ARCHIVED", "KNOWLEDGE_ARCHIVED", "RETIRED"}


class LegacySalvageTests(unittest.TestCase):
    def test_source_inventory_matches_archived_matrix(self) -> None:
        source_tools = [
            match.group(1)
            for path in SOURCE.rglob("*.cs")
            for match in TOOL.finditer(path.read_text(encoding="utf-8-sig"))
        ]
        with MATRIX.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))

        self.assertEqual(len(source_tools), 77)
        self.assertEqual(Counter(name.split(".")[0] for name in source_tools), EXPECTED)
        self.assertEqual(len(rows), 77)
        self.assertEqual(Counter(row["legacy_tool"] for row in rows), Counter(source_tools))
        self.assertTrue(all(row["decision"] in DECISIONS for row in rows))

        for row in rows:
            with self.subTest(tool=row["legacy_tool"]):
                self.assertTrue(
                    all(
                        row[field]
                        for field in (
                            "legacy_module",
                            "responsibility",
                            "current_equivalent",
                            "current_owner",
                            "gap",
                            "target_owner",
                            "migration_risk",
                            "replacement_evidence",
                            "source",
                            "replacement_contract",
                            "migration_status",
                            "active_dependency",
                            "tests",
                            "documentation",
                            "runtime_evidence_requirement",
                        )
                    )
                )
                self.assertTrue((ROOT / row["source"]).is_file())

        self.assertEqual(
            Counter(row["decision"] for row in rows),
            {
                "FUTURE_SPEC_ARCHIVED": 50,
                "KNOWLEDGE_ARCHIVED": 12,
                "RETIRED": 15,
            },
        )
        self.assertFalse(any(row["decision"] == "PORT" for row in rows))
        self.assertFalse(any(row["decision"] == "REPLACED" for row in rows))

        future = [row for row in rows if row["decision"] == "FUTURE_SPEC_ARCHIVED"]
        self.assertEqual(len(future), 50)
        self.assertTrue(
            all(row["migration_status"] == "LEGACY_PORT_NOT_ADOPTED_ARCHIVED" for row in future)
        )
        self.assertTrue(
            all(
                row["replacement_contract"] == "not_applicable_legacy_api_not_adopted"
                for row in future
            )
        )

        knowledge = [row for row in rows if row["decision"] == "KNOWLEDGE_ARCHIVED"]
        self.assertEqual(len(knowledge), 12)
        self.assertTrue(
            all(row["migration_status"] == "KNOWLEDGE_ARCHIVED_RUNTIME_NOT_ADOPTED" for row in knowledge)
        )

        retired = [row for row in rows if row["decision"] == "RETIRED"]
        self.assertEqual(len(retired), 15)
        self.assertTrue(all(row["migration_status"] == "RETIRED_LEGACY_API" for row in retired))


if __name__ == "__main__":
    unittest.main()
