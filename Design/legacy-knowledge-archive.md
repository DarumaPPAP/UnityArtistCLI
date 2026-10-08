# Legacy MyUnityMCP Knowledge Archive

この文書はMyUnityMCP v1.1.1のRuntime APIを保存するものではない。現行Productへ再利用価値がある判断境界だけを記録するIndexである。

## Preservation rules

- Legacy API名はCurrent Product APIとして再利用しない。
- 旧Support Matrixを現在のUnity version保証へ昇格しない。
- Mutation、Approval、Undo、Revision、Save、Bake、Visual Acceptanceの安全境界は、将来機能を新規設計する際のReview inputとしてのみ使用する。
- Current Productの事実は現行Manifest、Contract、Runtime Evidenceを正本とする。

## Archived domains

| Domain | 保存する知識 | 現在の扱い |
|---|---|---|
| Graphics | Visual direction、Lighting、Capture、Bake/APVの安全境界 | Graphics/Artistの現行Surfaceとは独立 |
| Profiler | 観測条件、測定値の限界、Capture/比較時のEvidence要件 | `profiler.observe` の現行Contractを正本とする |
| Addressables | Package/Settings/Group、typed mutation、Build非自動実行 | Future referenceのみ |
| Animation | Animator/Controller/Clip観測、typed parameter mutation | Future referenceのみ |
| Audio | AudioSource/Clip/Listener観測、typed source mutation | Future referenceのみ |
| UI | Canvas/RectTransform/UIDocument観測、typed RectTransform mutation | Future referenceのみ |
| Cinematic | PlayableDirector/Timeline/Bindingの観測とMutation境界 | Artist backendの公開Surfaceとは別判定 |
| World | Planning / Human review境界 | `world.plan`を正本とする |
| Agent | 旧Control Plane frontend | Retired |

詳細は [legacy-domain-support-boundaries.md](legacy-domain-support-boundaries.md) と [legacy-capability-salvage.csv](legacy-capability-salvage.csv) を参照する。

## Historical provenance

MyUnityMCP v1.1.1のソース履歴は公開済みGit tag `v1.1.1` とGit historyで保持する。main branchへLegacy Source Treeを恒久配置することはKnowledge保存要件ではない。
