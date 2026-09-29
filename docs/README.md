# UnitySubAgentHub Documentation Index

このIndexは、Hubの**Current Contract**とHistorical / Backend-specific資料を分離して読むための入口です。

## Current Hub contract

- [Repository README](../README.md)
- [Hub Architecture](../Design/subagent-hub-architecture.md)
- [Design Records](../Design/README.md)
- [Registry](../Registry/subagents.yaml)
- [Manifest / Snapshot Schemas](../Schemas/)
- [Specialist Execution Admission](../Design/specialist-execution-admission.yaml)

HubはRegistry / Manifest / Schema / Validationを所有します。Runtime resolution、Policy、Approval、Project binding、Execution、Retry、Evidence normalizationはUnityAgentが所有します。

## Registered specialists

| Specialist | Guide | Manifest |
|---|---|---|
| ArtistSubAgent | [Guide](../SubAgents/artist_subagent/README.md) | [Manifest](../SubAgents/artist_subagent/manifest.yaml) |
| GraphicsSubAgent | [Guide](../SubAgents/graphics_subagent/README.md) | [Manifest](../SubAgents/graphics_subagent/manifest.yaml) |
| WorldCreatorSubAgent | [Guide](../SubAgents/world_creator_subagent/README.md) | [Manifest](../SubAgents/world_creator_subagent/manifest.yaml) |
| PerformanceSubAgent | [Guide](../SubAgents/performance_subagent/README.md) | [Manifest](../SubAgents/performance_subagent/manifest.yaml) |

Current manifests are v5 and current exported Snapshot is v3.

## Backend-specific documentation

Artist backend implementationは移行上このRepositoryに同居していますが、Hub Runtimeではありません。

- [Artist Unity Package](../Packages/com.darumappap.unity-artist/Documentation~/README.md)
- [ArtistSubAgent Specification](../Specs/ArtistSubAgent/spec.md)
- [Unity API Compatibility](../Specs/Compatibility/unity-api-compatibility.md)
- [Compatibility Tests](../Tests/Compatibility/README.md)

## Historical / migration records

- [Migration from MyUnityMCP](../MIGRATION_FROM_MYUNITYMCP.md)
- `Legacy/MyUnityMCP-1.1.1/` — immutable historical source / current detachment evidence source
- `Design/DecisionLog/` — dated decisions
- `Design/legacy-capability-salvage-audit.md` — Legacy 77 Capabilityの回収・延期・削除Gate
- `Tests/Compatibility/*evidence*` — 時点Evidence

Historical Unity 2022.3 EvidenceはCurrent Production Supportを意味しません。Current manifestsが宣言する対象はUnity 6.x+のBuilt-in / URP / HDRPです。

## Candidate baseline files

Graphics / WorldCreator / Performanceには、Production昇格前の比較用として `contracts/capability-contracts.yaml` が残っています。これらは `status: pilot_unregistered` を保持する**Historical baseline**です。

Current Production Contractは各Manifestの `capability_contract_ref` を参照してください。

## Maintenance rule

- Specialist追加・Lifecycle変更時はRegistry、Manifest、Schema、Hub Tests、READMEを同期する
- Backend追加とSpecialist追加を同一Identityとして扱わない
- Registry登録をinstalled / available / eligible / Production Verifiedと書かない
- Current docsへHistorical Support Matrixを混在させない
- Legacy sourceはactive dependencyとdetachment gateが0になるまで削除しない

## Release channels

HubとArtist BackendはVersion ownerが異なります。

- `VERSION`: UnityArtistCLI / ArtistSubAgent backend release version
- `HUB_VERSION`: consumer-neutral Hub Snapshot release version
- Artist backend tag: `v<Version>`
- Hub Snapshot tag: `hub-v<Version>`

Hub Snapshot Releaseは4 SpecialistのManifestを配布しますが、Runtime readinessや自動Installを保証しません。Codex MarketplaceはUnityAgent側の単一entryを使用し、SubAgentごとのMarketplace Pluginは公開しません。
