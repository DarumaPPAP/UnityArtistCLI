# Legacy Capability Salvage Audit

## Final decision

MyUnityMCP v1.1.1 の77 Toolは、現行ProductへLegacy APIとして移植しない。

Legacy API parityはCurrent Productの完了条件でもLegacy Source保持条件でもない。現行Product Surfaceは、現行Manifest・Runtime resolution・Contract・Test・Evidenceを正本とする。

| Decision | 件数 | 意味 |
|---|---:|---|
| `FUTURE_SPEC_ARCHIVED` | 50 | 旧PORT候補。不採用。将来の新機能設計時の参考情報のみ |
| `KNOWLEDGE_ARCHIVED` | 12 | Skill / Documentation / Contractへ判断知識のみ保存。Runtime APIは不採用 |
| `RETIRED` | 15 | 旧Control Plane / Frontend / 内部実行Surface。再導入しない |
| `PORT` | 0 | Legacy移植対象なし |
| `REPLACED` | 0 | Legacy API parityをProduct要件にしないため使用しない |

機械可読な77件のCurrent Decisionは [legacy-capability-salvage.csv](legacy-capability-salvage.csv) を正本とする。

Historical Source provenanceは `tests/fixtures/legacy/MyUnityMCP-v1.1.1/capabilities.json` とGit tag `v1.1.1` に固定する。

## Current Product Surface

以下はLegacy APIの移植結果ではなく、現行Architectureで独立して成立しているProduct Surfaceである。

- GraphicsSubAgent: `graphics.inspect`, `graphics.diagnose`, `graphics.validate`
- ArtistSubAgent: `artist.camera.inspect`, `artist.camera.refine`, `visual.capture`
- PerformanceSubAgent: `performance.analyze` + Production `profiler.observe`
- WorldCreatorSubAgent: `world.plan`

Backend内部にコードが存在するだけではProduct Surfaceとみなさない。Manifest / Runtime resolution / Contract / Test / Evidenceまで揃ったCurrent Surfaceだけを現行機能として扱う。

## Archive policy

### Knowledge archive

再利用価値のある判断境界は次へ保持する。

- [Legacy domain support boundaries](legacy-domain-support-boundaries.md)
- [Legacy Knowledge Archive](legacy-knowledge-archive.md)
- UnityAgent Visual Direction Skill
- UnityAgent Content Import Analysis Skill
- WorldCreator planning contract
- 77件のresponsibility / risk / historical sourceを保持するMatrixとFrozen Fixture

### Future feature archive

旧PORT 50件は `FUTURE_SPEC_ARCHIVED` とする。

これは将来実装の約束ではない。将来同じProblemをProduct要件として採用する場合だけ、Legacy実装をコピーせず、現行Architecture・Unity Version・Safety Contract・Evidence Contractから新規設計する。

### Retired API

旧Agent Control Plane、旧Execution Frontend、旧内部Status API等は `RETIRED` とし、Current Productへ復活させない。

## Detachment status

Legacy Source削除のGateは完了した。

- [x] 50 PORT候補を不採用化し `FUTURE_SPEC_ARCHIVED` へ移行
- [x] Knowledge 12件を `KNOWLEDGE_ARCHIVED` として保存
- [x] Retired 15件を明示
- [x] UnityAgentのProduction-disabled `MyUnityMcp` Runtime Adapterを削除
- [x] 77 Tool inventory / package metadata / source blob SHAをFrozen Fixtureへ固定
- [x] Hub CI/TestのLegacy Source Tree直接依存をFrozen Fixtureへ切替
- [x] Repository AuthorityをLegacy Source RootからFrozen Provenanceへ変更
- [x] `Legacy/MyUnityMCP-1.1.1/` Source Treeをcurrent branchから削除
- [x] 公開済みGit tag `v1.1.1` とGit履歴を保持

Current Matrixの `active_dependency` は、34件を `legacy_adapter_removed`、43件を `no_active_legacy_runtime_dependency` として記録する。

## Frozen provenance

- Git tag: `v1.1.1`
- Annotated tag object: `f74d6f86f65178492aee1eaac5c01acb7ba5514a`
- Release commit: `ea437f11bcf5b46b6a7575f9d2f9b81a9c02da7c`
- Frozen fixture: `tests/fixtures/legacy/MyUnityMCP-v1.1.1/`
- Archived tool count: 77

旧Sourceそのものが必要な場合はGit tag / release commitから取得する。main branchへLegacy Source Treeを戻すことをKnowledge保存手段にしない。

## Non-goals

- Legacy 50 PORT候補の再実装
- MyUnityMCP transportの復活
- Legacy API compatibility layerの維持
- Backend内部の未公開機能をLegacy削除のためだけにProduction昇格すること
