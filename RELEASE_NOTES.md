# UnityArtistCLI 0.0.2-beta

UnityArtistCLI 0.0.2-beta は、ArtistSubAgentを現在のUnityAgent / UnitySubAgentHub Architectureへ同期するBeta releaseです。

## Production surface

- `artist_subagent` は provider-backed Specialist、`unity_artist_cli` はそのBackend identity
- `unity-artist` host CLI + official Unity CLI / Unity Pipeline transport
- LookDev、Lighting、Environment、Camera、Cinematic、Timeline、Capture、Evaluate、Refine
- UnityAgent Control Plane → ToolBroker → UnityArtistCLI の単一実行境界
- standalone Artist Codex Pluginは配布せず、Marketplace entryはUnityAgentに集約

## Current production support

- Unity 6.x+ + Built-in
- Unity 6.x+ + URP
- Unity 6.x+ + HDRP

Unity 2022.3の記録はHistorical Evidenceであり、現在のProduction supportには含めません。

## Hub / Specialist alignment

同じHub mainには Manifest v5 / Snapshot v3 として以下の4 Specialistが登録されています。

- ArtistSubAgent — provider-backed
- GraphicsSubAgent — reasoning / read-only analysis
- WorldCreatorSubAgent — reasoning / planning-only
- PerformanceSubAgent — reasoning / read-only analysis

Graphics / WorldCreator / Performance は独立した実行バイナリやMarketplace Pluginではありません。Runtime selection / environment observation / executionはUnityAgentが所有します。

## Verification status

Release Gateはstatic contract、Unity API compatibility、portable path、remote installer、checked-in Evidence contract、CLI build、UPM distribution layoutを検証します。

既存のUnity Editor / Pipeline E2E Evidenceは`0.0.1-beta`時点で取得された観測記録を保持しています。今回のVersion bumpだけを理由に、それらを`0.0.2-beta`の再実測結果として書き換えていません。
