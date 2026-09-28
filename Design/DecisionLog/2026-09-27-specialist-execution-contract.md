# Specialist Execution Contract v5

## 判定根拠

UnityAgent main `e388f19011d432513daed8d25b394a4e3019b27a` のProvider RegistryにはGraphics / Performance / WorldCreatorのSemantic Capabilityを実行するProduction Providerが存在しない。`Design/specialist-execution-admission.yaml` に3体の比較結果を記録する。

Graphicsはreasoningとsource / project observation、Performanceはreasoningとmeasurement observation、WorldCreatorはreasoningを採用する。Performanceの `profiler.observe` は現時点で無効化されたLegacy Providerのみが提供するため、Production観測Surfaceの実装・Evidenceが昇格の残るGateとなる。

## 明示Migration

Manifest v5は必須 `execution.kind` を導入し、`provider_backed` にはBackendを1件以上要求、`reasoning` にはBackendを禁止する。ReasoningはCodexRunner、Instructions参照、Output Contract参照、source Context binding、必要なObservation Capabilityを宣言する。モデル名は含めない。

Artistはv4からv5へ `execution.kind: provider_backed` を明示追加し、既存BackendとActivation、Evidenceを維持する。Snapshotはv3となる。旧v4/v2 SchemaはVersion付きファイルに保持し、現行Registryへ旧版を暗黙変換しない。

UnityAgent ConsumerはProfile v3へ明示移行する必要がある。ConsumerがRuntime内のInstructions / Output Contractを所有し、Hub参照とローカル参照の対応を明示してImport時に照合する。ImportはProviderを選択しない。

## 登録と検証

Manifest v5が利用可能であることはSpecialistの登録完了を意味しない。3体のProduction ManifestはConsumer / Runtime / Evidence Gateを満たしてからRegistryへ追加する。登録後もUnity Editor、Player、Target Device、Visual、Performanceの実測は別のVerification Levelである。
