# Repository Consolidation P0 Audit

## Scope and authority

User request: implement P0–P8 across DarumaPPAP/UnityAgent and DarumaPPAP/UnitySubAgentHub, verify each phase in a PR, then squash merge after required checks succeed. No direct main push, release/tag publication, new backends directory, policy relaxation, or automatic specialist installation.

Implementation specification: UnityAgent_Repository_Consolidation_Spec_v1.md, SHA-256 `fb4744860b5fc0f44f01d1c31db8df867c789ea8dccdef983a3728d797174cee`. The two received attachments have identical bytes. The separately named execution file CodexCloud_UnityAgent_Complete_Goal.md has not yet been received; do not invent its contents. Current explicit user instructions take precedence over general skill approval handoffs.

Historical baseline paths in this report and inventory are deliberately preserved for migration comparison. They are not declarations of the final layout. Inventory is not a replacement for repository authority or future layout contracts.

## Immutable baseline

| Repository | Latest main at preflight |
|---|---|
| UnityAgent | `1dc42590843d0373440306e1b93e9764a857be36` |
| UnitySubAgentHub | `aa6275c8673fa7a38d5d6a8aabbef5507ee96ad1` |
| Pinned Hub Source Lock | `61d3fad2e0aef50b69fc76fbbd839aca076de19f` |
| First reference: hatayama/unity-cli-loop | `b04b58e8c94c6b71808a5b29e65cc41e361ded19` |
| MyUnityMCP immutable v1.1.1 target | `f74d6f86f65178492aee1eaac5c01acb7ba5514a` |

Fetch and push dry-run succeeded for both repositories through the configured proxy; dry-run created no branch. Connector metadata reports admin/maintain/push/pull. The branch-protection endpoint returned 403 Resource not accessible by integration. Public Ruleset endpoints succeeded: both repositories forbid deletion/non-fast-forward on main, require linear history and a pull request, permit squash only, require resolved threads, and have no bypass actors. Never interpret the inaccessible legacy endpoint as absent protection.

Required checks: UnityAgent `Canonical Validation`; Hub `Validate Branch Name` and `Validate registry, manifests, and snapshot contract`. Workflow-level PR path filters are absent from these required jobs. Artist host contract is separately path-triggered. No ruleset or required check was modified.

## Contract and source audit

AGENTS.md, User/Approval/Evidence Policy, branch policy, repository authority maps, Source Lock, and current workflows were read. UnityAgent is the sole Control Plane; Hub is static metadata. Profile ID / provider ID separation, optional required=false/auto_install=false specialists, fail-closed activation, hashes/provenance, UPM names and asset GUIDs remain protected.

Route: architecture-design, using current-call Context Assembly; this route declares no required_policy_clauses. User, Approval and Evidence policies were additionally reviewed for this cross-repository task. The existing unrelated checkout fixture newline difference is preserved in the original checkout; worktrees isolate this audit.

Both Development and Pinned snapshots pass the existing real Consumer Import Gate as read-only `no_op`. Their commits differ but snapshot SHA-256 is `b156ee93fab5abddc8a7785c8493b835ce3111eae80394f4e42f6f59f574e6d5`; catalog_write_performed=false. Hash is byte identity evidence, not a cryptographic signature. Saved import plans are in consolidation/.

692 Agent and 199 Hub committed files are indexed with byte SHA-256, sizes, and root counts. The reference index contains 2142 Agent and 596 Hub path occurrences. Only frozen Legacy and 2022.3 fixture references are classified historical automatically; remaining entries require owning-caller review. Duplicate bytes alone never authorize removal. Four Prompt files match Context/Prompt/Templates byte-for-byte; callers must migrate before removing them. No production file was deleted in P0.

EnvironmentSnapshot.myunitymcp remains required in the environment schema, dataclass, discovery and fixtures after adapter retirement. It is an observation/wire compatibility surface; do not remove it as a directory cleanup without consumer migration evidence.

## Differences and disposition

