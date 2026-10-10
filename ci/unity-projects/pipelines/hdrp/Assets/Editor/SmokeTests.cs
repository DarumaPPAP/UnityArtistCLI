using NUnit.Framework;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityArtist;
using UnityEngine.Rendering.HighDefinition;
namespace UnityCi {
 public class PipelineSmokeTests {
  RenderPipelineAsset previousGraphics, previousQuality;
  [SetUp] public void OpenConcreteSceneAndConfigurePipeline() {
   previousGraphics = GraphicsSettings.defaultRenderPipeline; previousQuality = QualitySettings.renderPipeline;
   EditorSceneManager.OpenScene("Assets/Scenes/PipelineSmoke.unity");
   PlayerSettings.colorSpace = ColorSpace.Linear;
   var asset = ScriptableObject.CreateInstance<HDRenderPipelineAsset>();
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
   Assert.IsTrue(ArtistCompatibility.IsSupported(Application.unityVersion, "hdrp"));
  }
  [Test] public void NativePipelineSettingsCanBeConfigured() { Assert.IsInstanceOf<HDRenderPipelineAsset>(GraphicsSettings.defaultRenderPipeline);
   Assert.AreEqual(ColorSpace.Linear, PlayerSettings.colorSpace);
   var volume = new GameObject("SmokeVolume").AddComponent<Volume>();
   volume.isGlobal = true; volume.sharedProfile = ScriptableObject.CreateInstance<VolumeProfile>();
   var fog = volume.sharedProfile.Add<Fog>(); fog.meanFreePath.Override(50f);
   Assert.AreEqual(50f, fog.meanFreePath.value); }
 }
}
