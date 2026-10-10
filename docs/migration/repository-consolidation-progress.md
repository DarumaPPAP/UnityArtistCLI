# Repository Consolidation Progress

P0 verified: Agent #173 `007dbc66365a8c2ca26fa12cbc89d5b544d7339a`; Hub #93 `83dcd6e7a2cba94e5bc0b4975579252da1d5e69a`. P0 inventories/import plans remain immutable historical baseline files.

| Phase | Status | Branch / PR |
|---|---|---|
| P1 | Consumer dual-read merged | Agent #175 |
| P2 | Hub Catalog merged | Hub main `ccd6a21` |
| P3 | Agent final Hub core pin and Artist dual-read merged; required Canonical Green | Agent #176 `66463f54b92178a830a746b8d24e3cbe7d729605` |
| P4 | Hub Artist/Compatibility producer migration locally verified; PR/merge pending | `chore/repository-consolidation-p4` |
| P5 | Agent Python migration proceeds separately | Agent |
| P6 | Hub human docs and orphan cleanup implemented with P4 | `chore/repository-consolidation-p4` |
| P7 | Separate prepared commit; not applied to P4 | pending P4 integration |
| P8 | Layout contract deferred until all migrations land | pending |

Artist CLI, host tests and Artist scripts are now owned by `cli/artist/`. The support matrix is `ci/compatibility/support-matrix.yaml`; static verifiers are `ci/verify/`. All previously checked-in session and acceptance records contained measured assertions and are preserved byte-for-byte under `ci/evidence/artist/historical/`, with original SHA-256 and original paths in the separate historical index. There is no current measured evidence promotion. `passed` inside an archived record never proves current Editor/Pipeline/visual success.

6000.6 Artist E2E and historical 2022.3 project contents are retained, with only the local UPM dependency depth corrected. Frozen Legacy file hashes and tag object are unchanged. Human design/specification/decision/migration records live in docs. The before/after map, asset hashes and orphan GUID-search result are committed in `docs/migration/consolidation/p4-path-map.json`.

Local validation: authority/registry/export/branch-policy PASS; Hub 32 tests PASS; all 11 compatibility/backend/archive static verifiers PASS; integration 2 tests PASS; .NET Release build PASS (0 warnings, 0 errors); Artist CLI host 11 tests PASS; shell installer syntax PASS. Static evidence validators verify the preserved historical records, not current Unity execution.

Artist required host job retains its name and runs every PR, including unrelated PRs. Hub remains static metadata/contracts/validation; canonical IDs, package ID, C# assets and .meta/GUID bytes are unchanged. No Source Lock edits, runtime, new backends directory, Release/tag publication or push/PR/merge occurred in this producer implementation.

Next: parent verifies this Hub snapshot/host source against Agent main, creates P4 PR and observes required checks Green before Squash Merge. Agent final pin then targets the verified Hub merge full SHA. P7 and P8 follow on their own integration steps. Licensed Unity Editor / Pipeline / Player / visual / device execution remains `BLOCKED_NOT_RUN` / `not_observed`; PowerShell is unavailable locally.

Hub Consumer CI also resolves exactly one known Agent importer path (`Tools/import_subagent_catalog.py` or `tools/import_subagent_catalog.py`) before execution. Unknown and ambiguous checkouts fail closed; the unchanged read-only `no_op` assertion remains mandatory. The existing Hub workflow test exercises old-only, new-only, neither and both paths using the actual shell resolver. The relocated shell installer additionally published successfully to a disposable `/tmp` directory and its installed CLI returned the unchanged package identity/version.

The preserved 6000.6 package lock also updates only the local Artist file dependency depth to match its relocated manifest; all external package version/dependency observations remain unchanged.

P4 review correction: the relocated external CLI verifier now resolves the repository root through three parents, matching the PowerShell installer. Static evaluation confirms its fallback maps to `cli/artist/bin/Release/net8.0/unity-artist.exe`, rather than duplicating the CLI prefix. All four Artist script roots/default targets were inspected; PowerShell execution remains unavailable.

## P7 integrated CI foundation (2026-10-10)

P4 Hub #95 merged at `547007b11545d445d9e99a97c41a3d6f0a055d03`; Agent #177 re-pinned it at `ef6b409fab5ec5fde89ea291df1a72bb2c468f10`. P7 adds exact 6000.3.12f1 (official Graphics provenance) and 6000.6 minimal fixtures, retains the complete Artist fixture, and implements Built-in/URP/HDRP camera render/readback smoke plus scheduled/manual next-stream prerelease resolution. The required Hub contract job runs static fixture validation, 27 host evidence/resolver tests and .NET/11 Artist CLI contracts on every PR.

Independent review caught unsafe replay deletion and publication-command argument-order gaps. Regression tests demonstrate rejection of overlapping/symlink inputs/outputs, preservation of preexisting output/project, owned temporary cleanup, deterministic confined input hashes and revocation on input change. Authority allows only the named read-only observation Canary while preserving the public-release prohibition. All 35 Hub tests and 27 Unity host tests pass locally; fixture structural validation passes. Actual license/Editor/SRP registry/graphics/render/Player/device execution is `BLOCKED_NOT_RUN`, not a host PASS. The optional Editor job intentionally exits nonzero with blocked evidence when external provisioning is unavailable. Required cloud-check results must be observed before merge.