- Initial local checkouts lagged latest main by Agent #172 and Hub #90–#92. Fresh fetch corrected the baseline. The Consumer Gate described by the spec exists in both latest workflows; no replacement is needed.
- Artist CLI tests are a Python unittest harness exercising the .NET executable, not a separate .csproj. Preserve that actual test runner when moving under cli/artist/tests.
- Current Hub support matrix contains exactly three Unity 6.x+ family rows. This is a declared product contract, not evidence that exact versions/pipelines ran in this Cloud session.
- Canonical current Unity fixture is 6000.6.0f1 with com.unity.pipeline 0.6.0-exp.1. The 2022.3.22f1 fixture is historical. Recorded URP/HDRP paths have no corresponding current fixture; their prior evidence must not establish a fresh successful run.
- First-reference current workflows demonstrate full EditMode, a smaller 6000.5 fixture and stable PR compile jobs. This fetched upstream commit has no dynamic next-series Canary workflow. Implement the requested Canary independently with provenance rather than claim to copy an existing upstream Canary.
- The initial .NET channel installer tried a denied ci.dot.net host. The official allowed builds.dotnet.microsoft.com feed succeeded. Final host SDK is 8.0.425; no credential values were inspected or committed.

## Verification observed in this Cloud session

| Gate | Result |
|---|---|
| Agent canonical python Tools/validate_all.py | PASS: 574 unittest cases across 10 suites, plus canonical validators |
| Hub authority / registry / snapshot export | PASS: 0 errors |
| Hub unittest discovery | PASS: 32 tests |
| Artist backend / Unity API / portable-path static validators | PASS |
| .NET 8 Release build | PASS: 0 warnings, 0 errors |
| Artist executable contract tests | PASS: 11 tests |
| Development and Pinned Consumer Gate | PASS: read-only no_op, immutable source refs and SHA-256 |
| Unity Editor / License / Pipeline / Player / Visual / device | BLOCKED_NOT_RUN: no configured Editor, License or device runner |

Python 3.12.14, Node 24.19.0, Git and gh are present. PowerShell is unavailable locally; existing GitHub Canonical CI supplies its installer syntax gate. A generic gh auth check made inside the network sandbox could not contact the proxy; git operations with supported sandbox escalation and connector operations are the confirmed usable paths. api.github.com is not an allowed Cloud destination; use the connected GitHub API tools rather than bypass the proxy policy.

## Resume and migration order

Preserve all P0 evidence. Receive/read the designated execution file and compare its instructions with the canonical spec and current code. Execute P1 Consumer dual-read first, then P2 Hub core move, P3 pin merged full SHA, P4 Artist consumer preparation → Hub move → final pin, P5 src packaging/wheel/installer migration, P6 caller-first cleanup/knowledge preservation, P7 version/pipeline/Canary CI, P8 layout contracts and final audits. Each phase requires green checks before squash merge. Do not disable a failing gate or replace immutable source references with HEAD/main.

P1–P8 are not implemented by this P0 audit. No code/static migration completion or Editor success is claimed.

## P2 Hub core move

Registry, schemas and specialist contracts moved under Hub/. Static tools and tests have separate directories; unittest uses the canonical Hub/Tools importer. Snapshot source refs, registry identity-path validation, authority map, workflow triggers and Consumer entry were updated together. Old pinned source is retained by Consumer P1; Agent re-pin follows the verified Hub merge SHA. The 32 existing Hub behavioral tests and negative schema tests retain coverage; no gate removed.


## P4 Artist producer move and Hub P6 cleanup

Consumer preparation landed first in Agent #176 (`66463f54b92178a830a746b8d24e3cbe7d729605`). This producer branch moves CLI, Artist scripts/tests, support matrix, static verifiers and integration tests to their owning roots. C# package assets and .meta/GUIDs retain their exact bytes; only package documentation links change. The backend contract belongs to `cli/artist/artist-backend-contract.yaml`. Required host job names remain stable and its all-PR trigger prevents pending statuses on unrelated changes.

The [P4 before/after map](consolidation/p4-path-map.json) records each source/destination, preserved Legacy file hashes/tag object, project hashes, and the orphan `.meta` removal. Searching GUID `8192a3b4c5d6ef08192a3b4c5d6e7f0d` found only the orphan `Specs/UnityArtistCLI/spec.md.meta`; its paired file was absent and no asset depended on the GUID. No other metadata was removed.

All existing evidence and release/production acceptance YAMLs contained session observations or measured assertions, so all are historical. Their bytes and original status values remain immutable; [the separate index](../../ci/evidence/artist/historical/index.json) provides explicit historical classification and original-path resolution. Historical validators now require preservation hashes and clearly report an archive check. Missing baseline URP/HDRP fixtures cannot be inferred from their old YAML claims. Current Editor/Pipeline/capture/visual results remain `BLOCKED_NOT_RUN` / `not_observed`; no current measured evidence is committed by P4.

