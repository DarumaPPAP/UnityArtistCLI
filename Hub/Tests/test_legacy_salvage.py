from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tests/fixtures/legacy/MyUnityMCP-v1.1.1"
CAPABILITIES = FIXTURE_ROOT / "capabilities.json"
PROVENANCE = FIXTURE_ROOT / "provenance.json"
MATRIX = ROOT / "docs/architecture/legacy-capability-salvage.csv"
EXPECTED = {"graphics": 32, "agent": 10, "world": 3, "profiler": 8, "addressables": 4, "ui": 5, "animation": 5, "audio": 5, "cinematic": 5}
DECISIONS = {"FUTURE_SPEC_ARCHIVED", "KNOWLEDGE_ARCHIVED", "RETIRED"}


class LegacySalvageTests(unittest.TestCase):
    def test_frozen_inventory_matches_archived_matrix(self) -> None:
        fixture = json.loads(CAPABILITIES.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        capabilities = fixture["capabilities"]

        with MATRIX.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))

        fixture_names = [item["legacy_tool"] for item in capabilities]
        self.assertEqual(len(fixture_names), 77)
        self.assertEqual(Counter(name.split(".")[0] for name in fixture_names), EXPECTED)
        self.assertEqual(provenance["archived_tool_count"], 77)
        self.assertEqual(provenance["release"], "v1.1.1")
        self.assertEqual(
            provenance["release_commit_sha"],
            "ea437f11bcf5b46b6a7575f9d2f9b81a9c02da7c",
        )

        self.assertEqual(len(rows), 77)
        self.assertEqual(Counter(row["legacy_tool"] for row in rows), Counter(fixture_names))
        self.assertTrue(all(row["decision"] in DECISIONS for row in rows))

        fixture_by_name = {item["legacy_tool"]: item for item in capabilities}
        for row in rows:
            with self.subTest(tool=row["legacy_tool"]):
                item = fixture_by_name[row["legacy_tool"]]
                self.assertEqual(item["legacy_module"], row["legacy_module"])
                self.assertEqual(item["responsibility"], row["responsibility"])
                self.assertEqual(item["decision"], row["decision"])
                self.assertEqual(item["historical_source"], row["source"])
                self.assertTrue(item["source_blob_sha"])
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

        self.assertEqual(
            Counter(row["decision"] for row in rows),
            {
                "FUTURE_SPEC_ARCHIVED": 50,
                "KNOWLEDGE_ARCHIVED": 12,
                "RETIRED": 15,
            },
        )
        self.assertFalse(any(row["decision"] in {"PORT", "REPLACED"} for row in rows))

        future = [row for row in rows if row["decision"] == "FUTURE_SPEC_ARCHIVED"]
        self.assertTrue(
            all(row["migration_status"] == "LEGACY_PORT_NOT_ADOPTED_ARCHIVED" for row in future)
        )
        knowledge = [row for row in rows if row["decision"] == "KNOWLEDGE_ARCHIVED"]
        self.assertTrue(
            all(row["migration_status"] == "KNOWLEDGE_ARCHIVED_RUNTIME_NOT_ADOPTED" for row in knowledge)
        )
        retired = [row for row in rows if row["decision"] == "RETIRED"]
        self.assertTrue(all(row["migration_status"] == "RETIRED_LEGACY_API" for row in retired))


if __name__ == "__main__":
    unittest.main()
