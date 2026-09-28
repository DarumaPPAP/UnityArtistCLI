# Legacy Domain Support Matrixの知識移管

旧MyUnityMCPの5つの`get_support_matrix`は、旧実装の対応範囲を説明するToolでした。現行UnityAgent／UnitySubAgentHubのProduction CapabilityやUnity Version互換性を証明するものではありません。各Domainの新Toolを設計・評価するとき、以下の境界を確認するDocumentationとして保持します。実行時の対応判定は現行Profile、Provider Registry、観測されたProject／Package Factから行います。

| 旧Tool | 旧Sourceで宣言した範囲 | 非対象・未検証 | 現行Ownerでの扱い |
|---|---|---|---|
| `graphics.get_support_matrix` | Editor専用、旧Package 1.0.0、最小Unity 6000.0。Inspection／Planning、Light／Camera／Reflection Probe変更、条件付きVolume／Bake／APV、Graphics Device付きCapture、Visual Acceptanceを列挙 | 旧検証HostはUnity 6000.0.75f1のUbuntu BatchMode NoGraphics。Player、Target Device、全Unity 6000.x patch、全ClientのMCP disconnect callbackは未検証 | ArtistのVisual作業とGraphicsの技術診断を分け、現行Manifestと実Project Factで再判定する。旧Support Matrixを現行Production保証へ昇格しない |
| `ui.get_support_matrix` | Canvas、RectTransform、UIDocumentのInspection／Validationと承認制RectTransform変更 | Screen Space Overlayの描画はUnity標準。TextMeshPro semantic inspection、複雑なLayout編集、Runtime UI interaction automationは未検証 | UnityAgentの将来の決定論的Scene Tool候補。現在のTool提供を宣言しない |
| `animation.get_support_matrix` | Animator／Controller parameter／clipのInspection、Animation Event validation、承認制parameter追加 | State Machine、Transition、Curve、Clip Eventの変更は旧初期範囲から除外。AnimatorOverrideController変更、Humanoid retargeting、Runtime State監視は未検証 | UnityAgentの将来の決定論的Animation Tool候補。観測と変更を分ける |
| `audio.get_support_matrix` | AudioSourceのInspection、AudioClip metadata、AudioListener validation、承認制AudioSource property変更 | Clip replacement、Mixer Asset作成、Exposed Parameter authoring、Audio renderingは除外。Platform音声出力、Gamepad speaker、Runtime profilingは未検証 | Scene AudioSource Tool候補。Content PilotのAudio Import／Compression判断とは別責務 |
| `cinematic.get_support_matrix` | UnityEngine.DirectorModuleのPlayableDirector Inspection、Output binding validation、承認制Director property変更 | Timeline Track／Clip／BindingとCinemachine Shotの変更は旧初期範囲から除外。`com.unity.timeline` Track authoringと`com.unity.cinemachine` Camera authoringは未検証 | ArtistのCinematic契約と意味差を比較するためのReference。Optional Packageの存在とVersionをProjectごとに観測する |

Source: `Legacy/MyUnityMCP-1.1.1/Package/Editor/Execution/ExecutionHardening.cs`、`Operational/UI/UnityUiMcp.cs`、`Operational/Animation/UnityAnimationMcpRuntime.cs`、`Operational/Audio/UnityAudioMcp.cs`、`Operational/Cinematic/UnityCinematicMcp.cs`。このKnowledge移管は旧Runtime Toolの置換、独立実装、Parity、Live Evidenceを意味しません。PORT／RETIRE／active caller移行は[Legacy Capability Salvage Audit](legacy-capability-salvage-audit.md)で別途追跡します。
