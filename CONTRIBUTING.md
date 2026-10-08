# Contributing

## Repository boundary

UnitySubAgentHub owns specialist registry metadata, schemas, manifests, linked contracts, validation, and the co-located ArtistSubAgent backend source.

UnityAgent remains the only Control Plane and owns runtime resolution, policy, approval, environment discovery, binding, execution, retry / fallback, and evidence normalization.

Do not add runtime routing, automatic installation, project mutation, or Control Plane behavior to Hub validation.

## Branch workflow

Create work from `main` using only:

- `feature/*` for new functionality
- `fix/*` for bug fixes
- `chore/*` for CI, documentation, refactors, and repository maintenance
- `release/*` only when a temporary release-preparation branch is actually required

Open a pull request against `main`. The repository uses squash merging and automatically deletes merged head branches.

## Before opening a pull request

Run the checks relevant to your change.

Hub contract:

```sh
python Tests/Hub/validate_repository_authority.py
python Tests/Hub/validate_registry.py
python -m unittest discover -s Tests/Hub -p 'test_*.py' -v
python Tests/Hub/export_agent_snapshot.py --output /tmp/subagent-catalog.yaml
```

Artist backend:

```sh
python Tests/Backend/verify_artist_backend_contract.py
python Tests/Compatibility/verify-unity-api-compatibility.py
python Tests/Backend/verify_portable_paths.py
dotnet build src/UnityArtist.Cli/UnityArtist.Cli.csproj --configuration Release
```

## Specialist changes

When adding or changing a specialist:

1. Update its canonical `SubAgents/<id>/manifest.yaml`.
2. Keep `Registry/subagents.yaml` as the manifest index only.
3. Validate against the shared schemas.
4. Preserve optional install and fail-closed eligibility.
5. Keep specialist identity separate from backend / provider identity.
6. Update UnityAgent separately when new resolver-visible semantics require consumer support.

## Compatibility-sensitive Artist changes

Apply `.agents/skills/unity-artist-unity-api-compatibility/SKILL.md`.

Keep Unity implementation and EditMode compatibility tests in the same change. Do not infer package API support from Unity Editor version alone.

## Historical provenance

Do not restore the removed MyUnityMCP source tree to `main`. Use Git tag `v1.1.1` and `Tests/Fixtures/Legacy/MyUnityMCP-v1.1.1/` for historical provenance.
