# Migration from MyUnityMCP v1.1.1

The repository now maintains the UnitySubAgentHub registry and contract surface. ArtistSubAgent is its first registered specialist; its existing CLI and Unity package remain the implementation backend during this transition. MyUnityMCP v1.1.1 source is no longer kept on main; migration provenance is frozen in Git tag `v1.1.1` and `tests/fixtures/legacy/MyUnityMCP-v1.1.1/`.

| Responsibility | Current owner |
|---|---|
| Specialist identity, lifecycle, compatibility, dependencies, capabilities, backend and evidence references | `Hub/SubAgents/<id>/manifest.yaml` |
| Registry indexing and shared fail-closed contract | `Hub/Registry/subagents.yaml` |
| Manifest and registry shape | `Hub/Schemas/` |
| Goal, policy, approval, environment discovery, binding, routing, execution, loop/fallback and evidence | UnityAgent |
| LookDev, mood, lighting, environment, camera, Timeline, and Cinemachine | ArtistSubAgent |
| Current Artist implementation transport | `unity_artist_cli` backend using Official Unity CLI / Unity Pipeline |
| Old MCP bridge and 77-tool surface | Legacy only; production-disabled |

Every specialist is optional. Registration does not mean installation or readiness. UnityAgent excludes an uninstalled, incompatible, unbound, unavailable, false, or unknown specialist before ranking. Capability resolution never installs a specialist; setup is a separate explicit request.

The new Artist backend has no dependency on `com.coplaydev.unity-mcp`. Its commands are discovered through Unity Pipeline `[CliCommand]` methods and invoked by the current backend adapter. `unity_artist_cli` is an implementation identity and does not replace `artist_subagent` in capability routing.

See [UnitySubAgentHub Architecture](../architecture/subagent-hub-architecture.md), the [ArtistSubAgent manifest](../../Hub/SubAgents/artist_subagent/manifest.yaml), and the [backend behavior specification](../architecture/artist-subagent-spec.md) for the current contract.
