# UnitySubAgentHub Repository Policy

## Authority and boundary

This repository owns the SubAgent registry, shared schemas, per-specialist manifests, lifecycle metadata, contract references, and validation. It is not a runtime, orchestrator, resolver, installer, or execution surface. UnityAgent is the only Control Plane and remains authoritative for policy, approval, environment discovery, binding, capability resolution, execution, retry/fallback, and evidence normalization.

`Hub/repository-authority.yaml` is the machine-readable map of repository authority and mirrored declarations. `Hub/Registry/subagents.yaml` is the index. `Hub/SubAgents/<id>/manifest.yaml` is the source of truth for that specialist's identity, lifecycle, install mode, capabilities, compatibility, dependencies, backend references, and evidence requirements. Do not duplicate those facts in a second Hub catalog. Detailed specialist behavior may live in linked contracts.

## Required invariants

- Every specialist is optional. `required` must be false and `auto_install` must be false.
- Registry membership does not establish local installation, project binding, compatibility, or readiness.
- Uninstalled, incompatible, unbound, unavailable, false, or unknown activation checks exclude a specialist before ranking.
- No Hub or capability-resolution flow may automatically install or update a specialist. Setup is a separate, explicitly requested action.
- Only lifecycle `active` may be considered for new resolution. `deprecated`, `retired`, and `revoked` are excluded.
- `artist_subagent` and `unity_artist_cli` are different identities. Never route a SubAgent request by substituting its backend id.
- UnityAgent owns all runtime resolution and execution. Hub validators inspect metadata and referenced files only.
- Manifests and committed evidence use repository-relative paths. Never commit machine-specific paths or live installation state.
- Do not rewrite the published MyUnityMCP `v1.1.1` tag or mutate `Tests/Fixtures/Legacy/MyUnityMCP-v1.1.1/` without explicit provenance migration.

## Git workflow

Branch運用の正本は `.github/branch-policy.json`、説明は `docs/development/branch-policy.md` とする。
`main` は永続する統合正本であり、通常の作業は `main` から `feature/*`、`fix/*`、`chore/*`、必要時のみ `release/*` を作成する。
新機能は `feature/*`、不具合修正は `fix/*`、CI・Docs・Refactor・Repository整理は `chore/*` に分類する。`release/*` を `develop` の代替として常設しない。
新規branchに `codex/*`、`refactor/*`、`docs/*`、`ci/*` 等の追加prefixを作らない。通常PRのbaseは `main` とし、Squash Merge後に短命branchを削除する。

## Adding a specialist

Create one `Hub/SubAgents/<id>/manifest.yaml` that satisfies `Hub/Schemas/subagent-manifest.schema.json`, then add its path to `Hub/Registry/subagents.yaml`. Keep the manifest's backend ids separate from its specialist id. Use stable resolver-visible capability ids and declare exact supported Unity-version/render-pipeline pairs, dependencies, backend refs, and evidence refs. Every required dependency must have a gate in `activation.required_before_resolution`. A new specialist may require an explicit UnityAgent import migration when the consumer has no corresponding Runtime Profile.

Do not add runtime dispatch, candidate ranking, local environment discovery, package installation, or project mutation to this repository's Hub validation path. New manifest paths must be covered by the shared validator and CI.

## Validation

Run:

```sh
python Hub/Tools/validate_repository.py
python Hub/Tools/validate_registry.py
python -m unittest discover -s Hub/Tests -p 'test_*.py' -v
python Hub/Tools/export_snapshot.py --output /tmp/subagent-catalog.yaml
```

The Hub workflow validates that a consumer-neutral static Manifest snapshot can be exported, but it does not publish a Hub release or long-lived distribution artifact. UnityAgent Release pins an exact Hub commit and owns public distribution. Overlapping active capabilities are valid Hub metadata; the current UnityAgent Import Gate rejects them until its resolver supports ranking. The snapshot does not observe runtime installation, compatibility, binding, or readiness; UnityAgent must apply those checks against its own environment facts. UnityAgent owns runtime profile fields, including default profile, audience, goal type, primary capability, reference scope and evidence producer.

Keep the existing Artist gates green when changing its linked contracts:

```sh
python Tests/Backend/verify_artist_backend_contract.py
python Tests/Compatibility/verify-unity-api-compatibility.py
python Tests/Backend/verify_portable_paths.py
```

Compatibility-sensitive Artist code and API changes must apply `.agents/skills/unity-artist-unity-api-compatibility/SKILL.md`.

Direct Unity Editor, License, Pipeline, and visual end-to-end evidence must be distinguished from static host validation. Unknown observations must not be recorded as successful evidence.

## Artist backend compatibility

The first specialist's implementation remains in `Packages/com.darumappap.artist-subagent/` and `src/UnityArtist.Cli/` during this Hub transition. Its backend contract and detailed workflow specification remain linked from `Hub/SubAgents/artist_subagent/manifest.yaml`.

Preserve its bounded typed-argument CLI, explicit project targeting, allowlisted commands, Unity Undo, no automatic save, no arbitrary evaluation, and concrete-gate-only fallback behavior. Compatibility-sensitive changes must keep the Editor implementation and EditMode tests together. These Artist-specific rules do not define additional Hub runtime behavior.
