using NUnit.Framework;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityArtist;
using UnityEngine.Rendering.Universal;
namespace UnityCi {
 public class PipelineSmokeTests {
  RenderPipelineAsset previousGraphics, previousQuality;
  [SetUp] public void OpenConcreteSceneAndConfigurePipeline() {
   previousGraphics = GraphicsSettings.defaultRenderPipeline; previousQuality = QualitySettings.renderPipeline;
   EditorSceneManager.OpenScene("Assets/Scenes/PipelineSmoke.unity");
   var renderer = ScriptableObject.CreateInstance<UniversalRendererData>();
   AssetDatabase.CreateAsset(renderer, "Assets/CiRenderer.asset");
   var asset = UniversalRenderPipelineAsset.Create(renderer);
   AssetDatabase.CreateAsset(asset, "Assets/CiPipeline.asset");
   GraphicsSettings.defaultRenderPipeline = asset; QualitySettings.renderPipeline = asset;
  }
  [TearDown] public void RestorePipeline() {
   GraphicsSettings.defaultRenderPipeline = previousGraphics; QualitySettings.renderPipeline = previousQuality;
   AssetDatabase.DeleteAsset("Assets/CiPipeline.asset"); AssetDatabase.DeleteAsset("Assets/CiRenderer.asset");
  }
  [Test] public void SceneContainsCameraLightAndRenderableSubject() {
   Assert.IsNotNull(Camera.main); Assert.IsNotNull(Object.FindFirstObjectByType<Light>());
   var subject = GameObject.Find("FovSubject"); Assert.IsNotNull(subject);
   Assert.IsNotNull(subject.GetComponent<MeshRenderer>()); Assert.IsNotNull(subject.GetComponent<MeshFilter>().sharedMesh);
   Assert.IsTrue(ArtistCompatibility.IsSupported(Application.unityVersion, "urp"));
  }
  [Test] public void NativePipelineSettingsCanBeConfigured() { Assert.IsInstanceOf<UniversalRenderPipelineAsset>(GraphicsSettings.defaultRenderPipeline);
   Assert.IsNotNull(((UniversalRenderPipelineAsset)GraphicsSettings.defaultRenderPipeline).scriptableRenderer);
   var volume = new GameObject("SmokeVolume").AddComponent<Volume>();
   volume.isGlobal = true; volume.sharedProfile = ScriptableObject.CreateInstance<VolumeProfile>();
   var bloom = volume.sharedProfile.Add<Bloom>(); bloom.intensity.Override(0.5f);
   Assert.AreEqual(0.5f, bloom.intensity.value); }
 }
}
