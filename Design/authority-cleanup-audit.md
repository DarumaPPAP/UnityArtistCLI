# Authority cleanup audit (2026-09-26)

## Classification

| Surface | Decision | Evidence and ownership |
|---|---|---|
| `Hub/Registry/`, `Hub/Schemas/`, `Hub/SubAgents/*/manifest.yaml`, `Hub/Tests/` | KEEP | Static specialist identity, contracts and validation belong to the Hub. |
| `Tests/Routing/cases.yaml` | DELETE from Hub; MOVE routing coverage to UnityAgent | The file declared `expected_primary_route`; UnityAgent owns routes in `Orchestration/Routing/task-routes.yaml`. No Hub code referenced the fixture. |
| `Hub/SubAgents/artist_subagent/contracts/camera-fov-reference-profile.yaml` | DELETE | A fixed camera GUID, property and approval range were historical task fixtures. Only a Hub test asserted that the file existed. |
| `Templates/AcceptanceProfiles/balanced-graphics.json` | DELETE | No active repository or UnityAgent reference was found. Scores and budgets are project evaluation policy, not registry metadata. |
| Eight forwarding scripts in `Tests/Release/` | DELETE | Each only imported `verify_unity_artist_contract.main`; no active workflow or non-Legacy source referenced their filenames. The canonical validator remains. |
| Artist package, CLI, compatibility tests, local install scripts and backend skills | KEEP co-located | They are Specialist source owned by the Hub repository boundary. Hub does not dispatch them. Public distribution is owned by UnityAgent, which pins an exact Hub commit and packages required backend assets into the UnityAgent release. |
| MyUnityMCP v1.1.1 Source Tree | REMOVED FROM MAIN | Release/capability provenance was frozen under `Tests/Fixtures/Legacy/MyUnityMCP-v1.1.1/` and Git tag `v1.1.1`; current validators no longer read the Legacy source tree. |

## Contract decisions

- **FACT (before vNext):** The previous Hub exporter emitted `SubAgentProfileCatalog` fields including `default_profile`, `audience`, `goal_type`, `primary_capability` and a primary Provider. UnityAgent's legacy Profile-wire import path still validates those fields.
- **ARCHITECTURE INVARIANT:** UnityAgent remains the only Control Plane. Runtime route selection, capability resolution, current environment facts and execution do not belong to Hub data.
- **IMPLEMENTED CHANGE:** The registry no longer specifies `resolution.phase_order`. UnityAgent owns the algorithm. The manifest still declares required activation facts and fail-closed behavior.
- **IMPLEMENTED CHANGE (Hub vNext):** Registry v2 is a Manifest index. Manifest v4 and Snapshot v2 omit `default_profile`, `runtime_profile`, Backend `primary`, and UnityAgent-specific Evidence producer fields, Backend implementation fields, and Backend test evidence refs. UnityAgent's adapter retains consumer-owned Runtime Profile values.
- **IMPLEMENTED CHANGE (Hub vNext):** Hub validation permits overlapping active Capability declarations. UnityAgent's Import Gate enforces the current one-profile-per-capability limitation.

## Backend distribution boundary

The Artist package, CLI, tests and backend-specific skills remain co-located as Hub-owned Specialist source. Artist no longer has an independent product lifecycle, release tag, release workflow or remote release installer. UnityAgent is the sole public distribution owner and pins the exact Hub commit used for each release. A new backend repository is not required to preserve this authority boundary.

## Legacy detachment gate

The published annotated tag `v1.1.1` points to commit `ea437f11bcf5b46b6a7575f9d2f9b81a9c02da7c` and remains unchanged. The active release validator still requires a file under `Legacy/`; detachment is therefore deferred. Historical source can be inspected at the immutable tag after that validator is migrated, without rewriting history or moving the tag.

## Support status

The current manifest and support matrix contain only Unity 6.x+ Built-in, URP and HDRP. Unity 2022.3 gate and bounded fallback records remain historical evidence and do not establish current production support.
