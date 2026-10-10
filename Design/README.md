# Hub Design Records

`Design/`には、複数のOptional Specialist SubAgentを登録するUnitySubAgentHubのArchitecture ContractとDecision Recordを置きます。Hubの現行責務はmetadataのRegistry、Manifest、Schema、Validationです。

## Canonical records

- `Hub/Registry/subagents.yaml`: 登録ManifestのIndexとFail-Closed規則
- `Hub/SubAgents/<id>/manifest.yaml`: Specialist identity、lifecycle、installation、capability、compatibility、dependency、backend、evidence契約
- `Hub/Schemas/`: Registry / Manifestの共通Shape
- Manifestが参照するContract: Specialist固有の詳細仕様と受け入れ条件
- `subagent-hub-architecture.md`: HubとUnityAgentの責任境界
- `specialist-expansion-architecture.md`: Registered Specialist候補の境界とEval条件
- `legacy-capability-salvage-audit.md` / `legacy-capability-salvage.csv`: Legacy 77 ToolのSource inventory、分類、削除Gate

UnityAgentが唯一のControl Planeです。Hubの記録はSpecialistが導入済み、eligible、実行可能であることを示しません。HubはRuntime、Orchestrator、Request Resolver、Installerではありません。

## Current registered specialists

| Specialist | Execution kind | Current contract |
|---|---|---|
| `artist_subagent` | `provider_backed` | `Hub/SubAgents/artist_subagent/contracts/capability-contracts.yaml` |
| `graphics_subagent` | `reasoning` | `Hub/SubAgents/graphics_subagent/contracts/production-capability-contract.yaml` |
| `world_creator_subagent` | `reasoning` | `Hub/SubAgents/world_creator_subagent/contracts/production-capability-contract.yaml` |
| `performance_subagent` | `reasoning` | `Hub/SubAgents/performance_subagent/contracts/production-capability-contract.yaml` |

Graphics / WorldCreator / Performanceの `contracts/capability-contracts.yaml` はProduction昇格前のPilot baselineです。削除せず比較Evidenceとして保持しますが、Current Resolver contractとして読みません。

## Legacyとの区別

旧MyUnityMCPの設計記録はGit tag `v1.1.1`から参照します。mainには旧Design treeを保持しません。現在のHub ContractやUnityAgentのProduction Architectureとして読み替えないでください。