The 6000.6 Artist project and historical 2022.3 project retain all scenes/resources/scripts/version/package versions, changing only local package reference depth. Active callers, Python literal path components/import depth, shell/PowerShell installer depth, workflow commands and relative documentation links are synchronized. Old paths remain only in byte-preserved historical records, preserved fixture READMEs (explicitly contextualized by `ci/unity-projects/README.md`), P0/P4 provenance maps, the revision-aware inventory vocabulary and dated decisions about previously removed surfaces. Cross-repository Agent knowledge references are static documentary references and require final P5/P8 reconciliation against Agent's final paths.

Local verification passed authority/registry/export/branch policy, all 32 Hub tests, all 11 static compatibility/backend/archive verifiers, 2 integration contracts, .NET Release build (zero errors/warnings), 11 Artist CLI host tests and shell installer syntax. PowerShell and licensed Unity/Player/visual/device execution were not run. Hub P4/P6 implements no Source Lock mutation or runtime feature; parent integration must observe Consumer compatibility and required CI before merging. P7 prepared work is separate, and the final layout contract is deliberately deferred to P8.

Hub Consumer CI also resolves exactly one known Agent importer path (`Tools/import_subagent_catalog.py` or `tools/import_subagent_catalog.py`) before execution. Unknown and ambiguous checkouts fail closed; the unchanged read-only `no_op` assertion remains mandatory. The existing Hub workflow test exercises old-only, new-only, neither and both paths using the actual shell resolver. The relocated shell installer additionally published successfully to a disposable `/tmp` directory and its installed CLI returned the unchanged package identity/version.

The preserved 6000.6 package lock also updates only the local Artist file dependency depth to match its relocated manifest; all external package version/dependency observations remain unchanged.

P4 review correction: the relocated external CLI verifier now resolves the repository root through three parents, matching the PowerShell installer. Static evaluation confirms its fallback maps to `cli/artist/bin/Release/net8.0/unity-artist.exe`, rather than duplicating the CLI prefix. All four Artist script roots/default targets were inspected; PowerShell execution remains unavailable.

### P7 verification boundaries

See [Unity CI foundation](unity-ci-foundation.md) for exact fixture versions, official provenance, runner provisioning, commands and evidence artifacts. Required cloud validation covers fixture structure, resolver/evidence rejection, archive/contract integrity and executable Artist host tests. Rendering suites require a licensed exact Editor and measured graphics device; the Canary dynamically resolves an official next-minor prerelease. Both record nonempty test results, manifests/locks, exact Editor/pipeline/package identity, stdout/stderr, input/output SHA-256 inventories and run ID. Read-only observation does not create a Hub public release. Unavailable external gates remain `BLOCKED_NOT_RUN` and return a nonzero result; a Green host check never certifies Editor or visual success.

### Final Hub layout contract and reference exceptions

Authored roots: `.agents`, `.github`, `Hub`, `Packages`, `cli`, `ci`, `tests`, `docs`, and mandatory root configuration/documentation. `.devcontainer` is allowed for future development without creating an empty directory. Registry/Schema/SubAgents/Tests/TestProjects/Design/Specs/src/scripts/Legacy old roots are prohibited by the final required layout gate. Ownership is declared in repository-layout.json; domain authority and product identity remain in Hub/repository-authority.yaml and the unchanged manifests.

Intentional old-path references are confined to immutable P0 inventories, P4 migration maps, frozen v1.1.1 provenance, preserved historical evidence and explicit exactly-one old/new Agent importer compatibility. Legacy inventory original source fields remain immutable, while current explanatory Agent links use its lowercase src/tools/tests layout. There is no active old Hub root dependency and no new backends directory.

Actual required/host P7 CI is Green. Optional Editor compatibility jobs on [run 38066203244](https://github.com/DarumaPPAP/UnitySubAgentHub/actions/runs/38066203244) returned BLOCKED_NOT_RUN with retained manifests, input hashes, commit identity and logs; artifact IDs are `11674463178` (canonical-full), `11675213275` (6000.6), and `11674293315` (6.3). Artifacts expire on 2026-10-24. Actual Rendering/Pipeline/Canary/Player/device gates remain unobserved. Cloud's direct official Canary metadata read was blocked by proxy403; the GitHub scheduled/manual runner still requires its documented license/Editor/graphics provisioning.
