# Legacy Capability Salvage Audit

## Decision

MyUnityMCP v1.1.1 の77 Toolは、現行ProductへLegacy APIとして移植しない。

Legacy実装を残す条件を「旧APIとのParity」には置かない。現行Product Surfaceは、現行Manifest・Runtime resolution・Contract・Test・Evidenceを正本とし、Legacy APIの互換層を正本へ昇格しない。

| Decision | 件数 | 意味 |
|---|---:|---|
| `FUTURE_SPEC_ARCHIVED` | 50 | 旧PORT候補。不採用。将来の新機能設計時に参考情報としてのみ利用 |
| `KNOWLEDGE_ARCHIVED` | 12 | Skill / Documentation / Contractへ判断知識のみ保存。Runtime APIは不採用 |
| `RETIRED` | 15 | 旧Control Plane / Frontend /内部実行Surface。再導入しない |
| `PORT` | 0 | Legacy移植対象なし |
| `REPLACED` | 0 | Legacy API parityをProduct要件にしないため使用しない |

機械可読な全77件の記録は [legacy-capability-salvage.csv](legacy-capability-salvage.csv) を正本とする。

## Current Product Surface

以下はLegacy APIの移植結果ではなく、現行Architectureで独立して成立しているProduct Surfaceである。

- GraphicsSubAgent: `graphics.inspect`, `graphics.diagnose`, `graphics.validate`
- ArtistSubAgent: `artist.camera.inspect`, `artist.camera.refine`, `visual.capture`
- PerformanceSubAgent: `performance.analyze` + Production `profiler.observe`
- WorldCreatorSubAgent: `world.plan`

Backend内部に実装が存在しても、Manifest / Runtime resolution / Contract / Test / Evidenceまで揃っていない機能はProduct Surfaceとして扱わない。

## Archive policy

### Knowledge archive

価値のある判断境界は次へ保持する。

- [Legacy domain support boundaries](legacy-domain-support-boundaries.md)
- UnityAgent Visual Direction Skill
- UnityAgent Content Import Analysis Skill
- WorldCreator planning contract
- 77件のresponsibility / risk / historical sourceを保持するMatrix

### Future feature archive

旧PORT 50件は `FUTURE_SPEC_ARCHIVED` とする。

これは「後で実装する約束」ではない。将来同じProblemをProduct要件として採用する場合だけ、Legacy実装をコピーせず、現行Architecture・Unity Version・Safety Contract・Evidence Contractから新規設計する。

### Retired API

旧Agent Control Plane、旧Execution Frontend、旧内部Status API等は `RETIRED` とし、Current Productへ復活させない。

## Detachment policy

Legacy削除を阻害する条件は、今後次の3点だけとする。

1. Current Product codeがLegacy SourceをRuntime実行に必要としている
2. Current CI/TestがLegacy Source Treeを直接Fixtureとして必要としている
3. Historical provenanceがGit tag / immutable fixtureへ固定されていない

Legacy API parity不足は削除Blockerにしない。

## Next steps

1. UnityAgentのProduction-disabled `MyUnityMcp` Adapterを削除する
2. Legacy Source Inventoryをimmutable Fixture / Git tag provenanceへ変換する
3. HubのLegacy Source直接参照をFixtureへ切り替える
4. `Legacy/MyUnityMCP-1.1.1/` をmainから削除する
5. 公開済み `v1.1.1` tagとGit履歴は変更しない

## Non-goals

- Legacy 50 PORT候補の再実装
- MyUnityMCP transportの復活
- Legacy API compatibility layerの維持
- Backend内部の未公開機能をLegacy削除のためだけにProduction昇格すること
